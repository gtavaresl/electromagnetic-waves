import numpy as np
import math
import matplotlib.pyplot as plt

um = lambda t: 1 if t >= 0 else 0
v = lambda n, S: um(n) - um(n-(40/S))
gauss = lambda n, S: math.exp(-((n*S-40)**2)/200)

def FDTD(S, I, N, s):
    u = np.zeros((N,I))

    u[0, 0] = s(0, S(0))
    for n in range(1, N):
        u[n, 0] = s(n, S(0))
        for i in range(1, I-1):
            u[n, i] = (S(i)**2)*(u[n-1, i+1] - 2*u[n-1, i] + u[n-1, i-1]) + 2*u[n-1, i] - u[n-2, i]

    return u

def fig_2_3_4(S0, s):
    S = lambda i: S0
    I = 200
    N = int(I/S0)

    u = FDTD(S, I, N, s)

    label = 'S = ' + str(S0)
    plt.plot(np.array(range(I)), u[int(190/S0)], label = label)
    plt.ylim(-0.2, 1.2)
    plt.legend()

def fig_2_5():
    S = lambda i: 1 if i < 140 else 0.25
    I = 200
    N = 400

    u = FDTD(S, I, N, gauss)

    plt.plot(np.array(range(I)), u[250])
    plt.axvline(x = 140, color = 'r', linestyle = '--')
    plt.ylim(-0.8, 0.6)
    plt.xlim(0, 200)

def fig_2_6():
    S = lambda i: 1.0005
    I = 220
    N = 400
    s = lambda n, S: math.exp(-((n-60)**2)/(2*(10**2)))

    u = FDTD(S, I, N, s)

    fig, (ax1, ax2) = plt.subplots(2)

    # fig 2.6 (a)
    ax1.plot(np.array(range(I)), u[200], 'r', label = 'n = 200')
    ax1.plot(np.array(range(I)), u[210], 'b-', label = 'n = 210')
    ax1.plot(np.array(range(I)), u[220], 'b--', label = 'n = 220')
    
    # fig 2.6 (b)
    ax2.plot(np.array(range(20)), u[200][:20], 'r', label = 'n = 200')
    ax2.plot(np.array(range(20)), u[210][:20], 'b-', label = 'n = 210')
    ax2.plot(np.array(range(20)), u[220][:20], 'b--', label = 'n = 220')

    #plt.legend()

def fig_2_7():
    S = lambda i: 1 if i != 90 else 1.075
    I = 220
    N = 300
    #precisa consertar essa fonte
    s = lambda n, S: math.exp(-((n-60)**2)/100)

    u = FDTD(S, I, N, s)

    fig, (ax1, ax2) = plt.subplots(2)

    # fig 2.7 (a)
    ax1.plot(np.array(range(I)), u[190], 'r', label = 'n = 190')
    ax1.plot(np.array(range(I)), u[200], 'b-', label = 'n = 200')
    
    # fig 2.7 (b)
    ax2.plot(np.array(range(40)) + 70, u[190][70:110], 'r', label = 'n = 200')
    ax2.plot(np.array(range(40)) + 70, u[200][70:110], 'b-', label = 'n = 210')
    
    #plt.legend()
    

#fig_2_3_4(1, gauss)
#fig_2_3_4(0.5, gauss)
#fig_2_5()
#fig_2_6()
#fig_2_7()
plt.ylabel('Wavefunction u(i)')
plt.xlabel('Grid i coordinate')
plt.show()