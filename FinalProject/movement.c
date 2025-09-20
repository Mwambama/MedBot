#include "movement.h"
#include "open_interface.h"
#include "uart.h"
#include "timer.h"
#include "scan.h"

extern int move_distance;
extern int object_count;

// Function to play noise from medBot
int playSong(int songNum)
{
    unsigned char notes0[15] = { 60, 60, 67, 67, 69, 69, 67 };
    unsigned char duration0[15] = { 30, 30, 30, 30, 30, 30, 30 };

    unsigned char notes1[15] = { 69, 71, 73, 76, 78, 81, 78, 76, 73, 71, 69 };
    unsigned char duration1[15] = { 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8 };

    unsigned char notes2[15] = { 57, 69, 0, 57, 69, 0, 57, 69, 0, 57, 69, 0, 57,
                                 69, 0 };
    unsigned char duration2[15] = { 32, 32, 16, 32, 32, 16, 32, 32, 16, 32, 32,
                                    16, 32, 32, 16 };

    //SONG 0: setup song
    if (songNum == 0)
    {
        oi_loadSong(songNum, 7, notes0, duration0);
        oi_play_song(songNum);
    }
    //SONG 1: reaches something
    if (songNum == 1)
    {
        oi_loadSong(songNum, 11, notes1, duration1);
        oi_play_song(songNum);
    }

    //SONG 2: something in the way
    if (songNum == 2)
    {
        oi_loadSong(songNum, 15, notes2, duration2);
        oi_play_song(songNum);
    }

    return 0;
}

// Function to send a string to PuTTY terminal
void sendPutty(char str[])
{
    int j;
    for (j = 0; j < strlen(str); j++)
    {
        uart_sendChar(str[j]);
    }
}

// Function to move forward, avoid, cliff, objects, and boarder
double  move_forward(oi_t *sensor_data, double distance_mm){
    double sum = 0;
    oi_setWheels(100,100);
    while (sum < distance_mm) {
        oi_update(sensor_data);
        sum += sensor_data -> distance;
        bool bumped;
        bumped = sensor_data -> bumpLeft || sensor_data -> bumpRight;
        if(bumped){
            bool turnLeft = sensor_data -> bumpRight;
            move_backwards(sensor_data, 50);
            sum -= 150;
            if(turnLeft){
                turn_counter_clockwise(sensor_data, 90);
                move_forward(sensor_data, 100);
                turn_clockwise(sensor_data, 90);
                return sum;
            } else {
                turn_clockwise(sensor_data, 90);
                move_forward(sensor_data, 100);
                turn_counter_clockwise(sensor_data, 90);
                return sum;
            }
        }
        int frontLeft = sensor_data -> cliffFrontLeftSignal;
        int frontRight = sensor_data -> cliffFrontRightSignal;
        int Left = sensor_data -> cliffLeftSignal;
        int Right = sensor_data -> cliffRightSignal;
        // found cliff ahead, back up & turn around
        if(frontLeft < 100 || frontLeft > 2650 || frontRight < 100 || frontRight > 2650){///
            lcd_printf("cliff detected");
            oi_setWheels(0, 0);
            move_backwards(sensor_data, 35);
            turn_clockwise(sensor_data, 45);
            //Found cliff
            if(frontLeft < 500 || frontRight < 500){
                return -10;
            }
            // Found edge
            return -10;
        }
        if(Left < 500 || Left > 2600){
            oi_setWheels(0, 0);
            move_backwards(sensor_data, 35);
            turn_clockwise(sensor_data, 90);
            //Found cliff
            if(Left < 500){
                return -10;
            }
            // Found edge
            return -10;
        }
        if(Right < 500 || Right > 2600){
            oi_setWheels(0, 0);
            move_backwards(sensor_data, 35);
            turn_counter_clockwise(sensor_data, 90);
            // Found cliff
            if(Right < 500){
                return -10;
            }
            // Found edge
            return -10;
        }
    }
    oi_setWheels(0,0); // stop
    return sum;
}


// Function to move medBot backwards
double move_backwards(oi_t *sensor_data, double distance_mm)
{

    double total_distance = 0; // initialize total distance traveled
    oi_setWheels(-100, -100); // move backward at full speed
    while (total_distance < distance_mm) // move backward until total distance matches or exceeds target distance
    {
        oi_update(sensor_data);
        total_distance -= sensor_data->distance; // calculates total distance
    }
    oi_setWheels(0, 0); // stop
    return total_distance;
}

// Function to turn medBot clockwise
void turn_clockwise(oi_t *sensor, int degrees)
{
    oi_setWheels(-100, 100);
    double sum = 0;

    while (sum > -degrees)
    {
        oi_update(sensor);  // Update sensor data
        sum += sensor->angle;
        sensor->angle = 0;
    }
    oi_setWheels(0, 0);
}

// Function to turn medBot counter clockwise
void turn_counter_clockwise(oi_t *sensor, int degrees)
{
    oi_setWheels(100, -100);
    double sum = 0;

    while (sum < degrees)
    {
        oi_update(sensor);  // Update sensor data
        sum += sensor->angle;
        sensor->angle = 0;
    }
    oi_setWheels(0, 0);
}






