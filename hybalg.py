# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 11:03:56 2020

@author: ma076216
"""
import math
import random
demand_points_rnd = random.sample(range(1,19835),500)
demand_levels =[]
for i in range (len(demand_points_rnd)):
    
    demand_levels.append(random.randint(1,100))

demand_set = list(zip(demand_points_rnd,demand_levels))

number_clusters = 5
capacity = 100
from clusalg import *


clusters_f = findCluster(demand_points_rnd, demand_levels, number_clusters, .5)
clusters_list = []
for i in range (number_clusters):
    clusters_list.append(clusters_f[0][i]['dps']) 
    
total_demand_clusters = []
number_modules = []
utilization = []
for i in range (number_clusters):
    demand_sum = 0
    
    j=0
    for j in range(len(clusters_list[i])):
       
        demand_sum = demand_sum+clusters_list[i][j][1]
    
    total_demand_clusters.append(demand_sum)
    number_modules.append(demand_sum/capacity)
    utilization.append (number_modules[i]- math.floor(number_modules[i]))

uti_sort = sorted(utilization,reverse=True)
sim_thrishold = 7000
i = 0
dedicated_mod = []
shared_mod = []
remainder_mod=[]

while len(uti_sort)>0:
    if uti_sort[i]== 1:
        dedicated_mod.append(utilization.index(uti_sort[i],0, number_clusters-1))
        uti_sort.pop(0)
        continue
    if uti_sort[i]>=0.50:
        uti_shared = uti_sort[i]
        sh_l = []
        sh_l.append(utilization.index(uti_sort[i])) # get index of module with utilization >0.5 store it in shl
        j=i+1
        while j in range (1,len(uti_sort)-1): # iterate through remainng elements to find shared modules 
            uti_shared = uti_shared + uti_sort[j]
            if uti_shared > 1: # if a combination is greater than 100 utilization do not combine them and move on
                uti_shared = uti_shared - uti_sort[j]
                j+=1
                continue
            sh_l.append(utilization.index(uti_sort[j])) # if two modules can be combined, do it and get their indecies
            uti_sort.pop(j) # reomve the item combined from sorted utilization list  
        if len(sh_l)>1: #if 2 or more modules combined add them to the shared modules list, otherwise to dedicated list
            shared_mod.append(sh_l)
            uti_sort.pop(i)
            continue
        else:
            dedicated_mod.append(sh_l)
            uti_sort.pop(i)
            continue
    if uti_sort[i]<0.50:
        remainder_mod.append(utilization.index(uti_sort[i]))
        uti_sort.pop(i)
    
         
        