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
char mode[30] = "AWARE";
int is_playing = 0;

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

    while (1) 
    {
        // Read the buffer content from UART TX which is sent from python applicaton
        int buffer_len = uart_read_bytes(UART_PORT, data, BUF_SIZE - 1, 100 / portTICK_PERIOD_MS);  

        if (buffer_len > 0) 
        {
            data[buffer_len] = '\0';     // Convert bytes to C string...

            if (strncmp((char*)data, "CMD:SET_VOLUME:", 15) == 0) 
            {
                int value = atoi((char*)data + 15);
                // Calculate the value of ESP32 responce and send it 
                if (value < 0) value = 0;
                if (value > 100) value = 100;

                volume = value;

                printf("RESP:VOLUME:%d\n", volume);                             
            }
            else if (strncmp((char*)data, "CMD:GET_VOLUME", 14) == 0)
            {
                printf("RESP:VOLUME:%d\n", volume);
            }
            else if (strncmp((char*)data, "CMD:PLAY", 8) == 0)
            {
                is_playing = 1;
                printf("RESP:PLAYING:1\n");
            }
            else if (strncmp((char*)data, "CMD:PAUSE", 8) == 0)
            {
                is_playing = 0;
                printf("RESP:PLAYING:0\n");
            }
            else if (strncmp((char*)data, "CMD:PLAY", 8) == 0)
            {
                is_playing = 1;
                printf("RESP:PLAYING:1\n");
            }
            else if (strncmp((char*)data, "CMD:SET_MODE:", 13) == 0) 
            {
                char *new_mode = (char*)data + 13;
                // remove newline if present
                new_mode[strcspn(new_mode, "\r\n")] = 0;
                strncpy(mode, new_mode, sizeof(mode) - 1);
                mode[sizeof(mode) - 1] = '\0';
                printf("RESP:MODE:%s\n", mode);
            }
            else if (strncmp((char*)data, "CMD:GET_MODE", 12) == 0) 
            {
                printf("RESP:MODE:%s\n", mode);
            }
            else
            {
                printf("ERR:INVALID_CMD\n");
            }
        }
    }
}