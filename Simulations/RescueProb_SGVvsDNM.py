#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 15:45:29 2024

@author: puneeth
"""


import numpy as np
import multiprocessing as mp 
import pandas as pd 
from SexualSystems import *

NoR = 10**5
r_rng = [0.0001,0.001,'AM']
lw_crit  = [4.92,2.01,2]
lwnorm_rng = [round(x,2) for x in np.arange(0,1.01,0.04)]
lmnorm_rng = [1.05,1.1,1.5] + [round(x,2) for x in np.arange(2,10,1)]

output_writer = pd.ExcelWriter('RescueProb_SGVvsDNM.xlsx')

a = mp.cpu_count() - 2
print(a)
for r_ind, r in enumerate(r_rng) :    
    SGVExtProb = []
    DNMExtProb = [] 
    for lwnorm in lwnorm_rng :
        lw = lwnorm*lw_crit[r_ind]
        SGVExtProb_row = []
        DNMExtProb_row = []
        for lmnorm in lmnorm_rng : 
            lm = lmnorm*lw_crit[r_ind]
            print(r,lw,lm) 
            pool = mp.Pool(a)
            results = pool.starmap(Dioecious, [(r,lw,lm,10**4,10**(-4),0) for rep in range(NoR)])
            pool.close()
            pool.join()
            Ext = np.mean(results)
            DNMExtProb_row = DNMExtProb_row + [Ext]
            
            pool = mp.Pool(a)
            results = pool.starmap(Dioecious, [(r,lw,lm,10**4,0,10**(-4)) for rep in range(NoR)])
            pool.close()
            pool.join()
            Ext = np.mean(results)
            SGVExtProb_row = SGVExtProb_row + [Ext]
            
            
        SGVExtProb = SGVExtProb + [ SGVExtProb_row ]
        DNMExtProb = DNMExtProb + [ DNMExtProb_row ]
        
    SGVDF = pd.DataFrame(SGVExtProb,columns = lmnorm_rng,index = lwnorm_rng)
    DNMDF = pd.DataFrame(DNMExtProb,columns = lmnorm_rng,index = lwnorm_rng)
    
    SGVDF.to_excel(output_writer,sheet_name = 'SGV_'+str(r)) 
    DNMDF.to_excel(output_writer,sheet_name = 'DNM_'+str(r)) 
    
output_writer.save()
