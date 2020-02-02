
'''
Some example functions for processing LVIS data
'''

#######################################

import numpy as np
from lvisClass import lvisData
from pyproj import Proj, transform


#######################################

class proLVIS(lvisData):
  '''
  LVIS class with extra processing steps
  '''

  def __init__(self,filename,setElev=False,minX=-100000000,maxX=100000000,minY=-1000000000,maxY=100000000,onlyBounds=False):
    '''
    For now, calls the inherited initialiser using the "super" option
    class lvisData:
    '''
    super().__init__(filename,setElev=setElev,minX=minX,maxX=maxX,minY=minY,maxY=maxY,onlyBounds=onlyBounds):


  #######################################################

  def meanNoises(self,noiseBins):
    '''
    Calculates mean noise per waveform.
    noiseBins gives the number of bins 
    known to be filled with noise
    '''
    meanNoise=np.zeros((self.nWaves))
    for i in range(0,self.nWaves):          # loop over all waveforms
      z,wave=proLVIS.getOneWave(self,i)     # read waveform
      meanNoise[i]=np.mean(wave[0:noiseBins])  # add mean from slice
    return(meanNoise)

  #######################################################

  def estimateGround(self,sigThresh=3.5,statsLen=10):
    '''
    Processes waveforms to estimate ground
    Only works for bare Earth. DO NOT USE IN TREES
    '''
    # determine number of empty bins
    res=(self.z[0,0]-self.z[0,-1])/self.nBins
    noiseBins=int(statsLen/res)
    # 


  #######################################################

  def reproject(self,inEPSG,outEPSG):
    '''
    Reproject footprint coordinates
    '''
    # set projections
    inProj=Proj(init="epsg:"+str(inEPSG))
    outProj=Proj(init="epsg:"+str(outEPSG))
    # reproject data
    x,y=transform(inProj,outProj,self.lon,self.lat)
    self.lon=x
    self.lat=y
    return

#############################################################

