#include "ble_data.h"
#include <zephyr/bluetooth/hci.h>

static bool firstTime = true; // flag; true if advertisement has not started
static bool enablePrint = true;

static void ble_to_bytes(float* input, uint8_t output[AD_PAYLOAD_LEN]) {
    for (int i = 0; i < AD_PAYLOAD_LEN; i += 2) {
        short temp;
        if (input > 0) {
            temp = (short)(input[i / 2] * (float)100.0 + (float)0.5);
        } else {
            temp = (short)(input[i / 2] * (float)100.0 - (float)0.5);
        }
        // printf("short (%d) has %d\n", temp, sizeof(temp));
        memcpy(output + i, &temp, sizeof(short));
    }
}

static const struct bt_data ble_create_advert(float* readings, uint8_t* output) {
    const uint8_t AD_UUID[AD_UUID_LEN] = {0xF1, 0x45, 0x98, 0x91};
    memset(output, 0, (size_t)(AD_MAX_NUM_BYTES));
    // setting the UUID
    memcpy(output, AD_UUID, AD_UUID_LEN); // sets the UUID values

    ble_to_bytes(readings, output + AD_UUID_LEN);

    const struct bt_data content = {
        .type = BT_DATA_MANUFACTURER_DATA,
		.data = (const uint8_t*)output,
		.data_len = (uint8_t)(AD_MAX_NUM_BYTES)
    };

    return content;
}

extern void ble_advertise_readings(float* readings) {
    uint8_t output[AD_MAX_NUM_BYTES];
    const struct bt_data content = ble_create_advert(readings, output);
	const struct bt_data ad[] = {
        content,
	};

    if (enablePrint) {
        printf("content length: %d, ad[] size:%d\n", content.data_len, ARRAY_SIZE(ad));
        for (int i = 0; i < content.data_len; i++) {
            printf("0x%X ", content.data[i]);
        }
        printf("\n");
    }

    // start/update the advertisement
	if (firstTime) {
        for (int i = 0; i < 3; i++) {
            int rc = bt_le_adv_start(BT_LE_ADV_NCONN, ad, ARRAY_SIZE(ad),
			NULL, 0);
		    if (rc) {
			    printf("ERROR: advert start failed, with error code: %d\n", rc);
		    } else {
                firstTime = false;
                printf("advert started SUCCESSFULLY\n");
                break;
            }
        }
	} else {
		int rc = bt_le_adv_update_data(ad, ARRAY_SIZE(ad), NULL, 0);
		if (rc) {
			printf("ERROR: advert update failed, with error code: %d\n", rc);
		}
	}
}

extern void ble_setup() {
    int err;
	err = bt_enable(NULL);
    if (err) {
		printf("Bluetooth init failed (err %d)\n", err);
		return;
	}
}