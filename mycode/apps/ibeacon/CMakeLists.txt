# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(ibeacon)

FILE(GLOB app_sources src/*.c)
target_sources(app PRIVATE ${app_sources})
target_include_directories(app PRIVATE include)

if(IBEACON_RSSI)
  zephyr_compile_definitions(IBEACON_RSSI=${IBEACON_RSSI})
endif()
