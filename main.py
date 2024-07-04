import os.path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import yaml
from Readers import CTD_cnv, RBR, ax2profile

def sliding_mean(X, Y, pas):
    ret_X = np.linspace(min(X)+pas/2, max(X)-pas/2, int(((max(X)-pas/2) - (min(X)+pas/2))/pas))
    ret_Y = []
    for x in ret_X :
        mask = (X >= x-pas/2)*(X <= x+pas/2)
        window = mask*np.array(Y)
        if np.sum(mask) == 0 :
            ret_Y.append(np.nan)
        else :
            ret_Y.append(np.sum(window)/np.sum(mask))

    return ret_X, ret_Y

def linear_interp(X, Y, val):
    for i in range(len(X) - 1) :
        if X[i] <= val and X[i+1] > val :
            fact = (val - X[i])/(X[i+1] - X[i])
            return Y[i] + fact*(Y[i+1] - Y[i])
    return np.nan

if __name__ == '__main__':
    corr_path = "./correspondance_snk.yml"
    with open(corr_path, 'r') as file :
        corr_dict = yaml.safe_load(file)

    l_fig, l_ax = [], []
    l_fig_diff, l_ax_diff = [], []
    for (num, key) in enumerate(corr_dict["corr_list"].keys()) :
        site = corr_dict["corr_list"][key]
        print(key, "(",np.round((num/len(corr_dict["corr_list"].keys())*100), 1),"%) :")
        print("   Loading CTD", os.path.basename(site["CTD_path"]))
        ctd = CTD_cnv(site["CTD_path"])

        print("   Loading RBR", os.path.basename(site["RBR_path"]))
        rbr = RBR(site["RBR_path"])

        l_index = site["RBR_index"]
        print("   Initializing figures ...")
        fig, ax = plt.subplots()
        fig_diff, ax_diff = plt.subplots()
        l_fig.append(fig)
        l_ax.append(ax)
        l_fig_diff.append(fig_diff)
        l_ax_diff.append(ax_diff)
        print("   Plotting CTD ...")
        ctd.scatter_TP(l_ax[-1], s=2, color="red", label = "CTD")
        chaine_stats = ""
        for index in l_index :
            if chaine_stats != "":
                chaine_stats = chaine_stats + "\n"
            print("   RBR index n°", index, ":")
            print("      getting data from CTD and RBR ...")
            l_press_ctd, l_temp_ctd = ctd.get_l_pres(), ctd.get_l_temp()
            l_press_rbr_up, l_temp_rbr_up = rbr.get_l_pres("up", index), rbr.get_l_temp("up", index)
            l_press_rbr_down, l_temp_rbr_down = rbr.get_l_pres("down", index), rbr.get_l_temp("down", index)

            pas = 50
            print("      Downsampling CTD and RBR by", pas,"...")
            l_press_ctd = [l_press_ctd[i] for i in range(0, len(l_press_ctd), pas)]
            l_press_rbr_up = [l_press_rbr_up[i] for i in range(0, len(l_press_rbr_up), pas)]
            l_press_rbr_down = [l_press_rbr_down[i] for i in range(0, len(l_press_rbr_down), pas)]
            l_temp_ctd = [l_temp_ctd[i] for i in range(0, len(l_temp_ctd), pas)]
            l_temp_rbr_up = [l_temp_rbr_up[i] for i in range(0, len(l_temp_rbr_up), pas)]
            l_temp_rbr_down = [l_temp_rbr_down[i] for i in range(0, len(l_temp_rbr_down), pas)]

            pas = 5
            print("      Performing a sliding mean of", pas,"m on CTD ...")
            l_press_sm_ctd, l_temp_sm_ctd = sliding_mean(l_press_ctd, l_temp_ctd, pas)
            pas = 5
            print("      Performing a sliding mean of", pas, "m on RBR ...")
            l_press_sm_rbr_up, l_temp_sm_rbr_up = sliding_mean(l_press_rbr_up, l_temp_rbr_up, pas)
            l_press_sm_rbr_down, l_temp_sm_rbr_down = sliding_mean(l_press_rbr_down, l_temp_rbr_down, pas)

            pas = 2.5
            print("      Computing differences every", pas,"m...")
            l_press_diff = np.arange(min(list(l_press_sm_rbr_up) + list(l_press_sm_ctd)), max(list(l_press_sm_rbr_up) + list(l_press_sm_ctd)), pas)

            l_temp_diff_up_ctd = [linear_interp(l_press_sm_rbr_up, l_temp_sm_rbr_up, p) - linear_interp(l_press_sm_ctd, l_temp_sm_ctd, p) for p in l_press_diff]
            l_temp_diff_down_ctd = [linear_interp(l_press_sm_rbr_down, l_temp_sm_rbr_down, p) - linear_interp(l_press_sm_ctd, l_temp_sm_ctd, p) for p in l_press_diff]
            l_temp_diff_up_down = [linear_interp(l_press_sm_rbr_up, l_temp_sm_rbr_up, p) - linear_interp(l_press_sm_rbr_down, l_temp_sm_rbr_down, p) for p in l_press_diff]

            print("      Plotting differences ...")
            s = np.round(np.std([T for T in l_temp_diff_down_ctd if (not np.isnan(T))]),5)
            m = np.round(np.median([T for T in l_temp_diff_down_ctd if (not np.isnan(T))]), 5)
            chaine_stats = chaine_stats + "Profile n°"+str(index)+" m:"+str(m)+ "°C | s:"+str(s)+ "°C"

            ax_diff.scatter(l_temp_diff_down_ctd, l_press_diff, s=2, marker="+", color="purple", label="down"+str(index)+" - CTD")
            ax_diff.scatter(l_temp_diff_up_ctd, l_press_diff, s=2, marker="+", color = "orange", label = "up"+str(index)+" - CTD")
            ax_diff.scatter(l_temp_diff_up_down, l_press_diff, s=2, marker="+", color="green", label="up"+str(index)+" - down"+str(index))

            print("      Plotting RBR ...")
            rbr.scatter_TP(l_ax[-1], "down", index, s=2,color="purple", label = "RBR down "+str(index))
            rbr.scatter_TP(l_ax[-1], "up", index, s=2, color="orange", label="RBR up " + str(index))
        # l_ax[-1].set_xlim(3, 10)
        # l_ax[-1].set_ylim(5, 300)
        l_ax_diff[-1].set_xlim(-0.3, 0.3)

        print("   Formating figures ...")
        ax2profile(l_ax[-1], title=key + " mounted on " + site["mounting"] + " " + site["date"])
        ax2profile(l_ax_diff[-1], title=key + " mounted on " + site["mounting"] + " " + site["date"]+"\n" + chaine_stats)
    plt.show()