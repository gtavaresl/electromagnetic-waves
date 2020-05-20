import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import argparse
import time

def u(t):
    return 1 if t >= 0 else 0

def Vs(t):
    #return 2*u(t)
    return u(t)-u(t-((K*dz)/(10*Uf)))
    
def update(n):
    line[0].set_ydata(i[n])
    line[1].set_ydata(v[n])
    return line

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s","--source", default = int(0), help = "mode of source")
ap.add_argument("-c","--charge", default = int(100), help = "impedancy of charge")
ap.add_argument("-k", "--K", default = int(100), help = "number of iterations in z")
args = vars(ap.parse_args())

Uf = 2.7e8
Z0 = 50
Rs = 75
Rl = int(args["charge"])

L = Z0/Uf
C = 1/(Z0*Uf)

dz = 1e-3
dt = 0.8*(dz/Uf)
K = int(args["K"])
N = int((4*K*dz)/(Uf*dt)) 
Total = (10*K*dz)/Uf

v = np.zeros((N,K))
i = np.zeros((N,K-1))

z = np.array(range(K-1))*dz

b1 = (2*dt)/(Rs*C*dz)

flag_short = False
#Open circuit
b2 = 0
flag_open = True
if Rl == 0:
    #Short circuit
    b2 = math.inf
    flag_short = True
elif Rl > 0:
    #Charge
    b2 = (2*dt)/(Rl*C*dz)
    flag_open = False

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
    if flag_short:
        v[n, K-1] = 0
    else:
        v[n, K-1] = (1-b2)*v[n-1, K-1]
        if not flag_open:
            v[n, K-1] += 2*i[n-1, K-2]
    #Current loop
    for k in range(K-1):
        i[n, k] = i[n-1, k] - r*(v[n, k+1] - v[n, k])

v *= dt/(C*dz)

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

fig, (ax1, ax2) = plt.subplots(2)
line1,    = ax1.plot(z, i[0], color='r', label='Current [A]')
ax1.set_ylim(-0.025, 0.025)
ax1.grid(True)


z = np.append(z, [(K-1)*dz])
line2,    = ax2.plot(z, v[0], color='b', label='Voltage [V]')
ax2.set_ylim(-1, 1)
ax2.grid(True)


line = (line1, line2)


ani = FuncAnimation(fig, update, np.array(range(N)), interval = 20, blit = True)

plt.show()