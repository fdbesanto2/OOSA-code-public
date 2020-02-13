

'''
Manipulate a raster layer
'''

from readTiff import tiffHandle
from osgeo import gdal
import numpy as np
import osr


#################################

class rasterMaths(tiffHandle):
  '''
  Class with methods to perform raster maths
  '''

  #########################

  def convertResist(self,resistList=None):
    '''Convert land class to resistance. Can read LUT from a file'''

    # set resistance list
    if(resistList==None):
      self.resistLUT=self.defaultResist()
    else:
      print("No file reader yet")
      import sys
      sys.exit()

    # set values
    self.resist= np.where(self.data == 10, 0.25, \
    np.where(self.data == 20, 0.75, \
    np.where(self.data == 30, 20.0, \
    np.where(self.data == 0, -999.0, \
    np.where(self.data == 40, 2.0, 0)))))

    # overwrite
    self.data=self.resist


  ###########################

  def defaultResist(self):
    '''Set default resistance values'''
    LUT=[[0,10,20,30,40,-999],[-999.0,0.25,0.75,20.0,2.0,-999.0]]
    return(LUT)


############################################

if __name__=="__main__":
  '''Main block'''

  # set filename
  filename='/geos/netdata/avtrain/data/3d/oosa/week5/raster/roughClass.LT.tif'

  # read data to RAM
  tiff=rasterMaths(filename)

  # calculate resistance
  tiff.convertResist()

  # write geotiff
  tiff.writeTiff('resistance.LT.tif')

