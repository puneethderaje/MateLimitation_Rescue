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
r_rng = ["AM", 0.001, 0.0001]
lwnorm_rng = [round(x,2) for x in np.arange(0.9,1.005,0.005)]
lmnorm_rng = [round(x,2) for x in np.arange(1,5.1,0.2)]

#lw_rng = [round(x,2) for x in np.arange(0.1,6,0.1)]
#lm_rng = [1,10,20,30,40,50,60,70,80,90,100]

lwcrit_writer = pd.ExcelWriter('LamdaCritical_CM_MRp-4.xlsx', engine='openpyxl', mode='a')
lwcritDF = pd.read_excel(lwcrit_writer, sheet_name = 'Lamda_Cutoff_r' ,index_col=0, engine='openpyxl')

output_writer = pd.ExcelWriter('RescueProb_MatingSystem_Norm.xlsx') #Delete _Norm to generate the other file.  

a = mp.cpu_count() - 2
print(a)
for r in r_rng :    
    BiExtProb = []
    AnExtProb = [] 
    UnExtProb = []     
    #for lw in lwnorm_rng:
    for lwnorm in lwnorm_rng : 
        BiExtProb_row = []
        AnExtProb_row = []
        UnExtProb_row = []
        #for lm in lm_rng
        for lmnorm in lmnorm_rng : 
            print(r,lwnorm,lmnorm)
            
            lw = lwnorm*(lwcritDF['Androdioecious'][r] if r != 'AM' else 2) #Comment this line to generate RescueProb_MatingSystem.xlsx file
            lm = lmnorm*(lwcritDF['Androdioecious'][r] if r != 'AM' else 2) #Comment this line to generate RescueProb_MatingSystem.xlsx file
            pool = mp.Pool(a)
            results = pool.starmap(Androdioecious, [(r,lw,lm) for rep in range(NoR)])
            pool.close()
            pool.join()
            Ext = np.mean(results)
            AnExtProb_row = AnExtProb_row + [Ext]
            
            lw = lwnorm*(lwcritDF['Dioecious'][r] if r != 'AM' else 2)
            lm = lmnorm*(lwcritDF['Dioecious'][r] if r != 'AM' else 2)
            pool = mp.Pool(a)
            results = pool.starmap(Dioecious, [(r,lw,lm) for rep in range(NoR)])
            pool.close()
            pool.join()
            Ext = np.mean(results)
            UnExtProb_row = UnExtProb_row + [Ext]
            
            lw = lwnorm*(lwcritDF['Hermaphroditic'][r] if r != 'AM' else 1)
            lm = lmnorm*(lwcritDF['Hermaphroditic'][r] if r != 'AM' else 1)
            pool = mp.Pool(a)
            results = pool.starmap(Hermaphroditic, [(r,lw,lm) for rep in range(NoR)])
            pool.close()
            pool.join()
            Ext = np.mean(results)
            BiExtProb_row = BiExtProb_row + [Ext]
            
        AnExtProb = AnExtProb + [ AnExtProb_row ]
        BiExtProb = BiExtProb + [ BiExtProb_row ]
        UnExtProb = UnExtProb + [ UnExtProb_row ]
        
    BiDF = pd.DataFrame(BiExtProb,columns = lmnorm_rng,index = lwnorm_rng)
    AnDF = pd.DataFrame(AnExtProb,columns = lmnorm_rng,index = lwnorm_rng)
    UnDF = pd.DataFrame(UnExtProb,columns = lmnorm_rng,index = lwnorm_rng)
    AnDF.to_excel(output_writer,sheet_name = 'An_'+str(r)) 
    UnDF.to_excel(output_writer,sheet_name = 'Di_'+str(r)) 
    BiDF.to_excel(output_writer,sheet_name = 'He_'+str(r))
output_writer.save()
