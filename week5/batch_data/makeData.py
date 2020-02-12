
'''
Code to make many 
squirrel tracks
'''


######################################

import argparse


######################################


def readCommands():
  '''
  Read commandline arguments
  '''
  p = argparse.ArgumentParser(description=("Handle a set of points in geopandas"))
  p.add_argument("--input", dest ="inName", type=str, default='../data/squirrel.csv', help=("Input filename"))
  p.add_argument("--repeats", dest ="nRep",,type=int, default=10, help=("Number of repeat paths"))
  cmdargs = p.parse_args()
  return cmdargs


######################################



