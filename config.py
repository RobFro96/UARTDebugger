"""
UART DEBUGGER
Author: Robert Fromm
Date: 17.04.2024

Checking the presents of serial ports. Printing the received data.
Configuration file
"""


class config:
    # Enable Windows DPI awareness for sharped GUI on highres monitors
    dpi_aware = True

    # Templates for RegEx groups: dict containing display_name, regex and baudrate
    templates = [
        {"display_name": "Launchpad", "regex": "^MSP Application UART", "baudrate": 9600}
    ]

    # Blacklist serial ports by their description
    blacklist_by_descr = ["^Standardmäßgige Seriell"]

    # Blacklist serial ports by their port name (COM... or /dev/tty...)
    blacklist_by_port = ["COM1"]

    # Radio buttons for typical baud rates
    radio_box_baudrates = [9600, 115200]

    # Default selection
    default_baudrate_selection = 9600

    # Default value of custom baud rate
    default_custom_baudrate = 19200

    # filter all non-ASCII characters from console
    ascii_filter = True

    # Format of the line
    line_formatter = "\033[1m\033[90m[%(port)s]\033[0m %(msg)s"

    # Format of the logger
    coloredlogs_format = "%(asctime)s,%(msecs)03d %(message)s"

    # Time format of the logger
    coloredlogs_dateformat = "%H:%M:%S"

    # Polling delay
    delay = 0.5

    # Disable custom symbols
    no_symbols = False
