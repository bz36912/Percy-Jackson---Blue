/**
 * @file main.c
 * @author Bolong Zhang
 * @brief Prac2 main entry point
 * @version 0.1
 * @date 2024-03-24
 * 
 * @copyright Copyright (c) 2024
 * 
 */
#include "ble_data.h"
#include "usb_uart.h"

/**
 * @brief main function
 * 
 * @return int, 0 on success
 */
int main(void)
{
	ble_setup();
	float readings[AD_MAX_NUM_READINGS * ACC_NUM_AXIS];
	
	printf("before the while loop\n");
	while (true) {
		if (k_msgq_get(&bleQueue, &readings, K_MSEC(500)) == 0) {
			for (int i = 0; i < AD_MAX_NUM_READINGS; i += ACC_NUM_AXIS) {
				char buf[64];
				float* timeStep = readings + i;
				sprintf(buf, "{'x': %.2f, 'y': %.2f, 'z': %.2f}", (double)timeStep[X_AXIS], (double)timeStep[Y_AXIS], (double)timeStep[Z_AXIS]);
				usb_uart_send_str(buf);
			}
		}
	}
	return 0;
}
