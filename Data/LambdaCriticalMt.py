#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 15:42:27 2024

@author: puneeth
"""
import numpy as np
import multiprocessing as mp 
import pandas as pd 
from SexualSystems import * 

NoR = 10000
r_rng =r_rng = [round(x,8) for x in np.arange(0.0001,0.001,0.00004)] + [0.001]
lwnorm_rng = [round(x,2) for x in np.arange(0.9,1.02,0.02)]
mp_cpu = mp.cpu_count()

lwcrit_writer = pd.ExcelWriter('LamdaCritical_CM_MRp-4.xlsx', engine='openpyxl', mode='a')
lwcritDF = pd.read_excel(lwcrit_writer, sheet_name = 'Lamda_Cutoff_r' ,index_col=0, engine='openpyxl')

LCMwriter = pd.ExcelWriter('LamdaCriticalMutant_CM_MRp-4_PS10000.xlsx')
Lamda_Cutoff_Bi = []

for r in r_rng : 
    Lamda_Cutoff_Bi_row = []
    for lwnorm in lwnorm_rng :
        lw = lwnorm*lwcritDF['Hermaphroditic'][r]
        
        print('Hermaphroditic',r,lw,flush=True)
        lamda = 0
        Ext = 1
        while Ext == 1 : 
            lamda  = lamda + 1
            pool = mp.Pool(mp_cpu - 2)
            results = pool.starmap(Hermaphroditic, [(r,lw,lamda) for rep in range(NoR)])
            pool.close()
            pool.join()
            Ext = min(results)
        lamda = lamda - 1
        Ext = 1
        while Ext == 1 :
            lamda  = lamda + 0.1
            pool = mp.Pool(mp_cpu - 2)
            results = pool.starmap(Hermaphroditic, [(r,lw,lamda) for rep in range(NoR)])
            pool.close()
            pool.join()
            Ext = min(results)
        lamda = lamda - 0.1
        Ext = 1
        while Ext == 1 :
            lamda  = lamda + 0.01
            pool = mp.Pool(mp_cpu - 2)
            results = pool.starmap(Hermaphroditic, [(r,lw,lamda) for rep in range(NoR)])
            pool.close()
            pool.join()
            Ext = min(results)
        Lamda_Cutoff_Bi_row = Lamda_Cutoff_Bi_row + [lamda]
    Lamda_Cutoff_Bi = Lamda_Cutoff_Bi + [Lamda_Cutoff_Bi_row]
DF = pd.DataFrame(Lamda_Cutoff_Bi, columns = lwnorm_rng , index = r_rng )
DF.to_excel(LCMwriter,sheet_name = 'Hermaphroditic' )

Lamda_Cutoff_An = []
for r in r_rng : 
    Lamda_Cutoff_An_row = []
    for lwnorm in lwnorm_rng :
        lw = lwnorm*lwcritDF['Androdioecious'][r]
        print('Androdioecious',r,lw)
        lamda = 0
        Ext = 1
        while Ext == 1 : 
            lamda  = lamda + 1
            pool = mp.Pool(mp_cpu - 2)
            results = pool.starmap(Androdioecious, [(r,lw,lamda) for rep in range(NoR)])
            pool.close()
            pool.join()
            Ext = min(results)
        lamda = lamda - 1
        Ext = 1
        while Ext == 1 : 
            lamda  = lamda + 0.1
            pool = mp.Pool(mp_cpu - 2)
            results = pool.starmap(Androdioecious, [(r,lw,lamda) for rep in range(NoR)])
            pool.close()
            pool.join()
            Ext = min(results)
        lamda = lamda - 0.1
        Ext = 1
        while Ext == 1 :
            lamda  = lamda + 0.01
            pool = mp.Pool(mp_cpu - 2)
            results = pool.starmap(Androdioecious, [(r,lw,lamda) for rep in range(NoR)])
            pool.close()
            pool.join()
            Ext = min(results)
        Lamda_Cutoff_An_row = Lamda_Cutoff_An_row + [lamda]
    Lamda_Cutoff_An = Lamda_Cutoff_An + [Lamda_Cutoff_An_row]
DF = pd.DataFrame(Lamda_Cutoff_An, columns = lwnorm_rng , index = r_rng )
DF.to_excel(LCMwriter,sheet_name = 'Androdioecious' )

Lamda_Cutoff_Un = []
for r in r_rng : 
    Lamda_Cutoff_Un_row = []
    for lwnorm in lwnorm_rng :
        lw = lwnorm*lwcritDF['Dioecious'][r]
        print('Dioecious',r,lw)
        lamda = 0
        Ext = 1
        while Ext == 1 : 
            lamda  = lamda + 1
            pool = mp.Pool(mp.cpu_count()-2)
            results = pool.starmap(Dioecious, [(r,lw,lamda) for rep in range(NoR)])
            pool.close()
            pool.join()
            Ext = min(results)
        lamda = lamda - 1
        Ext = 1
        while Ext == 1 : 
            lamda  = lamda + 0.1
            pool = mp.Pool(mp.cpu_count()-2)
            results = pool.starmap(Dioecious, [(r,lw,lamda) for rep in range(NoR)])
            pool.close()
            pool.join()
            Ext = min(results)
        lamda = lamda - 0.1
        Ext = 1
        while Ext == 1 : 
            lamda  = lamda + 0.01
            pool = mp.Pool(mp.cpu_count()-2)
            results = pool.starmap(Dioecious, [(r,lw,lamda) for rep in range(NoR)])
            pool.close()
            pool.join()
            Ext = min(results)
        Lamda_Cutoff_Un_row = Lamda_Cutoff_Un_row + [lamda]
    Lamda_Cutoff_Un = Lamda_Cutoff_Un + [Lamda_Cutoff_Un_row]
DF = pd.DataFrame(Lamda_Cutoff_Un, columns = lwnorm_rng , index = r_rng )
DF.to_excel(LCMwriter,sheet_name = 'Dioecious' )
LCMwriter.save()   
