import os

import pandas as pd
from seabird.cnv import fCNV
from pyrsktools import RSK
from time import time
import matplotlib.pyplot as plt
from copy import copy, deepcopy
from tqdm import tqdm
import numpy as np
from datetime import datetime, timedelta


def ax2profile(ax, xlabel="", ylabel="", zlabel="", title="", invert = True, legend=True):
    if invert :
        ax.invert_yaxis()
    ax.grid()
    if legend :
        ax.legend()
    if xlabel != "" :
        ax.set_xlabel(xlabel)
    if ylabel != "" :
        ax.set_ylabel(ylabel)
    if zlabel != "" :
        ax.set_zlabel(zlabel)
    if title != "" :
        ax.set_title(title)


class Profile_file :
    def __init__(self, path):
        self.path = path

    def load_data_cnv(self):
        profile = fCNV(self.path)
        # print(profile.attrs)
        self.start_time = profile.attrs["datetime"]
        dict = {key:profile[key] for key in profile.keys()}
        self.data = pd.DataFrame(dict)
        if "timeM" in profile.keys() :
            l_ts = [ts for ts in list(self.data["timeM"])]
            self.middle_time = self.start_time  + timedelta(minutes=max(l_ts))


    def load_data_rsk(self):
        l_data_up = []
        l_data_down = []
        with RSK(self.path) as rsk :
            rsk.readdata()
            rsk.deriveseapressure()
            rsk.computeprofiles()
            profile_id_down = rsk.getprofilesindices(direction="down")
            profile_id_up = rsk.getprofilesindices(direction="up")
            keys = [chan.longName for chan in rsk.channels] + ["timestamp"]
            for index in profile_id_down :
                dict = {key:rsk.data[index][key] for key in keys}
                l_data_down.append(pd.DataFrame(dict))
            for index in profile_id_up :
                dict = {key:rsk.data[index][key] for key in keys}
                l_data_up.append(pd.DataFrame(dict))

            self.data = {"down":l_data_down, "up":l_data_up}


class CNV_profile_file(Profile_file) :
    def __init__(self, path=""):
        super().__init__(path)
        if path == "" :
            return
        else :
            self.load_data_cnv()

    def simplify(self, nb):
        if type(nb) != type(0) :
            print("Warning, simplifying nb int is not an int, not resampling")
            return self
        self.data = self.data.iloc[::nb, :]

    def zoom_on_depth(self, minD=None, maxD=None):
        l_D = self.get_l_depth()
        if minD==None :
            minD = min(l_D)
        if maxD==None :
            maxD = max(l_D)

        self.data = self.data[(self.data["DEPTH"] > minD)]
        self.data = self.data[(self.data["DEPTH"] < maxD)]

    def get_l_key(self, key):
        return list(self.data[key])

    def get_l_temp(self):
        return self.get_l_key("TEMP")

    def get_l_psal(self):
        return self.get_l_key("PSAL")

    def get_l_depth(self):
        return self.get_l_key("DEPTH")

    def get_lat(self):
        return self.get_l_key("LATITUDE")[0]

    def get_lon(self):
        return self.get_l_key("LONGITUDE")[0]

    def scatter_TD(self, ax, marker="+", s=10, color=None, label=None):
        l_y = self.get_l_depth()
        l_x = self.get_l_temp()
        ax.scatter(l_x, l_y, marker=marker, s=s, color=color, label=label)

    def scatter_SD(self, ax, marker="+", s=10, color=None, label=None):
        l_y = self.get_l_depth()
        l_x = self.get_l_psal()
        ax.scatter(l_x, l_y, marker=marker, s=s, color=color, label=label)



class CTD_cnv(CNV_profile_file) :
    def __init__(self, path=""):
        super().__init__(path)


    def get_l_pres(self):
        return self.get_l_key("PRES")

    def get_l_ts(self, unit="m"):
        if not unit in ["h", "m", "s"] :
            print("Warning : asked units not supported, return in minutes.")
            unit = "m"
        l_ts = self.get_l_key("timeM")
        if unit == "m" :
            return l_ts
        elif unit == "h" :
            return [ts/60 for ts in l_ts]
        elif unit == "s" :
            return [ts*60 for ts in l_ts]

    def scatter_TP(self, ax, marker="+", s=10, color=None, label=None):
        l_y = self.get_l_pres()
        l_x = self.get_l_temp()
        ax.scatter(l_x, l_y, marker=marker, s=s, color=color, label=label)

    def scatter_SP(self, ax, marker="+", s=10, color=None, label=None):
        l_y = self.get_l_pres()
        l_x = self.get_l_psal()
        ax.scatter(l_x, l_y, marker=marker, s=s, color=color, label=label)

    def scatter_3D_STD(self, ax, marker="+", s=10, color=None, label=None):
        l_z = self.get_l_depth()
        l_y = self.get_l_temp()
        l_x = self.get_l_psal()
        ax.scatter(l_x, l_y, l_z, marker=marker, s=s, color=color, label=label)

