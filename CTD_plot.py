from Readers import SVP_cnv, ax2profile
import matplotlib.pyplot as plt

if __name__ == '__main__':
    print("Loading SVP n°1")
    SVP1 = SVP_cnv("./CTD_Alaska/skq202409s_001svp.cnv")
    print("Loading SVP n°2")
    SVP2 = SVP_cnv("./CTD_Alaska/skq202409s_002svp.cnv")
    # print("Loading SVP n°3")
    # SVP3 = SVP_cnv("./CTD_Alaska/skq202409s_003svp.cnv")
    # print("Loading SVP n°4")
    # SVP4 = SVP_cnv("./CTD_Alaska/skq202409s_004svp.cnv")
    # print("Loading SVP n°5")
    # SVP5 = SVP_cnv("./CTD_Alaska/skq202409s_005svp.cnv")
    # print("Loading SVP n°6")
    # SVP6 = SVP_cnv("./CTD_Alaska/skq202409s_006svp.cnv")
    # print("Loading SVP n°7")
    # SVP7 = SVP_cnv("./CTD_Alaska/skq202409s_007svp.cnv")
    # print("Loading SVP n°8")
    # SVP8 = SVP_cnv("./CTD_Alaska/skq202409s_008svp.cnv")
    # print("Loading SVP n°9")
    # SVP9 = SVP_cnv("./CTD_Alaska/skq202409s_009svp.cnv")
    # print("Loading SVP n°10")
    # SVP10 = SVP_cnv("./CTD_Alaska/skq202409s_010svp.cnv")

    l_SVP = [SVP1, SVP2] #, SVP3, SVP4, SVP5, SVP6, SVP7, SVP8, SVP9, SVP10]
    l_fig, l_ax = [], []
    l_fig_shal, l_ax_shal = [], []
    for (i, svp) in enumerate(l_SVP):
        fig, ax = plt.subplots()
        fig_shal, ax_shal = plt.subplots()
        svp.scatter_VD(ax, s=2, color="red")
        svp.scatter_VD(ax_shal, s=2, color="red")
        ax_shal.set_ylim(-20, 400)
        ax2profile(ax, xlabel="Soudspeed (m/s)", ylabel="Depth (m)", invert=True, title="SVP n°"+str(i+1), legend=False)
        ax2profile(ax_shal, xlabel="Soudspeed (m/s)", ylabel="Depth (m)", invert=True, title="SVP n°"+str(i+1)+" (Shallow)", legend=False)

        l_ax.append(ax)
        l_fig.append(fig)
        l_ax_shal.append(ax_shal)
        l_fig_shal.append(fig_shal)

    plt.show()