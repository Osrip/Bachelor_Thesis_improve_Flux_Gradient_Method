# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 17:35:01 2015

@author: Jan
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plotiteration(iterationplotname,konv_arr,konv_time):
    
    #if konv_arr was created by CalculateFluxesMinimal its length is 4
    if len(konv_arr)==4:
        Minimal=True
        methodname=' Minimal'
    else:
        Minimal=False
    #if konv_arr was created by CalculateFluxesIteration its length is 2    
    if len(konv_arr)==2:
        Iteration=True
        methodname=' Iteration'
    else :
        Iteration=False
    
    if Minimal==False and Iteration == False :
        Evolution=True
        methodname='Evolution'
    else: 
        Evolution=False
    
    if Minimal ==True:
        u_star_konv,Qh_konv,mx_konv,my_konv=konv_arr
    if Iteration==True:
        u_star_konv,Qh_konv=konv_arr

    
    
    ustar_name='$u_* \mathrm{[m s^{-1}]}$'
    qh_name='$Q_H \mathrm{[W m^{-2}]}$'
    
    plt.rcParams.update({'font.size': 15})
    axf= plt.gca()    
    if Minimal==True or Iteration==True:
        #plt.figure()
        plt.plot(u_star_konv)
        plt.xlabel('Repetition',fontsize=15)
        plt.ylabel(ustar_name,fontsize=20)
        plt.title(konv_time)
        plt.savefig(iterationplotname+methodname+' u_star.png', dpi=400,bbox_inches='tight')
        plt.show()
    
    if Minimal==True or Iteration ==True:
        plt.figure()
        plt.plot(Qh_konv)
        plt.xlabel('Repetition',fontsize=15)
        plt.ylabel(qh_name,fontsize=20)
        plt.title(konv_time)
        plt.savefig(iterationplotname+methodname+' Qh.png', dpi=400,bbox_inches='tight')
        plt.show()
        
    if Minimal==True:
        plt.figure()
        plt.plot(mx_konv)
        plt.xlabel('Repetition',fontsize=15)
        plt.title(konv_time)
        plt.ylabel('$m_x \mathrm{[m s^{-1}]}$',fontsize=20)
        plt.savefig(iterationplotname+methodname+' mx.png', dpi=400,bbox_inches='tight')
        plt.show()
    
    if Minimal==True:
        plt.figure()
        plt.plot(my_konv)
        plt.xlabel('Repetition',fontsize=15)
        plt.title(konv_time)
        plt.ylabel('$m_y \mathrm{[W m^{-2}]}$',fontsize=20)
        axf.set_ylim([0,0.5])
        plt.savefig(iterationplotname+methodname+' my.png', dpi=400,bbox_inches='tight')
        plt.show()
        
    if Evolution==True:
        plt.plot(np.squeeze(konv_arr))
        plt.xlabel('Generation')
        plt.ylabel('1/ $F_{fit}$')
        plt.savefig(iterationplotname+methodname+'.png',bbox_inches='tight')