#!/usr/bin/python
#
# Author: andreatsh - andreatsh@lcm.mi.infn.it
#
#
# [Password requirements]
#
# A good password should contain at least 8 characters including:
#   - one uppercase letter
#   - one lowercase letter
#   - one digit or one special character (better if it contains both!)
#
# Warning: 
#   The first and the last character do not count!
#
# You can also check if your password is based on strings such as user name, 
# last name and/or user login.
#

import re 
import getpass

def ispwdweak(pstring, s1=None, s2=None, s3=None):

    if (len(pstring)<8): 
        return True, 0

    pwd = pstring

    if (re.search("\s", pwd)):
        return True, 1

    if (s1!=None):
        regex=re.sub("[aeiou]", ".", s1, flags=re.I) 
        if (re.search(regex, pwd, flags=re.IGNORECASE)):
            return True, 2
    if (s2!=None):
        regex=re.sub("[aeiou]", ".", s2, flags=re.I) 
        if (re.search(regex, pwd, flags=re.IGNORECASE)):
            return True, 2
    if (s3!=None):
        regex=re.sub("[aeiou]", ".", s3, flags=re.I) 
        if (re.search(regex, pwd, flags=re.IGNORECASE)):
            return True, 2

    pwd = pstring[1:-1]

    if (re.search("[a-z]", pwd) and re.search("[A-Z]", pwd) and 
        (re.search("[0-9]", pwd) or re.search("[^A-Za-z0-9_]", pwd))): 
        return False, 7
    else: 
        return True, 3

