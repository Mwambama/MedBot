#include <pharmacy_room.h>
#include <stdint.h>
#include <stdio.h> // Include for sprintf
#include "servo.h"
#include "lcd.h"
#include "Timer.h"
#include "button.h"
#include "ping.h"
#include "uart.h"
#include "adc.h"
#include "movement.h"
#include "open_interface.h"
#include "patient_room.h"
#include "scan.h"

// Scan and distance thresholds
#define SCAN_ANGLE_STEP 1
#define IR_THRESHOLD 70
#define TARGET_DISTANCE_CM 5

ObjectInfo detected_objects[10];
int object_count = 0;
int angle = 0;
float distanceToObject = 0;
int move_distance;

typedef enum
{
    MANUAL, AUTONOMOUS_SCAN, AUTONOMOUS_TURN, AUTONOMOUS_MOVE
} Mode;
Mode current_mode = MANUAL;

// Updated distances array to support greater distances
float distances[] = { 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 50,
                      55, 60, 65, 70 };

// Updated ir_values array corresponding to the new distances
int ir_values[] = { 1499, 1277, 1147, 1087, 987, 955, 919, 877, 842, 833, 803,
                    795, 779, 751, 731, 710, 690, 670, 650, 630 };


// Globally declare indices for each patient bed
int largest_index = 0;
int middle_index = 0;
int smallest_index = 0;


// Function to initialize everything needed
void setup()
{
    timer_init();
    lcd_init();
    uart_init(115200);
    uart_interrupt_init();
    button_init();
    adc_init();
    ping_init();
    servo_init();
    uart_sendStr("System setup complete.\n");
    playSong(0); // play song after setup is complete
}

// Calculates width using start angles, end angles, and distance
void set_linear_width(ObjectInfo *object)
{
    float radians = ((object->start_angle - object->end_angle) * 3.1415) / 180;
    (object->linear_width) = sqrt(
            (2 * pow(object->ping_distance, 2))
                    - (2 * pow(object->ping_distance, 2) * cos(radians)));
}

// Function to convert ADC value to distance using extended arrays
int adc_distance()
{
    int i;
    int raw_ir = adc_read();
    if (raw_ir >= ir_values[0])
    {
        return distances[0];
    }
    if (raw_ir <= ir_values[18])  // Extended range for greater distances
    {
        return distances[18];
    }
    for (i = 0; i < 18; i++)  // Iterate through the extended array
    {
        if (raw_ir <= ir_values[i] && raw_ir > ir_values[i + 1])
        {
            float slope = (distances[i + 1] - distances[i])
                    / (float) (ir_values[i + 1] - ir_values[i]);
            return distances[i] + slope * (raw_ir - ir_values[i]);
        }
    }
    return -1;
}


// Function to manually control if needed
void control_movement(oi_t *sensor_data, char command)
{
    switch (command)
    {
    case 'w':
        move_forward(sensor_data, 10); // Move forward with bump handling
        break;
    case 'a':
        turn_counter_clockwise(sensor_data, 15);
        break;
    case 's':
        move_backwards(sensor_data, 10);
        break;
    case 'd':
        turn_clockwise(sensor_data, 15);
        break;
    default:
        uart_sendStr("Invalid movement command.\n");
        break;
    }
}

