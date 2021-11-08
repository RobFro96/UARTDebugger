# UARTDebugger

## Introduction
When programming my microcontrollers I typically use the COM ports to output debug information. Programming wireless mircocontrollers I typical unplug boards after programming. PuTTY makes it hard to watch serial communication because the window closes after disconnect.

This program can watch multiple COM ports at a time. On disconnect, the program is not closed. It tries to reconnect to the device when present. The colored output is used for better visualization.

## Installation
- Install a version of Python 3: <https://www.python.org/>
- Make sure that Python is registered in the Windows PATH variable.
- Install dependencies: `pip install -r requirements.txt`
- Preferred Terminal:
  - Windows CMD: use *uart_debugger.bat*
  - Git Bash: use *uart_debugger.sh*

## Configuraion
- Edit the Batch or Bash file.
- Optional arguments:
  - `--baud 9999`: baud rate of serial ports. Default: 9600
  - `--delay 0.999`: polling delay on disconnect. Default: 0.5 [sec]
  - `--nocolors`: disable the all colors and styles
- Followed by a regex to match the COM port descriptions
- Example: `python uart_debugger.py --baud 115200 --nocolors ^MSP Application UART`
- Optional: Add a link to your Programs List