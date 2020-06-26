import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation
import argparse
import time

#degree function
def u(t):
    return 1 if t >= 0 else 0

def Vs(t, s):
    #s == 1 => pulse
    #else => degree
    return u(t)-u(t-((K*dz)/(10*Uf))) if s == 1 else 2*u(t)

#update animation    
def update(n):
    line[0].set_ydata(i[n])
    line[1].set_ydata(v[n])
    return line

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s","--source", default = int(0), help = "mode of source")
ap.add_argument("-c","--charge", default = int(100), help = "impedancy of charge")
ap.add_argument("-k", "--K", default = int(500), help = "number of iterations in z")
ap.add_argument("-r", "--reflections", default = int(10), help = "number of reflections")
args = vars(ap.parse_args())


#Constants
Uf = 2.7e8
Z0 = 50
L = Z0/Uf
C = 1/(Z0*Uf)
Rs = 75

#Variables
Rl = int(args["charge"])
s = int(args["source"])
dz = 1e-3
r = 0.5
dt = r*(dz/Uf)
K = int(args["K"])
N = int((int(args["reflections"])*K)/r) 
#Total = N/dt

#Arrays
v = np.zeros((N,K))
i = np.zeros((N,K-1))
z = np.array(range(K-1))*dz
#t = np.array(range(N))*dt

#beta_1
b1 = (2*dt)/(Rs*C*dz)

flag_short = False
#Theorical Vinf
if Rl < 0:
    Vinf = Vs(N*dt,s)
else:
    Vinf = (Rl*Vs(N*dt,s))/(Rs+Rl)

#Open circuit
b2 = 0
Iinf = 0
flag_open = True

if Rl == 0:
    #Short circuit
    b2 = math.inf
    Iinf = Vs(N*dt,s)/Rs
    flag_short = True
elif Rl > 0:
    #Charge
    b2 = (2*dt)/(Rl*C*dz)
    Iinf = Vinf/Rl
    flag_open = False

r = (dt**2)/(L*C*(dz**2))

print("[INFO] (N,K) = ", (N,K))
print("[INFO] (b1,b2,r) = ", (b1, b2, r))
print("[INFO] Theorical (Vinf,Iinf) = ", (Vinf, Iinf))
print("[INFO] Starting processing...")

ini = time.time()

#Initial conditions
i[0, 0] = Vs(0, s)/(Rs+Z0)
v[0, 0] = Z0*i[0,0]
v[0,0] *= (C*dz)/dt

#Max values
max_v = v[0,0]
max_i = i[0,0]

#Main loop
for n in range(1, N):
    #Source border condition
    v[n, 0] = (1-b1)*v[n-1, 0] - 2*i[n-1, 0] + ((2*Vs((n-1)*dt, s))/Rs)
    #Voltage loop
    for k in range(1, K-1):
        v[n, k] = v[n-1, k] - (i[n-1, k] - i[n-1, k-1])
    #Charge border condition
    if flag_short:
        v[n, K-1] = 0
    else:
        v[n, K-1] = (1-b2)*v[n-1, K-1] + 2*i[n-1, K-2]
    #Current loop
    for k in range(K-1):
        i[n, k] = i[n-1, k] - r*(v[n, k+1] - v[n, k])
    if max(v[n], key=abs) > max_v:
        max_v = max(v[n], key=abs)
    if max(i[n], key=abs) > max_i:
        max_i = max(i[n], key=abs)

v *= dt/(C*dz)
max_v *= dt/(C*dz)

fim = time.time() - ini

print("[INFO] End of processing...")
print("[INFO] Time spend = ", fim)
print("[INFO] Results (Vinf, Iinf) = ", (np.mean(v[N-1]), np.mean(i[N-1])))
print("[INFO] Max values: (V, I) = ", (max_v, max_i))

fig, (ax1, ax2) = plt.subplots(2)
#Plotting current
line1,    = ax1.plot(z, i[0], color='r', label='Current (i) [A]')
#line1,    = ax1.plot(t, [x[0] for x in i], color='r', label='Current (i) [A]')
ax1.set_ylim(-max_i, max_i)
ax1.legend()
ax1.grid(True)

#Plotting voltage
z = np.append(z, [(K-1)*dz])
line2,    = ax2.plot(z, v[0], color='b', label='Voltage (v) [V]')
#line2,    = ax2.plot(t, [x[0] for x in v], color='b', label='Voltage (v) [V]')
ax2.set_ylim(-max_v, max_v)
ax2.legend()
ax2.grid(True)

line = (line1, line2)
plt.xlabel('Distance (z) [m]')
#plt.xlabel('Time (t) [s]')

ani = animation.FuncAnimation(fig, update, np.array(range(N)), interval = 1, blit = True, repeat = False)

plt.show()