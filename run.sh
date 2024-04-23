#!/bin/bash
if [ -z "$1" ]; then
    echo "flashing nrf52840dk_nrf52840"
    west build -b nrf52840dk_nrf52840 mycode/apps/central_hr --pristine && west flash --recover
else
    echo "flashing Thingy52"
    west build -b thingy52_nrf52832 mycode/apps/ibeacon --pristine && west flash --recover
fi

# mycode/apps/shell_module
# native_tty
# peripheral_hr
# central_hr
# nrf52840dk_nrf52840
# thingy52_nrf52832