# class for driving self string over GPIO.PWM
__author__ = 'cygairko'


# noinspection PyMethodMayBeStatic
class Led:
    PORT_RED = 17  # GPIO port for red
    PORT_GREEN = 18  # GPIO port for green
    PORT_BLUE = 4  # GPIO port for blue
    FREQ = 100  # Frequency for PWM

    def __init__(self, mockup):
        self.mockup = mockup
        if not mockup:
            # import GPIO library
            # always needed with RPi.GPIO
            import RPi.GPIO as GPIO

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
        self._red = None
        self._green = None
        self._blue = None
        self._isOn = False

    # cleanup PWM and GPIO environment
    def __del__(self):
        print('cleaning up')
        if not self.mockup:
            self._red_pwm.stop()
            self._green_pwm.stop()
            self._blue_pwm.stop()
            # GPIO.cleanup()

    # method to start the pwm
    def start(self):
        if not self.mockup:
            self._red_pwm.start(0)
            self._green_pwm.start(0)
            self._blue_pwm.start(0)
        self.setColor(0, 0, 0)

    def setColor(self, red_in, green_in, blue_in):
        # update internal color values
        self._red = red_in
        self._green = green_in
        self._blue = blue_in
        if self._red == 0 and self._green == 0 and self._blue == 0:
            self._isOn = False
        self._changeColor(red_in, green_in, blue_in)

        return True

    def setOn(self, switch):
        self._isOn = switch
        # switch lights off (color = [0, 0, 0]), but keep actual color in mind
        if switch:
            self._changeColor(self._red, self._green, self._blue)
        elif not switch:
            self._changeColor(0, 0, 0)
        else:
            print('switch is not boolean')

    def isOn(self):
        return self._isOn

    def _changeColor(self, red_in, green_in, blue_in):
        if not self.mockup:
            # keep self values, just modify output values
            # change pwm duty cycles
            # calculate from 0..255 to 0..100%
            self._red_pwm.ChangeDutyCycle(red_in * 100.0 / 255.0)
            self._green_pwm.ChangeDutyCycle(green_in * 100.0 / 255.0)
            self._blue_pwm.ChangeDutyCycle(blue_in * 100.0 / 255.0)

    def printColor(self):
        print("r g b :", self._red, self._green, self._blue)

    def getColor(self):
        return [self._red, self._green, self._blue]