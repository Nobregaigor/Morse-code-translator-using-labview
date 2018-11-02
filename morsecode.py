import RPi.GPIO as GPIO

def encodeMorseCode(string):

    letters = {
         'A':   '._',
         'B':   '_...',
         'C':   '_._.',
         'D':   '_..',
         'E':   '.',
         'F':   '.._.',
         'G':	'__.',
         'H':	'...',
         'I':	'..',
         'J':	'.___',
         'K':	'_._',
         'L':	'._..',
         'M':	'__',
         'N':	'_.',
         'O':	'___',
         'P':	'.__.',
         'Q':	'__._',
         'R':	'._.',
         'S':	'...',
         'T':	'_',
         'U':	'.._',
         'V':	'..._',
         'W':	'.__',
         'X':	'_.._',
         'Y':	'_.__',
         'Z':	'__..',
         '1':	'.____',
         '2':	'..___',
         '3':	'...__',
         '4':	'...._',
         '5':	'.....',
         '6':	'_....',
         '7':	'__...',
         '8':	'___..',
         '9':	'____.',
         '0':	'_____'
     }


    phrase = []
    for c in string:
        morse = letters[c.upper()]
        print(morse)
        phrase.append(morse)
        print(phrase)



def decoderMorseCode(string):
# Function translate LabVIEW

    letters = {
        '._':   'A',
        '_...': 'B',
        '_._.': 'C',
        '_..':  'D',
        '.':    'E',
        '.._.': 'F',
        '__.':  'G',
        '...':  'H',
        '..':   'I',
        '.___': 'J',
        '_._':  'K',
        '._..': 'L',
        '__':   'M',
        '_.':   'N',
        '___':  'O',
        '.__.': 'P',
        '__._': 'Q',
        '._.':  'R',
        '...':  'S',
        '_':    'T',
        '.._':  'U',
        '..._': 'V',
        '.__':  'W',
        '_.._': 'X',
        '_.__': 'Y',
        '__..': 'Z',
        '.____':'1',
        '..___':'2',
        '...__':'3',
        '...._':'4',
        '.....':'5',
        '_....':'6',
        '__...':'7',
        '___..':'8',
        '____.':'9',
        '_____':'0'
    }

    if string in letters:
        return letters[string]
    else:
        return ''

def morseToMotor():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22,GPIO.OUT)
    v1 = GPIO.PWM(22,500)
