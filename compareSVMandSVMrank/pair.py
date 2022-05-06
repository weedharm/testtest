import numpy as np

def pair(x, y):
   x2 = []
   y2 = []
   
   for i in range(len(x)):
      for k in range(len(x)):
         if i==k or y[i]==y[k] :
            continue
         x2.append(x[i]-x[k])
         y2.append(np.sign(y[i]-y[k]))
   
   return np.asarray(x2), np.asarray(y2)