import time
import config
import matplotlib.pyplot as plt

#translate string to morse code
def encodeMorseCode(string):
    letters = config.letters
    phrase = ''
    space = ','
    for c in string:
        morse = letters[c.upper()]
        phrase += morse + space
    return phrase

#translate morse code to letters
def decoderMorseCode(key):
    morseCode = config.morseCode
    if key in morseCode:
        return morseCode[key]
    else:
        return ''

#write data adquired to dataFile
def writeToFile(data):
    data[1] = int(data[1])
    d = str(data)
    f = open(config.dataFile,"a")
    f.write(d + "\n")
    f.close()
    return d

#overwrite dataFile to empty file
def rewriteFile():
    f = open(config.dataFile,"w")
    f.write("")
    f.close()

#convert dataFile string data to array data
def readData(file): # Needs to be a string.
    f = open(file, 'r')
    processedData = []
    for line in f:
        s = processedData.append(eval(line))
    f.close()
    return processedData

#converts processed data to morse code string to be decoded
def processData(data):

    threshold = 50

    def normalizeData(data):
        n = range(len(data))
        for i in n:
            if (data[i][0] > threshold): #high pass filter if necessary
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

    uncertainty = config.dt*600
    dotArea = config.dt*1000
    dashArea = config.dt*3000
    withinCharacter = config.dt*(-1000) #should be -1000, but because of motor dynamics its less
    betweenCharacter = config.dt*(-3000)
    betweenWords = config.dt*(-7000)

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
            elif ((betweenCharacter - uncertainty*1.5) <= val <= (betweenCharacter + uncertainty)):
                return " "
            elif (betweenWords - uncertainty*1.5) <= val <= (betweenWords + uncertainty*1.5):
                return "  "
            else:
                print("min range = " + str(betweenWords - uncertainty*3))
                print("max range = " + str(betweenWords + uncertainty*3))
                print("***NOT IN RANGE***")
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

    # plt.plot(data['x'],data['y'])
    # plt.show()  # This will run alongside myDAQ, make sure to comment out for code to run fast
    return string

#decodes morse code string to regular string
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



def pdLabview():
    val = decodeRawMorseCode(processData(readData(config.dataFile)))
    return val

# =============================================================================

# print(readData(config.dataFile))
# print(processData(readData(config.dataFile)))


# pData = processData(readData(config.dataFile))
# result = decodeRawMorseCode(pData)
#
# print("__________________________________________________________________\n")
# print("processed Data result: " + pData)
# print("therefore, the translated result is: " + result)
# print("__________________________________________________________________\n\n")
