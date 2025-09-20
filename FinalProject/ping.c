#include "ping.h"
#include "Timer.h"
#include "math.h"
#include "inc/tm4c123gh6pm.h"
#include "driverlib/interrupt.h"
#include "lcd.h"

/*
 * adc.c
 *
 *  Created on: Oct 24, 2024
 *      Author: guru
 */

#define CLOCK_SPEED 16000000

volatile unsigned int ping_sent;
volatile unsigned int ping_received;
volatile int adc_flag = 0;
volatile int edge = 1; // if 1 positive edge, if 0 negative edge

int overflow_count = 0;

void ping_init()
{
    //part 1: Activating the sensor
    //set up wire PB3, enable for GPIO function before trigger pulse
    //Mask Timer Interrupt
    //Send trigger, PB3 set to output
    //Change PB3
    SYSCTL_RCGCGPIO_R |= 0b00000010; //enable port B clock
    SYSCTL_RCGCTIMER_R |= 0x08; //enable clock for timer 3

    GPIO_PORTB_DEN_R |= 0x08; //enable PB3
    GPIO_PORTB_PCTL_R = (GPIO_PORTB_PCTL_R & 0xFFFF0FFF) | 0x00007000; //set PB3 to T3CCP1 function

    //Configure Timer
    TIMER3_CTL_R &= 0x0000; //disable Timer B clear edge mode
    TIMER3_CFG_R = (TIMER3_CFG_R & 0x0) | 0x4; //set Timer 3 to 16 bit mode
    TIMER3_TBMR_R = 0x007; //set Timer3B to count down, edge-time mode, capture mode
    TIMER3_CTL_R |= 0x0C00; //enable for both edges
    TIMER3_TBILR_R |= 0xFFFF; //set timer starting value for counting down
    TIMER3_TBPR_R |= 0xFF; //set prescaler for timer b to extend it to a 24-bit timer
    TIMER3_IMR_R |= 0x400; //enable capture interrupt for Timer3B
    TIMER3_ICR_R |= 0x400; // clear interrupts

    NVIC_EN1_R |= 0x10; //enable TIMER3B interrupts
    IntRegister(INT_TIMER3B, TIMER3B_Handler);
    IntMasterEnable();
    TIMER3_CTL_R |= 0x0100; //enable Timer B
}

void send_pulse()
{
    TIMER3_CTL_R &= ~0x0100; //disable Timer B
    TIMER3_IMR_R &= 0x000; //mask all interrupts
    GPIO_PORTB_AFSEL_R &= 0xF7; //turn off alternate function for PB3
    GPIO_PORTB_DIR_R |= 0x08; //set PB3 for output

    GPIO_PORTB_DATA_R &= 0xF7; //set PB3 to low
    GPIO_PORTB_DATA_R |= 0x08; //set PB3 to high
    timer_waitMicros(5);
    GPIO_PORTB_DATA_R &= 0xF7; //set PB3 to low

    // reinitialize for input
    GPIO_PORTB_DIR_R &= 0xF7; //set PB3 for input
    GPIO_PORTB_AFSEL_R |= 0x08; //set PB3 for alternate function

    TIMER3_ICR_R = 0x400; //clear Timer B Capture Mode Event interrupt
    TIMER3_IMR_R |= 0x400; //unmask above interrupt
    TIMER3_CTL_R |= 0x0100; // enable Timer B
}

float ping_read()
{
    int cycles;
    float time;
    float distance;

    send_pulse();
    while (!adc_flag)
    {
    }
    adc_flag = 0;
    edge = 1;

    cycles = (ping_sent - ping_received);
    if (cycles < 0)
    {
        overflow_count++;
        cycles += 0xFFFFFF;
    }
    time = (float) cycles / CLOCK_SPEED;
    distance = (time / 2) * 343000; // half the time, multiplied by speed of sound 343000 mm/s
    lcd_printf("Dist: %.2f\nCycles: %d\nTime: %.2f\nOverFlow: %d", distance,
               cycles, time * 1000, overflow_count);
    return distance;
}

void TIMER3B_Handler()
{
    if (TIMER3_MIS_R & 0x400)
    {
        TIMER3_ICR_R = 0x400; //clear Timer B Capture Mode Event interrupt
        if (edge == 1)
        {
            ping_sent = TIMER3_TBR_R;
            edge = 0;
        }
        else if (edge == 0)
        {
            ping_received = TIMER3_TBR_R;
            adc_flag = 1;
            edge = -1;
        }
    }
}

