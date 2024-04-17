#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import threading

import coloredlogs
import serial

from config import config
from serial_select_window import SerialSelectWindow
from uart_debugger_utils import UartDebuggerUtils

"""
UART DEBUGGER
Author: Robert Fromm
Date: 08.01.2020

Checking the presents of serial ports. Printing the received data.
"""


class SerialThread(threading.Thread):
    """Class representing a single serial port. Thread continously reading the serial port and
    printing the data.
    """

    def __init__(self, port: UartDebuggerUtils.SerialPort, event: threading.Event) -> None:
        """construktor.

        Args:
            port (UartDebuggerUtils.SerialPort): port information
            event (threading.Event): event to stop the thread
        """
        threading.Thread.__init__(self)
        self.port = port
        self.event = event

    def run(self) -> None:
        """Run function that is started in the thread
        Continously trying to open and reading data from the serial port
        """
        is_connected = False
        while not self.event.wait(config.delay):
            try:
                connection = serial.Serial(self.port.port, self.port.baudrate, timeout=config.delay)
                self.print_line(b"\033[90mconnected")
                is_connected = True
                while not self.event.wait(1e-3):
                    buf = connection.readline()
                    if not buf:
                        continue
                    self.print_line(buf)
            except serial.SerialException:
                if is_connected:
                    self.print_line(b"\033[90mdisconnected")
                is_connected = False

    def print_line(self, buf: bytes) -> None:
        """Print a received by the serial port

        Args:
            buf (bytes): raw received data
        """
        # Remove non-ASCII data
        if config.ascii_filter:
            buf = bytearray([c for c in buf if c < 128])

        # Decode and convert to string
        msg = buf.decode("ansi")

        # Replace any special symbols
        if not config.no_symbols:
            msg = msg.replace("\\chk", "\u2713")

        # Remove trailing or leading whitespaces (e.g. new-line characters)
        msg = msg.strip()

        # Add additional information to the line
        msg = config.line_formatter % {"msg": msg, "port": self.port.port}

        # Print with logging library
        logging.info(msg)


def get_ports_by_result(result: SerialSelectWindow.Result) -> list[UartDebuggerUtils.SerialPort]:
    """Get the port information based on the result of the SerialSelectWindow
    In case of a single-port result only return the port information of this single port
    In case of a group-port result return the currently active ports belonging to this port

    Args:
        result (SerialSelectWindow.Result): result from the SerialSelectWindow

    Returns:
        list[UartDebuggerUtils.SerialPort]: ports to currently connect to
    """
    if not result.is_group:
        return [UartDebuggerUtils.SerialPort(result.portname, "", result.baudrate)]
    return UartDebuggerUtils.get_filtered_ports(result.baudrate, result.portname)


def main() -> None:
    """Main function
    """
    # Install coloredlogs for colored terminal output
    coloredlogs.install(fmt=config.coloredlogs_format, datefmt=config.coloredlogs_dateformat,
                        level=logging.INFO)

    # Open the SerialSelectWindow to get SerialPorts that we should connect to.
    window = SerialSelectWindow()
    result = window.open()

    # Close the program of SerialSelectWindow was canceled
    if not result.submitted:
        return

    event = threading.Event()
    ports_with_thread = []  # list of portnames, where currently a thread exists

    try:
        while not event.wait(config.delay):
            # Loop through every possible port
            for port in get_ports_by_result(result):
                if port.port in ports_with_thread:
                    continue

                # Open a thread for every possible port
                t = SerialThread(port, event)
                t.start()
                ports_with_thread.append(port.port)
    except KeyboardInterrupt:
        event.set()


if __name__ == "__main__":
    main()
