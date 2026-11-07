#include "stm32f4xx_hal.h"
#include <stdint.h>

static void inline DWT_Init(void) {
    CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk; 
    DWT->CTRL |= DWT_CTRL_CYCCNTENA_Msk;           
}

static inline uint32_t Get_Cycles(void) {
    uint32_t ticks, val, load;
    
    do {
        ticks = HAL_GetTick();
        val = SysTick->VAL;
    } while (ticks != HAL_GetTick());

    load = SysTick->LOAD;
    
    return (ticks * (load + 1)) + (load - val);
}

static inline uint32_t Get_Microseconds(void) {
    return DWT->CYCCNT / (SystemCoreClock / 1000000U);
}

typedef struct {
    const char *name;
    uint32_t count, min, max;
    uint64_t sum;

    uint32_t last_start;
    uint32_t max_jitter;
} metric_stats;

static inline void stats_add(metric_stats *stats, uint32_t time) {
    if (stats->count == 0 || time < stats->min) stats->min = time;
    if (time > stats->max) stats->max = time;
    stats->sum += time;
    stats->count++;
}

static inline void stats_jitter_add(metric_stats *stats, uint32_t cur_cycles, uint32_t expected) {
    if (stats->count > 1) {
        uint32_t actual_period = cur_cycles - stats->last_start;

        int32_t dif = (int32_t)actual_period - (int32_t)expected;
        uint32_t jitter = (dif > 0) ? (uint32_t)(dif) : (uint32_t)(-dif);

        if (stats->max_jitter < jitter) stats->max_jitter = jitter;
    }

    stats->last_start = cur_cycles;
}


