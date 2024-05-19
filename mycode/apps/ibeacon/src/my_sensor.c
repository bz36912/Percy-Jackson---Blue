/**
 * @file my_sensor.c
 * @author Bolong Zhang
 * @brief the sensors on the Thingy52
 * @version 0.1
 * @date 2024-03-24
 * 
 * @copyright Copyright (c) 2024
 * 
 */
#include "my_sensor.h"

/**
 * @brief initiates a sensor
 * 
 * @param dev the sensor device
 * @return int, 0 on success
 */
int mysensor_setup(const struct device *dev) {
    printf("device is %p, name is %s\n", dev, dev->name);
    if (!device_is_ready(dev)) {
		printf("device not ready:\n");
		return -1;
	}
    return 0;
}

/**
 * @brief extracts the sensor reading
 * For hts221, the function extracts temperature and humidity together, by setting numChannel to 2
 * 
 * @param dev the sensor device
 * @param numChannels number of sensors contained in the sensor device
 * @param channels the index number indicating the types of sensor reading
 * @param values where the reading will be stored
 * @return int 
 */
int mysensor_process_sample(const struct device *dev, int numChannels, int* channels, float* values)
{
	struct sensor_value sensorValue;
	if (sensor_sample_fetch(dev) < 0) {
		printf("Sensor sample update error\n");
        printf("device is %p, name is %s\n", dev, dev->name);
		return -1;
	}

	// iterates through each channel
    for (int i = 0; i < numChannels; i++) {
        if (sensor_channel_get(dev, (enum sensor_channel)(channels[i]), &sensorValue) < 0) {
		    printf("Cannot read %dth channel (%d)\n", i, channels[i]);
            printf("device is %p, name is %s\n", dev, dev->name);
		    return -2;
	    }
        values[i] = (float)sensor_value_to_double(&sensorValue);
    }
    return 0;
}

/**
 * @brief extracts the sensor reading. Used when the sensor reading is stored as an array.
 * For accelerometer, the array is {x, y, z}
 * 
 * @param dev the sensor device
 * @param arraySize the number of values to read
 * @param channel the index number indicating the types of sensor reading
 * @param values where the readings will be stored
 * @return int 
 */
int mysensor_process_array_data(const struct device *dev, int arraySize, int channel, float* values) {
	struct sensor_value sensorValue[arraySize];
	if (sensor_sample_fetch(dev) < 0) {
		printf("Sensor sample update error\n");
        printf("device is %p, name is %s\n", dev, dev->name);
		return -1;
	}

	// selects the channel
	if (sensor_channel_get(dev, (enum sensor_channel)(channel), sensorValue) < 0) {
		printf("Cannot read channel (%d)\n", channel);
		printf("device is %p, name is %s\n", dev, dev->name);
		return -2;
	}
	// iterates through each value in the array
    for (int i = 0; i < arraySize; i++) {
        values[i] = (float)sensor_value_to_double(&(sensorValue[i]));
    }
    return 0;
}
