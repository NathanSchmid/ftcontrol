#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import sys
import ftrobopy  # Import the ftrobopy module
from TouchStyle import *
import ftcontrol
import asyncio
import logging


class FtcGuiApplication(TouchApplication):
    def __init__(self, args):
        TouchApplication.__init__(self, args)

        # create the empty main window
        w = TouchWindow("ftcontrol")

        txt_ip = os.environ.get('TXT_IP')  # try to read TXT_IP environment variable
        if txt_ip is None: txt_ip = "localhost"  # use localhost otherwise
        try:
            self.txt = ftrobopy.ftrobopy(txt_ip, 65000)  # try to connect to IO server
        except:
            self.txt = None

        vbox = QVBoxLayout()

        if not self.txt:
            # display error of TXT could no be connected
            # error messages is centered and may span
            # over several lines
            err_msg = QLabel("Error connecting IO server")  # create the error message label
            err_msg.setWordWrap(True)  # allow it to wrap over several lines
            err_msg.setAlignment(Qt.AlignCenter)  # center it horizontally
            vbox.addWidget(err_msg)  # attach it to the main output area
        else:
            # initialization went fine. So the main gui
            # is being drawn
            self.test_button = QPushButton("Test")
            self.test_button.clicked.connect(self.on_test_button_clicked)  # connect button to event handler
            # self.grab_button.setEnabled(False)
            vbox.addWidget(self.test_button)  # attach it to the main output area

            # configure all TXT outputs to normal mode
            output_config = [self.txt.C_OUTPUT, self.txt.C_OUTPUT, self.txt.C_OUTPUT, self.txt.C_OUTPUT]
            input_config = [(self.txt.C_SWITCH, self.txt.C_DIGITAL),
                            (self.txt.C_SWITCH, self.txt.C_DIGITAL),
                            (self.txt.C_SWITCH, self.txt.C_DIGITAL),
                            (self.txt.C_SWITCH, self.txt.C_DIGITAL),
                            (self.txt.C_SWITCH, self.txt.C_DIGITAL),
                            (self.txt.C_SWITCH, self.txt.C_DIGITAL),
                            (self.txt.C_SWITCH, self.txt.C_DIGITAL),
                            (self.txt.C_SWITCH, self.txt.C_DIGITAL)]
            self.txt.setConfig(output_config, input_config)
            self.txt.updateConfig()

            self.motor_x = ftcontrol.PositionableMotor("x", self.txt.motor(1), self.txt.input(1))
            self.motor_y = ftcontrol.PositionableMotor("y", self.txt.motor(2), self.txt.input(2))
            self.motor_z = ftcontrol.PositionableMotor("z", self.txt.motor(3), self.txt.input(3))
            self.motor_w = ftcontrol.PositionableMotor("w", self.txt.motor(4), self.txt.input(4))

        w.centralWidget.setLayout(vbox)
        w.show()
        self.exec_()

    def on_test_button_clicked(self):
        asyncio.run(self.init())

    async def init(self):
        dim = ftcontrol.MultiPositionable((self.motor_x, self.motor_y, self.motor_z, self.motor_w))
        await dim.initialize((300, 512, 512, 300))
        await dim.goto((800, 70, 1800, 0))
        await dim.goto((800, 70, 2000, 0))
        await dim.goto((800, 70, 2000, 12))
        await dim.goto((200, 20, 500, 12))
        await dim.goto((200, 20, 500, 0))
        logging.debug("Position is " + str(dim.position))


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    FtcGuiApplication(sys.argv)

