#ifndef PING_H_
#define PING_H_

#include <stdint.h>
#include <stdbool.h>

void ping_init(void);

void send_pulse(void);

float ping_read(void);

void TIMER3B_Handler(void);


#endif /* PING_H_ */
