# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 19:31:50 2015

@author: Jan
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May 18 13:34:38 2015

@author: Jan
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
   

import IPython
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from numpy import *
import sys

#import "homemade" modules:
sys.path.insert(0, "C:\Users\Jan\Documents\Python Scripts\1 head data\Organised Program")
import dataimport
import Minimal
import Iteration
import Evolution
import plotiteration
    
T=True
F=False
    

# 
'''
rename(df, add_str)
rename adds a string to the name of all columns in a pandas dataframe 

input:
    df
        type:DataFrame
    
    add_str
        type: string
        
output:
    df
        type: DataFrame

'''  
def rename(df,add_str):
    col=df.columns.tolist()
    for i in range(len(col)):
      df=df.rename(columns={col[i]:(col[i]+add_str)})
    return df


'''
---DateToIndex(datestr, df)--
input:
    datestr
        type: string
        Information: Year-Month-Day Hour:Minute f.e.: '2015-04-24 12:15'
    df
        type: dataframe
        
output:
    ind
        type: int
        Information:
        Number of row in dataframe with the date written in datestr.
        
'''    
def DateToIndex(datestr, df):
    ind=int(np.where(df.index==datetime.strptime(datestr,'%Y-%m-%d %H:%M'))[0])
    return ind
    

            


'''
#############################
#######Adjustments###########
#############################
'''


'''
filename
Path to the file of the Towerdata. Make sure to always use two 
slashes instead of one: \\
Example: 
    filename='C:\\Users\\Jan\\Documents\\Python Scripts\\1 head data\\Organised Program\\fg_11995_ent-perm_LoggerNet_pressure.dat'
    In case the file is in the same folder as the python scripts you 
    could just use the filename and leave away the path.
    Example: filename= 'fg_11995_ent-perm_LoggerNet_pressure.dat'
'''

filename='C:\\Users\\Jan\\Documents\\Python Scripts\\1 head data\\Organised Program\\fg_11995_ent-perm_LoggerNet_pressure.dat'

'''
Choose Method to do flux calculation with:

MIN  for Minimal Value Method
ITR  for Iterational Method
EVO  for Evolutionary Algorithm

'''
method='MIN'

'''
savename defines the name of the plots and the result file
'''

savename='Run1'

'''
konv_time defines date and time for which the konv_arr and therefore the iteration plots are made.
The iteration plots show the calculation process for the selected date
'''
konv_time='2015-04-24 12:15'

'''
period
        type: List
        length: 2
        Information:
            period chooses the data for which the flux calculation is done
            , where period[0] is the first and period[1] is the last datapoint
            The dates have to be within the range of the towerfile
            
            In case the whole period should be chosen call period:
            period=['','']
                
            You could also choose start or endpoint only this way:
            period=['2015-04-19',''] or period=['','2015-04-19']
'''

period= ['2015-04-19','2015-04-30']





#---------Constants --------------
#density=p/(Rs*T) from ideal gas equation
Rs=287.058
K=0.4 #van kharmann canstant
g=9.8 # m/s^2  earth acceleration
Cp=1005 #1.005 J/(kg*K) spesific warmthkapacity air
height1=2.0
height2=7.6
z=(height1+height2)/2
alpha0=1

constants=[Rs,K,g,Cp,height1,height2,z,alpha0]






tow_data=dataimport.ImportData(filename,period)

tow_data=dataimport.CalculatedParameters(tow_data,constants)

tow_data=dataimport.resampling(tow_data)




#konv_ind gives number of row (index) in k for which the konv_arr are made
konv_ind= DateToIndex(konv_time,tow_data)

if method=='ITR':

    results,konv_arr=Iteration.CalculateFluxesIteration(tow_data,konv_ind,constants)

elif method=='MIN':

    results,konv_arr=Minimal.CalculateFluxesMinimal(tow_data,konv_ind,constants)

elif method=='EVO':
    
    results,konv_arr=Evolution.CalculateFluxesEvolution(tow_data,konv_ind,constants)
else :
    print "Please type in either 'ITR', 'MIN' 'EVO'"


plotiteration.plotiteration(savename,konv_arr,konv_time)




results=rename(results,'_'+method) 

results.to_csv(savename+'_'+method+'_results'+'.csv')

tow_data.to_csv(savename+'_TowData'+'.csv')