// Function to perform 180 degree scan
void perform_180_ir_scan(oi_t *sensor_data)
{
    int angleA;
    int i;

    // Reset object count and clear previous data
    object_count = 0;

    // Clear detected objects array
    for (i = 0; i < 10; i++)
    {
        detected_objects[i].start_angle = 0;
        detected_objects[i].end_angle = 0;
        detected_objects[i].distance = 0;
        detected_objects[i].linear_width = 0;
        detected_objects[i].ping_distance = 0;
    }

    int in_object = 0;
    int start_angle = -1;
    int last_end_angle = -1;  // To track the end of the last detected object

    for (angleA = 0; angleA <= 180; angleA += SCAN_ANGLE_STEP)
    {
        servo_move(angleA);  // Move the servo to the specified angle

        int ir_distance = adc_distance();
        int raw_ir = adc_read();
        int raw_ping = ping_read();


        char message[80];
        snprintf(message, sizeof(message),
                 "Angle: %d, IR Distance: %d Raw: %d, Ping: %d\n", angleA,
                 ir_distance, raw_ir, raw_ping);
        uart_sendStr(message);  // Log sensor readings

        // Object detection logic using IR distance
        if (ir_distance < IR_THRESHOLD && !in_object)
        {
            in_object = 1;
            start_angle = angleA;
            // Use IR distance initially
            detected_objects[object_count].distance = ir_distance;
            detected_objects[object_count].ping_distance = 0; // Set to 0 initially
        }
        else if (ir_distance >= IR_THRESHOLD && in_object)
        {
            in_object = 0;
            // Check for a significant gap between the current object and the previous one
            if (object_count > 0)
            {
                // Ensure objects are at least 2-3 degrees apart, or that the distances are significantly different
                if (angleA - detected_objects[object_count - 1].end_angle > 2
                        || abs(detected_objects[object_count - 1].ping_distance
                                - raw_ping) > 10)
                {
                    detected_objects[object_count].start_angle = start_angle;
                    detected_objects[object_count].end_angle = angleA;
                    object_count++;
                }
            }
            else // Always add the first object
            {
                detected_objects[object_count].start_angle = start_angle;
                detected_objects[object_count].end_angle = angleA;
                object_count++;
            }
            last_end_angle = angleA; // Update the end angle of the last detected object
        }

        // If an object is detected, update its ping distance
        if (in_object && detected_objects[object_count].distance != 0)
        {
            detected_objects[object_count].ping_distance = raw_ping;
            detected_objects[object_count].distance = ir_distance; // Retain IR distance as primary
        }
    }

    uart_sendStr("\n");
    uart_sendStr("Detected Objects:\n");
    uart_sendStr("Object\tStart Angle\tEnd Angle\tPingDistance\tWidth\n");
    uart_sendStr(
            "--------------------------------------------------------------\n");
    for (i = 0; i < object_count; i++)
    {
        char message[80];
        set_linear_width(&detected_objects[i]);
        snprintf(message, sizeof(message), "Object %d\t%d\t\t%d\t\t%d\t\t%d\n",
                 i + 1, detected_objects[i].start_angle,
                 detected_objects[i].end_angle,
                 detected_objects[i].ping_distance,
                 detected_objects[i].linear_width);
        uart_sendStr(message);
    }
}

// Display largest object after scan
void display_largest_object(oi_t *sensor_data)
{

    if (object_count == 0)
    {
        while (object_count == 0)
        {
            uart_sendStr("\nNo objects detected.\n");
            move_forward(sensor_data, 400);
            perform_180_ir_scan(sensor_data);
        }

        return;

    }

    int i;  // Variable declared outside of the for loop
    float largest_width = 0;
    int largest_index_temp = 0;  // Use a temporary variable for largest index

    // Find the largest object by comparing their angular widths
    for (i = 1; i < object_count; i++)
    {
        float width = detected_objects[i].linear_width;
        if (width > largest_width && width > 150)
        {
            largest_width = width;
            largest_index_temp = i;  // Update the temporary largest index
        }
    }

    // Display the details of the largest detected object
    uart_sendStr("\nLargest object detected:\n");
    char message[100];
    snprintf(message, sizeof(message),
             "Start Angle: %d, End Angle: %d, Distance: %d cm\n",
             detected_objects[largest_index_temp].start_angle,
             detected_objects[largest_index_temp].end_angle,
             detected_objects[largest_index_temp].ping_distance);
    uart_sendStr(message);

    // Update the global largest_index
    largest_index = largest_index_temp;

    // Prepare the system for the next action, such as turning towards the detected object
    current_mode = AUTONOMOUS_TURN;
}

