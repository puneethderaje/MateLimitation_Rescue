#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 19:28:05 2024

@author: puneeth
"""

import numpy as np
import multiprocessing as mp 
import pandas as pd 
from SexualSystems import * 

NoR = 10**(5)
r = 'AM'

N0_rng = 10**np.array(np.arange(2,5.5,0.1))
mu_rng = 10**np.array([-np.inf,-8])
p  = 10**(-4)

output_writer = pd.ExcelWriter('RescueProb_WtPopSize.xlsx')

lw_rng = [0.2,0.6,1,1.3,1.8,1.99]
lm_rng = [2.01,2.2,4]

a = mp.cpu_count() - 2
print(a)


for lm in lm_rng:
    for lw in  lw_rng:
        ExtProb = [] 
        for mu in mu_rng :    
            ExtProb_row = []
            for N0 in N0_rng :
                #print(mu,lw,lm,N0, flush=True)        
                if p == 'single':
                    psgv = N0**(-1)
                else: 
                    psgv = p
                pool = mp.Pool(a)
                results = pool.starmap(Dioecious, [(r,lw,lm,N0,mu,psgv) for rep in range(NoR)])
                pool.close()
                pool.join()
                Ext = np.mean(results)
                ExtProb_row = ExtProb_row + [Ext]
                print(mu,lw,lm,N0,Ext,flush=True) 
            ExtProb = ExtProb + [ ExtProb_row ]
        DF = pd.DataFrame(ExtProb,columns = N0_rng,index = mu_rng)
        DF.to_excel(output_writer,sheet_name = 'Un_lw'+str(lw)+'_lm'+str(lm)) 
output_writer.save()
