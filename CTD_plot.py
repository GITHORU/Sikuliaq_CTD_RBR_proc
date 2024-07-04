import numpy as np

from Readers import SVP_cnv, ax2profile
import matplotlib.pyplot as plt

if __name__ == '__main__':
    print("Loading SVP n°1")
    SVP1 = SVP_cnv("./CTD_Alaska/skq202409s_001svp.cnv")
    print("Loading SVP n°2")
    SVP2 = SVP_cnv("./CTD_Alaska/skq202409s_002svp.cnv")
    print("Loading SVP n°3")
    SVP3 = SVP_cnv("./CTD_Alaska/skq202409s_003svp.cnv")
    print("Loading SVP n°4")
    SVP4 = SVP_cnv("./CTD_Alaska/skq202409s_004svp.cnv")
    print("Loading SVP n°5")
    SVP5 = SVP_cnv("./CTD_Alaska/skq202409s_005svp.cnv")
    print("Loading SVP n°6")
    SVP6 = SVP_cnv("./CTD_Alaska/skq202409s_006svp.cnv")
    print("Loading SVP n°7")
    SVP7 = SVP_cnv("./CTD_Alaska/skq202409s_007svp.cnv")
    print("Loading SVP n°8")
    SVP8 = SVP_cnv("./CTD_Alaska/skq202409s_008svp.cnv")
    print("Loading SVP n°9")
    SVP9 = SVP_cnv("./CTD_Alaska/skq202409s_009svp.cnv")
    print("Loading SVP n°10")
    SVP10 = SVP_cnv("./CTD_Alaska/skq202409s_010svp.cnv")

    l_SVP = [SVP1, SVP2, SVP3, SVP4, SVP5, SVP6, SVP7, SVP8, SVP9, SVP10]
    l_names = ["KOD1-C(3)", "STK1-A(1)", "CHK1-B(2)", "SNK1-A(1)", "MESH-AF02","UNI1-B(2)", "MESH-AF05", "MESH-AF08", "MESH-AF10", "UNA1-B(2)" ]
    l_fnames = ["KOD1C3", "STK1A1", "CHK1B2", "SNK1A1", "MESHAF02","UNI1B2", "MESHAF05", "MESHAF08", "MESHAF10", "UNA1B2"]
    l_fig, l_ax = [], []
    all_V, all_D = [], []
    for svp in l_SVP :
        l_V = list(svp.get_l_speed())
        l_D = list(svp.get_l_depth())
        l_V = [l_V[i] for i in range(0, len(l_V), 100)]
        l_D = [l_D[i] for i in range(0, len(l_D), 100)]
        all_V = all_V + [np.nan] +l_V
        all_D = all_D + [np.nan] +l_D
    #l_fig_shal, l_ax_shal = [], []
    for (i, svp) in enumerate(l_SVP):
        print(l_fnames[i],":", svp.get_lat(), svp.get_lon())
        fig, ax = plt.subplots(nrows=1, ncols=2)
        #fig_shal, ax_shal = plt.subplots()
        minx, miny = 1460, -20
        maxx, maxy = 1500, 400
        svp.scatter_VD(ax[0], s=2, color="red")
        ax[0].plot([minx, maxx, maxx, minx, minx], [miny, miny, maxy, maxy, miny], color="orange", alpha=0.5)
        ax[1].plot(all_V, all_D, color="grey", alpha=0.2, label="Other\nCTDs")
        svp.scatter_VD(ax[1], s=2, color="orange", label=l_names[i]+"\nCTD")
        ax[1].set_ylim(miny, maxy)
        ax[1].set_xlim(minx, maxx)
        ax2profile(ax[0], xlabel="Soundspeed (m/s)", ylabel="Depth (m)", invert=True, title="SVP "+l_names[i], legend=False)
        ax2profile(ax[1], xlabel="Soundspeed (m/s)", invert=True, title="SVP n°"+l_names[i]+" (Shallow)", legend=True)

        l_ax.append(ax)
        l_fig.append(fig)
        # l_ax_shal.append(ax_shal)
        # l_fig_shal.append(fig_shal)

        fig.savefig("./figures/SVP_"+l_fnames[i]+"_plot.png")
        #fig_shal.savefig("./figures/PNG/SVP_" + l_fnames[i] + "_shal_plot.png")

    #plt.show()