""""simple random code generator with special chars numbers and letters"""


import random
from random import randrange

letters = ['A','a','B','b','C','c','D','d','E','e','F','f','G','g','H','h','I','i','J','j','K','k','L','l','M','n','O','o','P','p','Q','q','R','r','S','s','T','t','U','u','V','v','W','w','X','x','Y','y','z','Z']
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
        new.append(random_char(special))

    refcode=  "".join(new)
    return str(refcode)

if __name__ == '__main__':

    print('new code is',refcode())
