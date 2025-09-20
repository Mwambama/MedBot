#include <pharmacy_room.h>
#include <stdint.h>
#include <stdio.h>
#include "servo.h"
#include "lcd.h"
#include "Timer.h"
#include "button.h"
#include "ping.h"
#include "uart.h"
#include "adc.h"
#include "movement.h"
#include "open_interface.h"
#include "scan.h"
#include "patient_room.h"

int main(void) //bot 15 and 10 work with our code
{

    // initialize everything
    setup();

    oi_t *sensor_data = oi_alloc();
    oi_init(sensor_data);

    uart_sendStr("Ready for commands.\n");



    while (1)
    {
        if (flag)
        {
            flag = 0;
            handle_uart_data(uart_data, sensor_data); // Call this function to execute everything
        }


    }

    oi_free(sensor_data);
}


