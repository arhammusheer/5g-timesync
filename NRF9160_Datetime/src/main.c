#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/drivers/gpio.h>

#include <modem/lte_lc.h>
#include <modem/modem_info.h>

#include <date_time.h>

/* SW0_NODE is the devicetree node identifier for the "sw0" alias */
#define SW0_NODE DT_ALIAS(sw0)
static const struct gpio_dt_spec button = GPIO_DT_SPEC_GET(SW0_NODE, gpios);

/* LED0_NODE is the devicetree node identifier for the "led0" alias. */
#define LED0_NODE DT_ALIAS(led0)
static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(LED0_NODE, gpios);
int64_t t;

void button_pressed(const struct device *dev, struct gpio_callback *cb, uint32_t pins)
{
    gpio_pin_toggle_dt(&led);
    int err = date_time_now(&t);
    if (err)
    {
        printk("Failed to get date and time: %d\n", err);
    }

    // MODEM_INFO_CUR_BAND
    // MODEM_INFO_SUP_BAND
    // MODEM_INFO_AREA_CODE
    // MODEM_INFO_UE_MODE
    // MODEM_INFO_CELLID
    // MODEM_INFO_IP_ADDRESS
    // MODEM_INFO_TEMP
    // MODEM_INFO_LTE_MODE
    // MODEM_INFO_NBIOT_MODE
    // MODEM_INFO_RSRP
    // MODEM_INFO_IMEI
    // MODEM_INFO_OPERATOR

    // Print format: TIME; CUR_BAND; SUP_BAND; AREA_CODE; UE_MODE; CELLID; IP_ADDRESS; TEMP; LTE_MODE; NBIOT_MODE; RSRP; IMEI; OPERATOR
    printk("Time: %lld; ", t);
    print_modem_info(MODEM_INFO_RSRP, false);
    printk("; ");
    print_modem_info(MODEM_INFO_CUR_BAND, false);
    printk("; ");
    print_modem_info(MODEM_INFO_SUP_BAND, false);
    printk("; ");
    print_modem_info(MODEM_INFO_AREA_CODE, false);
    printk("; ");
    print_modem_info(MODEM_INFO_UE_MODE, false);
    printk("; ");
    print_modem_info(MODEM_INFO_CELLID, false);
    printk("; ");
    print_modem_info(MODEM_INFO_IP_ADDRESS, false);
    printk("; ");
    print_modem_info(MODEM_INFO_TEMP, false);
    printk("; ");
    print_modem_info(MODEM_INFO_LTE_MODE, false);
    printk("; ");
    print_modem_info(MODEM_INFO_NBIOT_MODE, false);
    printk("; ");
    print_modem_info(MODEM_INFO_IMEI, false);
    printk("; ");
    print_modem_info(MODEM_INFO_OPERATOR, true);

    //
}

static struct gpio_callback button_cb_data;

void print_modem_info(enum modem_info info, bool next_line)
{
    int len;
    char buf[80];

    switch (info)
    {
    case MODEM_INFO_RSRP:
        printk("Signal Strength: ");
        break;
    case MODEM_INFO_IP_ADDRESS:
        printk("IP Addr: ");
        break;
    case MODEM_INFO_FW_VERSION:
        printk("Modem FW Ver: ");
        break;
    case MODEM_INFO_ICCID:
        printk("SIM ICCID: ");
        break;
    case MODEM_INFO_IMSI:
        printk("IMSI: ");
        break;
    case MODEM_INFO_IMEI:
        printk("IMEI: ");
        break;
    case MODEM_INFO_DATE_TIME:
        printk("Network Date/Time: ");
        break;
    case MODEM_INFO_APN:
        printk("APN: ");
        break;
    case MODEM_INFO_CELLID:
        printk("Cell ID: ");
        break;
    case MODEM_INFO_CUR_BAND:
        printk("Current Band: ");
        break;
    case MODEM_INFO_OPERATOR:
        printk("Operator: ");
        break;
    case MODEM_INFO_SUP_BAND:
        printk("Supported Bands: ");
        break;
    case MODEM_INFO_AREA_CODE:
        printk("Area Code: ");
        break;
    case MODEM_INFO_UE_MODE:
        printk("UE Mode: ");
        break;
    case MODEM_INFO_LTE_MODE:
        printk("LTE Mode: ");
        break;
    case MODEM_INFO_NBIOT_MODE:
        printk("NBIoT Mode: ");
        break;
    case MODEM_INFO_TEMP:
        printk("Temperature: ");
        break;
    default:
        printk("Unsupported: ");
        break;
    }

    len = modem_info_string_get(info, buf, 80);
    if (len > 0)
    {
        printk("%s", buf);
        if (next_line)
        {
            printk("\n");
        }
    }
    else
    {
        printk("Error\n");
    }
}

void main(void)
{
    int err, ret;

    printk("Initializing modem\n");

    err = nrf_modem_lib_init();
    if (err)
    {
        printk("Modem initialization failed, err %d\n", err);
        return;
    }

    printk("Waiting for network\n");

    err = lte_lc_init();
    if (err)
        printk("MODEM: Failed initializing LTE Link controller, error: %d\n", err);

    err = lte_lc_func_mode_set(LTE_LC_FUNC_MODE_ACTIVATE_UICC);
    if (err)
        printk("MODEM: Failed enabling UICC power, error: %d\n", err);
    k_msleep(100);

    err = modem_info_init();
    if (err)
        printk("MODEM: Failed initializing modem info module, error: %d\n", err);

    print_modem_info(MODEM_INFO_FW_VERSION, true);
    print_modem_info(MODEM_INFO_IMEI, true);
    print_modem_info(MODEM_INFO_ICCID, true);

    printk("Waiting for network... ");
    err = lte_lc_init_and_connect();
    if (err)
    {
        printk("Failed to connect to the LTE network, err %d\n", err);
        return;
    }

    printk("OK\n");
    print_modem_info(MODEM_INFO_APN, true);
    print_modem_info(MODEM_INFO_IP_ADDRESS, true);
    print_modem_info(MODEM_INFO_RSRP, true);
    // Your application code goes here

    k_msleep(500);

    ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT_LOW);
    if (ret < 0)
    {
        return;
    }

    ret = gpio_pin_configure_dt(&button, GPIO_INPUT);
    if (ret < 0)
    {
        return;
    }

    ret = gpio_pin_interrupt_configure_dt(&button, GPIO_INT_EDGE_TO_ACTIVE);
    gpio_init_callback(&button_cb_data, button_pressed, BIT(button.pin));
    gpio_add_callback(button.port, &button_cb_data);

    printk("Ready\n");

    // Print time every 10 seconds
    // while (1)
    // {
    //     k_msleep(9990);

    //     // Turn on LED
    //     gpio_pin_set_dt(&led, 1);
    //     k_msleep(10);

    //     // Print Time
    //     int err = date_time_now(&t);
    //     if (err)
    //     {
    //         printk("Failed to get date and time: %d\n", err);
    //     }
    //     printk("%lld\n", t);

    //     // Turn off LED
    //     gpio_pin_set_dt(&led, 0);

    // }
}
