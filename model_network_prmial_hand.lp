\ Model netflow
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  10 flow[Pencils,Detroit,Boston] + 20 flow[Pencils,Detroit,New_York]
   + 60 flow[Pencils,Detroit,Seattle] + 40 flow[Pencils,Denver,Boston]
   + 40 flow[Pencils,Denver,New_York] + 30 flow[Pencils,Denver,Seattle]
   + 20 flow[Pens,Detroit,Boston] + 20 flow[Pens,Detroit,New_York]
   + 80 flow[Pens,Detroit,Seattle] + 60 flow[Pens,Denver,Boston]
   + 70 flow[Pens,Denver,New_York] + 30 flow[Pens,Denver,Seattle]
Subject To
 node_demand[Pencils,Boston]: flow[Pencils,Detroit,Boston]
   + flow[Pencils,Denver,Boston] = 50
 node_demand[Pencils,New_York]: flow[Pencils,Detroit,New_York]
   + flow[Pencils,Denver,New_York] = 50
 node_demand[Pencils,Seattle]: flow[Pencils,Detroit,Seattle]
   + flow[Pencils,Denver,Seattle] = 10
 node_demand[Pens,Boston]: flow[Pens,Detroit,Boston]
   + flow[Pens,Denver,Boston] = 40
 node_demand[Pens,New_York]: flow[Pens,Detroit,New_York]
   + flow[Pens,Denver,New_York] = 30
 node_demand[Pens,Seattle]: flow[Pens,Detroit,Seattle]
   + flow[Pens,Denver,Seattle] = 30
 node_supply[Pencils,Detroit]: flow[Pencils,Detroit,Boston]
   + flow[Pencils,Detroit,New_York] + flow[Pencils,Detroit,Seattle] = 50
 node_supply[Pencils,Denver]: flow[Pencils,Denver,Boston]
   + flow[Pencils,Denver,New_York] + flow[Pencils,Denver,Seattle] = 60
 node_supply[Pens,Detroit]: flow[Pens,Detroit,Boston]
   + flow[Pens,Detroit,New_York] + flow[Pens,Detroit,Seattle] = 60
 node_supply[Pens,Denver]: flow[Pens,Denver,Boston]
   + flow[Pens,Denver,New_York] + flow[Pens,Denver,Seattle] = 40
 cap[Detroit,Boston]: flow[Pencils,Detroit,Boston]
   + flow[Pens,Detroit,Boston] <= 100
 cap[Detroit,New_York]: flow[Pencils,Detroit,New_York]
   + flow[Pens,Detroit,New_York] <= 80
 cap[Detroit,Seattle]: flow[Pencils,Detroit,Seattle]
   + flow[Pens,Detroit,Seattle] <= 120
 cap[Denver,Boston]: flow[Pencils,Denver,Boston] + flow[Pens,Denver,Boston]
   <= 120
 cap[Denver,New_York]: flow[Pencils,Denver,New_York]
   + flow[Pens,Denver,New_York] <= 120
 cap[Denver,Seattle]: flow[Pencils,Denver,Seattle]
   + flow[Pens,Denver,Seattle] <= 120
Bounds
End
