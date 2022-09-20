""""simple random code generator with special chars numbers and letters"""


import random
from random import randrange

letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
special = ['@','&','#','$','~','!','%','_']

def random_string(letters):
    string=""
    strlen = len(letters)
    random = randrange(0,strlen)
    string = letters[random]
    return string

def random_char(special):
    char = ""
    charlen = len(special)
    random = randrange(0,charlen)
    char = special[random]
    return char


def random_int():
    num = randrange(0,255)
    return str(num)


def refcode():
    new=[]
    for x in range(0,3):
        new.append(random_string(letters))
        new.append(random_int())
        #new.append(random_char(special))

    refcode=  "".join(new)
    return str(refcode)

if __name__ == '__main__':

    print('new code is',refcode())
