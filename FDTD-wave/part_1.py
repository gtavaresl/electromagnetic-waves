import numpy as np
import math
import matplotlib.pyplot as plt

def f_tau(N, S):
    return 1+(1/(S**2))*(math.cos((2*math.pi*S)/N)-1)

n = 100
N = np.linspace(1, 10, num = n)
S = 1/2#math.sqrt(2)


Ntrans = (2*math.pi*S)/math.acos(1-2*(S**2))
print('Ntrans = ', Ntrans)
at = np.zeros(n)

Vp = np.zeros(n)


for i in range(n):
    if N[i] >= Ntrans:
        k = (math.acos(1+4*(math.cos(math.pi/N[i])-1)))
    else:
        k = math.pi
        tau = f_tau(N[i], S)
        at[i] = -math.log(-tau-math.sqrt((tau**2)-1))
    Vp[i] = (2*math.pi)/(N[i]*k)

# fig 2.1

fig, (ax1, ax2) = plt.subplots(2)

ax1.plot(N, Vp,'r', label = 'Numerical phase velocity')
ax3 = ax1.twinx()
ax3.plot(N, at, 'b--', label = 'Attenuation constant')

ax1.set_ylabel('Numerical Phase Velocity (nomalized to c)')
ax1.legend()

ax3.set_ylabel('Attenuation Constant (nepers/grid cell)')
ax3.set_ylim(0, 6)
ax3.legend()

ax1.axvline(x = Ntrans, color = 'g', linestyle = '--')




N = np.array(range(3,80))
Vp = np.zeros(np.size(N))

for i in range(np.size(N)):
    k = (math.acos(1+4*(math.cos(math.pi/N[i])-1)))
    Vp[i] = (2*math.pi)/(N[i]*k)

Vp = np.log10(100*(1-Vp))

# fig 2.2

ax2.plot(N, Vp, color='b')

plt.show()