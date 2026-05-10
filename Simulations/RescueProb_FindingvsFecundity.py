#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 19:03:09 2024

@author: puneeth
"""

import numpy as np
import multiprocessing as mp 
import pandas as pd 

def Unisexual(rw,rm,lw,lm,N0=10**4,mu=10**(-4),sgv=0,sr=0.5, timeseries=False) :
    """
    Simulates the eco-evolutionary dynamics of a population of unisexuals (dioecious) until either the population goes
    extinct or reaches twice the starting population size N0.
    
    Parameters
    ----------
    r : float (positive)
        The mate-searching efficiency
    lw : float (positive)
        The fecundity of the wildtype, i.e. the mean number of offsprings produced conditional on finding a mate.  
    lm : float (positive)
        The fecundity of the mutant, i.e. the mean number of offsprings produced conditional on finding a mate.  
    N0 : int
        The starting total population size. 
    sgv : float (between 0 and 1)
        The percentage of the starting population size that is mutant. 
    sr : float (between 0 and 1)
        The proportion of offsprings that are female. 
        
    Returns
    -------
    Ext : int (0 or 1)
        Is 0 is the population survives and 1 if the population went extinct
    Xseries : list of lists
        The timeseries data of Xm and Xw. 
    T : int (postive)
        The time to first mutation in generations. 
    """
    
    np.random.seed()
    #mu = 0.0001
    Xm = round(sgv*N0)
    Xw = N0 - Xm 
    #NoG = 1000
    T = 0 #Time to first Mutation
    DidMutationOccur = False
    lamda_w = lw
    lamda_m = lm
    [Xw_M,Xw_F] = np.random.multinomial(Xw,[1-sr,sr])
    [Xm_M,Xm_F] = np.random.multinomial(Xm,[1-sr,sr])
    Ext = 0 
    if timeseries: 
        Xseries = [ [Xw,Xm] ]
    else:
        Xseries = [] 
    while True : 
        if Xm_M + Xm_F == 0 and DidMutationOccur == False : 
            T += 1
        if Xm_M + Xm_F > 0 : 
            DidMutationOccur = True
        X_M = Xm_M + Xw_M
        X_F = Xm_F + Xw_F
        if X_M == 0 or X_F == 0 : 
            Ext = 1 
            if DidMutationOccur == False:
                T = np.inf
            break
        elif X_M + X_F > 2*N0 : 
            break 
        Xm_Mate = np.random.binomial(Xm_F, 1 - np.exp(-rm*X_M)) 
        Xw_Mate = np.random.binomial(Xw_F, 1 - np.exp(-rw*X_M)) 
        
        [Xww,Xwm] = np.random.multinomial(Xw_Mate, [Xw_M/X_M,Xm_M/X_M])
        [Xmw,Xmm] = np.random.multinomial(Xm_Mate, [Xw_M/X_M,Xm_M/X_M])
        
        lamda_w_eff = (Xww + 0.5*Xwm)*lamda_w + 0.5*Xmw*lamda_m 
        lamda_m_eff = (Xmm + 0.5*Xmw)*lamda_m + 0.5*Xwm*lamda_w 
        Xw = np.random.poisson((1-mu)*lamda_w_eff)
        Xm = np.random.poisson(lamda_m_eff+mu*lamda_w_eff)
        [Xw_M,Xw_F] = np.random.multinomial(Xw,[1-sr,sr])
        [Xm_M,Xm_F] = np.random.multinomial(Xm,[1-sr,sr])
        
        if timeseries: 
            Xseries = Xseries + [ [Xw_F + Xw_M, Xm_F + Xm_M] ]
    return [Ext,Xseries,T]


NoR_rng = [10**(5),10**5]
rw_rng = [0.0001,0.001]

lw_crit = [4.91, 2.01]

lw_base = 0.99*np.array(lw_crit)
percentage_rng = [10,50,100,500,1000,5000,10000]
fecundity_prop_rng = np.arange(-0.5,1.51,0.05)

output_writer = pd.ExcelWriter('RescueProb_FindingvsFecundity.xlsx')

a = mp.cpu_count() - 2
print(a)
typ = 1

for r_ind, rw in enumerate(rw_rng) :
    NoR = NoR_rng[r_ind]
    lw = lw_base[r_ind]
    ExtProb = []
    for percent in percentage_rng : 
        ExtProb_row = []
        for lw_x in fecundity_prop_rng : 
            lw_x = round(lw_x,2) 
            lm = (lw_x*percent)*0.01*lw+lw
            if typ == 1 :
                rm = (1-lw_x)*percent*0.01*rw+rw
            elif typ == 2 : 
                Nchoice = 1
                sr = (1-lw_x)*percent*0.01
                pnew = min( max( (1-np.exp(-rw*Nchoice))*(1+sr), 0 ), 1)
                rm = np.inf if pnew == 1 else -1/Nchoice * np.log( 1 - pnew ) 
            
            if lm <= 0 or rm <= 0 : 
                ExtProb_row = ExtProb_row + [1]
                print(rw,percent,lw_x,1, flush=True)
                continue 
            pool = mp.Pool(a)
            results = pool.starmap(Unisexual, [(rw,rm,lw,lm,10**4,10**(-4),0) for rep in range(NoR)])
            pool.close()
            pool.join()
            Ext = np.mean([results[i][0] for i in range(len(results)) ])
            ExtProb_row = ExtProb_row + [Ext]
            print(rw,percent,lw_x,Ext, flush=True)
        ExtProb = ExtProb + [ ExtProb_row ]
        
    DF = pd.DataFrame(ExtProb,columns = fecundity_prop_rng,index = percentage_rng)
    DF.to_excel(output_writer,sheet_name = str(rw)) 
    
output_writer._save()