// Function to calculate desired turning angle
int angle_calculation(int angle, float distanceToObject)
{
    static int botCenterToSensorCenterDist = 105;
    static int scanCenterToScanFront = 35;
    angle += 90;
    //pull target_angle from navigateToLargest
    //int scanAngle = angle + 90;
    angle *= M_PI / 180;

    //calculate below terms
    double scanFrontToObjectDist = distanceToObject + scanCenterToScanFront;
    double botCenterToObjectDist = 0;
    double turnAngle = 0;

    botCenterToObjectDist = sqrt(
            pow(botCenterToSensorCenterDist, 2) + pow(scanFrontToObjectDist, 2)
                    - 2
                            * ((botCenterToSensorCenterDist)
                                    * (scanFrontToObjectDist)) * cos(angle));


    turnAngle =
            acos(((pow(botCenterToObjectDist, 2))
                    + (pow(botCenterToSensorCenterDist, 2))
                    - (pow(scanFrontToObjectDist, 2)))
                    / (2 * botCenterToObjectDist * botCenterToSensorCenterDist));
    turnAngle *= 180 / M_PI;
    return turnAngle;
}



// Function that navigates to pharmacy
void navigate_to_largest_object(oi_t *sensor_data, int largest_index)
{
    // Validate the largest index
    if (largest_index < 0 || largest_index >= object_count)
    {
        uart_sendStr("Invalid largest index. Cannot navigate.\n");
        return;
    }

    // Loop to ensure a sufficiently large object is found
    while (1)
    {
        // Check if the largest object has sufficient width
        if (detected_objects[largest_index].linear_width > 150)
        {
            break; // Exit loop if a valid object is found
        }

        uart_sendStr(
                "The largest object is too small (width <= 150). Rescanning.\n");

        // Move forward and rescan
        move_forward(sensor_data, 70);
        perform_180_ir_scan(sensor_data);

        // Update `largest_index` after rescan
        float max_width = 0;
        int temp_index = -1;
        int i;
        for (i = 0; i < object_count; i++)
        {
            if (detected_objects[i].linear_width > max_width)
            {
                max_width = detected_objects[i].linear_width;
                temp_index = i;
            }
        }

        // Update largest_index only if objects were found
        if (temp_index >= 0)
        {
            largest_index = temp_index;
        }
        else
        {
            uart_sendStr(
                    "No objects detected during rescan. Continuing forward.\n");
        }
    }

    // Calculate target angle and distance
    int target_angle = (detected_objects[largest_index].start_angle
            + detected_objects[largest_index].end_angle) / 2;
    float new_distance = detected_objects[largest_index].ping_distance - 7;

    // Validate target angle
    if (target_angle < 0 || target_angle > 180)
    {
        char error_message[80];
        snprintf(error_message, sizeof(error_message),
                 "Invalid target angle: %d. Aborting.\n", target_angle);
        uart_sendStr(error_message);
        return;
    }

    // Turn and move towards the object
    char message[80];
    snprintf(message, sizeof(message), "Turning to target angle: %d degrees\n",
             target_angle);
    uart_sendStr(message);
    servo_move(target_angle);


    if (new_distance > TARGET_DISTANCE_CM)
    {

        // Turn and move forward
        if (target_angle < 90)
        {
            turn_clockwise(sensor_data, 90 - target_angle);
        }
        else
        {
            turn_counter_clockwise(sensor_data, target_angle - 90);
        }

        move_forward(sensor_data, 400);
        turn_counter_clockwise(sensor_data, 45);
        move_forward(sensor_data, 40);
        lcd_menu(sensor_data);
    }
}



