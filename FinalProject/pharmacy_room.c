#include "button.h"
#include "Timer.h"
#include "lcd.h"
#include "uart.h"
#include "open_interface.h"
#include <string.h>
#include <stdio.h>
#include "scan.h"
#include "patient_room.h"
#include "movement.h"
#include <stdint.h>

typedef enum
{
    HOME_MENU, MEDICATION_MENU, PATIENT_MENU, CONFIRM_MENU, PATIENT_ROOM_MENU
} MenuState;
MenuState current_menu = HOME_MENU;

char selected_medication[20] = "None    ";
char selected_patient[20] = "None       ";

// Menu to show medication options on lcd
void show_medication_menu()
{
    lcd_clear();
    lcd_printf("Medication Menu\n1. Xanax\n2. Fent\n3. Percs");
    current_menu = MEDICATION_MENU;
}

// Menu to show patient options on lcd
void show_patient_menu()
{
    lcd_clear();
    lcd_printf("Patient Menu\n1. Patient 1\n2. Patient 2\n3. Patient 3");
    current_menu = PATIENT_MENU;
}

// Returns to home menu on lcd
void return_to_home_menu()
{
    lcd_clear();
    lcd_printf(
            "medBot Home Menu\n1. Select Medication2. Select Patient\n3. Confirm and Send\n4. Return to Home");
    current_menu = HOME_MENU;
}

// Menu to verify selected information and send the cyBot to patient room
void confirm_and_send()
{
    lcd_clear();
    lcd_printf("Medication: %sPatient: %s1. Send medBot\n4. Return to menu",
               selected_medication, selected_patient);
    current_menu = CONFIRM_MENU;
}

// Needed external variables
extern int largest_index;
extern int middle_index;
extern int smallest_index;

// Function to show menu and select options
void lcd_menu(oi_t *sensor_data)
{

    return_to_home_menu(); // Start at the home menu

    int last_button = 0;
    int current_patient = 0;

    while (1)
    {
        int current_button = button_getButton();

        if (current_button != last_button)
        {
            switch (current_menu)
            {
            case HOME_MENU:
                if (current_button == 1) // Show medication menu when button 1 is selected
                {
                    show_medication_menu();
                }
                else if (current_button == 2) // Show patient menu when button 2 is selected
                {
                    show_patient_menu();
                }
                else if (current_button == 3) // Send medBot and verify information when button 3 is selected
                {
                    confirm_and_send();
                }
                else if (current_button == 4) // Return to home menu when button 4 is selected
                {
                    return_to_home_menu();
                }
                break;

                // Select medication
            case MEDICATION_MENU:
                if (current_button == 1)
                {
                    lcd_clear();
                    lcd_printf("Selected: Xanax");
                    strcpy(selected_medication, "Xanax   ");
                    timer_waitMillis(1500);
                    return_to_home_menu();
                }
                else if (current_button == 2)
                {
                    lcd_clear();
                    lcd_printf("Selected: Fentanyl");
                    strcpy(selected_medication, "Fentanyl");
                    timer_waitMillis(1500);
                    return_to_home_menu();
                }
                else if (current_button == 3)
                {
                    lcd_clear();
                    lcd_printf("Selected: Percocet");
                    strcpy(selected_medication, "Percocet");
                    timer_waitMillis(1500);

                    return_to_home_menu();
                }
                else if (current_button == 4)
                {
                    return_to_home_menu();
                }
                break;

                // Select patient
            case PATIENT_MENU:
                if (current_button == 1)
                {
                    lcd_clear();
                    lcd_printf("Selected: Patient 1");
                    strcpy(selected_patient, "Patient 1  ");
                    timer_waitMillis(1500);
                    current_patient = 1;
                    return_to_home_menu();
                }
                else if (current_button == 2)
                {
                    lcd_clear();
                    lcd_printf("Selected: Patient 2");
                    strcpy(selected_patient, "Patient 2  ");
                    timer_waitMillis(1500);
                    current_patient = 2;
                    return_to_home_menu();
                }
                else if (current_button == 3)
                {
                    lcd_clear();
                    lcd_printf("Selected: Patient 3");
                    strcpy(selected_patient, "Patient 3  ");
                    timer_waitMillis(1500);
                    current_patient = 3;
                    return_to_home_menu();
                }
                else if (current_button == 4)
                {
                    return_to_home_menu();
                }
                break;

                // Send medBot to patient room and verify information
            case CONFIRM_MENU:
                if (current_button == 1)
                {
                    // code for medBot to proceed to the destination
                    lcd_printf("Sending medBot!");
                    timer_waitMillis(1500);
                    perform_180_ir_scan(sensor_data);
                    display_largest_object();
                    navigate_to_patient_room(sensor_data, largest_index);
                    lcd_clear();
                    lcd_printf("Arrived at\n Patient Room");
                    timer_waitMillis(1500);

                    turn_counter_clockwise(sensor_data, 90);
                    move_forward(sensor_data, 850);
                    turn_clockwise(sensor_data, 90);
                    move_forward(sensor_data, 430);

                    if (current_patient == 1) // Bed one
                    {
                        bed_one(sensor_data, smallest_index);
                        patient_lcd(sensor_data); // med dispense menu

                    }
                    else if (current_patient == 2) // Bed two
                    {
                        bed_two(sensor_data, middle_index);
                        patient_lcd(sensor_data); // med dispense menu

                    }
                    else if (current_patient == 3) // Bed three
                    {
                        bed_three(sensor_data, largest_index);
                        patient_lcd(sensor_data); // med dispense menu

                    }

                }
                else if (current_button == 4) // Return to home menu
                {
                    return_to_home_menu();
                }
                break;

            }

            last_button = current_button;
        }

    }
}

// Sensor data
int sensor(oi_t *sensor_data)
{

    uart_sendStr("Ready for commands.\n");

    while (1)
    {
        if (flag)
        {
            flag = 0;
            handle_uart_data(uart_data, sensor_data);
        }
    }

}

