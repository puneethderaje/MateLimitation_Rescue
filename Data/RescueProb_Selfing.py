#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 05:12:56 2025

@author: puneeth
"""

import numpy as np
import multiprocessing as mp 
import pandas as pd 
from SexualSytems import *
NoR_rng = [10**5,10**5,10**5]

writer = pd.ExcelFile('LamdaCritical_CM_MRp-4.xlsx',engine='openpyxl')
DF_LambdaCritical = pd.read_excel(writer, sheet_name = 'Lamda_Cutoff_r' ,index_col=0)

r_rng = [0.0001,0.0005,0.001]

ps_rng = [round(x,2) for x in np.arange(0,1.01,0.05)]
IDself_rng = [x for x in np.arange(0,1,0.1)]

output_writer = pd.ExcelWriter('RescueProb_Selfing.xlsx')

a = mp.cpu_count() - 2
print(a)

d=0.1
s=1

lw_and = (1-d)*DF_LambdaCritical['Androdioecious'][0.001]
lm_and = (1+s)*DF_LambdaCritical['Androdioecious'][0.0001]

for r_ind,r in enumerate(r_rng) :
    NoR = NoR_rng[r_ind]
    DioExtProb = []
    AndExtProb = []
    for IDself in IDself_rng:
        
        
        AndExtProb_row = []
        
        for ps in ps_rng : 
            pool = mp.Pool(a)
            results = pool.starmap(Androdioecious, [(r,lw_and,lm_and,10**4,10**(-4),0,0.5,ps,IDself) for rep in range(NoR)])
            pool.close()
            pool.join()
            Ext = np.mean([results[i][0] for i in range(len(results)) ])
            AndExtProb_row = AndExtProb_row + [Ext]
            
            print(r,ps,IDself,Ext,flush=True)
            
        AndExtProb = AndExtProb + [ AndExtProb_row ]
        
    AndDF = pd.DataFrame(AndExtProb, columns = ps_rng, index = IDself_rng)
    AndDF.to_excel(output_writer,sheet_name = 'Androdioecious_'+str(r)) 
    
output_writer.save()


# NoR=10**5

# writer = pd.ExcelFile('LamdaCritical_CM_PS10000_MRp-4.xlsx',engine='openpyxl')
# DF_LambdaCritical = pd.read_excel(writer, sheet_name = 'Lamda_Cutoff' ,index_col=0)

# #r_rng = [0.0001,0.0005,0.001]
# r_rng = [round(x,6) for x in np.arange(0.0001,0.001,0.00005)]
# ps_rng = [round(x,2) for x in np.arange(0,1.01,0.2)]

# IDself_rng = [0.1,0.5,0.9]

# output_writer = pd.ExcelWriter('RescueProb_Selfing_Supl.xlsx')

# a = mp.cpu_count() - 2
# print(a)

# d=0.1
# s=1

# lw_and = (1-d)*DF_LambdaCritical['Androdioecious'][0.001]
# lm_and = (1+s)*DF_LambdaCritical['Androdioecious'][0.0001]

# for IDself_ind,IDself in enumerate(IDself_rng) :
#     DioExtProb = []
#     AndExtProb = []
#     for ps in ps_rng:
        
        
#         AndExtProb_row = []
        
#         for r in r_rng : 
#             pool = mp.Pool(a)
#             results = pool.starmap(Androdioecious, [(r,lw_and,lm_and,10**4,10**(-4),0,0.5,ps,IDself) for rep in range(NoR)])
#             pool.close()
#             pool.join()
#             Ext = np.mean([results[i][0] for i in range(len(results)) ])
#             AndExtProb_row = AndExtProb_row + [Ext]
            
#             print(r,ps,IDself,Ext,flush=True)
            
#         AndExtProb = AndExtProb + [ AndExtProb_row ]
        
#     AndDF = pd.DataFrame(AndExtProb, columns = r_rng, index = ps_rng)
#     AndDF.to_excel(output_writer,sheet_name = 'Androdioecious_'+str(IDself)) 
    
# output_writer.save()