class SVP_cnv(CNV_profile_file) :
    def __init__(self, path=""):
        super().__init__(path)

    def to_csv(self, csvpath):
        l_d, l_v = self.get_l_depth(), self.get_l_speed()
        l_d, l_v = zip(*sorted(zip(l_d, l_v)))
        chaine = "depth,speed\n"
        for (d, v) in tqdm(zip(l_d, l_v)):
            chaine = chaine + str(np.round(d, 3)) + "," + str(np.round(v, 3)) + "\n"
        with open(csvpath, 'w') as file:
            file.write(chaine)

    def get_l_speed(self):
        return self.get_l_key("soundspeed")

    def scatter_VD(self, ax, marker="+", s=10, color=None, label=None):
        l_y = self.get_l_depth()
        l_x = self.get_l_speed()
        ax.scatter(l_x, l_y, marker=marker, s=s, color=color, label=label)

class RBR(Profile_file) :
    def __init__(self, path):
        super().__init__(path)
        self.load_data_rsk()
        self.nb_profile = len(self.data["up"])

    def get_l_key(self, key, direction, index):
        return list(self.data[direction][index][key])

    def get_l_pres(self, direction, index):
        return self.get_l_key("sea_pressure", direction, index)

    def get_l_temp(self, direction, index):
        return self.get_l_key("temperature", direction, index)

    def get_l_ts(self, direction, index):
        l_ts_pd=  self.get_l_key("timestamp", direction, index)
        return [ts.to_pydatetime() for ts in l_ts_pd]

    def get_time_range(self, index):
        return self.get_l_ts("down", index)[0], self.get_l_ts("up", index)[-1]

    def scatter_TP(self, ax, direction, index, marker="+", s=10, color=None, label=None):
        l_y = self.get_l_pres(direction, index)
        l_x = self.get_l_temp(direction, index)
        ax.scatter(l_x, l_y, marker=marker, s=s, color=color, label=label)

    def scatter_TP_all_direction(self, ax, direction, marker="+", s=10, color=None, label=None):
        for i in range(self.nb_profile):
            self.scatter_TP(ax, direction, i, marker=marker, s=s, color=color, label=label+" "+str(i))

    def scatter_TP_all_down(self, ax, marker="+", s=10, color=None, label=None):
        self.scatter_TP_all_direction(ax, "down", marker=marker, s=s, color=color, label=label)

    def scatter_TP_all_up(self, ax, marker="+", s=10, color=None, label=None):
        self.scatter_TP_all_direction(ax, "up", marker=marker, s=s, color=color, label=label)

