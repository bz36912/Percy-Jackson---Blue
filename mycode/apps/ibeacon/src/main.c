/**
 * @file main.c
 * @author Bolong Zhang
 * @brief the entry point for the Prac2 code for Thingy52
 * @version 0.1
 * @date 2024-03-24
 * 
 * @copyright Copyright (c) 2024
 * 
 */

#include "my_sensor.h"
#include "ble_data.h"

/**
 * @brief the main function
 * 
 * @return int, 0 on success
 */
int main(void)
{
	printf("Starting iBeacon Demo debug\n");
	ble_setup();
	// the sensors
	const struct device *const accMeter = DEVICE_DT_GET_ONE(st_lis2dh);
	mysensor_setup(accMeter);

	printf("before the while loop\n");
	while (true) {
		float readings[AD_MAX_NUM_READINGS * ACC_NUM_AXIS];
		for (int i = 0; i < AD_MAX_NUM_READINGS; i++) {
			float* values = readings + i * ACC_NUM_AXIS;
			if (!mysensor_process_array_data(accMeter, ACC_NUM_AXIS, SENSOR_CHAN_ACCEL_XYZ, values)) {
				printf("xyz: (%.2f, %.2f, %.2f)\n", (double)(values[X_AXIS]), (double)(values[Y_AXIS]), (double)(values[Z_AXIS]));
			}
			k_sleep(K_MSEC(BLE_ADVERTISEMENT_DURATION / AD_MAX_NUM_READINGS));
		}
		
		ble_advertise_readings(readings);
	}

	return 0;
}