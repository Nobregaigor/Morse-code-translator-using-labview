import RPi.GPIO as GPIO
import time
import config
import morsecode


def runMotor(dCycle,dt): # Function that vibrates the motor.
    motor = GPIO.PWM(21,600)
    motor.start(0)
    motor.ChangeDutyCycle(dCycle)
    time.sleep(float(dt))
    motor.stop()


def main(): # Function that sets motor and pin, and vibrates to a phrase.
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21,GPIO.OUT)
    print("Hello!")
    message = input("What message you want to morsify?")
    p = morsecode.encodeMorseCode(str(message))
    print("Thank you. This is your message in morse code: '" + str(p) + "'\n")
    for i in range(3):
        print("Initializing transmission in: " + str(i) + " s")
        time.sleep(1)

    print("Tranfmission:")
    vibrateMorseCode(p)
    print("End of transmission.")
    print("Have a good day!")
    GPIO.cleanup()


def vibrateMorseCode(phrase): # Function vibrates motors to a given phrase.
    for c in phrase: # c is every character in a phrase.
        if c == '.': # runMotor for 1 unit, stop for 1 unit
            runMotor(100,config.dt)
            print(".")
            time.sleep(config.dt*1.7)
        elif c == '_': # run motor for 3 units, stop for 1 unit
            runMotor(100,config.dt*3)
            print("_")
            time.sleep(config.dt*1.7)
        elif c == ',': # stop motor for 2 units (+1 unit from the dot or dash)
            time.sleep(config.dt*2.5)
        elif c == '%': # stop motor for 6 units (+1 unit from the dot or dash)
            time.sleep(config.dt*1.1)
        else:
            pass


main()
