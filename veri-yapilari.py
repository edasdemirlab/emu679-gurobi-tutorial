# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 15:27:54 2023

@author: erdidasdemir
"""

import gurobipy as gp
from gurobipy import GRB


# Adopted from Tutorial: Getting Started with the Gurobi Python API using dictionaries
# https://support.gurobi.com/hc/en-us/articles/17307437899025-Tutorial-Getting-Started-with-the-Gurobi-Python-API-using-dictionaries

#1  Lists and Tuples
# list oluşturma örneği
l = [1, 2.0, "abc"] 
     
# tuple oluşturma örneği
t = (1, 2.0, "abc")

# l listesinin ilk ve üçüncü elemanlarını ekrana yazdırma
print(l[0]) 
print(l[2])

# t tuple'ının ilk elemanını ekrana yazdırma
print(t[1]) 

# Bir tuple değişmezdir, yani oluşturulduktan sonra değiştirilemez. 
# Buna karşılık, bir listeye eklemeler, değişiklikler ve çıkarmalar yapabilirsiniz. 
# Tuple’ların değişmeme özelliği onları dictionary’lerde dizin/endeks olarak kullanmanıza olanak tanır.


#2 Dictionaries
ders_kapasite = {}  # boş bir dictionary tanımlar
ders_kapasite['EMU679'] = 11 #EMU679 anahtarına 11 atar.
ders_kapasite['EMU430'] = 73 #EMU430 anahtarına 11 atar.

# Bu dictionary'i tek satırda da tanımlayabilirdik:
ders_kapasite = {'EMU679':11, 'EMU430':73}

#Dictonary elemanlarını ekrana şu şekilde yazdırabiliriz:
print(ders_kapasite)
print(ders_kapasite['EMU430'])
print(ders_kapasite['EMU679'])



# 3 Multidict
#Gurobi Python ara yüzü, matematiksel optimizasyon modellerinde sıklıkla ortaya çıkan bir durum için sözlük başlatmayı basitleştiren bir yardımcı veri yapısı olan Multidict’e sahiptir (gurobipy paketi ile gelir, düz Python’da yoktur).
#Multidict işlevi, bir veya daha fazla sözlüğü tek seferde tanımlamaya olanak tanır.  Her anahtarla ilişkili değer, 𝑛 uzunluğundaki bir listedir. Bu listeleri ayrı objelere bölünere 𝑛 ayrı sözlük oluşturulur. Fonksiyon bir liste döndürür. Bu listedeki ilk öğe, paylaşılan anahtar değerlerin listesi ve onu takip eden n ayrı sözlüktür. 

names, lower, upper = gp.multidict({ 'x': [0, 1], 'y': [1, 2], 'z': [0, 3]}) 

print(names) 
print(lower) 
print(upper) 


## 4 List Comprehension ve Generator
# List Comphrension ve Generator ifadaeleri, kısa ve öz bir şekilde örtülü numaralandırma yapmaya olanak tanıyan önemli Python özellikleridir. 
# Basit bir örnek vermek gerekirse aşağıdaki liste anlayışı 1'den 5'e kadar olan sayıların karelerini içeren bir liste oluşturur:

[x*x for x in [1, 2, 3, 4, 5]] # [1, 4, 9, 16, 25] 

sum(x*x for x in [1, 2, 3, 4, 5]) 


sum(x*x for x in range(1,6))
[(x,y) for x in range(4) for y in range(4) if x < y]
[(x,y) for x in range(4) for y in range(x+1, 4)]

## 5 Tuplelist
# Python liste sınıfının özel bir alt sınıfıdır.
# Bir tuple listesinden alt listeler oluşturmanıza olanak sağlar.
# Select yöntemiyle ilgili elemanları eşleşen tüm tuple'ları çağırmaya yarar.

l = gp.tuplelist([(1, 2), (1, 3), (2, 3), (2, 4)])
print(l.select(1, '*'))
print(l.select('*', 3))
print(l.select('*', [2, 4]))
print(l.select(1, 3))
print(l.select('*', '*'))



# 6 Tupledict
model = gp.Model('tupledict_ornek')
l = list([(1, 2), (1, 3), (2, 3), (2, 4)])
d = model.addVars(l, name="d")
model.update()




