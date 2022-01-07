#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================================
# tlights - Traffic Light Control Demo
# Copyright (C) 2021 by Ralf Kilian
#
# tlights is licensed under the GPLv3:
#
#     tlights is free software: you can redistribute it and/or modify it
#     under the terms of the GNU General Public License as published by the
#     Free Software Foundation, either version 3 of the License, or (at your
#     option) any later version.
#
#     tlights is distributed in the hope that it will be useful, but WITHOUT
#     ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#     FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
#     more details.
#
#     You should have received a copy of the GNU General Public License along
#     with tlights. If not, see <http://www.gnu.org/licenses/>.
#
# GitHub: https://github.com/urbanware-org/tlights
# GitLab: https://gitlab.com/urbanware-org/tlights
# ============================================================================

__version__ = "1.1.2"

import os
import sys
from PyQt4 import QtCore, QtGui, uic

interface = os.path.join("ui", "crossing.ui")
qtCreatorFile = interface
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

images = os.path.join("images")
crossing_day = os.path.join(images, "crossing_day.png")
crossing_night = os.path.join(images, "crossing_night.png")
sign_yield = os.path.join(images, "sign_yield.png")


class TrafficLight(object):
    """
        Traffic light control class.
    """
    default_seconds_red = 3
    default_seconds_green = 3

    tl_red = os.path.join(images, "trafficlight_red.png")
    tl_redyellow = os.path.join(images, "trafficlight_redyellow.png")
    tl_yellow = os.path.join(images, "trafficlight_yellow.png")
    tl_green = os.path.join(images, "trafficlight_green.png")
    tl_off = os.path.join(images, "trafficlight_off.png")

    def __init__(self, tl_object, is_red=True, is_yield=False,
                 seconds_red=default_seconds_red,
                 seconds_green=default_seconds_green):
        self.tl_object = tl_object
        self.set_off()

        self.standby_signal = 1

        self.is_red = is_red
        self.is_yield = is_yield

        self.seconds_red = seconds_red
        self.seconds_green = seconds_green

        self.loop_red = seconds_red
        self.loop_green = seconds_green

    def set_red(self):
        """
            Method to only set the red light.
        """
        set_pixmap(self.tl_object, self.tl_red)

    def set_redyellow(self):
        """
            Method to only set the red and yellow light.
        """
        set_pixmap(self.tl_object, self.tl_redyellow)

    def set_yellow(self):
        """
            Method to only set the yellow light.
        """
        set_pixmap(self.tl_object, self.tl_yellow)

    def set_green(self):
        """
            Method to only set the green light.
        """
        set_pixmap(self.tl_object, self.tl_green)

    def set_off(self):
        """
            Method to disable all lights.
        """
        set_pixmap(self.tl_object, self.tl_off)

    def switch(self):
        """
            Method to switch the traffic light status by one step.
        """
        if self.is_red:
            if self.loop_red > 0:
                self.set_red()
                self.loop_red -= 1
            else:
                self.set_redyellow()
                self.is_red = False
                self.loop_green = self.seconds_green
        else:
            if self.loop_green > 1:
                self.set_green()
                self.loop_green -= 1
            elif self.loop_green == 1:
                self.set_yellow()
                self.loop_green = 0
            else:
                self.set_red()
                self.is_red = True
                self.loop_red = self.seconds_red

    def standby(self):
        """
            Method to set standby mode. If the traffic light is at a yield
            position, it will flash with its yellow light, otherwise it will
            be completely switched off.
        """
        if self.is_yield:
            if self.standby_signal == 1:
                self.set_off()
                self.standby_signal = 0
            else:
                self.set_yellow()
                self.standby_signal = 1
        else:
            self.set_off()

    def autoswitch(self, standby_on):
        """
            Method to automatically switch the traffic light status step by
            step, setting the traffic lights on standby at night.
        """
        if standby_on:
            self.standby()
        else:
            self.switch()


class TrafficLightsDemo(QtGui.QMainWindow, Ui_MainWindow):
    """
        Class for the traffic light control demo.
    """

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.is_day = True
        self.standby = False

        self.__set_environment()
        self.btn_power.clicked.connect(self.switch_power)
        self.btn_daylight.clicked.connect(self.switch_daytime)

    def __set_environment(self):
        """
            Start-up method to set the environment.
        """
        self.tn = TrafficLight(self.tl_north, False, True, 3, 3)  # is_yield
        self.ts = TrafficLight(self.tl_south, False, True, 3, 3)  # is_yield
        self.tw = TrafficLight(self.tl_west, True, False, 3, 3)
        self.te = TrafficLight(self.tl_east, True, False, 3, 3)

        set_pixmap(self.yd_north, sign_yield)
        set_pixmap(self.yd_south, sign_yield)

        self.__set_time_day()
        self.__set_power_on()

    def __set_power_on(self):
        """
            Switch on traffic lights.
        """
        self.btn_power.setText("Standby")
        self.standby = False

    def __set_power_standby(self):
        """
            Switch traffic lights to standby.
        """
        self.btn_power.setText("Power on")
        self.standby = True

    def __set_time_day(self):
        """
            Switch to day.
        """
        self.btn_daylight.setText("Set night")
        self.is_day = True
        set_pixmap(self.bg_crossing, crossing_day)

    def __set_time_night(self):
        """
            Switch to night.
        """
        self.btn_daylight.setText("Set day")
        self.is_day = False
        set_pixmap(self.bg_crossing, crossing_night)

    def main_loop(self):
        """
            Main loop connected with the timer.
        """
        self.tn.autoswitch(self.standby)
        self.ts.autoswitch(self.standby)
        self.tw.autoswitch(self.standby)
        self.te.autoswitch(self.standby)

    def switch_daytime(self):
        """
            Switch between day and night.
        """
        if self.is_day:
            self.__set_time_night()
        else:
            self.__set_time_day()

    def switch_power(self):
        """
            Switch traffic lights on or to standby.
        """
        if self.standby:
            self.__set_power_on()
        else:
            self.__set_power_standby()


def set_pixmap(obj, pixmap):
    """
        Method to simply set a pixmap for a QLabel object.
    """
    p = QtGui.QPixmap(pixmap)
    obj.setPixmap(p)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app_icon = QtGui.QIcon()
    app_icon.addFile(
        os.path.join(images, "trafficlight_green.png"), QtCore.QSize(48, 48))
    app.setWindowIcon(app_icon)

    tldemo = TrafficLightsDemo()
    tldemo.show()

    timer = QtCore.QTimer()
    timer.timeout.connect(tldemo.main_loop)
    timer.start(1000)

    sys.exit(app.exec_())

# EOF
