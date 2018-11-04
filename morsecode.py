import time
import config

def encodeMorseCode(string):
    letters = config.letters
    phrase = ''
    space = ','
    for c in string:
        morse = letters[c.upper()]
        phrase += morse + space
    print(phrase)


def decoderMorseCode(letters):
# Function translate LabVIEW
    morseCode = config.morseCode
    if string in morseCode:
        return morseCode[letters]
    else:
        return ''


encodeMorseCode('SOS S')
