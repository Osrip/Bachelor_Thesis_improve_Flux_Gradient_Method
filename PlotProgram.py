# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 13:58:07 2016

@author: Jan
"""

import IPython
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from numpy import *
import sys

T=True
F=False

def rename(df,add_str):
    col=df.columns.tolist()
    for i in range(len(col)):
      df=df.rename(columns={col[i]:(col[i]+add_str)})
    return df

'''
-----Import CSV-----

If ECimport==True ECfile has to define the name of the EC data.

    

'''

EC_import=True

ECfile='C:\Users\Jan\Documents\Programming Bachelorthesis\edire\output\output_April_11to30_heigth2_korr.csv'

'''
savename defines the name of the loaded plots created by main_program
'''

savename='Run1'

if EC_import==True:
    
    EC=pd.read_csv(ECfile,header=0,index_col=0,parse_dates=True, dayfirst=True)

'''
csv_import 
    is an array, which consists of all the names of any other imported csv files
    calculated by "main program"
'''


csv_import=[savename+'_TowData'+'.csv',
            savename+'_'+'MIN'+'_results'+'.csv',
            savename+'_'+'ITR'+'_results'+'.csv',
            savename+'_'+'EVO'+'_results'+'.csv'
            ]


plot_df=pd.read_csv(csv_import[0],header=0,index_col=0,parse_dates=True)


for filename in csv_import[1:]:
    append_df=pd.read_csv(filename,header=0,index_col=0,parse_dates=True)
    if not (plot_df.index==append_df.index).all():
        print 'Warning: imported dataframes have different datetime indexies'
    plot_df=plot_df.join(append_df)


'''
period 
    defines the period which is plotted. period[0] is the start and 
    period[1] is the end. Dates always in datetime format or string.
    MAKE SURE THE DATES ARE WITHIN THE INDEX OF ECfile and plot_df!!!
'''
    
#period=[EC.index[0],EC.index[-1]]
period=['2015-04-24 9:45:00','2015-04-24 13:45:00']



EC=EC[period[0]:period[1]]
plot_df=plot_df[period[0]:period[1]]

EC=EC[['Ustr','Hc']]
EC=rename(EC,'_ECO')

'''
The DataFrame plot_df includes all columns, which can be plotted
'''

plot_df=plot_df.join(EC)







'''
-------X vs Y Scatter Plot---------

PlotInd_XY takes in columns names of plot_df and plots columns on x and y axis of plots

ylim defines the limits of the y axis.
if ylim==None the limits are chosen automatically


'''
#PlotInd_DayNnite=['Qh_ITR','Hc_ECO']
#PlotInd_XY=['Qh_MIN','Hc_ECO']

if True:
    try:    
    
        PlotInd_XY=['Ustr_ECO','U_star_ITR']
        ylim=[-0.1,0.5]
        
        
        
        df_plot=plot_df.loc[:,PlotInd_XY]    
        df_plot.plot(kind='scatter',x=PlotInd_XY[0],y=PlotInd_XY[1],logy=F,color='DarkGreen', label='Minimal',alpha=0.5, ylim=ylim)
        
        if not ylim==None:
            step=(ylim[1]-ylim[0])/10
            ax=plt.plot(np.arange(ylim[0],ylim[1],step),np.arange(ylim[0],ylim[1],step),'r',linewidth=1.5)
        #,ax=ax
          
        #plt.xlabel('$u_* \mathrm{FG} \mathrm{[m s^{-1}]}$',fontsize=20)
        #plt.ylabel('$u_* \mathrm{EC} \mathrm{[m s^{-1}]}$',fontsize=20)
        
        plt.savefig(savename+'_scatter'+'.png',dpi=400,bbox_inches='tight')
    except:
        print 'There occured an error trying to plot the X vs Y scatter plots '
        


'''
--------Day and Nighttime separated X vs Y Plot---------

works just like "X vs Y Scatter Plot" except of doing an additional sepereration of
day and nighttime data

A SunElevation column is required in plot_df

The "for loop" creates 4 prewritten plots

of course the loop can be removed.
'''
     
if True: 
    try:
        for i in range(4):
            
            if i==0:
                PlotInd_DayNnite=['Ustr_ECO','U_star_MIN']
                ylim=[-0.1,0.5]
                xlim=None
            if i==1:
                PlotInd_DayNnite=['Ustr_ECO','U_star_ITR']
                ylim=[-0.1,0.5]
                xlim=None
            if i==2:
                PlotInd_DayNnite=['Hc_ECO','Qh_MIN']
                
                xlim=[-70,200]
                ylim=None
            if i==3:
                PlotInd_DayNnite=['Hc_ECO','Qh_ITR']
                xlim=[-70,200]
                ylim=None
        
            ###day
            dayNnite_boo= plot_df['SunElevation'] > 0
            plot_df_day=plot_df[dayNnite_boo]
            df_plot=plot_df_day.loc[:,PlotInd_DayNnite]
            
            ax=df_plot.plot(kind='scatter',x=PlotInd_DayNnite[0],y=PlotInd_DayNnite[1],logy=F,color='red', label='Day', ylim=ylim,xlim=xlim,alpha=0.5)
            
            ###nite
            dayNnite_boo= plot_df['SunElevation']<0
            plot_df_nite=plot_df[dayNnite_boo]
            df_plot=plot_df_nite.loc[:,PlotInd_DayNnite]    
            
            ax=df_plot.plot(kind='scatter',x=PlotInd_DayNnite[0],y=PlotInd_DayNnite[1],logy=F,color='DarkBlue', label='Night', ylim=ylim,xlim=xlim,alpha=0.5,ax=ax)
            
            if ylim==None and not xlim==None  :
                ylim=xlim
            
            if not ylim==None:
                step=(ylim[1]-ylim[0])/10
                ax=plt.plot(np.arange(ylim[0],ylim[1],step),np.arange(ylim[0],ylim[1],step),'g',linewidth=1.5)
            
            #plt.xlabel('$u_* \mathrm{FG} \mathrm{[m s^{-1}]}$',fontsize=20)
            #plt.ylabel('$u_* \mathrm{EC} \mathrm{[m s^{-1}]}$',fontsize=20)    
            
            plt.savefig(savename+'_'+PlotInd_DayNnite[0]+'_vs_'+PlotInd_DayNnite[1]+'_daynite'+'.png',dpi=400,bbox_inches='tight')  
        
    except:
        print "There occured an error trying to plot the Day and Nighttime scatter plots. There has to be both day and nighttime data in the period"
        pass
'''
----------Timeseries-------------
makes two plots.
plot_ind defines the plotted columns. Its length is not determined.
'''

statistics= True


if True:
    try:
        for i in range (2):
            
            if i==0:
                plot_ind=['Ustr_ECO','U_star_ITR','U_star_MIN','U_star_EVO']
                
                add_name='ustr'
            if i==1:
                plot_ind=['Hc_ECO','Qh_ITR','Qh_MIN','Qh_EVO']
    
                add_name='sensible '
                
            if statistics==True:
                
                corcoef_plot=np.corrcoef(plot_df.loc[:,plot_ind[0]],plot_df.loc[:,plot_ind[1]])[0,1]
                mean_diff=abs(mean(plot_df.loc[:,plot_ind[0]])-mean(plot_df.loc[:,plot_ind[1]]))
                meanofmean=mean([mean(plot_df.loc[:,plot_ind[0]]),mean(plot_df.loc[:,plot_ind[1]])])
                mean0=mean(plot_df.loc[:,plot_ind[0]])
                mean1=mean(plot_df.loc[:,plot_ind[1]])
                
                
                rel_mean_diff=mean_diff/meanofmean
                print 'Correlation between '+str(plot_ind[0])+' and '+str(plot_ind[1])+'\n'+ str( corcoef_plot)   
                
                
                plot_str='Correlation: '+str(round(corcoef_plot,4))+'\n'+'mean '+plot_ind[0]+': '+str(round(mean0,4))+'\n'+'mean '+plot_ind[1]+': '+str(round(mean1,4))
                
        
                
            
                              
            df_plot=plot_df.loc[:,plot_ind]
                
            
            #df_plot.columns=['EC','FG iter','FG min' ] #'FG iter'
              
                
            fig=plt.figure()
            if i==0:
                ax=df_plot.plot(fontsize=13,alpha=0.7,linewidth=1.5) #,ylim=[-0.1,0.6]
            if i==1:
                ax=df_plot.plot(fontsize=13,alpha=0.7,linewidth=1.5) #color=['r','g','b']
            if False:
                plt.title('u_star')
            if False:
                plt.title('Qh')
            
            plt.legend(fontsize=15)        
                
            if i==0:
                unit_name='$u_* \mathrm{[m s^{-1}]}$'
            if i==1:
                unit_name='$Q_H \mathrm{[W m^{-2}]}$'
                
                
             
        
            plt.ylabel(unit_name)
            ax.yaxis.label.set_size(18)  
            ax.xaxis.label.set_size(15) 
            
            plt.savefig(savename+add_name+'.png',dpi=400,bbox_inches='tight')
            
            if statistics==True:
                plt.figtext(0.14,0.59  ,plot_str,fontsize='small',bbox = dict(alpha=1,boxstyle="square",
                             ec=(1., 0.5, 0.5),
                             fc=(1., 0.8, 0.8),
                             ))
                
                plt.savefig(savename+add_name+'_info.png',dpi=400,bbox_inches='tight')
                #,pad_inches=0.2
            plt.show()
    
    except:
        print 'There occured an error trying to plot the time series plot'

'''
----Quality parameters mx and my-----

'''


if True:
    try:    
        k_edit=plot_df
        #k_edit['Xr-Xs_TOW'][abs(k_edit['Xr-Xs_TOW'])>0.4]=np.nan
        plt.figure()
        #plt.plot(k_edit.index.values,np.log(k_edit['Xr-Xs_TOW']),'.')
        df=k_edit['Xr-Xs_MIN']
        #df.plot(kind='scatter',x='index',y='Xr-Xs_TOW')
        ax=plot_df.plot(kind='scatter',x='U_star_MIN',y='Xr-Xs_MIN', logy=True,fontsize=15,alpha=0.4,s=15,xlim=[-0.05,0.5],ylim=[10**-6,1])
        plt.ylabel('$m_x \mathrm{[m s^{-1}]}$')
        plt.xlabel('$x \mathrm{[m s^{-1}]}$')
        
        ax.yaxis.label.set_size(20)  
        ax.xaxis.label.set_size(20)
        #df.set_yscale('log')
        plt.savefig(savename+'xr-xs.png', dpi=400,bbox_inches='tight')
        plt.show()
        me=np.mean(k_edit['Xr-Xs_MIN'])
        print me
        
        ax=plot_df.plot(kind='scatter',x='Qh_MIN',y='Yr-Ys_MIN', logy=True,fontsize=15,alpha=0.4,s=15,xlim=[-60,150],ylim=[10**-4,2])
        plt.ylabel('$m_y \mathrm{[W m^{-2}]}$')
        plt.xlabel('$y \mathrm{[W m^{-2}]}$')
        
        ax.yaxis.label.set_size(20)  
        ax.xaxis.label.set_size(20)
        #df.set_yscale('log')
        plt.savefig(savename+'yr-ys.png', dpi=400,bbox_inches='tight')
        print np.mean(k_edit['Yr-Ys_MIN'])
        plt.show()
    except:
        print 'There occured an error trying to plot the quality parameter scatter plots'



'''
------------K-values--------------
Calculates K_Values and plots their distribution

EC data is required!

'''

height1=2.0
height2=7.6
Cp=1005 #1.005 J/(kg*K) spesific warmthkapacity air


if True:
    try:
        plot_df['Du/Dz']=(plot_df['WS2_speed']-plot_df['WS1_speed'])/((height2)-log(height1))
        plot_df['DT/Dz']=(plot_df['AirTC_2_Avg']-plot_df['AirTC_1_Avg'])/((height2)-log(height1))
    
        plot_df['Km_MIN']=plot_df['Du/Dz']/(-(plot_df['Ustr_ECO'])**2)
        plot_df['Kh_MIN']=-plot_df['DT/Dz']/(plot_df['Hc_ECO']/(plot_df['Density']*Cp))
        
        
            #axf= plt.gca()
        fig=plt.figure()
        plt.hist(-plot_df['Km_MIN'], bins=20,range=[0,2.5])    
        #plt.set_xlim = ([-20,15])
        #axf.set_xlim([-20,15])
        plt.xlabel('$K_m \mathrm{[m^{-2}s^{-1}]}$',fontsize=20)
        plt.ylabel('Amount',fontsize=14)
        plt.savefig(savename+'Km',dpi=400,bbox_inches='tight')
        fig=plt.figure()
        
        plt.hist(plot_df['Kh_MIN'], bins=20,range=[-0.5,1.5]) 
        plt.xlabel('$K_H \mathrm{[m^{-2}s^{-1}]}$',fontsize=20)
        plt.ylabel('Amount',fontsize=14)
        plt.savefig(savename+'Kh',dpi=400,bbox_inches='tight')
        #axf.set_xlim([-20,15])
    except:
        print 'There occured an error trying to plot the K value plots. EC data is required for these plots!'
    


