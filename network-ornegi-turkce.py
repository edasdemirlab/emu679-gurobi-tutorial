# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 21:27:17 2023

@author: erdidasdemir
"""
# adopted from https://www.gurobi.com/documentation/current/examples/netflow_py.html


import gurobipy as gp
from gurobipy import GRB

# Sabit verilerin tanımlanması
commodities = ['Pencils', 'Pens'] # ürün seti listesi
supply_nodes = nodes = ['Detroit', 'Denver'] # şehir listesi
demand_nodes = nodes = ['Boston', 'New York', 'Seattle'] # şehir listesi

# bağlantı ürün başına gönderim maliyeti -->  dict olarak tanimliyoruz, key'ler tuple
cost = {
    ('Pencils', 'Detroit', 'Boston'):   10,
    ('Pencils', 'Detroit', 'New York'): 20,
    ('Pencils', 'Detroit', 'Seattle'):  60,
    ('Pencils', 'Denver',  'Boston'):   40,
    ('Pencils', 'Denver',  'New York'): 40,
    ('Pencils', 'Denver',  'Seattle'):  30,
    ('Pens',    'Detroit', 'Boston'):   20,
    ('Pens',    'Detroit', 'New York'): 20,
    ('Pens',    'Detroit', 'Seattle'):  80,
    ('Pens',    'Denver',  'Boston'):   60,
    ('Pens',    'Denver',  'New York'): 70,
    ('Pens',    'Denver',  'Seattle'):  30}



# bağlantı kapasiteleri --> multi dict olarak tanimlayalim
# arcs-- key'leri tutan bir tuple list, capacity-- degeleri tutan bir tupledict olacak

arcs, capacity = gp.multidict({ 
    ('Detroit', 'Boston'):   100,
    ('Detroit', 'New York'):  80,
    ('Detroit', 'Seattle'):  120,
    ('Denver',  'Boston'):   120,
    ('Denver',  'New York'): 120,
    ('Denver',  'Seattle'):  120})


# Şehirlerin talep ve arzları. Negatif değerler talebe, pozitif değerler arza sahip olduklarını gösterir.
# örneğin, detroit'te pencils değerinin 50 olması 50'lik bir talebi gösterir.
# Boston'da ise Pencils -50'dir, bu Boston'un 50 tane pencils arzına sahip olduğunu gösterir.
# inflow dictionary'sini tanimlayalim, key'ler tuple olacak.
demand = {
    ('Pencils', 'Boston'):   50,
    ('Pencils', 'New York'): 50,
    ('Pencils', 'Seattle'):  10,
    ('Pens',    'Boston'):   40,
    ('Pens',    'New York'): 30,
    ('Pens',    'Seattle'):  30}

supply = {
    ('Pencils', 'Detroit'):   50,
    ('Pencils', 'Denver'):    60,
    ('Pens',    'Detroit'):   60,
    ('Pens',    'Denver'):    40}



# Modeli yaratalım
m = gp.Model('netflow')

# Değişkenleri modele ekleyelim
flow = m.addVars(commodities, arcs, obj=cost, name="flow")


# kisitlari ekleyelim

# kisit 1: 
# arz ve talep denge kisitlari, akis-denge (flow balance) kisitlari

# demand esitligi
m.addConstrs(
    (flow.sum(h, '*', j) == demand[h, j] for h in commodities for j in demand_nodes), "node_demand")

# arz esitlikleri
m.addConstrs((flow.sum(h, i, '*') == supply[h, i] for h in commodities for i in supply_nodes), "node_supply")
 

# Arc-capacity constraints
m.addConstrs((flow.sum('*', i, j) <= capacity[i, j] for i, j in arcs), "cap")


# Compute optimal solution
m.optimize()

# Print solution
if m.Status == GRB.OPTIMAL:
    solution = m.getAttr('X', flow)
    for h in commodities:
        print('\nOptimal flows for %s:' % h)
        for i, j in arcs:
            if solution[h, i, j] > 0:
                print('%s -> %s: %g' % (i, j, solution[h, i, j]))