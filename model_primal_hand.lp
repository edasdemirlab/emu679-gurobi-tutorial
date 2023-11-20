\ Model orman_tahsis
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  503 x_ij[1,1] + 140 x_ij[1,2] + 203 x_ij[1,3] + 675 x_ij[2,1]
   + 100 x_ij[2,2] + 45 x_ij[2,3] + 630 x_ij[3,1] + 105 x_ij[3,2]
   + 40 x_ij[3,3] + 330 x_ij[4,1] + 40 x_ij[4,2] + 295 x_ij[4,3]
   + 105 x_ij[5,1] + 460 x_ij[5,2] + 120 x_ij[5,3] + 490 x_ij[6,1]
   + 55 x_ij[6,2] + 180 x_ij[6,3] + 705 x_ij[7,1] + 60 x_ij[7,2]
   + 400 x_ij[7,3]
Subject To
 alan_tahsis_kisiti: x_ij[1,1] + x_ij[1,2] + x_ij[1,3] = 75
 alan_tahsis_kisiti: x_ij[2,1] + x_ij[2,2] + x_ij[2,3] = 90
 alan_tahsis_kisiti: x_ij[3,1] + x_ij[3,2] + x_ij[3,3] = 140
 alan_tahsis_kisiti: x_ij[4,1] + x_ij[4,2] + x_ij[4,3] = 60
 alan_tahsis_kisiti: x_ij[5,1] + x_ij[5,2] + x_ij[5,3] = 212
 alan_tahsis_kisiti: x_ij[6,1] + x_ij[6,2] + x_ij[6,3] = 98
 alan_tahsis_kisiti: x_ij[7,1] + x_ij[7,2] + x_ij[7,3] = 113
 kereste_kisiti: 310 x_ij[1,1] + 50 x_ij[1,2] + 198 x_ij[2,1]
   + 46 x_ij[2,2] + 210 x_ij[3,1] + 57 x_ij[3,2] + 112 x_ij[4,1]
   + 30 x_ij[4,2] + 40 x_ij[5,1] + 32 x_ij[5,2] + 105 x_ij[6,1]
   + 25 x_ij[6,2] + 213 x_ij[7,1] + 40 x_ij[7,2] >= 40000
 otlatma_kisiti: 0.01 x_ij[1,1] + 0.04 x_ij[1,2] + 0.03 x_ij[2,1]
   + 0.06 x_ij[2,2] + 0.04 x_ij[3,1] + 0.07 x_ij[3,2] + 0.01 x_ij[4,1]
   + 0.02 x_ij[4,2] + 0.05 x_ij[5,1] + 0.08 x_ij[5,2] + 0.02 x_ij[6,1]
   + 0.03 x_ij[6,2] + 0.02 x_ij[7,1] + 0.04 x_ij[7,2] >= 5
 yaban_endeksi_kisiti: 0.050761421319797 x_ij[1,1]
   + 0.1015228426395939 x_ij[1,2] + 0.1205583756345178 x_ij[1,3]
   + 0.0697969543147208 x_ij[2,1] + 0.0761421319796954 x_ij[2,2]
   + 0.08248730964467 x_ij[2,3] + 0.0571065989847716 x_ij[3,1]
   + 0.0697969543147208 x_ij[3,2] + 0.0761421319796954 x_ij[3,3]
   + 0.0380710659898477 x_ij[4,1] + 0.0444162436548223 x_ij[4,2]
   + 0.1142131979695431 x_ij[4,3] + 0.0761421319796954 x_ij[5,1]
   + 0.0761421319796954 x_ij[5,2] + 0.0888324873096447 x_ij[5,3]
   + 0.0444162436548223 x_ij[6,1] + 0.0634517766497462 x_ij[6,2]
   + 0.0951776649746193 x_ij[6,3] + 0.050761421319797 x_ij[7,1]
   + 0.0571065989847716 x_ij[7,2] + 0.1205583756345178 x_ij[7,3] >= 70
Bounds
End
