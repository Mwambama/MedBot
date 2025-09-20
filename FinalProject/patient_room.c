/*
 * patient_room.c
 *
 *  Created on: Dec 1, 2024
 *      Author: mrvogel
 */

#include "button.h"
#include "Timer.h"
#include "lcd.h"
#include "uart.h"
#include "open_interface.h"
#include <string.h>
#include <stdio.h>
#include "scan.h"
#include "pharmacy_room.h"
#include "movement.h"

#include <stdint.h>


extern int largest_index;

// Function to display patient room options menu on lcd
void patient_room_options()
{
    lcd_clear();
    lcd_printf("1. Dispense\nMedication\n2. Send Away");
}

// Function to show patient room options on lcd and select an option
void patient_lcd(oi_t *sensor_data)
{
    button_init();
    timer_init();
    lcd_init();
    uart_interrupt_init();



    patient_room_options(); // patient menu home

    int last_button = 0;

    while (1)
    {
        int current_button = button_getButton();

        if (current_button != last_button)
        {
            if (current_button == 1)
            {
                lcd_printf("Medication dispensed");
                timer_waitMillis(1500);
                lcd_printf("Returning to base");
                timer_waitMillis(1500);
                turn_counter_clockwise(sensor_data, 180);
                move_forward(sensor_data, 500);
                perform_180_ir_scan(sensor_data);
                display_largest_object();
                navigate_to_home(sensor_data, largest_index);
                lcd_printf("Returned to base");

            }
            if (current_button == 2)
            {
                // send away function
                lcd_printf("Returning to base");
                timer_waitMillis(1500);
                turn_counter_clockwise(sensor_data, 180);
                move_forward(sensor_data, 500);
                perform_180_ir_scan(sensor_data);
                display_largest_object();
                navigate_to_home(sensor_data, largest_index);
                lcd_printf("Returned to base");
            }
        }
    }
}

