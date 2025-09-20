#ifndef ADC_H_
#define ADC_H_
#include "lcd.h"

#include <inc/tm4c123gh6pm.h>
#include <stdint.h>
#include <stdbool.h>
#include "driverlib/interrupt.h"

void adc_init(void);

int adc_read(void);

int adc_read_avg(void);

float calculate_distance(void);

#endif /* ADC_H_ */
