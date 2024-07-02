import os
from tqdm import tqdm
from Readers import RBR, CTD_cnv

if __name__ == '__main__':
    l_rbr_path = os.listdir("./RBR_Alaska")
    l_rbr_path = [os.path.join("./RBR_Alaska", path) for path in l_rbr_path]
    l_ctd_path = os.listdir("./CTD_Alaska")
    l_ctd_path = [path for path in l_ctd_path if path.split("_")[0] == "SKQ202409S"]
    l_ctd_path = [os.path.join("./CTD_Alaska", path) for path in l_ctd_path]

    l_rbr_path = [os.path.normpath(path).replace("\\", "/") for path in l_rbr_path]
    l_ctd_path = [os.path.normpath(path).replace("\\", "/") for path in l_ctd_path]

    print(os.path.normpath(l_ctd_path[0]).replace("\\", "/"))

    print("Loading RBRs ...")
    l_rbr = []
    for path in l_rbr_path:
        l_rbr.append(RBR(path))
    print("Loading CTDs ...")
    l_ctd = []
    for path in tqdm(l_ctd_path):
        l_ctd.append(CTD_cnv(path))

    corr_path = "./correspondance_semiauto.yml"
    with open(corr_path, 'w') as file:
        file.write("corr_list :\n")
        count = 0
        for ctd in tqdm(l_ctd):
            for rbr in l_rbr:
                for i in range(rbr.nb_profile):
                    tmin, tmax = rbr.get_time_range(i)
                    if tmin <= ctd.middle_time <= tmax:
                        file.write("  corr"+str(count)+" :\n")
                        file.write('    CTD_path : "' +r"{}".format(os.path.join(ctd.path))+'"\n')
                        file.write('    RBR_path : "' +r"{}".format(os.path.join(rbr.path))+'"\n')
                        file.write('    RBR_index : [' + str(max([i-1, 0]))+',' +str(i)+','+str(min([i+1, rbr.nb_profile-1]))+']\n')
                        file.write('    date : "'+str(ctd.start_time)+'"\n')
                        file.write('    mounting : "???"\n')
                        print("------")
                        print(tmin, ctd.start_time, tmax)
                        print(ctd.path)
                        print(rbr.path)
                        print(i)
                        print("------")
                        count += 1