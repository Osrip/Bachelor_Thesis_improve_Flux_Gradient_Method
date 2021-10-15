# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 15:28:57 2015

@author: Jan
"""
import IPython
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import *



'''
---ImportData (filename,period)---

Input:
    filename
        type: String
        Information: 
            Path to the file of the Towerdata. Make sure to always use two 
            slashes instead of one: \\
            Example: 
            filename='C:\\Users\\Jan\\Documents\\Python Scripts\\1 head data\\Organised Program\\fg_11995_ent-perm_LoggerNet_pressure.dat'
            In case the file is in the same folder as the python scripts you 
            could just use the filename and leave away the path.
            Example: filename= 'fg_11995_ent-perm_LoggerNet_pressure.dat'
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
        
Output:
    k
        type: pandas DataFrame
        Information:
            columns: ['WS1_speed',
                      'WS2_speed',
                      'AirTC_1_Avg',
                      'AirTC_2_Avg',
                      'AirPressure',
                      'SunElevation'] Column names of Dataframe can be printed using: name_of_DataFrame.columns.tolist()


'''
def ImportData(filename,period):
    

        
    
    def rename(df,add_str):
        col=df.columns.tolist()
        for i in range(len(col)):
          df=df.rename(columns={col[i]:(col[i]+add_str)})
        return df
        
        
    #########################
    ######Import Data########
    #########################
    
    
    # header=1 defines value for header but unnescessary if skiprow is used
    k=pd.read_csv(filename,na_values=['NAN',7999,-7999,'INF','+INF','-INF'],header=0,index_col=0,parse_dates=True)
    

    

    
    
    
    ################################
    #####rearrange data#############
    ################################
    
    
    
    #All parameters, which are used for the calculations are picked out of the EdiRe data.
    

    
    
    

    '''
    ##--------k_full--------------
    k_full includes all tower data of the imported file and can therefore be used to 
    find with certain environmental conditions and pick out dates to be analysed
    It is however not used for any calculations in this program, so forget about it
    '''
    k_full=k
    
    '''
    #----k------
    #k is the dataframe that includes all important parameters from the towerdata,
    #which are used for the flux calculations or plots.
    
    '''
    
    if period[0]=='' and not period[1]=='':
        k=k[:period[1]]
    elif period[1]=='' and not period[0]=='':
        k=k[:period[0]]
    elif not period==['','']:
        k=k[period[0]:period[1]]
    
    
    k=k.loc[:,['WS1_speed','WS2_speed','AirTC_1_Avg','AirTC_2_Avg','Pressure [mbar]','SunElevation']]
    
    
    k=k.rename(columns={'Pressure [mbar]':'AirPressure'})

    return (k)

'''
---CalculatedParameters(k,constants)---
Input:
    k
    type: Pandas DataFrame
    Information:
        Columns:
        ['WS1_speed', (in m/s)   
         'WS2_speed', (in m/s)
         'AirTC_1_Avg', (in °C)
         'AirTC_2_Avg', (in °C)
         'AirPressure', (in Pa *10^-2)
         'SunElevation'] (not required for the calculations)
    
    constants
        array of constants
         
Output:
    k
    type: Pandas DataFrame
    Information:
        Columns:
            ['WS1_speed', (in m/s)
             'WS2_speed', (in m/s)
             'AirTC_1_Avg', (in °K)
             'AirTC_2_Avg', (in °K)
             'AirPressure', (in Pa)
             'SunElevation', (not required for calculations)
             'middle_AirTC', (in °K) (mean of 'AirTC_1_Avg' and 'AirTC_2_Avg')
             'Density',
             'Du/Dlnz',
             'DT/Dlnz']

'''    
def CalculatedParameters(k,constants):
    Rs,K,g,Cp,height1,height2,z,alpha0=constants
    #global Rs,K,g,Cp,height1,height2,z,alpha0
    #--------TO SI UNITS----------
    #Convert from hPa to Pa
    k['AirPressure']=k['AirPressure']*(float(10**2))
    # Convert to Kalvin
    k['AirTC_1_Avg']=273.15+ k['AirTC_1_Avg']
    k['AirTC_2_Avg']=273.15+ k['AirTC_2_Avg']

    #  expected density about 1,2 kg/m^3      
    
    

    
    
    
    
    #---------------Calculations before resampling----------------------                                  
    
    k['middle_AirTC']=(k['AirTC_1_Avg']+k['AirTC_2_Avg'])/2.0
    
    k['Density']=(k['AirPressure']/(Rs*k['middle_AirTC']))
    
    k['Du/Dlnz']=(k['WS2_speed']-k['WS1_speed'])/(log(height2)-log(height1))
    k['DT/Dlnz']=(k['AirTC_2_Avg']-k['AirTC_1_Avg'])/(log(height2)-log(height1))
    
    return k
    
'''
---resampling(k)---

input:
    k
        type: Pandas DataFrame
        Information:
            In this case k consists of 1 minute data. 
            The function also accepts other timesteps though.
output:
    k
        type: Pandas DataFrame
        Information
            The output dataframe is resampled to 30 minute data with an offset 
            of 15 minutes

Illustration of the resampling process:
    #--------------RESAMPLING----------------------
    #Resampling of the one minute tower data to 30 minute data.
    #The resampling is done in the same manner as by EdiRe, which assigns the calculated value 
    #to the value in the middle of the values of which the mean was taken:
    #Example:
    #1
    #2
    #3 <-- assigns the mean of 1 to 5 to the value 3
    #4
    #5
    #6
    
'''    
def resampling(k):
    

    
    k_30min=k.resample('30T',loffset='15T')
    k=k_30min
    #k_full_30min=k_full.resample('30T',loffset='15T')
    #k_full_monthly=k_full.resample('1M')
    
    return k
