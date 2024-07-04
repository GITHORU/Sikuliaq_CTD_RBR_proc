import os.path
from time import time
from Readers import CTD_cnv, ax2profile
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import multiprocessing as mp
from math import factorial

def calc_rho(t, p, S):
    p = p / 10  # dbar -> bar

    a0 = 999.842594
    a1 = 6.793952 * 10 ** (-2)
    a2 = -9.095290 * 10 ** (-3)
    a3 = 1.001685 * 10 ** (-4)
    a4 = -1.120083 * 10 ** (-6)
    a5 = 6.536332 * 10 ** (-9)

    rhow = a0 + a1*t + a2*t**2 + a3*t**3 + a4*t**4 + a5*t**5

    b0 = 8.24493*10**(-1)
    b1 =-4.0899*10**(-3)
    b2 = 7.6438*10**(-5)
    b3 =-8.2467*10**(-7)
    b4 = 5.3875*10**(-9)

    c0 =-5.72466*10**(-3)
    c1 = 1.0227*10**(-4)
    c2 =-1.6546*10**(-6)

    d0 = 4.8314*10**(-4)

    rhoSt0 = rhow + (b0 + b1*t + b2*t**2 +b3*t**3 +b4*t**4)*S + (c0 + c1*t + c2*t**2)*S**(3/2) + d0*S**2

    e0 = 19652.21
    e1 = 148.4206
    e2 =-2.327105
    e3 = 1.360477*10**(-2)
    e4 =-5.155288*10**(-5)

    Kw = e0 + e1*t + e2*t**2 + e3*t**3 + e4*t**4

    f0 = 54.6746
    f1 =-0.603459
    f2 = 1.09987*10**(-2)
    f3 =-6.1670*10**(-5)

    g0 = 7.944*10**(-2)
    g1 = 1.6483*10**(-2)
    g2 =-5.3009*10**(-4)

    h0 = 3.239908
    h1 = 1.43713*10**(-3)
    h2 = 1.16092*10**(-4)
    h3 =-5.77905*10**(-7)

    Aw = h0 + h1*t + h2*t**2 + h3*t**3

    i0 = 2.2838*10**(-3)
    i1 =-1.0981*10**(-5)
    i2 =-1.6078*10**(-6)

    j0 = 1.91075*10**(-4)

    k0 = 8.50935*10**(-5)
    k1 =-6.12293*10**(-6)
    k2 = 5.2787*10**(-8)

    Bw = k0 + k1*t + k2*t**2

    A = Aw + (i0 + i1*t + i2*t**2)*S + j0*S**(3/2)

    m0 =-9.9348*10**(-7)
    m1 = 2.0816*10**(-8)
    m2 = 9.1697*10**(-10)

    B = Bw + (m0 + m1*t + m2*t**2)*S

    KSt0 = Kw + (f0 + f1*t + f2*t**2 + f3*t**3)*S + (g0 + g1*t + g2*t**2)*S**(3/2)

    KStp = KSt0 + A*p + B*p**2

    return rhoSt0/(1 - p/KStp)
    #
    # Cp = 999.83 + 5.053 * p - 0.048 * p ** 2
    # Bp = 0.808 - 0.0085 * p
    # aTp = 0.0708 * (1 + 0.351 * p + 0.068 * (1 - 0.0683 * p) * T)
    # gTp = 0.003 * (1 - 0.059 * p - 0.012 * (1 - 0.064 * p) * T)
    # return Cp + Bp*S - aTp*T - gTp*(35-S)*T

def model_rho(S, a1, b1, a2, b2, c2):
    #f = a1*np.sqrt(c1*(S-b1))
    #f = a1*np.log(c1*(S-b1))
    #x = c1*(S-b1)
    #TY_f = calc_TY_f(x) #(x-1) - (x-1)**2/factorial(2)+ 2*(x-1)**3/factorial(3) - 2*3*(x-1)**4/factorial(4)
    g = np.exp(a2*(S-b2))
    f = -1/(np.exp(a1*(S-b1))) + c2
    return f + g  #f + g

def calc_TY_f(x):
    somme = 0
    deg = 4
    for i in range(1,deg) :
        somme += (-1)**(i-1)*((x-1)**i)/i
    return somme



def model_1(d, a, b):
    s = np.exp(np.log(d)/a) + b
    return (s)

def inv_model_1(s, a, b):
    d = (s-b)**a
    #y = np.exp(np.log(x)/a) + b
    return (d)

def model_2(data, a, b, c, d, e, f, g):
    T, D = data[:, 0], data[:, 1]
    #s = np.exp(np.log(d)/a) + b
    #s = (d + a * np.exp(-b * np.exp(-c*(D)))) + e*D
    s = T*D #np.exp(np.log(a*D)/c) +
    return (s)

def load_CTD(path) :
    print("Loading CTD : " + os.path.basename(path) + " ...")
    ctd = CTD_cnv(path)
    print(os.path.basename(path)+" loaded !")
    return ctd


