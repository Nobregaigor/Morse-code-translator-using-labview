import time
import config
#import morseClass
import json
import matplotlib.pyplot as plt

def encodeMorseCode(string):
    letters = config.letters
    phrase = ''
    space = ','
    for c in string:
        morse = letters[c.upper()]
        phrase += morse + space
    return phrase


def decoderMorseCode(key):
# Function translate LabVIEW
    morseCode = config.morseCode
    if key in morseCode:
        return morseCode[key]
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
    allowedError = 8
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
                    # print(i)
                    Xdash = True
                elif (Xi >= rangeDot[0]) and (Xi <= rangeDot[1]) and (absErrorX(Xi, Xim) < allowedError):
                    Xdot = True
                else:
                    Xdash = False
                    Xdot = False

            elif absErrorX(Xi, Xim) > stepChange:
                timeTrigger = Yi
                bool = trigger(bool)
                print('\n' + 'trigger active at line = ' + str(i+1) + ', bool = ' + str(bool) + '; timeTrigger = ' + str(timeTrigger) + '\n')

            yerr = absErrorY(Yi, timeTrigger)

            print('line= ' + str(i + 1) + '; yi = ' + str(Yi) + '; yerr = ' + str(yerr))

            #check if it is a signal
            if ((Xdash == True) or (Xdot == True)) and (bool == True):
                # yerr = absErrorY(Yi, timeTrigger)
                # print('line= ' + str(i + 1) + '; yi = ' + str(Yi) + '; timeTrigger = ' + str(timeTrigger) + '; yerr = ' + str(yerr))

                # if (yerr <= checkTimeError[0]+100) and (yerr >= checkTimeError[0]-100):
                if (yerr <= checkTimeError[0]+100) and (yerr >= checkTimeError[0]):
                    string = string + "."
                    print('----> adding a dot, found in line = ' + str(i+1) + '\n')
                elif (yerr <= checkTimeError[1]+100) and (yerr >= checkTimeError[1]):
                    print('----> adding a dash, found in line = ' + str(i+1) + '\n')
                    string = string + "_"

          #if it is not a signal, check only for time
            else:
                # yerr = absErrorY(Yi, timeTrigger) #difference between the nowTime and the last time there was a difference
                if (yerr <= checkTimeError[0]+100) and (yerr >= checkTimeError[0]-100):
              #space bewteen parts of the same letter
                    print("***  Within same character in a word, at line = " + str(i+1))
                    pass
                elif (yerr <= checkTimeError[1]+100) and (yerr >= checkTimeError[1]-100):
              #space bewteen letters
                    print("***  Between a character within a word, at line = " + str(i+1))
                    pass
                elif (yerr <= checkTimeError[2]+100) and (yerr >= checkTimeError[2]-100):
              #space bewteen words
                    print("***  Space between a word, at line = " + str(i+1))
                    string = string + " "
                # else:
                #     string = string + " "*2

    return string

# s = processData()
# print(s)

def processData2(data):

    def normalizeData(data):
        n = range(len(data))
        for i in n:
            if (data[i][0] > 10): #high pass filter if necessary
                data[i][0] = 1
            else:
                data[i][0] = 0
        return data

    def formatData(data):
        n = range(len(data))
        datax = []
        datay = []
        for i in n:
            datax.append(data[i][1])
            datay.append(data[i][0])
        data = {"x": datax, "y": datay}
        return data

    uncertainty = 260
    dotArea = 1000
    dashArea = 2000 # this should be adjusted for 3000
    withinCharacter = -1000
    betweenCharacter = -3600 #this should be adjusted for -3000 at the end
    btweenWords = -7000

    def checkValue(val):
        if (val > 0): # positive change -> dot or dash
            if (dotArea - uncertainty) <= val <= (dotArea + uncertainty):
                return "."
            elif (dashArea - uncertainty) <= val <= (dashArea + uncertainty):
                return "_"
            else:
                pass
        else:
            if ((withinCharacter - uncertainty) <= val <= (withinCharacter + uncertainty)):
                pass
            elif ((betweenCharacter - uncertainty) <= val <= (betweenCharacter + uncertainty)):
                return " "
            elif (btweenWords - uncertainty) <= val <= (btweenWords + uncertainty):
                return "  "
            else:
                pass

    data = normalizeData(data)
    data = formatData(data)

    n = range(len(data['x']))
    stepChange = 1

    sq = {'x': [None,None], 'y': [None,None]}
    string = ''
    area = 0

    #set up initial square:
    sq['x'][0] = data['x'][0]
    sq['y'][0] = data['y'][0]

    sq['x'][1] = data['x'][1]
    sq['y'][1] = data['y'][1]



    for i in n:
        if (i== 0) or (i==1):
            pass
        else:
            xa = data['x'][i-2]
            xb = data['x'][i-1]
            xi = data['x'][i]

            ya = data['y'][i-2]
            yb = data['y'][i-1]
            yi = data['y'][i]

            #check if xi belongs to the square or it is a step change
            if (abs(yi - yb) > 0 ): #stepChange -> break the square
                print("yi = " + str(yi) + "; yb = " + str(yb) + " step chaneg at i = " + str(i))
                area = (sq['x'][1] - sq['x'][0]) * (sq['y'][1] - sq['y'][0])
                print("dx = " + str(sq['x'][1] - sq['x'][0]))
                print("dy = " + str(sq['y'][1] - sq['y'][0]))
                print('area = ' + str(area))

                #check equivalent value
                val = checkValue(area)
                print("therefore, adding a " + str(val))
                try:
                    string = string + val
                except:
                    pass

                # plt.plot(sq['x'],sq['y'])
                # plt.show()

                print(' ')

                #new square start from here
                sq['x'][0] = xb
                sq['y'][0] = yb

            else: #not a step change, keep the square but change last dimensions
                sq['x'][1] = xb
                sq['y'][1] = yb

    plt.plot(data['x'],data['y'])
    plt.show()
    return string


def decodeRawMorseCode(string):
    words = string.split('  ')

    n = range(len(words))
    phrase = ''
    for i in n:
        char = words[i].split()
        n2 = range(len(char))

        word = ''
        for j in n2:
            newChar = decoderMorseCode(char[j])
            word = word + newChar
        phrase = phrase + word + ' '

    return phrase

pData = processData2(readData("dataFile.txt"))
result = decodeRawMorseCode(pData)

print("__________________________________________________________________\n")
print("processed Data result: " + pData)
print("therefore, the translated result is: " + result)
print("__________________________________________________________________\n\n")
