#ifndef RSSI_DATA_H
#define RSSI_DATA_H

#include "common_lib.h"
#include <zephyr/bluetooth/bluetooth.h>

// controls the advertisement
#define BLE_ADVERTISEMENT_DURATION 200 // in milli-seconds

#define ACC_NUM_AXIS 3
#define ACC_BYTES_PER_READING (ACC_NUM_AXIS * 2)
#define X_AXIS 0
#define Y_AXIS 1
#define Z_AXIS 2

// format parameter for the BLE protocol
#define AD_MAX_NUM_BYTES 28
#define AD_UUID_LEN 4
#define AD_PAYLOAD_LEN (AD_MAX_NUM_BYTES - AD_UUID_LEN)
#define AD_MAX_NUM_READINGS (int)(AD_PAYLOAD_LEN / ACC_BYTES_PER_READING)

extern void ble_advertise_readings(float* readings);
extern void ble_setup();

#endif