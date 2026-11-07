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
} metric_stats;

static inline void stats_add(metric_stats *stats, uint32_t time) {
    if (stats->count == 0 || time < stats->min) stats->min = time;
    if (time > stats->max) stats->max = time;
    stats->sum += time;
    stats->count++;
}


