import RPi.GPIO as GPIO
import time
import config
import morsecode


def runMotor(dCycle): # Function that vibrates the motor.
    motor = GPIO.PWM(21,600)
    motor.start(0)
    motor.ChangeDutyCycle(dCycle)
    time.sleep(float(config.dt))
    motor.stop()


def main(): # Function that sets motor and pin, and vibrates to a phrase.
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21,GPIO.OUT)
    p = morsecode.encodeMorseCode("SOS")
    print(p)
    vibrateMorseCode(p)
    GPIO.cleanup()


def vibrateMorseCode(phrase): # Function vibrates motors to a given phrase.
    for c in phrase: # c is every character in a phrase.
        if c == '.':
            runMotor(100)
            print(".")
            time.sleep(config.dt)
        elif c == '_':
            runMotor(70)
            print("_")
            time.sleep(config.dt*2)
        elif c == ',':
            time.sleep(config.dt*2)
        elif c == '%':
            time.sleep(config.dt*6)
        else:
            pass


main()
