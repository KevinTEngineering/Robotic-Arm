# ////////////////////////////////////////////////////////////////
# //                     IMPORT STATEMENTS                      //
# ////////////////////////////////////////////////////////////////

import math
import sys
import time

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from threading import Thread

from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.animation import Animation
from functools import partial
from kivy.config import Config
from kivy.core.window import Window
from pidev.kivy import DPEAButton
from pidev.kivy import PauseScreen
from time import sleep
import RPi.GPIO as GPIO 
from pidev.stepper import stepper
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus


# ////////////////////////////////////////////////////////////////
# //                      GLOBAL VARIABLES                      //
# //                         CONSTANTS                          //
# ////////////////////////////////////////////////////////////////
START = True
STOP = False
UP = False
DOWN = True
ON = True
OFF = False
YELLOW = .180, 0.188, 0.980, 1
BLUE = 0.917, 0.796, 0.380, 1
CLOCKWISE = 0
COUNTERCLOCKWISE = 1
ARM_SLEEP = 2.5
DEBOUNCE = 0.10

lowerTowerPosition = 60
upperTowerPosition = 76


# ////////////////////////////////////////////////////////////////
# //            DECLARE APP CLASS AND SCREENMANAGER             //
# //                     LOAD KIVY FILE                         //
# ////////////////////////////////////////////////////////////////
class MyApp(App):

    def build(self):
        self.title = "Robotic Arm"
        return sm

Builder.load_file('main.kv')
Window.clearcolor = (.1, .1,.1, 1) # (WHITE)

cyprus.open_spi()

# ////////////////////////////////////////////////////////////////
# //                    SLUSH/HARDWARE SETUP                    //
# ////////////////////////////////////////////////////////////////

sm = ScreenManager()
arm = stepper(port = 0, speed = 10)

# ////////////////////////////////////////////////////////////////
# //                       MAIN FUNCTIONS                       //
# //             SHOULD INTERACT DIRECTLY WITH HARDWARE         //
# ////////////////////////////////////////////////////////////////
	
class MainScreen(Screen):
    version = cyprus.read_firmware_version()
    armPosition = 0
    lastClick = time.clock()

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.initialize()

    def debounce(self):
        processInput = False
        currentTime = time.clock()
        if ((currentTime - self.lastClick) > DEBOUNCE):
            processInput = True
        self.lastClick = currentTime
        return processInput

    def toggleArm(self):
        if self.ids.armControl.text == "Lower Arm":
            cyprus.set_pwm_values(1, period_value=100000, compare_value=100000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
            self.ids.armControl.text = "Raise Arm"
        elif self.ids.armControl.text == "Raise Arm":
            cyprus.set_pwm_values(1, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
            self.ids.armControl.text = "Lower Arm"

    def roboticArm(self):
        Thread(target = self.toggleArm).start()


    def toggleMagnet(self):
        if self.ids.magnetControl.text == "Hold Ball":
            cyprus.set_servo_position(2,1)
            self.ids.magnetControl.text = "Release Ball"
        elif self.ids.magnetControl.text == "Release Ball":
            cyprus.set_servo_position(2, .5)
            self.ids.magnetControl.text = "Hold Ball"

    def magnet(self):
        Thread(target=self.toggleMagnet).start()

    # The dime blocks the sensor and allows free movement
    # Short s0.start_relative_moe(1.15)
    # Tall s0.start_relative_move(1.48)

    def auto(self):
        if cyprus.read_gpio() & 0b0001:
            cyprus.set_pwm_values(1, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
            sleep(0.20)
            self.s0.go_until_press(0, 5000)
            while self.s0.isBusy():
                sleep(0.2)
            self.s0.set_as_home()
            sleep(0.8)
            self.s0.start_relative_move(1.15)
            while self.s0.isBusy():
                sleep(0.2)
            cyprus.set_pwm_values(1, period_value=100000, compare_value=100000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
            cyprus.set_servo_position(2,1)
            sleep(2)
            cyprus.set_pwm_values(1, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
            sleep(2)
            self.s0.start_relative_move(0.33)
            while self.s0.isBusy():
                sleep(0.2)
            sleep(0.8)
            cyprus.set_pwm_values(1, period_value=100000, compare_value=100000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
            sleep(1.2)
            cyprus.set_servo_position(2, 0.5)
            sleep(0.7)
            cyprus.set_pwm_values(1, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
            sleep(2)
            self.s0.goHome()

        elif cyprus.read_gpio() & 0b0010:
            cyprus.set_pwm_values(1, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
            sleep(0.20)
            self.s0.go_until_press(0, 5000)
            while self.s0.isBusy():
                sleep(0.2)
            self.s0.set_as_home()
            sleep(0.8)
            self.s0.start_relative_move(1.48)
            while self.s0.isBusy():
                sleep(0.2)
            cyprus.set_pwm_values(1, period_value=100000, compare_value=100000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
            cyprus.set_servo_position(2,1)
            sleep(2)
            cyprus.set_pwm_values(1, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
            sleep(2)
            self.s0.start_relative_move(-0.33)

            while self.s0.isBusy():
                sleep(0.2)
            sleep(0.8)
            cyprus.set_pwm_values(1, period_value=100000, compare_value=100000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
            sleep(1.2)
            cyprus.set_servo_position(2, 0.5)
            sleep(0.9)
            cyprus.set_pwm_values(1, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
            sleep(2)
            self.s0.goHome()

    def setArmPosition(self, position):
        self.s0.start_go_to_position(position * .01)
        # self.s0.start_relative_move(position * .01)

    def setArm(self):
        Thread(target=self.setArmPosition).start()

    def homeArm(self):
        arm.home(self.homeDirection)
        
    def isBallOnTallTower(self):
        print("Determine if ball is on the top tower")

    def isBallOnShortTower(self):
        print("Determine if ball is on the bottom tower")
        
    def initialize(self):
        cyprus.initialize()
        cyprus.set_pwm_values(1, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL)

        self.s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
                     steps_per_unit=200, speed=1)
        self.s0.goTo(0)
        cyprus.setup_servo(2)
        self.s0.free_all()

        cyprus.set_servo_position(2, 0.5)



    def resetColors(self):
        self.ids.armControl.color = YELLOW
        self.ids.magnetControl.color = YELLOW
        self.ids.auto.color = BLUE

    def quit(self):
        MyApp().stop()
    
sm.add_widget(MainScreen(name = 'main'))


# ////////////////////////////////////////////////////////////////
# //                          RUN APP                           //
# ////////////////////////////////////////////////////////////////

MyApp().run()
cyprus.close_spi()
