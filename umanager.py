#!/usr/bin/python

# Author: 		Gabriele Bozzola (sbozzolo)
# Email:		sbozzolator@gmail.com
# Date:			03.05.2016
# Last Edit:    19.03.2017 (andreatsh)

import userGUI
import os, sys

if ( __name__ == "__main__" ):
    
    tx,ty = userGUI.get_term_size()
    if (tx<28 or ty<96):
        print("\033[91m[ERROR]:\033[0m Your terminal is too small. Quit.")
        exit(1)

    # Enable debug mode:
    # Allows developers to run umanager as normal user for testing
    if (len(sys.argv)==2):
        if (sys.argv[1]=="-d" or sys.argv[1]=="-D"):
            gui = userGUI.GUI().run()
        else:
            print("\033[91m[ERROR]:\033[0m Invalid argument. Quit.")
    else:
        if (os.getuid()==0):
	        gui = userGUI.GUI().run()
        else:
            print("\033[91m[ERROR]:\033[0m You're not superuser. Quit.")