// Function to drive to patient room after sending from pharmacy
void navigate_to_patient_room(oi_t *sensor_data, int largest_index)
{
    // Validate the largest index
    if (largest_index < 0 || largest_index >= object_count)
    {
        uart_sendStr("Invalid largest index. Cannot navigate.\n");
        return;
    }

    // Loop to ensure a sufficiently large object is found
    while (1)
    {
        // Check if the largest object has sufficient width
        if (detected_objects[largest_index].linear_width > 150)
        {
            break; // Exit loop if a valid object is found
        }

        uart_sendStr(
                "The largest object is too small (width <= 150). Rescanning.\n");

        // Move forward and rescan
        move_forward(sensor_data, 70);
        perform_180_ir_scan(sensor_data);

        // Update `largest_index` after rescan
        float max_width = 0;
        int temp_index = -1;
        int i;
        for (i = 0; i < object_count; i++)
        {
            if (detected_objects[i].linear_width > max_width)
            {
                max_width = detected_objects[i].linear_width;
                temp_index = i;
            }
        }

        // Update largest_index only if objects were found
        if (temp_index >= 0)
        {
            largest_index = temp_index;
        }
        else
        {
            uart_sendStr(
                    "No objects detected during rescan. Continuing forward.\n");
        }
    }

    // Calculate target angle and distance
    int target_angle = (detected_objects[largest_index].start_angle
            + detected_objects[largest_index].end_angle) / 2;
    float new_distance = detected_objects[largest_index].ping_distance - 7;

    // Validate target angle
    if (target_angle < 0 || target_angle > 180)
    {
        char error_message[80];
        snprintf(error_message, sizeof(error_message),
                 "Invalid target angle: %d. Aborting.\n", target_angle);
        uart_sendStr(error_message);
        return;
    }

    // Turn and move towards the object
    char message[80];
    snprintf(message, sizeof(message), "Turning to target angle: %d degrees\n",
             target_angle);
    uart_sendStr(message);
    servo_move(target_angle);


    if (new_distance > TARGET_DISTANCE_CM)
    {

        // Turn and move forward
        if (target_angle < 90)
        {
            turn_clockwise(sensor_data, 90 - target_angle);
        }
        else
        {
            turn_counter_clockwise(sensor_data, target_angle - 90);
        }
        move_forward(sensor_data, 350);


}
}

// Function to drive to home after patient room
void navigate_to_home(oi_t *sensor_data, int largest_index)
{
    // Validate the largest index
    if (largest_index < 0 || largest_index >= object_count)
    {
        uart_sendStr("Invalid largest index. Cannot navigate.\n");
        return;
    }

    // Loop to ensure a sufficiently large object is found
    while (1)
    {
        // Check if the largest object has sufficient width
        if (detected_objects[largest_index].linear_width > 300)
        {
            break; // Exit loop if a valid object is found
        }

        uart_sendStr(
                "The largest object is too small (width <= 150). Rescanning.\n");

        // Move forward and rescan
        move_forward(sensor_data, 70);
        perform_180_ir_scan(sensor_data);

        // Update `largest_index` after rescan
        float max_width = 0;
        int temp_index = -1;
        int i;
        for (i = 0; i < object_count; i++)
        {
            if (detected_objects[i].linear_width > max_width)
            {
                max_width = detected_objects[i].linear_width;
                temp_index = i;
            }
        }

        // Update largest_index only if objects were found
        if (temp_index >= 0)
        {
            largest_index = temp_index;
        }
        else
        {
            uart_sendStr(
                    "No objects detected during rescan. Continuing forward.\n");
        }
    }

    // Calculate target angle and distance
    int target_angle = (detected_objects[largest_index].start_angle
            + detected_objects[largest_index].end_angle) / 2;
    float new_distance = detected_objects[largest_index].ping_distance - 7;

    // Validate target angle
    if (target_angle < 0 || target_angle > 180)
    {
        char error_message[80];
        snprintf(error_message, sizeof(error_message),
                 "Invalid target angle: %d. Aborting.\n", target_angle);
        uart_sendStr(error_message);
        return;
    }

    // Turn and move towards the object
    char message[80];
    snprintf(message, sizeof(message), "Turning to target angle: %d degrees\n",
             target_angle);
    uart_sendStr(message);
    servo_move(target_angle);


    if (new_distance > TARGET_DISTANCE_CM)
    {

        // Turn and move forward
        if (target_angle < 90)
        {
            turn_clockwise(sensor_data, 90 - target_angle);
        }
        else
        {
            turn_counter_clockwise(sensor_data, target_angle - 90);
        }

        move_forward(sensor_data, 50);

    }
}

