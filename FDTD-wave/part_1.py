import numpy as np
import math
import matplotlib.pyplot as plt

def f_tau(N, S):
    return 1+(1/(S**2))*(math.cos((2*math.pi*S)/N)-1)

def Ntrans(S):
    return (2*math.pi*S)/math.acos(1-2*(S**2))

def theta(N):
    return 1+4*(math.cos(math.pi/N)-1)

# fig 2.1

def fig_2_1(S, n):
    print('[INFO] Ntrans = ', Ntrans(S))
    N = np.linspace(1, 10, num = n)
    at = np.zeros(n)
    Vp = np.zeros(n)
    for i in range(n):
        if  N[i] <= Ntrans(S):
            k = math.pi
            tau = f_tau(N[i], S)
            at[i] = -math.log(-tau-math.sqrt((tau**2)-1))
        else:
            k = math.acos(f_tau(N[i], S))
        Vp[i] = (2*math.pi)/(N[i]*k)

    fig, ax1 = plt.subplots()

    ax1.plot(N, at, 'b--', label = 'Attenuation constant')
    ax2 = ax1.twinx()
    ax2.plot(N, Vp,'r', label = 'Numerical phase velocity')

    ax2.set_ylabel('Numerical Phase Velocity (nomalized to c)')
    #ax2.legend()
    ax2.set_ylim(0, 2)

    ax1.set_ylabel('Attenuation Constant (nepers/grid cell)')
    ax1.set_ylim(0, 6)

    ax1.axvline(x = Ntrans(S), color = 'g', linestyle = '--', label = 'Transition point')
    ax1.legend()
    
    plt.xlim(1,10)
    plt.xlabel('Grid Sampling Density (points per free-space wavelength)')
    plt.show()

# fig 2.2

def fig_2_2(S, n):
    print('[INFO] Ntrans = ', Ntrans(S))
    N = np.linspace(3, 80, num = n)
    Vp = np.zeros(np.size(N))

    for i in range(np.size(N)):
        k = math.acos(f_tau(N[i], S))
        Vp[i] = (2*math.pi)/(N[i]*k)

    Vp = 100*(1-Vp)
    # fig 2.2

    label = 'S = ' + str(S)
    plt.plot(N, Vp, color='b', label = label)
    plt.yscale('log')
    plt.ylim(10**-2, 10**2)
    plt.xlabel('Grid Sampling Density (points per free-space wavelength)')
    plt.ylabel('Phase Velocity Error (%)')
    plt.legend()
    plt.show()

#fig_2_1(1/math.sqrt(2), 100)
fig_2_2(1/2, 100)