import random as rd

f1=open('data.txt','w')

for i in range(1,10000):
  a=rd.uniform(-10,1)
  b=rd.uniform(-100,100)
  c=rd.uniform(-200,100)
  deta=b*b-4*a*c
  while deta<0:
      a=rd.uniform(-10,1)
      b=rd.uniform(-100,100)
      c=rd.uniform(-200,100)
      deta=b*b-4*a*c
  f1.write('%f %f %f\n' %(a,b,c))
  
