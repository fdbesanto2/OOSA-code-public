

'''
Week 3 quartile task
'''

import numpy as np
from sys import exit
from binarySearches import *


##########################################################

class dataSorter(object):
  '''
  Class to hold and manipulate data
  '''

  def __init__(self,filename):
    '''Initialise by reading data from a file'''
    self.wage,self.age=np.loadtxt(filename,delimiter=',',usecols=(0,1),unpack=True,dtype=float,comments="#")
    self.doneSort=False   # a flag to say if we have sorted yet or not


  def sortData(self):
    '''An unfinished sort array'''
    self.sortedWage=np.sort(self.wage)
    self.doneSort=True


  def findQuartile(self,thisW):
    '''Find a quartile of percentage q'''

    # if not already sorted, then sort
    if(self.doneSort==False):
      self.sortData()

    # binary search
    w,thisQ=binarySearch(self.sortedWage,thisW)  # loop
    #w,thisQ=binaryRecurse(self.sortedWage,thisW,0,self.sortedWage.shape[0])  # recursion

    return((thisQ/self.sortedWage.shape[0])*100)


##########################################################

if __name__=="__main__":
  '''The main block'''

  # read data in to object
  filename="../data/wages.csv"
  dataObj=dataSorter(filename)

  # print to show it is working
  print("Data read from",filename)
  print("Mean wage is",np.mean(dataObj.wage))

  # sort it
  dataObj.sortData()

  # find quartiles
  qList=[25,50,75]
  for q in qList:
    thisW=dataObj.sortedWage[int((q/100)*dataObj.sortedWage.shape[0])]
    print(q,"quartile is",thisW)

  # now find what quartile a particular wage occurs in
  thisW=27000
  thisQ=dataObj.findQuartile(thisW)
  print(thisW,"is in the",thisQ,"quartile")

