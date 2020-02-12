
'''
Code to make many 
squirrel tracks
'''


######################################

import argparse
import numpy as np
import pandas as pd
from math import pi
from glob import glob
from random import random


######################################


def readCommands():
  '''
  Read commandline arguments
  '''
  p = argparse.ArgumentParser(description=("Handle a set of points in geopandas"))
  p.add_argument("--inDir", dest ="inDir", type=str, default='/Users/dill/teaching/oosa/2019-20/OOSA-code-public/week5/batch_data', help=("Input filename"))
  p.add_argument("--repeats", dest ="nReps",type=int, default=30, help=("Number of repeat paths"))
  cmdargs = p.parse_args()
  return cmdargs


######################################

def writeData(data,namen):
  '''Write data to a csv file'''

  f=open(namen,'w')

  line="x,y,time\n"
  f.write(line)

  for i in range(0,data['x'].shape[0]):
    line=str(data['x'][i])+','+str(data['y'][i])+','+str(data['time'][i])+'\n'
    f.write(line)

  f.close()
  print("Written to",namen)
  return


######################################

def rotateData(data):
  '''Rotate coordinates somewhat'''

  # find bounds
  minX=np.min(data['x'])
  maxX=np.max(data['x'])
  minY=np.min(data['y'])
  maxY=np.max(data['y'])

  # set random shifts
  zen=random()*2.0*pi
  dx=(1.0-random())*(maxX-minX)*2.0
  dy=(1.0-random())*(maxY-minY)*2.0

  # rotate
  tX=data['x']-minX
  tY=data['y']-minY

  x=tX*np.cos(zen)-tY*np.sin(zen)
  y=tX*np.sin(zen)+tY*np.cos(zen)

  # translate
  data['x']=x+minX+dx
  data['y']=y+minY+dy


######################################

if __name__=='__main__':
  '''Main block'''

  # read command line
  cmd=readCommands()

  # list directory
  fileList=glob(cmd.inDir+'/*.csv')

  # loop over files
  for f in fileList:
    for i in range(0,cmd.nReps):
      # read data
      data=pd.read_csv(f)

      # rotate and translate
      rotateData(data)

      # write file
      namen=f.split('.')[-2]+"_"+str(i)+".csv"
      writeData(data,namen)

