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
   

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def CalculateFluxesIteration(df_in,konv_time,const):
    global i,S_konv,u_star_konv,S
    #global parameters in const
    global Rs,K,g,Cp,height1,height2,z,alpha0
    #global environmental parameters
    global rho,T,Du_Dlnz,DT_Dlnz
    
    Rs,K,g,Cp,height1,height2,z,alpha0=const
    
    
    
    def f_ustar(u_star,Qh):
       global i,S_konv,u_star_konv,S
       
       #Rs,K,g,Cp,height1,height2,z,alpha0=const
       #rho,T,Du_Dlnz,DT_Dlnz   = env_par
       
               
       L=-1*(u_star**3/(K*(g/T)*(Qh/(rho*Cp))))
                
       S=z/L
                
       if S<0:
           fm=(1.0-19.3*S)**(-0.25)
       else:
           fm=1.0+6.0*S
                
       u_star=(K/fm)*Du_Dlnz
                
       if i==konv_time:
           S_konv.append(S)
           u_star_konv.append(u_star)
       return u_star
       
    def f_Qh(u_star,Qh):
       global i,S_konv,u_star_konv,S
       
       #Rs,K,g,Cp,height1,height2,z,alpha0=const
       #rho,T,Du_Dlnz,DT_Dlnz   = env_par
       
       L=-1*(u_star**3/(K*(g/T)*(Qh/(rho*Cp))))
                
       S=z/L
                
       if S<0:
          fh=0.95*((1-11*S)**(-0.5))
       else:
          fh=0.95+7.8*S
                
       cov_wt=-((alpha0*K*u_star)/fh)*DT_Dlnz
       Qh=cov_wt*rho*Cp
                
       if i==konv_time:
          S_konv.append(S)
          Qh_konv.append(Qh)
          
       return Qh
    
                
    
    

    ###################################
    ###########Calculations##############
    ####################################
    
    
    
    
    ##################################
    
    
    
   

    
    
    u_star_cal=np.empty((np.shape(df_in)[0],1))
    Qh_cal=np.empty((np.shape(df_in)[0],1))
    stability=np.empty((np.shape(df_in)[0],1))
    
    for i in range(np.shape(df_in)[0]):
        #initial values
        u_star=0.3
        Qh=0
        
        if i == konv_time:
            ran=30
            #u_star_konv=np.empty((ran,1))
            u_star_konv=[]
            Qh_konv=[]
            S_konv=[]
        else:
            ran=1000
            
        rho=df_in['Density'].values[i]
        T=df_in['middle_AirTC'].values[i]
        Du_Dlnz=df_in['Du/Dlnz'].values[i]
        DT_Dlnz=df_in['DT/Dlnz'].values[i]
        
        env_par=rho,T,Du_Dlnz,DT_Dlnz      
        
        if i==konv_time :
            u_star_konv.append(u_star)
            Qh_konv.append(Qh)

        '''
        The for loop with the index j represents the iterational process 
        '''        
        
        
        for j in range(ran):
    #------------u*(u*,Qh)--------------        
            
            u_star=f_ustar(u_star,Qh)
    
    
    #-----------Qh(u*,Qh)----------------   
           
            Qh=f_Qh(u_star,Qh)
    
            
            
        u_star_cal[i]=u_star
        Qh_cal[i]=Qh
        stability[i]=S
        
    #df_out['U_star']=u_star_cal
    #df_out['Qh']=Qh_cal
    #df_out['stability']=stability
    
    
    solution_arr=np.array([np.squeeze(u_star_cal),np.squeeze(Qh_cal),np.squeeze(stability)]).transpose()
    df_out=pd.DataFrame(solution_arr,index=df_in.index,columns=['U_star','Qh','stability'])     
    
    konv_arr=u_star_konv,Qh_konv
    
    return df_out,konv_arr
    

