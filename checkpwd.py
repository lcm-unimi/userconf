#!/usr/bin/python
#
# Author: andreatsh - andreatsh@lcm.mi.infn.it
#

from re import search as search   
import getpass

def pwdpolicy():
    print("")
    print("Your password must have at least 8 characters including:")
    print("\t- one uppercase letter")
    print("\t- one lowercase letter")
    print("\t- one digit or one special character (better if it contains both!)")
    print("")
    print("Warning: \n\tThe first and and the last character do not count!")
    print("")


def ispwdweak(string):

    if (len(string)<8): 
        return True

    pwd = string[1:-1]
    if (search(r'[a-z]', pwd) and search(r'[A-Z]', pwd) and 
        search(r'[0-9]', pwd) and search(r'[^A-Za-z0-9_]', pwd) ): 
        return False
    else: 
        return True

