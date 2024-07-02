from Readers import CTD_cnv, ax2profile
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

# X = PSAL
# Y = DEPTH
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




if __name__ == '__main__':
    print("Loading CTD n°1 ...")
    CTD1 = CTD_cnv("./CTD_Alaska/SKQ202409S_001.cnv")
    # print("Loading CTD n°2 ...")
    # CTD2 = CTD_cnv("./CTD_Alaska/SKQ202409S_002.cnv")
    # print("Loading CTD n°3 ...")
    # CTD3 = CTD_cnv("./CTD_Alaska/SKQ202409S_003.cnv")

    print("Computing lists ...")
    l_CTD = [CTD1]#, CTD2, CTD3]
    l_s, l_t, l_d = [], [], []
    for ctd in l_CTD :
        ctd.simplify(100)
        l_s = l_s + ctd.get_l_psal()
        l_t = l_t + ctd.get_l_temp()
        l_d = l_d + ctd.get_l_depth()

    # print("Estimating model 1...")
    # l_X = l_d
    # l_Y = l_s
    # p0 = [8 , np.min(l_s)]
    # #meilleure determination avec l'inverse du model
    # (a1, b1), _ = curve_fit(inv_model_1, l_Y, l_X, p0)
    # print("Done !", a1, b1)
    #
    # figPvsD, axPvsD = plt.subplots()
    # axPvsD.scatter(l_X, l_Y, marker="+", s=5)
    # l_X_mod = np.linspace(min(l_X), max(l_X), 10000)
    # axPvsD.plot(l_X_mod, [model_1(x, a1, b1) for x in l_X_mod], color="red")

    print("Estimating model 2...")
    l_X = l_t
    l_Y = l_d
    l_Z = l_s
    data = np.array([[t, d] for (t,d) in zip(l_X, l_Y)])
    #p0_gom = [max(l_s)-min(l_s), 3, 0.1, min(l_s), 0.5/1000, 0, 0]
    p0 = [1, 1, 3, -1, min(l_s), 0, 0]
    (a, b, c, d, e, f, g), _ = p0, 0.0 # curve_fit(model_2, data, l_Z, p0) #
    print("Done !", a, b, c, d, e, f, g)


    l_Y_mod = np.linspace(min(l_Y), max(l_Y), 1000)
    l_X_mod = [np.mean(l_t) for _ in l_Y_mod]
    l_Z_mod = [float(model_2(np.array([[x, y]]), a, b, c, d, e, f, g)) for (x,y) in zip(l_X_mod, l_Y_mod)]

    fig, ax = plt.subplots()
    ax.plot(l_Y_mod, l_Z_mod, color="red")
    ax.scatter(l_Y, l_Z)
    plt.show()

    # figSTD = plt.figure()
    # axSTD = figSTD.add_subplot(projection="3d")
    # axSTD.scatter(l_X, l_Y, l_Z, marker="+", s=1)
    # l_X_mod = np.linspace(min(l_X), max(l_X), 100)
    # l_Y_mod = np.linspace(min(l_Y), max(l_Y), 100)
    # arr_X_mod, arr_Y_mod = np.meshgrid(l_X_mod, l_Y_mod)
    # arr_Z_mod = np.array([[ float(model_2(np.array([[x, y]]), a, b, c, d, e, f, g)) for x in l_X_mod] for y in l_Y_mod])
    # axSTD.plot_surface(arr_X_mod, arr_Y_mod, arr_Z_mod, alpha=0.2, cmap="jet")
    # axSTD.scatter(l_X, l_Y, l_Z)
    #
    # ax2profile(axSTD, xlabel="Temp (°C)", ylabel="Depth (m)", zlabel="PSal", invert=False)
    #
    # plt.show()

    #
    # fig = plt.figure()
    # ax = fig.add_subplot(projection="3d")
    #
    # ax.scatter(l_s, l_t, l_d, marker ="+", s=5)
    # ax2profile(ax, xlabel="PSal", ylabel="Temp (°C)", zlabel="Depth (m)", invert=False)

    plt.show()
