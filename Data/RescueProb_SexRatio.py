#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 23:03:58 2025

@author: puneeth
"""
import numpy as np
import multiprocessing as mp 
import pandas as pd 
from SexualSystems import *

NoR_rng = [10**5,10**5,10**5]
#sr_rng = np.arange(0,1.01,0.05)

sr_rng = list(np.arange(0,1.01,0.05)) + list(np.arange(0.92,1,0.02))

lwcrit_writer = pd.ExcelWriter('LamdaCritical_CM_MRp-4.xlsx', engine='openpyxl', mode='a')
lwcritDF = pd.read_excel(lwcrit_writer, sheet_name = 'Lamda_Cutoff_r' ,index_col=0, engine='openpyxl')

#r_rng = [0.0001,0.001,'AM']
r_rng = ['AM']

s = 10#1.02 #[1.1,1.5,2,5,7,9,10]
d_rng = [0.5]
#d_rng = [0.1,0.3,0.7,0.9,0.97,0.98,0.99]
#d_rng = [0.1,0.2,0.3,0.4,0.5]

output_writer = pd.ExcelWriter('RescueProb_SexRatio2.xlsx')

a = mp.cpu_count() - 2
print(a)


for r_ind,r in enumerate(r_rng) :
    NoR = NoR_rng[r_ind]
    
    
    DioExtProb = []
    AndExtProb = []
    #for s in s_rng :
    for d in d_rng:
        lw_dio = d*(lwcritDF['Dioecious'][r] if r != 'AM' else 2)
        lw_and = d*(lwcritDF['Androdioecious'][r] if r != 'AM' else 2)
        lm_dio = s*(lwcritDF['Dioecious'][r] if r != 'AM' else 2)
        lm_and = s*(lwcritDF['Androdioecious'][r] if r != 'AM' else 2)
        
        DioExtProb_row = []
        AndExtProb_row = []
        
        for sr in sr_rng : 
            pool = mp.Pool(a)
            results = pool.starmap(Dioecious, [(r,lw_dio,lm_dio,10**4,10**(-4),0,sr) for rep in range(NoR)])
            pool.close()
            pool.join()
            Ext = np.mean(results)
            DioExtProb_row = DioExtProb_row + [Ext]
            
            print(r,sr,Ext,flush=True)
            
            pool = mp.Pool(a)
            results = pool.starmap(Androdioecious, [(r,lw_and,lm_and,10**4,10**(-4),0,sr) for rep in range(NoR)])
            pool.close()
            pool.join()
            Ext = np.mean(results)
            AndExtProb_row = AndExtProb_row + [Ext]
            
            print(r,sr,Ext,flush=True)
            
        DioExtProb = DioExtProb + [ DioExtProb_row ]
        AndExtProb = AndExtProb + [ AndExtProb_row ]
        
    #DioDF = pd.DataFrame(DioExtProb, columns = sr_rng, index = s_rng)
    DioDF = pd.DataFrame(DioExtProb, columns = sr_rng, index = d_rng)
    DioDF.to_excel(output_writer,sheet_name = 'Dioecious_'+str(r)) 
    
    #AndDF = pd.DataFrame(AndExtProb, columns = sr_rng, index = s_rng)
    AndDF = pd.DataFrame(AndExtProb, columns = sr_rng, index = d_rng)
    AndDF.to_excel(output_writer,sheet_name = 'Androdioecious_'+str(r)) 
    
output_writer.save()