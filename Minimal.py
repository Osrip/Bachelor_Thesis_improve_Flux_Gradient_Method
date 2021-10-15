# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 19:57:04 2015

@author: Jan
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
'''
df_out,konv_arr=CalculateFluxesMinimal(df_in,konv_time,const)

input
    df_in
        type: pandas dataframe
        Information:
            ['WS1_speed',
             'WS2_speed',
             'AirTC_1_Avg',
             'AirTC_2_Avg',
             'AirPressure',
             'SunElevation',
             'middle_AirTC',
             'Density',
             'Du/Dlnz',
             'DT/Dlnz']
    konv_time
        type: int
        Information:
            Gives the number of the row (index) in df_in for which the konvergens arrays
             (konv_arr) are exported
    
    const
        type:list
        Information: Imports natural constants required for the calculation
        
     
output
    df_out
        type: pandas dataframe
        Information:
            ['U_star',  (m/s)
            'Qh',       (W/m^2)
            'stability',(dim.less) Formula 2.16 inn Thesis
            'Xr-Xs',    (m/s)    Quality parameter mx indicates accuracy of solution (Formula 4.12)
            'Yr-Ys']    (W/m^2)  Quality parameter mx indicates accuracy of solution (Formula 4.13)
            
    konv_arr
        type: tuple
        Information:
        u_star_konv,Qh_konv,mx_konv,my_konv
        
        Displays the developement of the parameter with increasing repitition at the datapoint given by konv_time
            
    
    
     

'''
def CalculateFluxesMinimal(df_in,konv_time,const):
    
    #global parameters in const
    global Rs,K,g,Cp,height1,height2,z,alpha0
    #global environmental parameters
    global rho,T,Du_Dlnz,DT_Dlnz
    
    #assigning const values
    Rs,K,g,Cp,height1,height2,z,alpha0=const
    
    
    

    
    '''
    f_ustar (Formula) and f_Qh (Formula) apply steps 1 to 4 mentioned in Chapter 3.2.2.
    in order to calculate friction velocity and sensitive heat flux
    The functions are called by the functions mx and my
    '''
    def f_ustar(u_star,Qh):
       global S 
       #Rs,K,g,Cp,height1,height2,z,alpha0
       #Rs,K,g,Cp,height1,height2,z,alpha0=const
       #rho,T,Du_Dlnz,DT_Dlnz=env_par
       
       #Calculate Obukhov Length (Formula 2.15)    
       L=-1*(u_star**3/(K*(g/T)*(Qh/(rho*Cp))))
       
       #Calculate dimensionless stability parameter (Formula 2.16)
       S=z/L
       
       #Calculate value of stability correction parameter (Formulas 2.19 and 2.21)
       if S<0:
           fm=(1.0-19.3*S)**(-0.25)
       else:
           fm=1.0+6.0*S
       
       #Calculate u* applying Formula 2.17
       u_star=(K/fm)*Du_Dlnz
                
    
       return u_star
       
    def f_Qh(u_star,Qh):
       
       global S 
       #Rs,K,g,Cp,height1,height2,z,alpha0
       #Rs,K,g,Cp,height1,height2,z,alpha0=const
       #rho,T,Du_Dlnz,DT_Dlnz=env_par
       
       #Calculate Obukhov Length (Formula 2.15)
       L=-1*(u_star**3/(K*(g/T)*(Qh/(rho*Cp))))
       
       #Calculate dimensionless stability parameter (Formula 2.16)
       S=z/L
       
       #Calculate value of stability correction parameter (Formulas 2.20 and 2.22)
       if S<0:
          fh=0.95*((1-11*S)**(-0.5))
       else:
          fh=0.95+7.8*S
       
       #Calculate Qh applying Formulas 2.18 and 2.11
       cov_wt=-((alpha0*K*u_star)/fh)*DT_Dlnz
       Qh=cov_wt*rho*Cp
                
    
          
       return Qh
    
    '''
    mx and my actually return 1/mx and 1/my so the algorithm is actually looking 
    for the maximum. 
    There is no special reason for this though. I decided to keep it this way because
    the algorithm was tested in this version.
    '''
    
    #mx: Formula 4.12 and 4.5
    def mx(Xs,Ys):
        m=1/abs(f_ustar(Xs,Ys)-Xs)
        return m
    
    #my: Formula 4.13 and 4.5    
    def my(Xs,Ys):
        m=1/abs(f_Qh(Xs,Ys)-Ys)
        return m
    
    # f_s2 calculates a second point of X or Y in order to determine the gradient (Formula 4.6)    
    def f_s2(Xs1):
        global fac_s2
        Xs2=Xs1-(Xs1*fac_s2)
        return Xs2

    
    ###################################
    ###########Calculations##############
    ####################################
    
  
    
    #fac_s2 is called f_G in the thesis. (Formula 4.6)
    global fac_s2
    fac_s2=0.001
    
    '''
    ------Konvergens plots----------
    For the entry in k which equals the value of konv_time, the convergens of 
    different parameters during the repitizions of the loop is saved into arrays
    which can be plottet with the module "plotiteration"
    Therefore the konvergens arrays have the length of the variable "ran" which 
    sets the total number of repititions
    
    '''
    u_star_konv=[]
    Qh_konv=[]
    S_konv=[]
    mx_konv=[]
    my_konv=[]
    
    # konv_time
    
    
    
    
    u_star_cal=np.empty((np.shape(df_in)[0],1))
    Qh_cal=np.empty((np.shape(df_in)[0],1))
    stability=np.empty((np.shape(df_in)[0],1))
    diff_xr_xs=np.empty((np.shape(df_in)[0],1))
    diff_yr_ys=np.empty((np.shape(df_in)[0],1))
    

    '''
    ---------FOR Loops----------
    The first FOR loop which changes the index "i" 
    sets the entry of "k" for which 
    the calculation of u* and Qh is done.
    
    The second FOR loop which changes the index j 
    sets the number of the repition
    during the process of finding the minimum.
    '''
    
    '''
    -------WHILE Loop----------
    As explained in chapter 4.2.3 for the calculation of u* only positive guess 
    values are used when caluating u* while negative guess values of Qh are used 
    when calculating Qh in case of a negative solution of Qh.
    This method is implemented by the while loop.
    The boolean variable "restart" tells wheather the calculation should be restarted 
    with a negative guess value of Qh
    The integer "check" counts the amount of times that the while loop has been restarted
    where check==1 is the first run so check==2 would be the first restart.
    When the while loop is restarted more than once an error occured.
    
    '''
    
    
    for i in range(np.shape(df_in)[0]):
        
        restart=True
        check=0
        while restart==True  :
            restart=False
            check+=1
            
            if check==3:  #prevents a possible infinte loop eventhough this problem never occured in any tests
                print('WARNING: possible infinite loop occured')            
                break
            
            # fac_Xs1 and fac_Ys1 are called f_N in the thesis (Formula 4.8)
            # It is used to calculate the new X and Y.
            fac_Xs1=0.01
            fac_Ys1=0.01
            
            #------Initial guess values-------
            #Initial guess value of u_star
            Xs1=0.3
            Xs2=f_s2(Xs1)    
                
            '''
            ----guess value Qh----
            When check==1 (first run of WHILE loop), a positive guess value is used for Qh
            when check==2 (second run of WHILE loop), a negative guess value is used for Qh
            '''
            if check==1:  
                Ys1=30
            else:
                Ys1=-30
            Ys2=f_s2(Ys1)
            
            #-----------------------
            
            # ran is the total number of repititions in order to find the minimum
            if i == konv_time:
                ran=2500
                
        
            else:
                ran=2500
                
            #Environmental parameters required for calculations
            rho=df_in['Density'].values[i]
            T=df_in['middle_AirTC'].values[i]
            Du_Dlnz=df_in['Du/Dlnz'].values[i]
            DT_Dlnz=df_in['DT/Dlnz'].values[i]
            env_par=[rho,T,Du_Dlnz,DT_Dlnz]
            
            
            if i==konv_time :
                if check==1:
                    mx_konv.append(1/mx(Xs1,Ys1))
                    u_star_konv.append(Xs1)
                Qh_konv.append(Ys1)
                my_konv.append(1/my(Xs1,Ys1))
        
        
        
        
        
            for j in range(ran):
                
                
                #for every 50th run of the loop fac (called f_N in Thesis) is decreased.
                if j%50==0:
                    fac_Xs1-=fac_Xs1*0.1
                    fac_Ys1-=fac_Ys1*0.1
                    
            
        #####------ X  : u_star -------  
                '''
                This IF Condition choses a new value for X in the solution room of mx 
                shown in Figure 4.4
                
                When the gradient (called Delta my in the thesis) is positive,
                a larger value is chosen for x. For a positive gradient, a lower value is chosen.
                Xs1 and Ys1 are the values, which were calculated in the previous repetition of the
                FOR loop. Xs2 is a value which is slightly larger than
                Xs1 (Formula 4.6). It is used to determine the gradient.
                '''
                if mx(Xs1,Ys1)>mx(Xs2,Ys1):
                    Xs1+=Xs1*fac_Xs1
                    Xs2=f_s2(Xs1)
        
                else:
                    Xs1-=Xs1*fac_Xs1
                    Xs2=f_s2(Xs1)
        
                # The results of U_star are saved to the konvergens array 
                # when i==konv_time
                if i==konv_time:
                    if check==1:
                        u_star_konv.append(Xs1)
                        
                    S_konv.append(S)
                    
                    
                   
                    
                
                        
        #####------ Y  : Qh ------- 
                '''
                This IF Condition choses a new value for Y in the solution room of my 
                shown in Figure 4.5
                
                When the gradient (called Delta my in the thesis) is positive,
                a larger value is chosen for Y. For a positive gradient, a lower value is chosen.
                Xs1 and Ys1 are the values, which were calculated in the previous repetition of the
                FOR loop. Ys2 is a value which is slightly larger than
                Ys1 (Formula 4.6). It is used to determine the gradient.
                '''
                if my(Xs1,Ys1)>my(Xs1,Ys2):
                    Ys1+=Ys1*fac_Ys1
                    Ys2=f_s2(Ys1)
        
                else: 
                    Ys1-=Ys1*fac_Ys1
                    Ys2=f_s2(Ys1)
        
                    
                if i==konv_time:
                    if check==1:
                        mx_konv.append(1/mx(Xs1,Ys1))
                    S_konv.append(S)
                    Qh_konv.append(Ys1)
                    my_konv.append(1/my(Xs1,Ys1))
           
            Qh_cal[i]=Ys1
            stability[i]=S
            diff_yr_ys[i]=1/my(Xs1,Ys1)
            if check==1:
                u_star_cal[i]=Xs1
                diff_xr_xs[i]=1/mx(Xs1,Ys1)
                
                    
            '''
            A negative guess value is used for the calculation of Qh in case Qh has
            a result close to zero (<0.4) when using a positive guess value for Qh
            For that reason the loop is restarted, check is set to 2 and a negative
            guess value for Qh is used.
            '''
            if abs(Ys1)<0.4 and check==1:         
                restart=True
                
                if i==konv_time:
                    #u_star_konv=[]
                    Qh_konv=[]
                    S_konv=[] 
                    mx_konv=[]
                    my_konv=[]
                
    
    
        
    #df_out['U_star']=u_star_cal
    #df_out['Qh']=Qh_cal
    #df_out['stability']=stability
    #df_out['Xr-Xs']=diff_xr_xs
    #df_out['Yr-Ys']=diff_yr_ys
    
    #create df_out
    solution_arr=np.array([np.squeeze(u_star_cal),np.squeeze(Qh_cal),np.squeeze(stability),np.squeeze(diff_xr_xs),np.squeeze(diff_yr_ys)]).transpose()
    df_out=pd.DataFrame(solution_arr,index=df_in.index,columns=['U_star','Qh','stability','Xr-Xs','Yr-Ys'])    
    
    konv_arr=u_star_konv,Qh_konv,mx_konv,my_konv
    
    return [df_out,konv_arr]
