#ifndef USB_UART_H
#define USB_UART_H

#include <zephyr/device.h>
#include <zephyr/drivers/uart.h>
#include "common_lib.h"

extern void usb_uart_send_str(char *str);
extern int usb_uart_setup();

#endif