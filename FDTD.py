import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

def u(t):
    return 1 if t >= 0 else 0

def Vs(t):
    #return 2*u(t)
    return u(t)-u(t-((K*dz)/(10*Uf)))
    
def update(n):
    ln.set_ydata(v[n])
    return ln,

Uf = 2.7e8
Z0 = 50
Rs = 75
Rl = 100

L = Z0/Uf
C = 1/(Z0*Uf)

dz = 1e-3
dt = 0.6*(dz/Uf)
K = 2000
N = int((4*K*dz)/(Uf*dt)) 
Total = (10*K*dz)/Uf

v = np.zeros((N,K))
i = np.zeros((N,K-1))

z = np.array(range(K))*dz

b1 = (2*dt)/(Rs*C*dz)
b2 = (2*dt)/(Rl*C*dz)
r = (dt**2)/(L*C*(dz**2))

ini = time.time()

#Initial conditions
v[0, 0] = (Z0*Vs(0))/(Rs+Z0)
i[0, 0] = Vs(0)/(Rs+Z0)

#Main loop
for n in range(1, N):
    #Source border condition
    v[n, 0] = (1-b1)*v[n-1, 0] - 2*i[n-1, 0] + ((2*Vs((n-1)*dt))/Rs)
    #Voltage loop
    for k in range(1, K-1):
        v[n, k] = v[n-1, k] - (i[n-1, k] - i[n-1, k-1])
    #Charge border condition
    v[n, K-1] = (1-b2)*v[n-1, K-1] + 2*i[n-1, K-2]
    #Current loop
    for k in range(K-1):
        i[n, k] = i[n-1, k] - r*(v[n, k+1] - v[n, k])

v = (dt*v)/(C*dz)

fim = time.time() - ini

print("K = ", K)
print("N = ", N)
print("Tempo de computacao = ", fim)
print("Tempo de simulacao = ", Total)

#Vinf = (Rl*Vs)/(Rs+Rl)
#print("Vinf = ", (Rl*Vs(N*dt))/(Rs+Rl))
#print(v[N-1])

#Iinf = 1/(Rs+Rl)
#print("Iinf = ", 1/(Rs+Rl))
#print(i[N-1])

fig, ax = plt.subplots()
ln,   = ax.plot(z, v[0])

ani = FuncAnimation(fig, update, np.array(range(N)), interval = 1,blit = True)

plt.grid(True)
plt.ylim(-2,2)
plt.show()