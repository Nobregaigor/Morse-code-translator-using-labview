import time
import config
#import morseClass
import json

def encodeMorseCode(string):
    letters = config.letters
    phrase = ''
    space = ','
    for c in string:
        morse = letters[c.upper()]
        phrase += morse + space
    return phrase


def decoderMorseCode(letters):
# Function translate LabVIEW
    morseCode = config.morseCode
    if string in morseCode:
        return morseCode[letters]
    else:
        return ''


def writeToFile(data):
    data[1] = int(data[1])
    d = str(data)
    f = open("dataFile.txt","a")
    f.write(d + "\n")
    f.close()

    return d

def rewriteFile():
    f = open("dataFile.txt","w")
    f.write("")
    f.close()

#convert the text file to python language
def readData(file): # Needs to be a string.
    f = open(file, 'r')
    processedData = []
    for line in f:
        s = processedData.append(eval(line))
    f.close()
    return processedData


def processData():

    data = readData('dataFile.txt')

    checkTimeError = [1000, 3000, 7000]
    string = ''
    Xi = None #freq
    Yi = None #time
    Xdash = False
    Xdot = False
    allowedError = 7
    stepChange = 30 #detects a change in freq
    rangeDash = [56.5, 60.5]
    rangeDot = [63, 67]

    # newFreq = Xi
    # OldFreq = Xi - 1

    timeTrigger = 0
    def absErrorY(Yi, timeTrigger):
        return abs(Yi - timeTrigger)

    def absErrorX(Xi, xTrigger):
        return abs(Xi - xTrigger)

    def trigger(bool):
        if (bool == True):
            return False
        else:
            return True

    n = range(len(data))
    bool = False
    for i in n:
        if i == 0:
            pass
        else:
            # Values to calculate errors
            Xim = data[i-1][0]
            Yim = data[i-1][1]
            Xi = data[i][0]
            Yi = data[i][1]
            #check if there is a frequency change
            if absErrorX(Xi, Xim) <= stepChange:
                #check if there is a frequency change that falls under Dash or Dot
                if (Xi >= rangeDash[0]) and (Xi <= rangeDash[1]) and (absErrorX(Xi, Xim) < allowedError):   #0,50,50,51,50,51
                    Xdash = True
                    Xdot = False
                elif (Xi >= rangeDot[0]) and (Xi <= rangeDot[1]) and (absErrorX(Xi, Xim) < allowedError):
                    Xdash = False
                    Xdot = True
                else:
                    Xdash = False
                    Xdot = False

            elif absErrorX(Xi, Xim) > stepChange:
                timeTrigger = Yi
                bool = trigger(bool)
                print('\n' + 'trigger active at line = ' + str(i+1) + ', bool = ' + str(bool) + '; timeTrigger = ' + str(timeTrigger) + '\n')

            yerr = absErrorY(Yi, timeTrigger)

            print('line= ' + str(i + 1) + '; xi = ' + str(Xi) + '; yi = ' + str(Yi) + '; yerr = ' + str(yerr))

            #check if it is a signal
            if ((Xdash == True) or (Xdot == True)) and (bool == True):
                # yerr = absErrorY(Yi, timeTrigger)
                # print('line= ' + str(i + 1) + '; yi = ' + str(Yi) + '; timeTrigger = ' + str(timeTrigger) + '; yerr = ' + str(yerr))

                # if (yerr <= checkTimeError[0]+100) and (yerr >= checkTimeError[0]-100):
                if ((yerr <= checkTimeError[0]+100) and (yerr >= checkTimeError[0]-100)) and (Xdot == True):
                    string = string + "."
                    print('----> Adding a dot to morse code message, found in line = ' + str(i+1) + '\n')
                    timeTrigger = 0
                elif ((yerr <= checkTimeError[1]+100) and (yerr >= checkTimeError[1]-100)) and (Xdash == True):
                    print('----> Adding a dash to morse code message, found in line = ' + str(i+1) + '\n')
                    string = string + "_"
                    timeTrigger = 0

          #if it is not a signal, check only for time
            else:
                # yerr = absErrorY(Yi, timeTrigger) #difference between the nowTime and the last time there was a difference
                if (yerr <= checkTimeError[0]+100) and (yerr >= checkTimeError[0]-100):
              #space bewteen parts of the same letter
                    print("***** Space within characters in a word, at line = " + str(i+1))
                    pass
                elif (yerr <= checkTimeError[1]+100) and (yerr >= checkTimeError[1]-100):
              #space bewteen letters
                    print("***** Space between characters within a word, at line = " + str(i+1))
                    pass
                elif (yerr <= checkTimeError[2]+100) and (yerr >= checkTimeError[2]-100):
              #space bewteen words
                    print("***** Space between a word, at line = " + str(i+1))
                    string = string + " "
                # else:
                #     string = string + " "*2

    print("\nMorse code message: %s" % string)
    return string

s = processData()