// Function to scan for bed one and drive to it
void bed_one(oi_t *sensor_data, int smallest_index) // smallest object
{
    perform_180_ir_scan(sensor_data);

    if (object_count == 0)
    {
        uart_sendStr("\nNo beds detected.\n");
        return;
    }

    int i;
    float smallest_width = detected_objects[0].end_angle
            - detected_objects[0].start_angle;

    int smallest_index_temp = 0;  // Use a temporary variable for smallest index

    // Find the smallest object by comparing their angular widths
    for (i = 1; i < object_count; i++)
    {
        float width = detected_objects[i].end_angle
                - detected_objects[i].start_angle;
        if (width < smallest_width)
        {
            smallest_width = width;
            smallest_index_temp = i;
        }
    }

    // Update the global smallest_index
    smallest_index = smallest_index_temp;

    // Display the details of the smallest detected object
    uart_sendStr("\nBed one detected\n");
    char message[100];
    snprintf(message, sizeof(message),
             "Start Angle: %d, End Angle: %d, Distance: %d cm\n",
             detected_objects[smallest_index].start_angle,
             detected_objects[smallest_index].end_angle,
             detected_objects[smallest_index].distance);
    uart_sendStr(message);

    int target_angle = (detected_objects[smallest_index].start_angle
            + detected_objects[smallest_index].end_angle) / 2;
    float new_distance = detected_objects[smallest_index].ping_distance - 7;
    // Validate target angle
        if (target_angle < 0 || target_angle > 180)
        {
            char error_message[80];
            snprintf(error_message, sizeof(error_message),
                     "Invalid target angle: %d. Aborting.\n", target_angle);
            uart_sendStr(error_message);
            return;
        }

        // Turn and move towards the object
        snprintf(message, sizeof(message), "Turning to target angle: %d degrees\n",
                 target_angle);
        uart_sendStr(message);
        servo_move(target_angle);


        if (new_distance > TARGET_DISTANCE_CM)
        {

            // Turn and move forward
            if (target_angle < 90)
            {
                turn_clockwise(sensor_data, 90 - target_angle);
            }
            else
            {
                turn_counter_clockwise(sensor_data, target_angle - 90);
            }
            move_forward(sensor_data, 350);
        }
}

// Function to scan for bed two and drive to it
void bed_two(oi_t *sensor_data, int middle_index) // middle sized object
{
    {
        perform_180_ir_scan(sensor_data);

        if (object_count == 0)
        {
            uart_sendStr("\nNo beds detected.\n");
            return;
        }

        int i;
        int middle_index_temp = 0;

        float middle_width = detected_objects[0].end_angle
                - detected_objects[0].start_angle;

        // Find the middle object by comparing their angular widths
        for (i = 1; i < object_count; i++)
        {
            float width = detected_objects[i].end_angle
                    - detected_objects[i].start_angle;
            if (width < middle_width && width > middle_width)
            {
                middle_width = width;
                middle_index_temp = i;

            }
        }
        // Update the global largest_index
        middle_index = middle_index_temp;

        // Display the details of the middle detected object
        uart_sendStr("\nBed two detected\n");
        char message[100];
        snprintf(message, sizeof(message),
                 "Start Angle: %d, End Angle: %d, Distance: %d cm\n",
                 detected_objects[middle_index].start_angle,
                 detected_objects[middle_index].end_angle,
                 detected_objects[middle_index].distance);
        uart_sendStr(message);

        int target_angle = (detected_objects[smallest_index].start_angle
                    + detected_objects[smallest_index].end_angle) / 2;
            float new_distance = detected_objects[largest_index].ping_distance - 7;

            // Validate target angle
                if (target_angle < 0 || target_angle > 180)
                {
                    char error_message[80];
                    snprintf(error_message, sizeof(error_message),
                             "Invalid target angle: %d. Aborting.\n", target_angle);
                    uart_sendStr(error_message);
                    return;
                }

                // Turn and move towards the object
                snprintf(message, sizeof(message), "Turning to target angle: %d degrees\n",
                         target_angle);
                uart_sendStr(message);
                servo_move(target_angle);


                if (new_distance > TARGET_DISTANCE_CM)
                {

                    // Turn and move forward
                    if (target_angle < 90)
                    {
                        turn_clockwise(sensor_data, 90 - target_angle);
                    }
                    else
                    {
                        turn_counter_clockwise(sensor_data, target_angle - 90);
                    }
                    move_forward(sensor_data, 350);
                }
    }
}

