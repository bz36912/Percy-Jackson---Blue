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
#ifndef MY_SENSOR_H
#define MY_SENSOR_H

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/sensor.h>
#include <stdio.h>
#include <zephyr/sys/util.h>
#include <zephyr/drivers/sensor/ccs811.h>

int mysensor_process_sample(const struct device *dev, int numChannels, int* channels, float* values);
int mysensor_setup(const struct device *dev);
int mysensor_process_array_data(const struct device *dev, int arraySize, int channel, float* values);

#endif