if __name__ == '__main__':
    print("Importing RBR ...")
    rbr = RBR("./RBR_Alaska/234446_20240627_1222.rsk")
    print("Importing CTD ...")
    ctd = CTD_cnv("./CTD_Alaska/SKQ202409S_006.cnv")

    print(ctd.start_time, ctd.middle_time)

    for i in range(rbr.nb_profile):
        tmin, tmax = rbr.get_time_range(i)
        print(i, ":", tmin, tmax, (tmin <= ctd.middle_time <= tmax ))

    print(ctd.start_time)

    # print("Importing RBR ...")
    # rbr = RBR("./RBR_Alaska/234446_20240627_1222.rsk")
    # print("Importing CTD ...")
    # ctd = CTD_cnv("./CTD_Alaska/SKQ202409S_007.cnv")
    # ctd.simplify(50)
    #
    # fig, ax = plt.subplots()
    # rbr.scatter_TP(ax, "down", 3, s=2, color="purple", label="RBR down 1")
    # rbr.scatter_TP(ax, "up", 3, s=2, color="orange", label="RBR up 1")
    # #rbr.scatter_TP_all_down(ax, s=2, label="RBR down")
    # #rbr.scatter_TP_all_up(ax, s=2, label="RBR up")
    # ctd.scatter_TP(ax, s=2, color="red", label="CTD n°10")
    # ax2profile(ax)

    # # F1 = CTD_cnv("./CTD_Alaska/SKQ202409S_001.cnv")
    # # F1 = F1.simplify(5)
    # # print(F1.get_l_temp()[:5])
    # # print(F1.get_l_pres()[:5])
    # # print(F1.get_l_psal()[:5])
    # # print(F1.get_l_ts(unit="s")[:5])
    # # print(F1.get_l_ts(unit="m")[:5])
    # # print(F1.get_l_ts(unit="h")[:5])
    # # print(F1.get_lat(), F1.get_lon())
    # # # #print(F1.data)
    # # F2 = SVP_cnv("./CTD_Alaska/skq202409s_001svp.cnv")
    # # print(F2.get_l_temp()[:5])
    # # print(F2.get_l_depth()[:5])
    # # print(F2.get_l_speed()[:5])
    # # print(F2.get_l_psal()[:5])
    # # print(F2.get_lat(), F2.get_lon())
    # # #print(F2.data)
    # # F3 = RBR("./RBR_Alaska/234446_20240621_1514.rsk")
    # # print(F3.get_l_temp("up", 0)[:5])
    # # print(F3.get_l_temp("down", 0)[:5])
    # # print(F3.get_l_pres("up", 0)[:5])
    # # print(F3.get_l_pres("down", 0)[:5])
    # # print(F3.nb_profile)
    # # #print(F3.data["up"][0])
    # # #print(F3.data["down"][-1])
    #
    # # print("Loading CTD ...")
    # # CTD = CTD_cnv("./CTD_Alaska/SKQ202409S_001.cnv")
    # # print("Loading SVP ...")
    # # SVP = SVP_cnv("./CTD_Alaska/skq202409s_001svp.cnv")
    # #
    # # fig, ax = plt.subplots()
    # # CTD.scatter_TD(ax, label="temp CTD D")
    # # CTD.scatter_TP(ax, label="temp CTD P")
    # # SVP.scatter_TD(ax, label="temp CTD D")
    # # ax2profile(ax)
    # # plt.show()
    #
    # # print("Loading SVP n°1")
    # # SVP1 = SVP_cnv("./CTD_Alaska/skq202409s_001svp.cnv")
    # # SVP1_5 = SVP1.simplify(5)
    # # SVP1_50 = SVP1.simplify(50)
    # #
    # # fig_simp, ax_simp = plt.subplots()
    # # SVP1.scatter_VD(ax_simp, label="RAW")
    # # SVP1_5.scatter_VD(ax_simp, label="PROC 5")
    # # SVP1_50.scatter_VD(ax_simp, label="PROC 50")
    # # ax2profile(ax_simp)
    # # plt.show()
    #
    # # print("Loading SVP n°1")
    # # SVP1 = SVP_cnv("./CTD_Alaska/skq202409s_001svp.cnv")
    # # print("Loading SVP n°2")
    # # SVP2 = SVP_cnv("./CTD_Alaska/skq202409s_002svp.cnv")
    # # print("Loading SVP n°3")
    # # SVP3 = SVP_cnv("./CTD_Alaska/skq202409s_003svp.cnv")
    # # print("Loading SVP n°4")
    # # SVP4 = SVP_cnv("./CTD_Alaska/skq202409s_004svp.cnv")
    # # print("Loading SVP n°5")
    # # SVP5 = SVP_cnv("./CTD_Alaska/skq202409s_005svp.cnv")
    # # print("Loading SVP n°6")
    # # SVP6 = SVP_cnv("./CTD_Alaska/skq202409s_006svp.cnv")
    # # print("Loading SVP n°7")
    # # SVP7 = SVP_cnv("./CTD_Alaska/skq202409s_007svp.cnv")
    # # print("Loading SVP n°8")
    # # SVP8 = SVP_cnv("./CTD_Alaska/skq202409s_008svp.cnv")
    # # print("Loading SVP n°9")
    # # SVP9 = SVP_cnv("./CTD_Alaska/skq202409s_009svp.cnv")
    # # print("Loading SVP n°10")
    # # SVP10 = SVP_cnv("./CTD_Alaska/skq202409s_010svp.cnv")
    #
    # print("Loading CTD n°1")
    # CTD1 = CTD_cnv("./CTD_Alaska/SKQ202409S_001.cnv")
    # print("Loading CTD n°2")
    # CTD2 = CTD_cnv("./CTD_Alaska/SKQ202409S_002.cnv")
    # print("Loading CTD n°3")
    # CTD3 = CTD_cnv("./CTD_Alaska/SKQ202409S_003.cnv")
    # print("Loading CTD n°4")
    # CTD4 = CTD_cnv("./CTD_Alaska/SKQ202409S_004.cnv")
    # print("Loading CTD n°5")
    # CTD5 = CTD_cnv("./CTD_Alaska/SKQ202409S_005.cnv")
    # print("Loading CTD n°6")
    # CTD6 = CTD_cnv("./CTD_Alaska/SKQ202409S_006.cnv")
    # print("Loading CTD n°7")
    # CTD7 = CTD_cnv("./CTD_Alaska/SKQ202409S_007.cnv")
    # print("Loading CTD n°8")
    # CTD8 = CTD_cnv("./CTD_Alaska/SKQ202409S_008.cnv")
    # print("Loading CTD n°9")
    # CTD9 = CTD_cnv("./CTD_Alaska/SKQ202409S_009.cnv")
    # print("Loading CTD n°10")
    # CTD10 = CTD_cnv("./CTD_Alaska/SKQ202409S_010.cnv")
    #
    # #l_SVP = [SVP1, SVP2, SVP3]#, SVP4, SVP5, SVP6, SVP7, SVP8, SVP9, SVP10]
    # l_CTD = [CTD1, CTD2, CTD3, CTD4, CTD5, CTD6, CTD7, CTD8, CTD9, CTD10]
    #
    # #SVP1.to_csv("./data/SVP_001.csv")
    #
    # fig_STD = plt.figure()
    # ax_STD = fig_STD.add_subplot(projection="3d")
    #
    # for (i, ctd) in enumerate(l_CTD):
    #     ctd_c = copy(ctd)
    #     ctd_c.simplify(50)
    #     ctd_c.scatter_3D_STD(ax_STD, label="SVP n°" + str(i + 1))
    #
    # ax2profile(ax_STD, xlabel="PSal", ylabel="Temperature (°C)", zlabel="Depth (m)", title="Temp vs Depth", invert=False)
    #
    # # fig_T_CTD, ax_T_CTD = plt.subplots()
    # # fig_S_CTD, ax_S_CTD = plt.subplots()
    # # fig_T_s_CTD, ax_T_s_CTD = plt.subplots()
    # # fig_S_s_CTD, ax_S_s_CTD = plt.subplots()
    # #
    # # for (i, ctd) in enumerate(l_CTD):
    # #     ctd_c = copy(ctd)
    # #     ctd_c.simplify(50)
    # #     ctd_c.scatter_TD(ax_T_CTD, label="SVP n°" + str(i + 1))
    # #     ctd_c.scatter_SD(ax_S_CTD, label="SVP n°" + str(i + 1))
    # #
    # # for (i, ctd) in enumerate(l_CTD):
    # #     ctd_c = copy(ctd)
    # #     ctd_c.simplify(10)
    # #     ctd_c.zoom_on_depth(maxD=300)
    # #     ctd_c.scatter_TD(ax_T_s_CTD, label="SVP n°" + str(i + 1))
    # #     ctd_c.scatter_SD(ax_S_s_CTD, label="SVP n°" + str(i + 1))
    # #
    # # ax2profile(ax_T_CTD, xlabel="Temp (°C)", ylabel="Depth (m)", title="Temp vs Depth")
    # # ax2profile(ax_S_CTD, xlabel="PSal", ylabel="Depth (m)", title="PSal vs Depth")
    # # ax2profile(ax_T_s_CTD, xlabel="Temp (°C)", ylabel="Depth (m)", title="Temp vs Depth (shallow)")
    # # ax2profile(ax_S_s_CTD, xlabel="PSal", ylabel="Depth (m)", title="PSal vs Depth (shallow)")
    # #
    # #
    # # fig_T, ax_T = plt.subplots()
    # # fig_V, ax_V = plt.subplots()
    # # fig_T_s, ax_T_s = plt.subplots()
    # # fig_V_s, ax_V_s = plt.subplots()
    # #
    # # for (i, svp) in enumerate(l_SVP) :
    # #     svp_c = copy(svp)
    # #     svp_c.simplify(50)
    # #     svp_c.scatter_TD(ax_T, label="SVP n°"+str(i+1))
    # #     svp_c.scatter_VD(ax_V, label="SVP n°"+str(i+1))
    # #
    # # for (i, svp) in enumerate(l_SVP) :
    # #     svp_c = copy(svp)
    # #     svp_c.simplify(10)
    # #     svp_c.zoom_on_depth(maxD=300)
    # #     svp_c.scatter_TD(ax_T_s, label="SVP n°"+str(i+1))
    # #     svp_c.scatter_VD(ax_V_s, label="SVP n°"+str(i+1))
    # #
    # # ax2profile(ax_T, xlabel="Temp (°C)", ylabel="Depth (m)", title="Temp vs Depth")
    # # ax2profile(ax_V, xlabel="Soundspeed (m.s-1)", ylabel="Depth (m)", title="Soundspeed vs Depth")
    # # ax2profile(ax_T_s, xlabel="Temp (°C)", ylabel="Depth (m)", title="Temp vs Depth (shallow)")
    # # ax2profile(ax_V_s, xlabel="Soundspeed (m.s-1)", ylabel="Depth (m)", title="Soundspeed vs Depth (shallow)")

    plt.show()


