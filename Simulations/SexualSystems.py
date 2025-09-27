#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 12 10:58:07 2025

@author: puneeth
"""
import numpy as np
def Dioecious(r,lw,lm,N0=10**4,mu=10**(-4),sgv=0,sr=0.5, timeseries=False) :
    """
    Simulates the eco-evolutionary dynamics of a population of Dioeciouss (dioecious) until either the population goes
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
    Xm = round(sgv*N0)
    Xw = N0 - Xm 
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
        elif X_M + X_F > max(2*N0,2*10**4): 
            break 
        
        if r == 'AM':
            Xm_Mate = Xm_F
            Xw_Mate = Xw_F
        else: 
            Xm_Mate = np.random.binomial(Xm_F, 1 - np.exp(-r*X_M)) 
            Xw_Mate = np.random.binomial(Xw_F, 1 - np.exp(-r*X_M)) 
        
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
    if timeseries: 
        return [Ext, Xseries]
    return Ext
        
def Hermaphroditic(r,lw,lm,N0=10**4,mu=10**(-4),sgv=0, ID_self=0, ps=0, timeseries=False):
    """
    Simulates the eco-evolutionary dynamics of a population of bisexual (hermaphrodites) until either the population goes
    extinct or reaches twice the starting population size.
    
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
        The proportion of offsprings that are hermaphrodites. 
    ps : float (between 0 and 1)
        The probability of selfing. 
    ID_self : float (between 0 and 1)
        The coefficient of inbreeding depression, i.e., the fecundity of a selfed individual is reduced by a factor of 1-ID_self
        
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
    Xm = round(sgv*N0)
    Xw = N0-Xm
    T = 0 #Time to first Mutation
    DidMutationOccur = False
    Ext = 0 
    if timeseries : 
        Xseries = [ [Xw,Xm] ]
    else:
        Xseries = []
    while True :
        if Xm == 0 and DidMutationOccur == False: 
            T += 1
        if Xm > 0 : 
            DidMutationOccur = True
        X = Xm + Xw
        if X == 0 : 
            Ext = 1 
            if DidMutationOccur == False : 
                T = 0
            break
        elif X > max(2*N0,2*10**4) : 
            break 
        if r == 'AM' : 
            [Xw_Mate,Xw_Self,Xw_NoMate] = [Xw,0,0]
            [Xm_Mate,Xm_Self,Xm_NoMate] = [Xm,0,0]
        else: 
            [Xw_Mate,Xw_Self,Xw_NoMate] = np.random.multinomial(Xw, [1 - np.exp(-r*(X-1) ), ps*np.exp(-r*(X-1)), (1-ps)*np.exp(-r*(X-1))  ])
            [Xm_Mate,Xm_Self,Xm_NoMate] = np.random.multinomial(Xm, [1 - np.exp(-r*(X-1) ), ps*np.exp(-r*(X-1)), (1-ps)*np.exp(-r*(X-1))  ])
            
        Xww = 0 
        Xwm = 0
        Xmw = 0
        Xmm = 0 
        
        if X - 1 > 0 : 
            if Xw_Mate > 0 :
                [Xww,Xwm] = np.random.multinomial(Xw_Mate, [(Xw - 1)/(X-1),Xm/(X-1)])
            if Xm_Mate > 0 :
                [Xmw,Xmm] = np.random.multinomial(Xm_Mate, [Xw/(X-1),(Xm - 1)/(X-1)])
        
        lamda_w_eff = (Xww + 0.5*Xwm)*lw + 0.5*Xmw*lm + Xw_Self*(1 - ID_self)*lw
        lamda_m_eff = (Xmm + 0.5*Xmw)*lm + 0.5*Xwm*lw + Xm_Self*(1 - ID_self)*lm
        
        Xw = np.random.poisson((1-mu)*lamda_w_eff)
        Xm = np.random.poisson(lamda_m_eff + mu*lamda_w_eff)
        if timeseries: 
            Xseries = Xseries + [ [Xw, Xm] ]
    if timeseries: 
        [Ext, Xseries]
    return Ext

def Androdioecious(r,lw,lm,N0=10**4,mu=10**(-4),sgv=0,sr=0.5,ps=0,ID_self=0,timeseries=False) :
    """
    Simulates the eco-evolutionary dynamics of a population of androdioecious individuals until either the population goes
    extinct or reaches twice the starting population size.
    
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
        The proportion of offsprings that are hermaphrodites. 
    ps : float (between 0 and 1)
        The probability of selfing. 
    ID_self : float (between 0 and 1)
        The coefficient of inbreeding depression, i.e., the fecundity of a selfed individual is reduced by a factor of 1-ID_self
        
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
    Xm = round(sgv*N0)
    Xw = N0 - Xm
    T = 0 #Time to first Mutation
    DidMutationOccur = False
    [Xw_M,Xw_B] = np.random.multinomial(Xw,[1-sr,sr])
    [Xm_M,Xm_B] = np.random.multinomial(Xm,[1-sr,sr])
    Ext = 0
    ID_self = 0 
    if timeseries:
        N = [ [Xw,Xm] ]
    else:
        N = []
    while True : 
        X_M = Xm_M + Xw_M
        X_B = Xm_B + Xw_B
        Xw = Xw_M + Xw_B
        Xm = Xm_M + Xm_B
        if Xm == 0 and DidMutationOccur == False: 
            T += 1
        if Xm > 0 : 
            DidMutationOccur = True
        X = X_M + X_B
        if X == 0 : 
            Ext = 1
            if DidMutationOccur == False : 
                T = np.inf
            break
        if X_M + X_B > max(2*N0,2*10**4) : 
            break 
        if r == 'AM': 
            [Xw_Mate,Xw_Self,Xw_NoMate] = [Xw_B,0,0]
            [Xm_Mate,Xm_Self,Xm_NoMate] = [Xm_B,0,0]
        else: 
            [Xw_Mate,Xw_Self,Xw_NoMate] = np.random.multinomial(Xw_B, [1 - np.exp(-r*(X-1) ), ps*np.exp(-r*(X-1)), (1-ps)*np.exp(-r*(X-1))  ])
            [Xm_Mate,Xm_Self,Xm_NoMate] = np.random.multinomial(Xm_B, [1 - np.exp(-r*(X-1) ), ps*np.exp(-r*(X-1)), (1-ps)*np.exp(-r*(X-1))  ])
        
        Xww = 0 
        Xwm = 0
        Xmw = 0
        Xmm = 0
        
        if X - 1 > 0 : 
            if Xw_Mate > 0 :
                [Xww,Xwm] = np.random.multinomial(Xw_Mate, [(Xw - 1)/(X-1),Xm/(X-1)])
            if Xm_Mate > 0 :
                [Xmw,Xmm] = np.random.multinomial(Xm_Mate, [Xw/(X-1),(Xm - 1)/(X-1)])
        
        lamda_w_eff = (Xww + 0.5*Xwm)*lw + 0.5*Xmw*lm + Xw_Self*(1 - ID_self)*lw
        lamda_m_eff = (Xmm + 0.5*Xmw)*lm + 0.5*Xwm*lw + Xm_Self*(1 - ID_self)*lm
        
        Xw = np.random.poisson((1-mu)*lamda_w_eff)
        Xm = np.random.poisson(lamda_m_eff+ mu*lamda_w_eff)
        
        [Xw_M,Xw_B] = np.random.multinomial(Xw,[1-sr,sr])
        [Xm_M,Xm_B] = np.random.multinomial(Xm,[1-sr,sr])
        
        if timeseries: 
            N = N + [ [Xw_B + Xw_M, Xm_B + Xm_M] ]
    if timeseries: 
        return [Ext, N]
    return Ext