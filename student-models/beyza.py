#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 14:01:22 2023

@author: beyzauzun
"""

import gurobipy as gp
from gurobipy import GRB

#sabit verilerin tanımlanması (analiz alan ve reçetelerin tanımlanması)

receteler = ['a', 'b', 'c'] # reçete sayısı
analiz_alani =['1','2','3','4','5','6','7'] #analiz alani sayısı

# analiz alan boyutu -->  dict olarak tanimliyoruz, key'ler tuple (si)
s = {
    ('1'):   75,
    ('2'):   90,
    ('3'):   140,
    ('4'):   60,
    ('5'):   212,
    ('6'):   98,
    ('7'):   113}

#net değer akış tanımlama  -->  dict olarak tanimliyoruz, key'ler tuple  (pij)
p = {
    ('1', 'a'):   503, # 403 yazmışsın 503 olacak
    ('1', 'b'):   140,
    ('1', 'c'):   203,
    ('2', 'a'):   675,
    ('2', 'b'):   100,
    ('2', 'c'):   45,
    ('3', 'a'):   630,
    ('3', 'b'):   105,
    ('3', 'c'):   40,
    ('4', 'a'):   330,
    ('4','b'):   40,
    ('4','c'):   295,
    ('5','a'):   105,
    ('5','b'):   460,
    ('5','c'):   120,
    ('6','a'):   490,
    ('6','b'):   55,
    ('6','c'):   180,
    ('7','a'):   705,
    ('7','b'):   60,
    ('7','c'):   400}


#kereste verimi tanımlama  -->  dict olarak tanimliyoruz, key'ler tuple  (tij)
t = {
    ('1', 'a'):   310,
    ('1', 'b'):   50,
    ('1', 'c'):   0,
    ('2', 'a'):   198,
    ('2', 'b'):   46,
    ('2', 'c'):   0,
    ('3', 'a'):   210,
    ('3', 'b'):   57,
    ('3', 'c'):   0,
    ('4', 'a'):   112,
    ('4','b'):   30,
    ('4','c'):   0,
    ('5','a'):   40,
    ('5','b'):   32,
    ('5','c'):   0,
    ('6','a'):   105,
    ('6','b'):   25,
    ('6','c'):   0,
    ('7','a'):   213,
    ('7','b'):   40,
    ('7','c'):   0}


#otlatma kapasitesi tanımlama  -->  dict olarak tanimliyoruz, key'ler tuple  (gij)
g = {
    ('1', 'a'):   0.01,
    ('1', 'b'):   0.04,
    ('1', 'c'):   0,
    ('2', 'a'):   0.03,
    ('2', 'b'):   0.06,
    ('2', 'c'):   0,
    ('3', 'a'):   0.04,
    ('3', 'b'):   0.07,
    ('3', 'c'):   0,
    ('4', 'a'):   0.01,
    ('4','b'):   0.02,
    ('4','c'):   0,
    ('5','a'):   0.05,
    ('5','b'):   0.08,
    ('5','c'):   0,
    ('6','a'):   0.02,
    ('6','b'):   0.03,
    ('6','c'):   0,
    ('7','a'):   0.02,
    ('7','b'):   0.04,
    ('7','c'):   0}


#ovahşi doğa endeksi tanımlama  -->  dict olarak tanimliyoruz, key'ler tuple  (wij)
w = {
    ('1', 'a'):   40,
    ('1', 'b'):   80,
    ('1', 'c'):   95,
    ('2', 'a'):   55,
    ('2', 'b'):   60,
    ('2', 'c'):   65,
    ('3', 'a'):   45, # 55 yazmissin 45 olarak duzelttim
    ('3', 'b'):   55,
    ('3', 'c'):   60,
    ('4', 'a'):   30,
    ('4', 'b'):   35,
    ('4','c'):   90,
    ('5','a'):   60,
    ('5','b'):   60,
    ('5','c'):   70,
    ('6','a'):   35,
    ('6','b'):   50, # 35 yazmissin 50 olarak duzelttim
    ('6','c'):   75,
    ('7','a'):   40,
    ('7','b'):   45,
    ('7','c'):   95}

# Modeli yaratalım
model = gp.Model('x')

# Değişkenleri modele ekleyelim
x = model.addVars(analiz_alani, receteler, obj=p, vtype=GRB.CONTINUOUS, name="x")



# kisitlari ekleyelim

# kisit 1: analiz alan kısıtı si'ler için
 
# =============================================================================
# model.addConstrs(
#     (x.sum(i, '*') == s[i] for i in analiz_alani for j in receteler))
# =============================================================================

# erdi:   
model.addConstrs(
    (x.sum(i, '*') == s[i] for i in analiz_alani))


# kisit 2: kereste kapasite kısıtı tij'ler için
# =============================================================================
# model.addConstrs(
#     (x.sum('*', '*')* t[i,j]>= 40000000 for i in analiz_alani for j in receteler))
# =============================================================================

# erdi:  
model.addConstr(
    gp.quicksum(x[i, j]* t[i,j] for i in analiz_alani for j in receteler) >= 40000)


# kisit 3: otlatma kısıtı gij'ler için
# =============================================================================
# model.addConstrs(
#     (x.sum('*', '*')* g[i,j]>= 5 for i in analiz_alani for j in receteler))
# =============================================================================

# erdi:
model.addConstr(
    gp.quicksum(x[i, j]* g[i,j] for i in analiz_alani for j in receteler) >= 5)
    


# kisit 4: yaban endeksi kısıtı wij'ler için 
# =============================================================================
# model.addConstrs(
#     (x.sum('*', '*')* w[i,j]/788 >= 70 for i in analiz_alani for j in receteler))
# 
# =============================================================================

model.addConstr(
    gp.quicksum(x[i, j] * w[i,j] for i in analiz_alani for j in receteler)/788 >= 70)


# optimal çözümü bulalım 
model.ModelSense = -1  # default gurobi minimizasyon yapar, bu parametreyi -1 tanimlayarak amac fonksiyonunu maksimizasyona cevirebiliriz.
model.optimize()
# model.write("model_hand.lp")  # bunu yorumdan cikarip calistirirsan modeli acik lp olarak dosyanin bulundugu klasore yazar. onu not defteri ile acip manuel kontrol yapabilirsin.


solution = model.getAttr('X', x)
solution