if __name__ == '__main__':
    # tic = time()
    # print("Loading CTD n°1 ...")
    # CTD1 = CTD_cnv("./CTD_Alaska/SKQ202409S_001.cnv")
    # print("Loading CTD n°2 ...")
    # CTD2 = CTD_cnv("./CTD_Alaska/SKQ202409S_002.cnv")
    # print("Loading CTD n°3 ...")
    # CTD3 = CTD_cnv("./CTD_Alaska/SKQ202409S_003.cnv")
    # print("Loading CTD n°4 ...")
    # CTD4 = CTD_cnv("./CTD_Alaska/SKQ202409S_004.cnv")
    # print("Loading CTD n°5 ...")
    # CTD5 = CTD_cnv("./CTD_Alaska/SKQ202409S_005.cnv")
    # print("Loading CTD n°6 ...")
    # CTD6 = CTD_cnv("./CTD_Alaska/SKQ202409S_006.cnv")
    # print("Loading CTD n°7 ...")
    # CTD7 = CTD_cnv("./CTD_Alaska/SKQ202409S_007.cnv")
    # print("Loading CTD n°8 ...")
    # CTD8 = CTD_cnv("./CTD_Alaska/SKQ202409S_008.cnv")
    # print("Loading CTD n°9 ...")
    # CTD9 = CTD_cnv("./CTD_Alaska/SKQ202409S_009.cnv")
    # print("Loading CTD n°10 ...")
    # CTD10 = CTD_cnv("./CTD_Alaska/SKQ202409S_010.cnv")
    # print("OK ! :", time()-tic)

    l_CTD_path = ["./CTD_Alaska/SKQ202409S_001.cnv",
                    "./CTD_Alaska/SKQ202409S_002.cnv",
                    "./CTD_Alaska/SKQ202409S_003.cnv",
                    "./CTD_Alaska/SKQ202409S_004.cnv"]

    l_CTD_path = ["./CTD_Alaska/SKQ202409S_001.cnv",
                    "./CTD_Alaska/SKQ202409S_002.cnv",
                    "./CTD_Alaska/SKQ202409S_003.cnv",
                    "./CTD_Alaska/SKQ202409S_004.cnv",
                    "./CTD_Alaska/SKQ202409S_005.cnv",
                    "./CTD_Alaska/SKQ202409S_006.cnv",
                    "./CTD_Alaska/SKQ202409S_007.cnv",
                    "./CTD_Alaska/SKQ202409S_008.cnv",
                    "./CTD_Alaska/SKQ202409S_009.cnv",
                    "./CTD_Alaska/SKQ202409S_010.cnv"]


    print("Nb CPUs available :",mp.cpu_count())
    print("Nb CPUs used :",max([min([int(mp.cpu_count()/4), len(l_CTD_path)]), 0]))
    pool = mp.Pool(processes = max([min([int(mp.cpu_count()/4), len(l_CTD_path)]), 0]))
    l_CTD = pool.map(load_CTD, l_CTD_path)

    fig3D = plt.figure()
    ax3D = fig3D.add_subplot(projection="3d")
    fig2D, ax2D = plt.subplots(nrows=2, ncols=2)
    l_s, l_t, l_p = [], [], []
    for ctd in l_CTD :
        print(os.path.basename(ctd.path))
        #ctd.zoom_on_depth(maxD=300)
        ctd.simplify(5000)
        l_s, l_t, l_p = l_s + ctd.get_l_psal(), l_t + ctd.get_l_temp(), l_p + ctd.get_l_pres()
        ax3D.scatter(ctd.get_l_temp(), ctd.get_l_pres(), ctd.get_l_psal(), s=1)

    ax2D[0,0].scatter(l_t, l_p, c=l_s, cmap="jet", s=1)
    ax2D[0,1].scatter(l_t, l_s, s=1)
    ax2D[1,0].scatter(l_s, [calc_rho(T, p, S) for (T, p, S) in zip(l_t, l_p, l_s)], s=1)
    ax2D[1,1].scatter(l_p, l_s, s=1)
    ax2profile(ax2D[0,0], xlabel="Temp (°C)", ylabel="Pressure (dbar)", invert=False)
    ax2profile(ax2D[0,1], xlabel="Temp (°C)", ylabel="PSal", invert=False)
    ax2profile(ax2D[1,0], xlabel="PSal", ylabel="Rho", invert=False)
    ax2profile(ax2D[1,1], xlabel="Pressure (dbar)", ylabel="PSal", invert=False)
    ax2profile(ax3D, xlabel="Temp (°C)", ylabel="Pressure (dbar)", zlabel="PSal", invert=False)

    data = np.array([[t, p, s] for (t,p,s) in zip(l_t, l_p, l_s)])
    #p0_gom = [max(l_s)-min(l_s), 3, 0.1, min(l_s), 0.5/1000, 0, 0]
    #p0 = [0.2876724325037172, 32.38421963859541, 2.6682393825860538, 2.6769805621058795, 33.73553144318889, 1025.986540509439]
    #p0 = [1.6, 33, 5, 34, 950]
    p0 = [11.760456712921053, 32.407274769039304, 2.522210957993802, 33.67266119747667, 1026.1422063524294]
    p0 = [ 0.4984165971300929 , 35.17706984142072 , 3.859191965502381 , 34.014122231581986 , 1029.3460740359494 ]
    print("Estimating best fit ...")
    #np.array([0.1, 20, 0.1, 20, 900]), np.array([20, 50, 20, 50, 1100])
    (a1, b1, a2, b2, c2), _ = p0, 0.0 #curve_fit(model_rho, l_s, [calc_rho(T, p, S) for (T, p, S) in zip(l_t, l_p, l_s)], p0, bounds=(np.array([0.0, 20, 0.0, 20, 900]), np.array([20, np.inf, 20, 50, 1500])), method="dogbox", loss="soft_l1") #
    print("Done ! : [", a1, ",", b1, ",", a2, ",", b2, ",", c2,"]")
    fig_model, ax_model = plt.subplots()
    ax_model.scatter(l_s, [-1/(np.exp(a1*(s-b1))) + c2 for s in l_s], s=1, color="grey", alpha=0.2)
    ax_model.scatter(l_s, [np.exp(a2*(s-b2)) + c2 for s in l_s], s=1, color="grey", alpha=0.2)
    ax_model.scatter(l_s, [calc_rho(T, p, S) for (T, p, S) in zip(l_t, l_p, l_s)], s=1, label="raw")
    ax_model.scatter(l_s, [model_rho(s, a1, b1, a2, b2, c2) for s in l_s], s=1, label="model")
    ax2profile(ax_model, invert=False, xlabel="Psal", ylabel="Rho")

    # print("Computing lists ...")
    # l_CTD = [CTD1]#, CTD2, CTD3]
    # l_s, l_t, l_d = [], [], []
    # for ctd in l_CTD :
    #     ctd.simplify(100)
    #     l_s = l_s + ctd.get_l_psal()
    #     l_t = l_t + ctd.get_l_temp()
    #     l_d = l_d + ctd.get_l_depth()
    #
    # # print("Estimating model 1...")
    # # l_X = l_d
    # # l_Y = l_s
    # # p0 = [8 , np.min(l_s)]
    # # #meilleure determination avec l'inverse du model
    # # (a1, b1), _ = curve_fit(inv_model_1, l_Y, l_X, p0)
    # # print("Done !", a1, b1)
    # #
    # # figPvsD, axPvsD = plt.subplots()
    # # axPvsD.scatter(l_X, l_Y, marker="+", s=5)
    # # l_X_mod = np.linspace(min(l_X), max(l_X), 10000)
    # # axPvsD.plot(l_X_mod, [model_1(x, a1, b1) for x in l_X_mod], color="red")
    #
    # print("Estimating model 2...")
    # l_X = l_t
    # l_Y = l_d
    # l_Z = l_s
    # data = np.array([[t, d] for (t,d) in zip(l_X, l_Y)])
    # #p0_gom = [max(l_s)-min(l_s), 3, 0.1, min(l_s), 0.5/1000, 0, 0]
    # p0 = [1, 1, 3, -1, min(l_s), 0, 0]
    # (a, b, c, d, e, f, g), _ = p0, 0.0 # curve_fit(model_2, data, l_Z, p0) #
    # print("Done !", a, b, c, d, e, f, g)
    #
    #
    # l_Y_mod = np.linspace(min(l_Y), max(l_Y), 1000)
    # l_X_mod = [np.mean(l_t) for _ in l_Y_mod]
    # l_Z_mod = [float(model_2(np.array([[x, y]]), a, b, c, d, e, f, g)) for (x,y) in zip(l_X_mod, l_Y_mod)]
    #
    # fig, ax = plt.subplots()
    # ax.plot(l_Y_mod, l_Z_mod, color="red")
    # ax.scatter(l_Y, l_Z)
    # plt.show()
    #
    # # figSTD = plt.figure()
    # # axSTD = figSTD.add_subplot(projection="3d")
    # # axSTD.scatter(l_X, l_Y, l_Z, marker="+", s=1)
    # # l_X_mod = np.linspace(min(l_X), max(l_X), 100)
    # # l_Y_mod = np.linspace(min(l_Y), max(l_Y), 100)
    # # arr_X_mod, arr_Y_mod = np.meshgrid(l_X_mod, l_Y_mod)
    # # arr_Z_mod = np.array([[ float(model_2(np.array([[x, y]]), a, b, c, d, e, f, g)) for x in l_X_mod] for y in l_Y_mod])
    # # axSTD.plot_surface(arr_X_mod, arr_Y_mod, arr_Z_mod, alpha=0.2, cmap="jet")
    # # axSTD.scatter(l_X, l_Y, l_Z)
    # #
    # # ax2profile(axSTD, xlabel="Temp (°C)", ylabel="Depth (m)", zlabel="PSal", invert=False)
    # #
    # # plt.show()
    #
    # #
    # # fig = plt.figure()
    # # ax = fig.add_subplot(projection="3d")
    # #
    # # ax.scatter(l_s, l_t, l_d, marker ="+", s=5)
    # # ax2profile(ax, xlabel="PSal", ylabel="Temp (°C)", zlabel="Depth (m)", invert=False)

    plt.show()
