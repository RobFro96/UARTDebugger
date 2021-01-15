#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import threading
import time
import serial
import datetime
import platform
import re
import logging
import coloredlogs

coloredlogs.install(fmt='%(asctime)s,%(msecs)03d %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

"""
UART DEBUGGER
Author: Robert Fromm
Date: 08.01.2020

Checking the presents of serial ports. Printing the received data.
"""

ASCII_FILTER = True
FORMAT = "\033[1m\033[90m[%(port)s]\033[0m %(msg)s"


class SerialThread(threading.Thread):
    def __init__(self, port: str, args, event: threading.Event):
        threading.Thread.__init__(self)
        self.port = port
        self.args = args
        self.event = event

    def run(self):
        is_connected = False
        while not self.event.wait(self.args.delay):
            try:
                connection = serial.Serial(self.port, self.args.baud, timeout=self.args.delay)
                self.print_line("\033[90mconnected  ")
                while not self.event.wait(1e-3):
                    buf = connection.readline()
                    if buf:
                        if ASCII_FILTER:
                            buf = bytearray([c for c in buf if c < 128])

                        is_connected = True
                        self.print_line(buf.decode("ansi"))
            except serial.SerialException:
                if is_connected:
                    self.print_line("\033[90mdisconnected  ")
                is_connected = False

    def print_line(self, msg):
        msg = msg[:-2]
        time_str = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        port = self.port.upper() if platform.system() == "Windows" else self.port

        msg = FORMAT % {"msg": msg, "time_str": time_str, "port": port}
        if self.args.nocolors:
            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            msg = ansi_escape.sub("", msg)
        logging.info(msg)


def main():
    parser = argparse.ArgumentParser(
        description="UART DEBUGGER\nPrinting the received data of serial ports.")
    parser.add_argument("ports", action="store", type=str,
                        nargs="+", help="Serial ports to listen.")
    parser.add_argument("-b", "--baud", type=int, action="store", default=9600,
                        help="baud rate of serial ports.")
    parser.add_argument("-d", "--delay", type=float, action="store", default=.5,
                        help="Polling delay")
    parser.add_argument("-c", "--nocolors", action="store_true",
                        help="Disable the all colors and styles")

    args = parser.parse_args()
    event = threading.Event()

    for port in args.ports:
        thread = SerialThread(port, args, event)
        thread.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            event.set()
            break


if __name__ == "__main__":
    main()
