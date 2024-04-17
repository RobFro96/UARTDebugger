import dataclasses
import tkinter

from config import config
from uart_debugger_utils import UartDebuggerUtils

"""
UART DEBUGGER
Author: Robert Fromm
Date: 17.04.2024

Checking the presents of serial ports. Printing the received data.
Window based on Tkinter to select a serial port or regex
"""


class SerialSelectWindow:
    """Window created with Tkinter to select serial port.
    """
    @classmethod
    def enable_dpi_awareness(cls) -> None:
        """Enable tkinter DPI Awarness for better GUI scaling on windows
        """
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

    @dataclasses.dataclass
    class Result:
        """Result after closing the window
        """
        submitted: bool
        is_group: bool = False
        portname: str = None
        baudrate: int = 9600

    def __init__(self) -> None:
        """Constructor.
        """
        self.result = self.Result(False)
        self.__create_window()
        self.__refresh_ports()

    def __create_window(self) -> None:
        """Create the Window
        """
        # DPI awareness
        if config.dpi_aware:
            self.enable_dpi_awareness()

        # Windows Title and Icon
        self.window = tkinter.Tk()
        self.window.title("UART Debugger - Select Serial Port")
        # self.window.iconbitmap("icon.ico")

        # Regex Label and Listbox
        tkinter.Label(self.window, text="Group of Serial Ports",
                      anchor="w").pack(side="top", fill="x", pady=5)
        self.list_box_groups = tkinter.Listbox(self.window, height=1, selectmode="single")
        self.list_box_groups.pack(side="top", fill="both", expand=True, pady=5)

        # Baud rate selection
        baud_frame = tkinter.Frame(self.window)
        baud_frame.pack(side="top", fill="x", pady=5)
        self.baud_rate_selection = tkinter.IntVar(value=-1)

        for baudrate in config.radio_box_baudrates:
            tkinter.Radiobutton(
                baud_frame, text=str(baudrate),
                variable=self.baud_rate_selection, value=baudrate).pack(
                side="left", padx=5)

        tkinter.Radiobutton(
            baud_frame, text="custom:", variable=self.baud_rate_selection, value=-1).pack(
            side="left", padx=5)

        self.baud_rate_selection.set(config.default_baudrate_selection)

        self.custom_baud_rate = tkinter.StringVar(value="19200")
        tkinter.Entry(
            baud_frame, textvariable=self.custom_baud_rate, width=7).pack(side="left", padx=5)

        # Port Label and Listbox
        tkinter.Label(self.window, text="Single Serial Port",
                      anchor="w").pack(side="top", fill="x", pady=5)
        self.list_box = tkinter.Listbox(self.window, height=1, selectmode="single")
        self.list_box.pack(side="top", fill="both", expand=True, pady=5)

        # Buttons at the bottom
        control_frame = tkinter.Frame(self.window)
        control_frame.pack(side="bottom", fill="x", pady=5)

        tkinter.Button(control_frame, text="Refresh",
                       command=self.__refresh_ports).pack(side="left", padx=5)
        tkinter.Button(control_frame, text="Cancel",
                       command=self.__on_cancel).pack(side="left", padx=5)

        self.list_box.bind('<Double-Button>', self.__on_submit_single_port)
        self.list_box_groups.bind('<Double-Button>', self.__on_submit_group)

        # Window size
        if config.dpi_aware:
            self.window.minsize(450, 500)
        else:
            self.window.minsize(300, 400)

        self.window.geometry("+300+500")

    def __refresh_ports(self) -> None:
        """Refreshs the ports list and updates the GUI
        """
        self.list_box_groups.delete(0, "end")
        for template in config.templates:
            display = "%s: %d" % (template["display_name"], template["baudrate"])
            self.list_box_groups.insert("end", display)

        self.ports = UartDebuggerUtils.get_filtered_ports()
        self.list_box.delete(0, "end")
        for port in self.ports:
            display = "%s: %s" % (port.port, port.description)
            self.list_box.insert("end", display)

    def open(self) -> Result:
        """Opens window and returns result if closed or serial port selected.

        Returns:
            Result: result
        """
        tkinter.mainloop()
        return self.result

    def __on_submit_group(self, *_) -> None:
        """If a group item is double clicked -> submit window
        """
        if len(self.list_box_groups.curselection()) == 0:
            return

        template = config.templates[self.list_box_groups.curselection()[0]]
        self.result = self.Result(True, True, template["regex"], template["baudrate"])
        self.window.destroy()

    def __on_submit_single_port(self, *_) -> None:
        """On submitted pressed or double click on serial port -> submit window
        """
        if len(self.list_box.curselection()) == 0:
            self.__refresh_ports()
            return

        portname = self.ports[self.list_box.curselection()[0]].port
        baudrate = self.baud_rate_selection.get()
        if baudrate == -1:
            try:
                baudrate = int(self.custom_baud_rate.get())
            except ValueError:
                baudrate = config.default_baudrate_selection
        self.result = self.Result(True, False, portname, baudrate)
        self.window.destroy()

    def __on_cancel(self) -> None:
        """On cancel button pressed
        """
        self.result = self.Result(False)
        self.window.destroy()


if __name__ == "__main__":
    win = SerialSelectWindow()
    print(win.open())
