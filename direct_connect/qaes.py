'''
See http://www.tylerlesmann.com/2008/dec/19/encrypting-database-data-django/
Written by Tyler Lesmann
'''
import string
from random import choice
from Crypto.Cipher import AES

EOD = '`%EofD%`' # This should be something that will not occur in strings

def genstring(length=16, chars=string.printable):
    return ''.join([choice(chars) for i in range(length)])

def encrypt(key, s):
    obj = AES.new(key)
    datalength = len(s) + len(EOD)
    if datalength < 16:
        saltlength = 16 - datalength
    else:
        saltlength = 16 - datalength % 16
    ss = ''.join([s, EOD, genstring(saltlength)])
    return obj.encrypt(ss)

def decrypt(key, s):
    obj = AES.new(key)
    ss = obj.decrypt(s)
    return ss.split(EOD)[0]
