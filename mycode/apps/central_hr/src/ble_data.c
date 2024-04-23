#include "ble_data.h"
#include <zephyr/bluetooth/hci.h>

static struct bt_le_scan_param scan_param = {
	.type       = BT_LE_SCAN_TYPE_PASSIVE,
	.options    = BT_LE_SCAN_OPT_NONE,
	.interval   = BT_GAP_SCAN_FAST_INTERVAL,
	.window     = BT_GAP_SCAN_FAST_WINDOW,
};

K_MSGQ_DEFINE(bleQueue, sizeof(float) * AD_MAX_NUM_READINGS * ACC_NUM_AXIS, 20, 1);
static char targetAddr[BT_ADDR_LE_STR_LEN] = ""; // the BLE address to look/filter for

static void ble_to_readings(uint8_t input[AD_PAYLOAD_LEN], float* output) {
    short temp;
    for (int i = 0; i < AD_PAYLOAD_LEN; i += 2) {
        memcpy(&temp, input + i, sizeof(temp));
        output[i / 2] = (float)temp / (float)100.0;
    }
}

static bool search_eir_found(struct bt_data *data, void *addrStr)
{
    const uint8_t AD_UUID[AD_UUID_LEN] = {0xF1, 0x45, 0x98, 0x91};
    if (!memcmp(AD_UUID, data->data, AD_UUID_LEN)) {
        printf("FOUND the device. Its addr is %s, its length: %d, type: %d\n", (char*)addrStr, data->data_len, data->type);
        strcpy(targetAddr, (char*)addrStr);
    }
    return false;
}

static bool extract_eir_found(struct bt_data *data, void *addrStr)
{
    float readings[AD_MAX_NUM_READINGS * ACC_NUM_AXIS];
    ble_to_readings((uint8_t*)(data->data) + AD_UUID_LEN, readings);
    if (k_msgq_put(&bleQueue, &readings, K_NO_WAIT)) {
        printf("adding to bleQueue failed\n");
    }
    return false;
}

/**
 * @brief callback when any device is found during scanning
 * 
 * @param addr addr of the device
 * @param rssi signal intensity
 * @param type type of device
 * @param ad its content of advertisement
 */
static void ble_scan_device_found(const bt_addr_le_t *addr, int8_t rssi, uint8_t type,
			 struct net_buf_simple *ad)
{
    char addrStr[BT_ADDR_LE_STR_LEN];
    bt_addr_le_to_str(addr, addrStr, sizeof(addrStr));
    if (strlen(targetAddr) == 0) { //find the device address
        printf("searching for device: %s, AD evt type %u, AD data len %u, RSSI %i\n",
		addrStr, type, ad->len, rssi);
        bt_data_parse(ad, search_eir_found, (void *)addrStr);
    } else { // use the found address to filter for the correct device
        if (strstr(addrStr, targetAddr) == NULL) {
            return; // wrong device
        }
        bt_data_parse(ad, extract_eir_found, (void *)addrStr);
    }
}

extern void ble_setup() {
    int err;
	err = bt_enable(NULL);
    if (err) {
		printf("Bluetooth init failed (err %d)\n", err);
		return;
	}

    if (bt_le_scan_start(&scan_param, ble_scan_device_found)) {
        printf("rssi_scan(): scan failed to start");
    }
}