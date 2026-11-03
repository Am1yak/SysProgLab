#include "stm32f4xx_hal.h"
#include <stdint.h>

#define ADC_DEADBAND 50
#define SERVO_STEP 10
#define SERVO_MIN_CCR 1000
#define SERVO_MAX_CCR 2000

static uint32_t current_az_ccr = 1500;
static uint32_t current_el_ccr = 1500;

static uint32_t clamp_ccr(uint32_t val) {
    if (val < SERVO_MIN_CCR) return SERVO_MIN_CCR;
    if (val > SERVO_MAX_CCR) return SERVO_MAX_CCR;
    return val;
}

void Proccess_Solar_Tracking(uint32_t raw_north,
     uint32_t raw_south,
     uint32_t raw_east, 
     uint32_t raw_west) {
        int32_t err_az = (int32_t)raw_east - (int32_t)raw_west;
        int32_t err_el = (int32_t)raw_north - (int32_t)raw_south;

        if (err_az > ADC_DEADBAND) {
            current_az_ccr -= SERVO_STEP;
        } else if (err_az < -ADC_DEADBAND) {
            current_az_ccr += SERVO_STEP;
        }

        if (err_el > ADC_DEADBAND) {
            current_el_ccr += SERVO_STEP;
        } else if (err_el < -ADC_DEADBAND) {
            current_el_ccr -= SERVO_STEP;
        }

        current_az_ccr = clamp_ccr(current_az_ccr);
        current_el_ccr = clamp_ccr(current_el_ccr);

        __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, current_az_ccr);
        __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_2, current_el_ccr);
     }