/*
 * pharmacy_room.h
 *
 *  Created on: Nov 15, 2024
 *      Author: mrvogel
 */
#include "open_interface.h"

#ifndef PHARMACY_ROOM_H_
#define PHARMACY_ROOM_H_


void show_medication_menu();

void show_patient_menu();

void return_to_home_menu();

void confirm_and_send();

void lcd_menu(oi_t *sensor_data);

int sensor(oi_t *sensor_data);


#endif /* PHARMACY_ROOM_H_ */
