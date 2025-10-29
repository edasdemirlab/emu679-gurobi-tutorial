\ Model netflow
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  10 x_hij[Pencils,Detroit,Boston] + 20 x_hij[Pencils,Detroit,New_York]
   + 60 x_hij[Pencils,Detroit,Seattle] + 40 x_hij[Pencils,Denver,Boston]
   + 40 x_hij[Pencils,Denver,New_York] + 30 x_hij[Pencils,Denver,Seattle]
   + 20 x_hij[Pens,Detroit,Boston] + 20 x_hij[Pens,Detroit,New_York]
   + 80 x_hij[Pens,Detroit,Seattle] + 60 x_hij[Pens,Denver,Boston]
   + 70 x_hij[Pens,Denver,New_York] + 30 x_hij[Pens,Denver,Seattle]
Subject To
 node_demand[Pencils,Boston]: x_hij[Pencils,Detroit,Boston]
   + x_hij[Pencils,Denver,Boston] = 50
 node_demand[Pencils,New_York]: x_hij[Pencils,Detroit,New_York]
   + x_hij[Pencils,Denver,New_York] = 50
 node_demand[Pencils,Seattle]: x_hij[Pencils,Detroit,Seattle]
   + x_hij[Pencils,Denver,Seattle] = 10
 node_demand[Pens,Boston]: x_hij[Pens,Detroit,Boston]
   + x_hij[Pens,Denver,Boston] = 40
 node_demand[Pens,New_York]: x_hij[Pens,Detroit,New_York]
   + x_hij[Pens,Denver,New_York] = 30
 node_demand[Pens,Seattle]: x_hij[Pens,Detroit,Seattle]
   + x_hij[Pens,Denver,Seattle] = 30
 node_supply[Pencils,Detroit]: x_hij[Pencils,Detroit,Boston]
   + x_hij[Pencils,Detroit,New_York] + x_hij[Pencils,Detroit,Seattle] = 50
 node_supply[Pencils,Denver]: x_hij[Pencils,Denver,Boston]
   + x_hij[Pencils,Denver,New_York] + x_hij[Pencils,Denver,Seattle] = 60
 node_supply[Pens,Detroit]: x_hij[Pens,Detroit,Boston]
   + x_hij[Pens,Detroit,New_York] + x_hij[Pens,Detroit,Seattle] = 60
 node_supply[Pens,Denver]: x_hij[Pens,Denver,Boston]
   + x_hij[Pens,Denver,New_York] + x_hij[Pens,Denver,Seattle] = 40
 cap[Detroit,Boston]: x_hij[Pencils,Detroit,Boston]
   + x_hij[Pens,Detroit,Boston] <= 100
 cap[Detroit,New_York]: x_hij[Pencils,Detroit,New_York]
   + x_hij[Pens,Detroit,New_York] <= 80
 cap[Detroit,Seattle]: x_hij[Pencils,Detroit,Seattle]
   + x_hij[Pens,Detroit,Seattle] <= 120
 cap[Denver,Boston]: x_hij[Pencils,Denver,Boston]
   + x_hij[Pens,Denver,Boston] <= 120
 cap[Denver,New_York]: x_hij[Pencils,Denver,New_York]
   + x_hij[Pens,Denver,New_York] <= 120
 cap[Denver,Seattle]: x_hij[Pencils,Denver,Seattle]
   + x_hij[Pens,Denver,Seattle] <= 120
Bounds
End
