


'''
Intersect a vector with a raster
and add up resistance
'''

# add to our path
from sys import path
path.append('/home/shancoc2/src/OOSA-code-public/week5/rasters')
from resistSquirrel import rasterMaths
import argparse
import pandas as pd
import numpy as np
from pyproj import Proj, transform


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


#######################

if __name__=="__main__":
  '''Main block'''

  # set input names
  tiffName='/geos/netdata/avtrain/data/3d/oosa/week5/raster/roughClass.LT.tif'
  trackName='/home/shancoc2/src/OOSA-code-public/week5/data/squirrel.csv'

  # read the tiff
  tiff=rasterMaths(tiffName)

  # calculate resistance raster layer
  tiff.convertResist()

  # read the track and reproject
  track=vectorSquirrel(trackName,epsg=tiff.epsg)

  # load two up

