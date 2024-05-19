#include "usb_uart.h"

#define UART_DEVICE_NODE DT_CHOSEN(zephyr_shell_uart)
static const struct device *const usbUart = DEVICE_DT_GET(UART_DEVICE_NODE);

/**
 * @brief sends uart message
 * 
 * @param str the message
 */
extern void usb_uart_send_str(char *str)
{
	int msg_len = (int)(strlen(str));
	for (int i = 0; i < msg_len; i++) {
		uart_poll_out(usbUart, str[i]);
        // k_sleep(K_MSEC(1));
	}
	uart_poll_out(usbUart, '\n');
}

/**
 * @brief sets up the UART connection to the PC
 * 
 * @return int 0 on success, else it is an error
 */
extern int usb_uart_setup() {
	if (!device_is_ready(usbUart)) {
		printf("UART device not found!");
		return -1;
	}
	return 0;
}