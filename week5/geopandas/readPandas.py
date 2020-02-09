
'''
An example of reading a file
in to geopandas and doing
simple analysis
'''


######################################

import pandas as pd


######################################

if __name__=="__main__":
  '''Main block'''
  # relative path to filename from OOSA-code-public folder
  filename='../data/squirrel.csv'

  # read data in to RAM
  data=pd.read_csv(filename)

  # sort by the time column
  sortedData=data.sort_values('time')
