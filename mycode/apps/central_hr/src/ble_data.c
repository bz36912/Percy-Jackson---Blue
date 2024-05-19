#include "ble_data.h"
#include <zephyr/bluetooth/hci.h>

static struct bt_le_scan_param scan_param = {
	.type       = BT_LE_SCAN_TYPE_PASSIVE,
	.options    = BT_LE_SCAN_OPT_NONE,
	.interval   = BT_GAP_SCAN_FAST_INTERVAL,
	.window     = BT_GAP_SCAN_FAST_WINDOW,
};

K_MSGQ_DEFINE(bleQueue, sizeof(float) * QUEUE_ELEM_SIZE, 20, 1);
static char targetAddr[BT_ADDR_LE_STR_LEN] = ""; // the BLE address to look/filter for

/**
 * @brief convert the encoded bytes into floats
 * 
 * @param input the encoded bytes
 * @param output floats
 */
static void ble_to_readings(uint8_t input[AD_PAYLOAD_LEN], float* output) {
    short temp;
    for (int i = 0; i < AD_PAYLOAD_LEN; i += 2) {
        memcpy(&temp, input + i, sizeof(temp));
        output[i / 2] = (float)temp / (float)100.0;
    }
}

/**
 * @brief NRF board uses this function to check if BLE device on the scan is Thingy:52
 * 
 * @param data the scanned device's data
 * @param addrStr the MAC address string of the scanned device
 * @return true there is more information after this packet
 * @return false all information of this packet is read
 */
static bool search_eir_found(struct bt_data *data, void *addrStr)
{
    const uint8_t AD_UUID[AD_UUID_LEN] = {0xF1, 0x45, 0x98};
    if (!memcmp(AD_UUID, data->data, AD_UUID_LEN)) {
        printf("FOUND the device. Its addr is %s, its length: %d, type: %d\n", (char*)addrStr, data->data_len, data->type);
        strcpy(targetAddr, (char*)addrStr);
    }
    return false;
}

static int transIndex = 0; // used to find duplicate advertisements being received
/**
 * @brief after finding the Thingy:52, this function reads the acceleration information 
 * in the Thingy:52 advertisement
 * 
 * @param data the scanned device's data
 * @param addrStr the MAC address string of the scanned device
 * @return true there is more information after this packet
 * @return false all information of this packet is read
 */
static bool extract_eir_found(struct bt_data *data, void *addrStr)
{
    float readings[QUEUE_ELEM_SIZE];
    if (data->data[AD_UUID_LEN] == transIndex) { // the bytes after UUID indexes the transmission over time
        printf("duplicate ad: %d\n", transIndex);
        return false; // this is a duplicate advertisement, so don't add to the queue
    }
    transIndex = data->data[AD_UUID_LEN];

    // creating the element to be added to the queue
    readings[QUEUE_ELEM_SIZE - 1] = data->data[AD_UUID_LEN]; 
    ble_to_readings((uint8_t*)(data->data) + AD_UUID_LEN + AD_INDEX_LEN, readings);
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

/**
 * @brief sets up the BLE in Zephyr
 * 
 */
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