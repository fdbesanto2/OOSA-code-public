


'''
Intersect a vector with a raster
and add up resistance
'''

# add to our path
from sys import path
#path.append('/home/shancoc2/src/OOSA-code-public/week5/rasters')
path.append('/Users/dill/teaching/oosa/2019-20/OOSA-code-public/week5/rasters')
from resistSquirrel import rasterMaths
import argparse
import pandas as pd
import numpy as np
from pyproj import Proj, transform
from math import sqrt


#######################

class vectorSquirrel():

  def __init__(self,filename,epsg=27700):
    '''Initialiser'''
    # read the file in to pandas dataframe
    df=pd.read_csv(filename)

    # sort by the time column
    self.sortedData=df.sort_values('time').reset_index(drop=True)

    # reproject x and y
    inProj=Proj(init="epsg:4326")
    outProj=Proj(init="epsg:"+str(epsg))
    # reproject data
    self.x,self.y=transform(inProj, outProj, np.array(df.x), np.array(df.y))
    self.time=np.array(df.time)


  def interpolateLine(self,xRes,yRes):
    '''Function to interpolate lines through a raster'''

    # create empty lists
    x=[]
    y=[]
    t=[]

    # loop over recorded points
    for i in range(0,self.x.shape[0]-1):
      # determine distance between two points
      dx=self.x[i+1]-self.x[i]
      dy=self.y[i+1]-self.y[i]
      dt=self.time[i+1]-self.time[i]
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
      c=self.y[i]-m*self.x[i]

      # how many pixels does this cross in x and y?
      nXint=int(abs(dx)/xRes)
      nYint=int(abs(dy)/yRes)
      if(nXint<0):  # do at least one point per segment
        nXint=1
      if(nYint<0):
        nYint=1

      # x pixel crossings
      thisX=np.arange(0,dx,dirX*xRes)+self.x[i]
      thisY=m*thisX+c
      thisT=self.time[i]+dt*(thisX-self.x[i])/dx
      x.extend(thisX)
      y.extend(thisY)
      t.extend(thisT)

      # y pixel crossings
      thisY=np.arange(0,dy,dirY*yRes)+self.y[i]
      thisX=(thisY-c)/m
      thisT=self.time[i]+dt*(thisY-self.y[i])/dy
      x.extend(thisX)
      y.extend(thisY)
      t.extend(thisT)

    # copy over interpolated arrays
    self.x=np.array(x)
    self.y=np.array(y)
    self.time=np.array(t)


  def pathResist(self,tiff):
    '''Calculate the resistance for a squirrel's path'''

    # interpolate the line to get all pixels between nodes
    self.interpolateLine(tiff.pixelWidth,abs(tiff.pixelHeight))

    # determine indices
    xInd=np.array((self.x-tiff.xOrigin)//tiff.pixelWidth,dtype=int)
    yInd=np.array((self.y-tiff.yOrigin)//tiff.pixelHeight,dtype=int)
    useInd=np.where((xInd>=0)&(xInd<tiff.nX)&(yInd>=0)&(yInd<tiff.nY))

    # add up track, if any is contained
    if(len(useInd)>0):
      useInd=useInd[0]
      #tempArr=np.ndarray.flatten(tiff.resist[xInd[useInd]][yInd[useInd]])
      #tempArr[tempArr<0]=0.0
      self.trackResist=np.sum(tiff.resist[xInd[useInd]][yInd[useInd]])/len(xInd)



#######################

if __name__=="__main__":
  '''Main block'''

  # set input names
  #tiffName='/geos/netdata/avtrain/data/3d/oosa/week5/raster/roughClass.LT.tif'
  #trackName='/home/shancoc2/src/OOSA-code-public/week5/data/squirrel.csv'
  tiffName='/Users/dill/data/bess/maps/roughClass.LT.tif'
  trackName='/Users/dill/teaching/oosa/2019-20/OOSA-code-public/week5/data/squirrel.csv'

  # read the tiff
  tiff=rasterMaths(tiffName)

  # calculate resistance raster layer
  tiff.convertResist()

  # read the track and reproject
  track=vectorSquirrel(trackName,epsg=tiff.epsg)

  # calculate resistance of the path
  track.pathResist(tiff)

  # write out
  print("Resistance is",track.trackResist)

