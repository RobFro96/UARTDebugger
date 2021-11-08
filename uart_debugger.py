#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import datetime
import logging
import platform
import re
import threading
import time

import coloredlogs
import serial
import serial.tools.list_ports

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


def has_thread(port, threads):
    for t in threads:
        if t.port == port:
            return True
    return False


def main():
    parser = argparse.ArgumentParser(
        description="UART DEBUGGER\nPrinting the received data of serial ports.")
    parser.add_argument("regex", action="store", type=str, help="Regex to match port's name")
    parser.add_argument("-b", "--baud", type=int, action="store", default=9600,
                        help="baud rate of serial ports.")
    parser.add_argument("-d", "--delay", type=float, action="store", default=.5,
                        help="Polling delay")
    parser.add_argument("-c", "--nocolors", action="store_true",
                        help="Disable the all colors and styles")

    args = parser.parse_args()
    event = threading.Event()

    threads = []

    try:
        while True:
            for port, descr, _ in serial.tools.list_ports.comports():
                if re.match(args.regex, descr) and not has_thread(port, threads):
                    t = SerialThread(port, args, event)
                    t.start()
                    threads.append(t)
            if event.wait(.1):
                break
    except KeyboardInterrupt:
        event.set()


if __name__ == "__main__":
    main()
