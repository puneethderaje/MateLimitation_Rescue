#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 00:14:04 2024

@author: puneeth
"""
from SexualSystems import *
import numpy as np
import multiprocessing as mp 
import pandas as pd 


""" 1 - Lamda_Critical for Wildtype, No Selfing, All 3 Models """ 
r_rng = [round(x,5) for x in np.arange(0.00002,0.0012,0.00002 )]
NoR = 1000
writer = pd.ExcelWriter('LamdaCritical_CM_MRp-4.xlsx')
Lamda_Cutoff_Uni = []
mp_cpu = mp.cpu_count() - 2
print('Uni')
for r in r_rng : 
    print(r,flush=True)
    lamda = 0
    Ext = 1
    while Ext == 1 : 
        lamda  = lamda + 100
        pool = mp.Pool(mp_cpu)
        results = pool.starmap(Dioecious, [(r,lamda,lamda) for rep in range(NoR)])
        pool.close()
        pool.join()
        Ext = min(results)
    lamda = lamda - 100
    Ext = 1 
    while Ext == 1 : 
        lamda  = lamda + 1
        pool = mp.Pool(mp_cpu)
        results = pool.starmap(Dioecious, [(r,lamda,lamda) for rep in range(NoR)])
        pool.close()
        pool.join()
        Ext = min(results)
    lamda = lamda - 1
    Ext = 1
    while Ext == 1 : 
        lamda  = lamda + 0.1
        pool = mp.Pool(mp_cpu)
        results = pool.starmap(Dioecious, [(r,lamda,lamda) for rep in range(NoR)])
        pool.close()
        pool.join()
        Ext = min(results)
    lamda = lamda - 0.1
    Ext = 1
    while Ext == 1 :
        lamda  = lamda + 0.01
        pool = mp.Pool(mp_cpu)
        results = pool.starmap(Dioecious, [(r,lamda,lamda) for rep in range(NoR)])
        pool.close()
        pool.join()
        Ext = min(results)
    Lamda_Cutoff_Uni = Lamda_Cutoff_Uni + [lamda]

print('Bi')
Lamda_Cutoff_Bi = []
for r in r_rng : 
    print(r)
    lamda = 0
    Ext = 1
    while Ext == 1 : 
        lamda  = lamda + 1
        pool = mp.Pool(mp_cpu)
        results = pool.starmap(Hermaphroditic, [(r,lamda,lamda) for rep in range(NoR)])
        pool.close()
        pool.join()
        Ext = min(results)
    lamda = lamda - 1
    Ext = 1
    while Ext == 1 : 
        lamda  = lamda + 0.1
        pool = mp.Pool(mp_cpu)
        results = pool.starmap(Hermaphroditic, [(r,lamda,lamda) for rep in range(NoR)])
        pool.close()
        pool.join()
        Ext = min(results)
    lamda = lamda - 0.1
    Ext = 1
    while Ext == 1 : 
        lamda  = lamda + 0.01
        pool = mp.Pool(mp_cpu)
        results = pool.starmap(Hermaphroditic, [(r,lamda,lamda) for rep in range(NoR)])
        pool.close()
        pool.join()
        Ext = min(results)
    Lamda_Cutoff_Bi = Lamda_Cutoff_Bi + [lamda]
    

print('An')
Lamda_Cutoff_An = []
for r in r_rng : 
    print(r)
    lamda = 0
    Ext = 1
    while Ext == 1 : 
        lamda  = lamda + 1
        pool = mp.Pool(mp_cpu)
        results = pool.starmap(Androdioecious, [(r,lamda,lamda) for rep in range(NoR)])
        pool.close()
        pool.join()
        Ext = min(results)
    lamda = lamda - 1
    Ext = 1
    while Ext == 1 :
        lamda  = lamda + 0.1
        pool = mp.Pool(mp_cpu)
        results = pool.starmap(Androdioecious, [(r,lamda,lamda) for rep in range(NoR)])
        pool.close()
        pool.join()
        Ext = min(results)
    lamda = lamda - 0.1
    Ext = 1
    while Ext == 1 :
        lamda  = lamda + 0.01
        pool = mp.Pool(mp_cpu)
        results = pool.starmap(Androdioecious, [(r,lamda,lamda) for rep in range(NoR)])
        pool.close()
        pool.join()
        Ext = min(results)
    Lamda_Cutoff_An = Lamda_Cutoff_An + [lamda]
    
DF = pd.DataFrame([Lamda_Cutoff_Uni,Lamda_Cutoff_Bi,Lamda_Cutoff_An],columns = r_rng,index = ['Dioecious','Hermaphroditic','Androdioecious'] )
DF = DF.transpose()
DF.to_excel(writer,sheet_name = 'Lamda_Cutoff_r' )
writer.save()

r = 0.0001
N0_rng = [int(10**x) for x in np.arange(1,5,0.2)]
NoR = 1000
#writer = pd.ExcelWriter('LamdaCritical_CM_PS_MRp-4.xlsx')
Lamda_Cutoff_Uni = []
mp_cpu = mp.cpu_count() - 2
print('Uni')
for N0 in N0_rng : 
    print(N0,flush=True)
    lamda = 0
    Ext = 1
    while Ext == 1 : 
        lamda  = lamda + 100
        pool = mp.Pool(mp_cpu)
        results = pool.starmap(Dioecious, [(r,lamda,lamda,N0) for rep in range(NoR)])
        pool.close()
        pool.join()
        #Ext = np.mean([results[i][0] for i in range(len(results)) ])
        Ext = min(results)
    lamda = lamda - 100
    Ext = 1 
    while Ext == 1 : 
        lamda  = lamda + 1
        pool = mp.Pool(mp_cpu)
        results = pool.starmap(Dioecious, [(r,lamda,lamda,N0) for rep in range(NoR)])
        pool.close()
        pool.join()
        # Ext = np.mean([results[i][0] for i in range(len(results)) ])
        Ext = min(results)
    lamda = lamda - 1
    Ext = 1
    while Ext == 1 : 
        lamda  = lamda + 0.1
        pool = mp.Pool(mp_cpu)
        results = pool.starmap(Dioecious, [(r,lamda,lamda,N0) for rep in range(NoR)])
        pool.close()
        pool.join()
        # Ext = np.mean([results[i][0] for i in range(len(results)) ])
        Ext = min(results)
    lamda = lamda - 0.1
    Ext = 1
    while Ext == 1 :
        lamda  = lamda + 0.01
        pool = mp.Pool(mp_cpu)
        results = pool.starmap(Dioecious, [(r,lamda,lamda,N0) for rep in range(NoR)])
        pool.close()
        pool.join()
        # Ext = np.mean([results[i][0] for i in range(len(results)) ])
        Ext = min(results)
    Lamda_Cutoff_Uni = Lamda_Cutoff_Uni + [lamda]
    print(lamda)

print('Bi')
Lamda_Cutoff_Bi = []
for N0 in N0_rng : 
    print(N0,flush=True)
    lamda = 0
    Ext = 1
    while Ext == 1 : 
        lamda  = lamda + 1
        pool = mp.Pool(mp_cpu)
        results = pool.starmap(Hermaphroditic, [(r,lamda,lamda,N0) for rep in range(NoR)])
        pool.close()
        pool.join()
        # Ext = np.mean([results[i][0] for i in range(len(results)) ])
        Ext = min(results)
    lamda = lamda - 1
    Ext = 1
    while Ext == 1 : 
        lamda  = lamda + 0.1
        pool = mp.Pool(mp_cpu)
        results = pool.starmap(Hermaphroditic, [(r,lamda,lamda,N0) for rep in range(NoR)])
        pool.close()
        pool.join()
        # Ext = np.mean([results[i][0] for i in range(len(results)) ])
        Ext = min(results)
    lamda = lamda - 0.1
    Ext = 1
    while Ext == 1 : 
        lamda  = lamda + 0.01
        pool = mp.Pool(mp_cpu)
        results = pool.starmap(Hermaphroditic, [(r,lamda,lamda,N0) for rep in range(NoR)])
        pool.close()
        pool.join()
        # Ext = np.mean([results[i][0] for i in range(len(results)) ])
        Ext = min(results)
    Lamda_Cutoff_Bi = Lamda_Cutoff_Bi + [lamda]
    print(lamda)
    

print('An')
Lamda_Cutoff_An = []
for N0 in N0_rng : 
    print(N0,flush=True)
    lamda = 0
    Ext = 1
    while Ext == 1 : 
        lamda  = lamda + 1
        pool = mp.Pool(mp_cpu)
        results = pool.starmap(Androdioecious, [(r,lamda,lamda,N0) for rep in range(NoR)])
        pool.close()
        pool.join()
        # Ext = np.mean([results[i][0] for i in range(len(results)) ])
        Ext = min(results)
    lamda = lamda - 1
    Ext = 1
    while Ext == 1 :
        lamda  = lamda + 0.1
        pool = mp.Pool(mp_cpu)
        results = pool.starmap(Androdioecious, [(r,lamda,lamda,N0) for rep in range(NoR)])
        pool.close()
        pool.join()
        # Ext = np.mean([results[i][0] for i in range(len(results)) ])
        Ext = min(results)
    lamda = lamda - 0.1
    Ext = 1
    while Ext == 1 :
        lamda  = lamda + 0.01
        pool = mp.Pool(mp_cpu)
        results = pool.starmap(Androdioecious, [(r,lamda,lamda,N0) for rep in range(NoR)])
        pool.close()
        pool.join()
        # Ext = np.mean([results[i][0] for i in range(len(results)) ])
        Ext = min(results)
    Lamda_Cutoff_An = Lamda_Cutoff_An + [lamda]
    print(lamda)
    
DF = pd.DataFrame([Lamda_Cutoff_Uni,Lamda_Cutoff_Bi,Lamda_Cutoff_An],columns = N0_rng,index = ['Dioecious','Hermaphroditic','Androdioecious'] )
DF = DF.transpose()
DF.to_excel(writer,sheet_name = 'Lamda_Cutoff_N0' )
writer.save()
