import numpy as np
import math
import matplotlib.pyplot as plt

um = lambda t: 1 if t >= 0 else 0
v = lambda n, S: um(n) - um(n-(40/S))
gauss = lambda n, S: math.exp(-((n*S-40)**2)/(2*(10**2)))


def FDTD(S, I, N, s):
    u = np.zeros((N,I))

    u[0, 0] = s(0, S)
    for n in range(1, N):
        u[n, 0] = s(n, S)
        for i in range(1, I-1):
            u[n, i] = (S**2)*(u[n-1, i+1] - 2*u[n-1, i] + u[n-1, i-1]) + 2*u[n-1, i] - u[n-2, i]

    return u



S = 1
I = 200
N = 200

s = gauss

u = FDTD(S, I, N, s)
label = 'S = ' + str(S)
plt.plot(np.array(range(I)), u[150], 'r--', label = label)

S = 0.5
N = int(N/S)

u = FDTD(S, I, N, s)
label = 'S = ' + str(S)
plt.plot(np.array(range(I)), u[int(150/S)], 'b', label = label)

plt.legend()
plt.show()