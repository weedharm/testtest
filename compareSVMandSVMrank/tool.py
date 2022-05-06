import numpy as np

def sort(s):
   r=[]
   for i in range(len(s)):
      if s[i]>0 :
         r.append(1)
      else:
         r.append(0)
   r=np.asarray(r)
   return r