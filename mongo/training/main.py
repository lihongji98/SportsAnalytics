import sys
from mongo_python import *

if(__name__== "__main__"):
    if(len(sys.argv) < 2):
        print("Wrong number of parameters, usage: (1,2,3,4,5,6,7)")
        exit()
    number = int()
    eval("exercise_"+sys.argv[1]+'()')