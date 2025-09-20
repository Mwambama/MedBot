#ifndef MOVEMENT_H
#define MOVEMENT_H
#include "open_interface.h"

void sendPutty(char str[]);

double move_forward(oi_t  *sensor_data,   double distance_mm);

void turn_clockwise(oi_t *sensor, int angle);

void turn_counter_clockwise(oi_t *sensor, int angle);

double move_backwards(oi_t *sensor_data, double distance_mm);

int playSong(int songNum);


#endif
