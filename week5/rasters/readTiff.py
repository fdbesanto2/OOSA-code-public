

'''
Example script to read
a geotiff in to RAM
'''

############################################

from osgeo import gdal
import numpy as np
import argparse
import osr


############################################

def readCommands():
  '''
  Read commandline arguments
  '''
  p = argparse.ArgumentParser(description=("Handle a set of points in geopandas"))
  p.add_argument("--input", dest ="inName", type=str, default='/geos/netdata/avtrain/data/3d/oosa/week5/raster/roughClass.LT.tif', help=("Input filename"))
  p.add_argument("--output", dest ="outName", type=str, default='data.tif', help=("Output filename"))
  p.add_argument("--coarsen", dest ="coarsen", type=int, default=1, help=("Factor to coarsen resolution by"))
  cmdargs = p.parse_args()
  return cmdargs


############################################

class tiffHandle():
  '''
  Class to handle geotiff files
  '''

  #################################################

  def __init__(self,filename):
    '''Class initialiser. Reads filename'''
    # open a dataset object
    ds=gdal.Open(filename)

    # read all geolocation information
    proj=osr.SpatialReference(wkt=ds.GetProjection())
    self.epsg=int(proj.GetAttrValue('AUTHORITY',1))

    # read data dimensions from geotiff object
    self.nX=ds.RasterXSize             # number of pixels in x direction
    self.nY=ds.RasterYSize             # number of pixels in y direction

    # geolocation tiepoint
    transform_ds = ds.GetGeoTransform()# extract geolocation information
    self.xOrigin=transform_ds[0]       # coordinate of x corner
    self.yOrigin=transform_ds[3]       # coordinate of y corner
    self.pixelWidth=transform_ds[1]    # resolution in x direction
    self.pixelHeight=transform_ds[5]   # resolution in y direction

    # read data. Returns as a 2D numpy array
    self.data=ds.GetRasterBand(1).ReadAsArray(0,0,self.nX,self.nY)


  #################################################

  def coarsenRes(self,coarsen):
    '''Coarsen resolution'''

    # adjust resolution of header parameters
    self.nX=self.nX/coarsen
    self.nY=self.nY/coarsen
    self.pixelWidth=self.pixelWidth*coarsen
    self.pixelHeight=self.pixelHeight*coarsen

    # re-bin the data?

    # this is incomplete
    from sys import exit
    print("The coarsenRes() method is incomplete")
    exit()


  #################################################

  def writeTiff(self,filename):
    '''
    Write a geotiff from a raster layer
    '''

    # set geolocation information (note geotiffs count down from top edge in Y, so be cafeful about direction)
    geotransform = (self.xOrigin, self.pixelWidth, 0, self.yOrigin, 0, self.pixelHeight)

    # load data in to geotiff object
    dst_ds = gdal.GetDriverByName('GTiff').Create(filename, self.nX, self.nY, 1, gdal.GDT_Float32)

    dst_ds.SetGeoTransform(geotransform)    # specify coords
    srs = osr.SpatialReference()            # establish encoding
    srs.ImportFromEPSG(self.epsg)           # projection code
    dst_ds.SetProjection(srs.ExportToWkt()) # export coords to file
    dst_ds.GetRasterBand(1).WriteArray(self.data)  # write image to the raster
    dst_ds.GetRasterBand(1).SetNoDataValue(-999)  # set no data value
    dst_ds.FlushCache()                     # write to disk
    dst_ds = None

    print("Image written to",filename)
    return



############################################

if __name__=="__main__":
  '''Main block'''

  # read the command line
  cmd=readCommands()
  inName=cmd.inName
  outName=cmd.outName
  coarsen=cmd.coarsen

  # read the geotiff
  tiff=tiffHandle(inName)

  # coarsen the resolution
  #tiff.coarsenRes(coarsen)

  # write to a new geotiff
  tiff.writeTiff(outName)

