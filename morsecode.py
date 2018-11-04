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

    data = readData("dataFile.txt")

    checkTimeError = [1000, 3000, 7000]
    string = ''
    Xi = None #freq
    Yi = None #time
    Xdash = False
    Xdot = False
    allowedError = 50
    rangeDash = [56.5, 60.5]
    rangeDot = [63, 67]

    # newFreq = Xi
    # OldFreq = Xi - 1

    timeTrigger = 0
    def absErrorY(Yi, timeTrigger):
        return abs(Yi - timeTrigger)

    def absErrorX(Xi, xTrigger):
        return abs(Xi - xTrigger)

    n = range(len(data))
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
            if absErrorX(Xi, Xim) <= allowedError:
                #check if there is a frequency change that falls under Dash or Dot
                if (Xi >= rangeDash[0]) and (Xi <= rangeDash[1]):   #0,50,50,51,50,51
                    # print(i)
                    Xdash = True
                elif (Xi >= rangeDot[0]) and (Xi <= rangeDot[1]):
                    Xdot = True
                else:
                    Xdash = False
                    Xdot = False

            elif absErrorX(Xi, Xim) > allowedError: #Trigger timer 2
                timeTrigger = Yi

            #check if it is a signal
            if (Xdash == True) or (Xdot == True):
                yerr = absErrorY(Yi, timeTrigger)
                print('line= ' + str(i + 1) + '; yi = ' + str(Yi) + '; timeTrigger = ' + str(timeTrigger) + '; yerr = ' + str(yerr))

                # if (yerr <= checkTimeError[0]+100) and (yerr >= checkTimeError[0]-100):
                if (yerr <= checkTimeError[0]+100) and (yerr >= checkTimeError[0]):
                    string = string + "."
                    print(i)
                elif (yerr <= checkTimeError[1]+100) and (yerr >= checkTimeError[1]-100):
                    string = string + "_"

          #if it is not a signal, check only for time
            else:
                yerr = absErrorY(Yi, timeTrigger) #difference between the nowTime and the last time there was a difference
                if (yerr <= checkTimeError[0]+100) and (yerr >= checkTimeError[0]-100):
              #space bewteen parts of the same letter
                    pass
                elif (yerr <= checkTimeError[1]+100) and (yerr >= checkTimeError[1]-100):
              #space bewteen letters
                    pass
                elif (yerr <= checkTimeError[2]+100) and (yerr >= checkTimeError[2]-100):
              #space bewteen words
                    string = string + " "
                # else:
                #     string = string + " "*2

    return string

# s = processData()
# print(s)
