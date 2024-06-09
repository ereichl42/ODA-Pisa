# I want to understand how python works. So here I just print the path of the current file, and path of current working directory.
#

import os

print("")
print("This is the mostInner.py file.")
print("Path of the current file: ", os.path.abspath(__file__))
print("Current working directory: ", os.getcwd())
# Where is therefore this file executed from?
print("Executed from: ", os.path.abspath("."))
print("")