// // Function to scan for bed three and drive to it
void bed_three(oi_t *sensor_data, int largest_index) // largest object
{
    perform_180_ir_scan(sensor_data);

    if (object_count == 0)
    {
        uart_sendStr("\nNo beds detected.\n");
        return;
    }

    int i;
    float largest_width = detected_objects[0].end_angle
            - detected_objects[0].start_angle;

    // Find the largest object by comparing their angular widths
    for (i = 1; i < object_count; i++)
    {
        float width = detected_objects[i].end_angle
                - detected_objects[i].start_angle;
        if (width > largest_width)
        {
            largest_width = width;
            largest_index = i;
        }
    }

    // Display the details of the largest detected object
    uart_sendStr("\nBed three detected\n");
    char message[100];
    snprintf(message, sizeof(message),
             "Start Angle: %d, End Angle: %d, Distance: %d cm\n",
             detected_objects[largest_index].start_angle,
             detected_objects[largest_index].end_angle,
             detected_objects[largest_index].distance);
    uart_sendStr(message);

    int target_angle = (detected_objects[largest_index].start_angle
                + detected_objects[largest_index].end_angle) / 2;
        float new_distance = detected_objects[largest_index].ping_distance - 7;
        // Validate target angle
            if (target_angle < 0 || target_angle > 180)
            {
                char error_message[80];
                snprintf(error_message, sizeof(error_message),
                         "Invalid target angle: %d. Aborting.\n", target_angle);
                uart_sendStr(error_message);
                return;
            }

            // Turn and move towards the object
            snprintf(message, sizeof(message), "Turning to target angle: %d degrees\n",
                     target_angle);
            uart_sendStr(message);
            servo_move(target_angle);


            if (new_distance > TARGET_DISTANCE_CM)
            {

                // Turn and move forward
                if (target_angle < 90)
                {
                    turn_clockwise(sensor_data, 90 - target_angle);
                }
                else
                {
                    turn_counter_clockwise(sensor_data, target_angle - 90);
                }
                move_forward(sensor_data, 350);

    }

}

void handle_uart_data(char command, oi_t *sensor_data)
{
    switch (command)
    {
    case 'w':
    case 'a':
    case 's':
    case 'd':
        control_movement(sensor_data, command);
        uart_sendStr("Movement command executed.\n");
        break;
    case 't':
        if (current_mode == MANUAL)
        {
            current_mode = AUTONOMOUS_SCAN;
            uart_sendStr(
                    "Switched to Autonomous Mode. Press 'h' to start scanning.\n");
        }
        else
        {
            current_mode = MANUAL;
            uart_sendStr("Switched to Manual Mode.\n");
        }
        break;
    case 'h':
        if (current_mode == AUTONOMOUS_SCAN)
        {
            perform_180_ir_scan(sensor_data); // Perform a 180-degree IR scan
            display_largest_object(sensor_data);
            uart_sendStr(
                    "Press 'h' again to move towards the largest object.\n");
            current_mode = AUTONOMOUS_TURN;

        }
        else if (current_mode == AUTONOMOUS_TURN
                || current_mode == AUTONOMOUS_MOVE)
        {
            navigate_to_largest_object(sensor_data, largest_index); // Navigate to the largest detected object

        }
        break;
    case 'q':
        uart_sendStr("Disconnecting from Client.\n");
        break;
    default:
        uart_sendStr("Invalid command received.\n");
        break;
    }
}

