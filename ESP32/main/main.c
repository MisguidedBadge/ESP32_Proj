/* Hello World Example

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/
// Standard libraries
#include <stdio.h>
#include <string.h>
// OS Stuff
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
// ESP System
#include "esp_system.h"
#include "esp_spi_flash.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
// NVS / TCP
#include "nvs_flash.h"
#include "tcpip_adapter.h"
//#include "protocol_examples_common.h"
// 
#include "driver/uart.h"
#include "driver/gpio.h"
#include "lwip/err.h"
#include "lwip/sockets.h"
#include "lwip/sys.h"
#include "lwip/netdb.h"


//#ifdef CONFIG_EXAMPLE_IPV4
//#define HOST_IP_ADDR CONFIG_EXAMPLE_IPV4_ADDR
//#else
//#defin HOST_IP_ADDR CONFIG_EXAMPLE_IPV6_ADDR

/* Set the SSID and Password via project configuration, or can set directly here */
#define DEFAULT_SSID CONFIG_EXAMPLE_WIFI_SSID
#define DEFAULT_PWD CONFIG_EXAMPLE_WIFI_PASSWORD

#if CONFIG_EXAMPLE_WIFI_ALL_CHANNEL_SCAN
#define DEFAULT_SCAN_METHOD WIFI_ALL_CHANNEL_SCAN
#elif CONFIG_EXAMPLE_WIFI_FAST_SCAN
#define DEFAULT_SCAN_METHOD WIFI_FAST_SCAN
#else
#define DEFAULT_SCAN_METHOD WIFI_FAST_SCAN
#endif /*CONFIG_EXAMPLE_SCAN_METHOD*/

#if CONFIG_EXAMPLE_WIFI_CONNECT_AP_BY_SIGNAL
#define DEFAULT_SORT_METHOD WIFI_CONNECT_AP_BY_SIGNAL
#elif CONFIG_EXAMPLE_WIFI_CONNECT_AP_BY_SECURITY
#define DEFAULT_SORT_METHOD WIFI_CONNECT_AP_BY_SECURITY
#else
#define DEFAULT_SORT_METHOD WIFI_CONNECT_AP_BY_SIGNAL
#endif /*CONFIG_EXAMPLE_SORT_METHOD*/

#if CONFIG_EXAMPLE_FAST_SCAN_THRESHOLD
#define DEFAULT_RSSI CONFIG_EXAMPLE_FAST_SCAN_MINIMUM_SIGNAL
#if CONFIG_EXAMPLE_FAST_SCAN_WEAKEST_AUTHMODE_OPEN
#define DEFAULT_AUTHMODE WIFI_AUTH_OPEN
#elif CONFIG_EXAMPLE_FAST_SCAN_WEAKEST_AUTHMODE_WEP
#define DEFAULT_AUTHMODE WIFI_AUTH_WEP
#elif CONFIG_EXAMPLE_FAST_SCAN_WEAKEST_AUTHMODE_WPA
#define DEFAULT_AUTHMODE WIFI_AUTH_WPA_PSK
#elif CONFIG_EXAMPLE_FAST_SCAN_WEAKEST_AUTHMODE_WPA2
#define DEFAULT_AUTHMODE WIFI_AUTH_WPA2_PSK
#else
#define DEFAULT_AUTHMODE WIFI_AUTH_OPEN
#endif
#else
#define DEFAULT_RSSI -127
#define DEFAULT_AUTHMODE WIFI_AUTH_OPEN
#endif /*CONFIG_EXAMPLE_FAST_SCAN_THRESHOLD*/



    wifi_config_t wifi_config = {
        .sta = {
            .ssid = "bigred12",
            .password = "12Mustangs$",
            .scan_method = DEFAULT_SCAN_METHOD,
            .sort_method = DEFAULT_SORT_METHOD,
            .threshold.rssi = DEFAULT_RSSI,
            .threshold.authmode = DEFAULT_AUTHMODE,
        },
    };

    
    uart_config_t uart_config = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_CTS_RTS,
        .rx_flow_ctrl_thresh = 122,
    };

void app_main(void)
{
    // Var init
    //const int uart_num = UART2;
    wifi_init_config_t init_config = WIFI_INIT_CONFIG_DEFAULT();
    wifi_mode_t mode = WIFI_MODE_STA;
    char * sentence = "Test \n";
    uint8_t data[128];
    int length = 0;
    const int uart_buffer_size = (1024 * 2);
    QueueHandle_t uart_queue;
    // Initialize Wifi and connect
    esp_err_t ret = nvs_flash_init();
    ESP_ERROR_CHECK(esp_wifi_init(&init_config));
    ESP_ERROR_CHECK(esp_wifi_set_mode(mode));
    ESP_ERROR_CHECK(esp_wifi_set_config(ESP_IF_WIFI_STA, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());
    ESP_ERROR_CHECK(esp_wifi_connect());

    // Configure UART parameters
    // Green TX , Red +V, Black GND, White RX
    ESP_ERROR_CHECK(uart_param_config(UART_NUM_2, &uart_config));
    ESP_ERROR_CHECK(uart_set_pin(UART_NUM_2, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE, 18, 19));
    ESP_ERROR_CHECK(uart_driver_install(UART_NUM_2, uart_buffer_size, 
                                                    uart_buffer_size, 10, &uart_queue, 0));
    ESP_ERROR_CHECK(uart_set_mode(UART_NUM_2, UART_MODE_RS485_HALF_DUPLEX));
    // UART Send
    while(1)
    {
    uart_write_bytes(UART_NUM_2, (const char *) sentence, strlen(sentence));
    ESP_ERROR_CHECK(uart_wait_tx_done(UART_NUM_2, 10000));
    // UART Receive
    ESP_ERROR_CHECK(uart_get_buffered_data_len(UART_NUM_2, (size_t*)&length));
    length = uart_read_bytes(UART_NUM_2, data, length, 10000);
    // Establish a socket connection if this is successful
    }    
    printf("%s \n", data);

    esp_wifi_disconnect();

    //delay(10000);

    fflush(stdout);
   // esp_restart();

}
