

'''
A function to interpolate
points along a line
'''



######################################

from pyproj import Proj, transform
import pandas as pd
import numpy as np
import argparse
from math import sqrt


############################################

def readCommands():
  '''
  Read commandline arguments
  '''
  p = argparse.ArgumentParser(description=("Handle a set of points in geopandas"))
  p.add_argument("--input", dest ="inName", type=str, default='../data/squirrel.csv', help=("Input filename"))
  p.add_argument("--res", dest ="res", type=float, default=1.5, help=("Raster resolution"))
  p.add_argument("--bounds", dest ="bounds",nargs=4,type=float, default=[509774,218993,511927,220676], help=("Raster bounds"))
  cmdargs = p.parse_args()
  return cmdargs


######################################

class pseudoRaster():
  '''To hold the key elements of a raster'''

  def __init__(self,res,bounds):
    '''Initialiser'''
    self.res=res
    self.minX=bounds[0]
    self.minY=bounds[1]
    self.maxX=bounds[2]
    self.maxY=bounds[3]


######################################

def interpolateLine(points,rast):
  '''Function to interpolate lines through a raster'''

  # create empty lists
  x=[]
  y=[]
  t=[]

  # loop over recorded points
  for i in range(0,points['x'].shape[0]-1):
    # determine distance between two points
    dx=points.x[i+1]-points.x[i]
    dy=points.y[i+1]-points.y[i]
    dt=points.time[i+1]-points.time[i]
    dist=sqrt(dx**2+dy**2)

    # determine direction, to help us increment
    if(dx<0):
      dirX=-1
    else:
      dirX=1
    if(dy<0):
      dirY=-1
    else:
      dirY=1

    # line equation parameters
    m=dy/dx
    c=points.y[i]-m*points.x[i]

    # how many pixels does this cross in x and y?
    nXint=int(abs(dx)/rast.res)
    nYint=int(abs(dy)/rast.res)
    if(nXint<0):  # do at least one point per segment
      nXint=1
    if(nYint<0):
      nYint=1


    # x pixel crossings
    thisX=np.arange(0,dx,dirX*rast.res)+points.x[i]
    thisY=m*thisX+c
    thisT=points.time[i]+dt*(thisX-points.x[i])/dx
    x.extend(thisX)
    y.extend(thisY)
    t.extend(thisT)

    # y pixel crossings
    thisY=np.arange(0,dy,dirY*rast.res)+points.y[i]
    thisX=(thisY-c)/m
    thisT=points.time[i]+dt*(thisY-points.y[i])/dy
    x.extend(thisX)
    y.extend(thisY)
    t.extend(thisT)

  # copy lists in to a new pandas array
  interpData=pd.DataFrame({'x':x,'y':y,'time':t})

  # sort it again, as x and y crossings will be out of order
  interpData=interpData.sort_values('time').reset_index(drop=True)

  return(interpData)



######################################

if __name__=="__main__":
  '''Main block'''

  # read the command line
  cmd=readCommands()

  # save key raster details to a class to make passing easier
  rast=pseudoRaster(cmd.res,cmd.bounds)

  # relative path to filename from OOSA-code-public folder
  filename=cmd.inName

  # read data in to RAM
  data=pd.read_csv(filename)

  # sort by the time column
  sortedData=data.sort_values('time').reset_index(drop=True)

  # reproject to OSNG in metres, to help intersect with the raster
  inProj=Proj(init="epsg:4326")
  outProj=Proj(init="epsg:27700")
  x,y=transform(inProj, outProj, np.array(sortedData.x), np.array(sortedData.y))
  sortedData['x']=x
  sortedData['y']=y

  # interpolate points along raster
  interpData=interpolateLine(sortedData,rast)

  # write out results for checking
  interpData.to_csv('interpolated.csv',columns=['x','y','time'])
  print("Written to interpolated.csv")
  sortedData.to_csv('sorted.csv')
  print("Written to sorted.csv")

