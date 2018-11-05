import matplotlib.pyplot as plt

data = [[0,0.5],[0,1],[1,1.5],[1,2],[0,2.5],[0,3],[0,3.5],[0,4],[0,4.5],[0,5],[1,5.5],[1,6],[1,6.5],[1,7],[1,7.5],[1,8],[0,8.5],[0,9],[0,9.5]]


def processData(data):

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


    def checkValue(val):
        if (val > 0): # positive change -> dot or dash
            if (val == 1):
                return "."
            elif (val == 3):
                return "_"
            else:
                pass
        else:
            if (val == -1) or (val == -3):
                return ""
            elif (val == -7):
                return " "
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

                plt.plot(sq['x'],sq['y'])
                plt.show()

                print(' ')

                #new square start from here
                sq['x'][0] = xa
                sq['y'][0] = ya

            else: #not a step change, keep the square but change last dimensions
                sq['x'][1] = xb
                sq['y'][1] = yb


print(string)
