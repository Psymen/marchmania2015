#!/usr/bin/env python

# Import standard library
from os import environ, sep
from os.path import exists, basename, splitext
from glob import glob

# Import common modules
from pandas import read_csv

class DataLoader(object):
    
    def __init__(self, dirName=None):

        # Can take directory name from input        
        if dirName is None:
            dirName = raw_input('Input location of data directory - ')

        # Correct common linux approach
        if '~' in dirName:
            dirName = dirName.replace('~', environ['HOME'])
            
        # Make sure ending is correct
        if not dirName.endswith(sep):
            dirName = dirName + sep

        # Confirm file exists and get list of data files
        if exists(dirName):
            dataFiles = glob(dirName + '*.csv')
        else:
            print dirName + " doesn't exist"
            return

        # Load each file into a pandas DataFrame
        for fName in dataFiles:
            
            temp = basename(fName)
            name = splitext(temp)[0]
            self.__dict__[name] = read_csv(fName)

