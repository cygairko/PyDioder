# class for driving self string over GPIO.PWM
__author__ = 'cygairko'
# import GPIO library
# always needed with RPi.GPIO
import RPi.GPIO as GPIO

#noinspection PyMethodMayBeStatic
class Led:
    PORT_RED = 17    # GPIO port for red
    PORT_GREEN = 18    # GPIO port for green
    PORT_BLUE = 4    # GPIO port for blue
    FREQ = 100   # Frequency for PWM

    def __init__(self):
        GPIO.setwarnings(False)

        # choose BCM or BOARD numbering schemes. I use BCM
        GPIO.setmode(GPIO.BCM)

        # set color ports as outputs
        GPIO.setup(self.PORT_RED, GPIO.OUT)
        GPIO.setup(self.PORT_GREEN, GPIO.OUT)
        GPIO.setup(self.PORT_BLUE, GPIO.OUT)

        # create objects for PWM on color output ports
        self._red_pwm = GPIO.PWM(self.PORT_RED, self.FREQ)
        self._green_pwm = GPIO.PWM(self.PORT_GREEN, self.FREQ)
        self._blue_pwm = GPIO.PWM(self.PORT_BLUE, self.FREQ)

        # colors
        self.red = None
        self.green = None
        self.blue = None

    # cleanup PWM and GPIO environment
    def __del__(self):
        self._red_pwm.stop()
        self._green_pwm.stop()
        self._blue_pwm.stop()
        GPIO.cleanup()

    # method to start the pwm
    def start(self):
        self._red_pwm.start(0)
        self._green_pwm.start(0)
        self._blue_pwm.start(0)
        Led.setcolor(self, 0, 0, 0)

    def setcolor(self, red_in, green_in, blue_in):
        # update internal color values
        self.red = red_in
        self.green = green_in
        self.blue = blue_in

        # change pwm duty cycle
        # calculate from 0..255 to 0..100%
        self._red_pwm.ChangeDutyCycle(self.red * 100.0 / 255.0)
        self._green_pwm.ChangeDutyCycle(self.green * 100.0 / 255.0)
        self._blue_pwm.ChangeDutyCycle(self.blue * 100.0 / 255.0)

        return True

    def printcolor(self):
        print("r g b :", self.red, self.green, self.blue)

    def getcolor(self):
        return [self.red, self.green, self.blue]


