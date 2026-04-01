// FILE: audix_firmware.c 
// This file is the main entry point for the ESP32 firmware. 
// It initializes the necessary components and handles communication with the Python application.


#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/uart.h"

#define UART_PORT UART_NUM_0
#define BUF_SIZE 1024

int volume = 50;

void app_main(void)
{
    uart_config_t uart_config = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS,
        .parity    = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE
    };

    uart_param_config(UART_PORT, &uart_config);
    uart_driver_install(UART_PORT, BUF_SIZE, 0, 0, NULL, 0);

    uint8_t data[BUF_SIZE];

    printf("READY\n");

    while (1) {
        int len = uart_read_bytes(UART_PORT, data, BUF_SIZE - 1, 100 / portTICK_PERIOD_MS);

        if (len > 0) {
            data[len] = '\0';

            if (strstr((char*)data, "SET_VOLUME:")) {

                int value = atoi((char*)data + 11);
                if (value < 0) value = 0;
                if (value > 100) value = 100;
                volume = value;
                printf("OK:VOLUME=%d\n", volume);
            } 
            else {
                printf("ERROR\n");
            }
        }
    }
}