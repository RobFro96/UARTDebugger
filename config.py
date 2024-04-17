"""
UART DEBUGGER
Author: Robert Fromm
Date: 17.04.2024

Checking the presents of serial ports. Printing the received data.
Configuration file
"""


class config:
    dpi_aware = True    # Enable Windows DPI awareness for sharped GUI on highres monitors

    # Templates for RegEx groups: dict containing display_name, regex and baudrate
    templates = [
        {"display_name": "Launchpad", "regex": "^MSP Application UART", "baudrate": 9600}
    ]
    blacklist_by_descr = ["^Standardmäßgige Seriell"]
    blacklist_by_port = ["COM1"]
    radio_box_baudrates = [9600, 115200]
    default_baudrate_selection = 9600
    default_custom_baudrate = 19200
    ascii_filter = True
    line_formatter = "\033[1m\033[90m[%(port)s]\033[0m %(msg)s"
    coloredlogs_format = "%(asctime)s,%(msecs)03d %(message)s"
    coloredlogs_dateformat = "%H:%M:%S"
    delay = 0.5
    no_symbols = False
