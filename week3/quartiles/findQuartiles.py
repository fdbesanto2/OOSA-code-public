

'''
Week 3 quartile task
'''

import numpy as np
from sys import exit


##########################################################

class dataSorter(object):
  '''
  Class to hold and manipulate data
  '''

  def __init__(self,filename):
    '''Initialise by reading data from a file'''
    self.wage,self.age=np.loadtxt(filename,delimiter=',',usecols=(0,1),unpack=True,dtype=float,comments="#")


  # need to sort it

  def sortData(self):
    '''An unfinished sort array'''
    print("This function unfinished. EXIT")
    exit()



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

  # binary search for values of interest?


