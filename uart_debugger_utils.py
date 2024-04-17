import dataclasses
import re

import serial
import serial.tools.list_ports

from config import config

"""
UART DEBUGGER
Author: Robert Fromm
Date: 17.04.2024

Checking the presents of serial ports. Printing the received data.
Helper functions to get and filter serial ports present on the PC
"""


class UartDebuggerUtils:
    @dataclasses.dataclass
    class SerialPort:
        """Port information of a serial port: portname, description, baudrate
        """
        port: str
        description: str
        baudrate: int = 9600

    @classmethod
    def get_all_ports(cls, baudrate: int = 9600) -> list[SerialPort]:
        """Get the serial ports connected to the PC

        Args:
            baudrate (int, optional): Baudrate to fill all information of SerialPort dataclass.
              Defaults to 9600.

        Returns:
            list[SerialPort]: list of all available ports
        """
        port_list = sorted(serial.tools.list_ports.comports())

        return [cls.SerialPort(port[0], port[1], baudrate) for port in port_list]

    @classmethod
    def get_filtered_ports(
            cls, baudrate: int = 9600, whitelist_regex: str = None) -> list[SerialPort]:
        """Get all serial ports filtered by an additional whitelist_regex and blacklists defined in
        the config.py

        Args:
            baudrate (int, optional):  Baudrate to fill all information of SerialPort dataclass. Defaults to 9600.
            whitelist_regex (str, optional): Optional whitelist regex string. Defaults to None.

        Returns:
            list[SerialPort]: list of all filtered ports
        """
        ports = cls.get_all_ports(baudrate)
        filtered_ports = []

        for port in ports:
            # Blacklist by portname
            if port.port in config.blacklist_by_port:
                continue

            # Blacklist by port description
            if cls.__is_port_blacklisted(port.description):
                continue

            # Optional whitelist
            if whitelist_regex:
                if not re.match(whitelist_regex, port.description):
                    continue

            filtered_ports.append(port)

        return filtered_ports

    @classmethod
    def __is_port_blacklisted(cls, description: str) -> bool:
        """Helper function to loop through all blacklists present in the config.py

        Args:
            description (str): port's description

        Returns:
            bool: True, if description is blacklisted
        """
        for blacklist in config.blacklist_by_descr:
            if re.match(blacklist, description):
                return True
        return False
