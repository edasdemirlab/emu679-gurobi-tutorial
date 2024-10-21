# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 23:12:48 2023

@author: erdidasdemir
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 21:27:17 2023

@author: erdidasdemir
"""
# adopted from https://www.gurobi.com/documentation/current/examples/netflow_py.html


import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import os

# dosya isimlerini tanimlayalim
# girdi dosyalari model_inputs--> network klasoru icerisinde oldugu icin os.path.join fonksiyonuyla dosyalarin konumunu da ekliyorum.
commodities_file = os.path.join('model_inputs','network', 'commodities.csv')
nodes_file = os.path.join('model_inputs','network', 'nodes.csv')
cost_file = os.path.join('model_inputs','network', 'arc_cost.csv')
capacity_file = os.path.join('model_inputs', 'network','arc_capacity.csv')
demand_file = os.path.join('model_inputs', 'network','node_demand.csv')
supply_file = os.path.join('model_inputs', 'network','node_supply.csv')

# dosyalari okuyalim
commodities_df = pd.read_csv(commodities_file)
nodes_df =  pd.read_csv(nodes_file)
cost_df = pd.read_csv(cost_file)
capacity_df = pd.read_csv(capacity_file)
demand_df = pd.read_csv(demand_file)
supply_df = pd.read_csv(supply_file)


# Sabit verilerin tanımlanması
commodities = commodities_df["commodity"].tolist() # ['Pencils', 'Pens'] # ürün seti listesi
supply_nodes = nodes_df.query('type == "supply"')["node"].tolist()  # arz eden şehirler
demand_nodes =  nodes_df.query('type == "demand"')["node"].tolist() # talep eden şehirler


# cost dictionary olusturalim
# bağlantı ürün başına gönderim maliyeti -->  dict olarak tanimliyoruz, key'ler tuple
cost = cost_df.set_index(['commodity', 'from', 'to'])['cost'].to_dict()

# alternatif yol
# =============================================================================
# cost = {}
# for i in range(len(cost_df)):
#     row = cost_df.loc[i, :]
#     cost[row["commodity"], row["from"], row["to"]] = row["cost"]
# 
# =============================================================================


# =============================================================================
# cost = {
#     ('Pencils', 'Detroit', 'Boston'):   10,
#     ('Pencils', 'Detroit', 'New York'): 20,
#     ('Pencils', 'Detroit', 'Seattle'):  60,
#     ('Pencils', 'Denver',  'Boston'):   40,
#     ('Pencils', 'Denver',  'New York'): 40,
#     ('Pencils', 'Denver',  'Seattle'):  30,
#     ('Pens',    'Detroit', 'Boston'):   20,
#     ('Pens',    'Detroit', 'New York'): 20,
#     ('Pens',    'Detroit', 'Seattle'):  80,
#     ('Pens',    'Denver',  'Boston'):   60,
#     ('Pens',    'Denver',  'New York'): 70,
#     ('Pens',    'Denver',  'Seattle'):  30}
# =============================================================================


# bağlantı kapasiteleri --> multi dict olarak tanimlayalim
# arcs-- key'leri tutan bir tuple list, capacity-- degeleri tutan bir tupledict olacak
# arcs'lara model tanimlarken ihtiyacimiz olacagi icin multi dict tanimladik.

capacity_multidict = capacity_df.set_index(['from', 'to'])['capacity'].to_dict()
# alternatif yol
# =============================================================================
# capacity_multidict = {}
# for i in range(len(capacity_df)):
#     row = capacity_df.loc[i, :]
#     capacity_multidict[row["from"], row["to"]] = row["capacity"]
#     
# =============================================================================


arcs, capacity = gp.multidict(capacity_multidict)

# =============================================================================
# arcs, capacity = gp.multidict({ 
#     ('Detroit', 'Boston'):   100,
#     ('Detroit', 'New York'):  80,
#     ('Detroit', 'Seattle'):  120,
#     ('Denver',  'Boston'):   120,
#     ('Denver',  'New York'): 120,
#     ('Denver',  'Seattle'):  120})
# 
# =============================================================================

# Şehirlerin talep ve arzları. Negatif değerler talebe, pozitif değerler arza sahip olduklarını gösterir.
# örneğin, detroit'te pencils değerinin 50 olması 50'lik bir talebi gösterir.
# Boston'da ise Pencils -50'dir, bu Boston'un 50 tane pencils arzına sahip olduğunu gösterir.
# inflow dictionary'sini tanimlayalim, key'ler tuple olacak.
demand = demand_df.set_index(['commodity', 'node'])['demand'].to_dict()

# alternatif yol
# =============================================================================
# demand = {}
# for i in range(len(demand_df)):
#     row = demand_df.loc[i, :]
#     demand[row["commodity"], row["node"]] = row["demand"]
# 
# =============================================================================

supply = supply_df.set_index(['commodity', 'node'])['supply'].to_dict()

# alternatif yol
# =============================================================================
# supply = {}
# for i in range(len(supply_df)):
#     row = supply_df.loc[i, :]
#     supply[row["commodity"], row["node"]] = row["supply"]
#     
# =============================================================================

# =============================================================================
# demand = {
#     ('Pencils', 'Boston'):   50,
#     ('Pencils', 'New York'): 50,
#     ('Pencils', 'Seattle'):  10,
#     ('Pens',    'Boston'):   40,
#     ('Pens',    'New York'): 30,
#     ('Pens',    'Seattle'):  30}
# 
# supply = {
#     ('Pencils', 'Detroit'):   50,
#     ('Pencils', 'Denver'):    60,
#     ('Pens',    'Detroit'):   60,
#     ('Pens',    'Denver'):    40}
# =============================================================================



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



# print model to a file
m.update()
m.write("model_network_prmial_hand.lp")
m.write("model_network_dual_hand.dlp")

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