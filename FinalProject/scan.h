/*
 * scan.h
 *
 *  Created on: Nov 15, 2024
 *      Author: mrvogel
 */

#include "open_interface.h"


#ifndef SCAN_H_

#define SCAN_H_

typedef struct
{
    int start_angle;
    int end_angle;
    int distance;
    int linear_width;
    int ping_distance;
} ObjectInfo;


void handle_uart_data(char command, oi_t *sensor_data);

void navigate_to_largest_object(oi_t *sensor_data, int largest_index);

void display_largest_object();

void perform_180_ir_scan(oi_t *sensor_data);

void control_movement(oi_t *sensor_data, char command);

int adc_distance();

void setup();

void navigate_to_patient_room (oi_t *sensor_data, int largest_index);

void navigate_to_home(oi_t *sensor_data, int largest_index);

void bed_two(oi_t *sensor_data, int middle_index);

void bed_one(oi_t *sensor_data, int smallest_index);

void bed_three(oi_t *sensor_data, int largest_index);

int angle_calculation(int angle, float distanceToObject);

void set_linear_width(ObjectInfo *object);


#endif /* SCAN_H_ */

