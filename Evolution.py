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
from numpy import *


    
def CalculateFluxesEvolution(df_in,konv_time,const):
    
   
    
    Rs,K,g,Cp,height1,height2,z,alpha0=const
        
    def f_ustar(u_star,Qh,const,env_par):
       
       
       Rs,K,g,Cp,height1,height2,z,alpha0=const
       rho,T,Du_Dlnz,DT_Dlnz   = env_par
       
               
       L=-1*(u_star**3/(K*(g/T)*(Qh/(rho*Cp))))
                
       S=z/L
                
       if S<0:
           fm=(1.0-19.3*S)**(-0.25)
       else:
           fm=1.0+6.0*S
                
       u_star=(K/fm)*Du_Dlnz
                

       return u_star
       
    def f_Qh(u_star,Qh,const,env_par):
       
       
       Rs,K,g,Cp,height1,height2,z,alpha0=const
       rho,T,Du_Dlnz,DT_Dlnz   = env_par
       
       L=-1*(u_star**3/(K*(g/T)*(Qh/(rho*Cp))))
                
       S=z/L
                
       if S<0:
          fh=0.95*((1-11*S)**(-0.5))
       else:
          fh=0.95+7.8*S
                
       cov_wt=-((alpha0*K*u_star)/fh)*DT_Dlnz
       Qh=cov_wt*rho*Cp
                

       return Qh
            
    
          
    
       
    def mx(Xs,Ys,const,env_par):
        m=1/abs(f_ustar(Xs,Ys,const,env_par)-Xs)
        return m
        
    def my(Xs,Ys,const,env_par):
        m=1/abs(f_Qh(Xs,Ys,const,env_par)-Ys)
        return m
        
    def f_s2(Xs1):
        global fac_s2
        Xs2=Xs1-(Xs1*fac_s2)
        return Xs2
    
                


    
    ###Generations
    gen=50
    #gen=500
    
    ####Size of Population
    pop_s=10
    #300
    #pop_s=300
    #50
    
    ###percentage of inidviduals which create offspring . 
    #pop_s*part has to be a whole number!!!
    ###
    part=0.10
    #0.1
    
    ###scales of the normal distribution used in order to do the mutation

    x_rad=0.0005
    y_rad=0.05

    
    
    ####space of the initial population###
    xlim_low=-1
    xlim_high=3
    ylim_low=-100
    ylim_high=200
    
    ia=np.empty((5,pop_s))
    ia_new=np.empty((5,pop_s))
   
    '''
     ia contains the genetical information x and y , 
    the quality parameters mx my
    and the firness Fi of every inidivual
    ia=[x,y,mx,my,Fi]
        0 1 2  3  4
    ''' 
    u_star_cal=[]
    Qh_cal=[]
    
    '''
    ----------Initilisation----------
    The initial population is created using a uniformly distributed random parameter
    
    '''
    
    
    ia[0]=np.random.uniform(low=xlim_low,high=xlim_high,size=pop_s)
    ia[1]=np.random.uniform(low=xlim_low,high=xlim_high,size=pop_s)
    
    fit_konv=[]
    
    
    
    for i in range(np.shape(df_in)[0]):
            rho=df_in['Density'].values[i]
            T=df_in['middle_AirTC'].values[i]
            Du_Dlnz=df_in['Du/Dlnz'].values[i]
            DT_Dlnz=df_in['DT/Dlnz'].values[i]
            
            env_par=rho,T,Du_Dlnz,DT_Dlnz
            
            '''
            The for loop with the index j goes through each generation gen
            '''
            for j in range (gen):
                
                              
                
                '''
                --------Evaluation-----------
                
                The following for loop calculates the quality parameters mx
                and my for each individual in a generation
                '''
                for l in range (pop_s):
                    #np.apply_along_axis(myfunc,1,lalala)
                    ia[2,l]=mx(ia[0,l],ia[1,l],const,env_par)
                    ia[3,l]=my(ia[0,l],ia[1,l],const,env_par)
                
                '''
                The following for loop calculates the fitness for each individual 
                of a generation
                '''
                for l in range (pop_s):
                    #Fitnessfunktion
                    #ia[4,l]=ia[2,l]/mx_mean + ia[3,l]/my_mean
                    ia[4,l]=1/(ia[2,l]/0.003 + ia[3,l]/5)
                
                '''
                -------------Selection---------------
                len_reprod 
                    is an integer representing the amount of individuals
                    to be selcted for reproduction
                max_ind 
                    contains the indexes of each individual sorted by the individuals 
                    fittness
                rand_exp 
                    is an exponentially deviated random parameter containing integers 
                    which are not bigger than the size of the population
                
                '''
                
                len_reprod=int(pop_s*part)
                max_ind=np.argsort(ia[4])
                #Rand max consists of exponentially deviated integers
                rand_exp=np.array(np.random.exponential(scale=len_reprod, size=len_reprod),dtype=int)
                #integers bigger than the population size are being replaced with random integers within pop_s
                for l in range (len_reprod):
                    if rand_exp[l]>(pop_s-1):
                        rand_exp[l]=np.random.randint(low=0, high=len_reprod, size=None)
                
                '''
                In the following loop the exponentially deviated parameter is used 
                in order to make it most probable to choose the indexes of the fittest individuals
                which are in max_ind
                
                The indexes of the selected individuals are then saved to rand_max
                '''
                rand_max=[]
                for l in rand_exp:
                    rand_max.append(max_ind[l])
                rand_max=np.array(rand_max)
                
                new_x=[]
                new_y=[]
                
                
                '''
                --------------Mutation-------------------
                In the following loop the genetic information of the selected individuals 
                is being mutated in order to create individuals for the next geberation
                This is done applying a normally distributed random parameter
                
                int(1/part)
                    gives the amount of offsprings per selected individual as "part" defines 
                    the percentage of inidviduals being selected in the population.
                    
                
                '''
                
                for l in  rand_max:
                    

                    new_x.append(np.random.normal(loc=ia[0,l], scale=x_rad, size=(int(1/part))))

                    new_y.append(np.random.normal(loc=ia[1,l], scale=y_rad, size=(int(1/part))))
                new_x=np.ravel(np.array(new_x))
                ia[0]=new_x
                new_y=np.ravel(np.array(new_x))
                ia[1]=new_y
                
                if i==konv_time:
                    av_fit=np.mean(ia[4,:])
                    fit_konv.append(av_fit)
            
            '''
            ------Result-------
            The genetic information of the fittest individuals in the last generation 
            reprensents the result
            '''
            max_ind=np.argmax(ia[4])   
            u_star_cal.append(f_ustar(ia[0,max_ind],ia[1,max_ind],const,env_par))
            Qh_cal.append(f_Qh(ia[0,max_ind],ia[1,max_ind],const,env_par))
                    
                    
                    
       
    
    #create df_out
    solution_arr=np.array([np.squeeze(u_star_cal),np.squeeze(Qh_cal)]).transpose()
    df_out=pd.DataFrame(solution_arr,index=df_in.index,columns=['U_star','Qh'])     
                    
                
    return df_out, fit_konv    
        
    
                
    
    
            
            
    
    

    
