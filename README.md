# Sikuliaq_CTD_RBR_proc
## Setup
### Python environment
First, clone this repository. Then cd into the created directory. To create a Python venv :
```
python -m venv ./.venv
```
Then activate this venv
For Windows :
```
.venv/Scripts/activate
```
For Linux (could need sudo) :
```
source ./venv/bin/activate
```
You can then install all requirements with the command :
```
pip install -r requirements.txt
```
### Data
This repos only contains 1 example of each type of file (CTD, SVP and RBR). GitHub is not meant to store large amounts of data. So you will need to download from the ship disk the 10 CTD cnv files, the 10 SVP cnv files and the 8 RBR rsk files.
You should put the cnv files in the "CTD_Alaska" directory, while the rsk files go to the RBR_Alaska
## Tools
### Readers
The file "Readers.py" contains a set a class and tools to manipulate CTD, SVP and RBR files.
#### CTD
CTDs are represented by the class CTD_cnv, which is used to load the data and to get easily needed informations.
To declare a CTD_cnv :
```
path = "./CTD_Alaska/SKQ202409S_001.cnv"
ctd = CTD_cnv(path)
```
You can then access the data (Temperature, Pressure, PSalinity, Depths, Timestamps for the launch, coordinates, etc): 
```
l_temp = ctd.get_l_temp()
l_pres = ctd.get_l_pres()
l_psal = ctd.get_l_psal()
l_depth= ctd.get_l_depth()
l_ts_s = ctd.get_l_ts(unit="s")
l_ts_m = ctd.get_l_ts(unit="m")
l_ts_h = ctd.get_l_ts(unit="h")
lat, lon = ctd.get_lat(), ctd.get_lon()
```
You can also acces the starting time the CTD :
```
st = ctd.start_time
```
This object also contains methods meant to plot the data using matplotlib. You can plot :
the temperature profile :
```
fig, ax = plt.subplots()
ctd.scatter_TP(ax, s=2, marker="+", color="purple", label="CTD n°1")
```
the salinity profile on pressures :
```
fig, ax = plt.subplots()
ctd.scatter_SP(ax, s=2, marker="+", color="purple", label="CTD n°1")
```
Or the same graphs on the depth
```
fig, ax = plt.subplots()
ctd.scatter_TD(ax, s=2, marker="+", color="purple", label="CTD n°1")
ctd.scatter_SD(ax, s=2, marker="+", color="purple", label="CTD n°1")
```
You can then format the figures as an ocean profile using :
```
ax2profile(ax, xlabel="Temperature (°C)", ylabel="Depth (m)", zlabel="", title="My graph", invert = True)
plt.show()
```
(NB : The invert attribute descide if the Y axis should be inverted (positive pressure/depth) or not)
You can finally plot a 3D graph containing the Temperature, Salinity and Depth data :
```
fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ctd.scatter_3D_STD(ax, s=2, marker="+", color="purple", label="CTD n°1")
ax2profile(ax_STD, xlabel="PSal", ylabel="Temperature (°C)", zlabel="Depth (m)", title="Temp vs Depth", invert=False)
```
#### SVP
SVPs are represented by the class SVP_cnv. It is close to a CTD_cnv object. The only difference reside in the data you can extract. as Temperature, Salinity and Pressure are used to calculate the Sound speed, you cannot acces those informations. But you can acces Soundspeed. Their are theirfore the aditionnal scattering methods for soundspeed:
```
ctd.scatter_VD(ax, s=2, marker="+", color="orange", label="CTD n°1")
```
#### RBR
RBR files are differents. It devide the data in down and up profile of temperature vs pressure. One file can contain multiple profiles. To simplify the reading of this files, it is represented as the RBR class. This class was made to be used in the same was thant the cnv files. The difference reside in the fact that when you are asking for data, you need to give in input the direction (either "up" or "down"), and the index of the profile.
To load the file :
```
rbr = RBR("./RBR_Alaska/234446_20240621_1514.rsk")
```
You can get lists of Pressure, Temperature and timestamps :
```
l_temp = rbr.get_l_temp("up", 0)
l_pres = rbr.get_l_pres("up", 0)
l_ts   = rbr.get_l_ts("up", 0)
```
You can also get the time range of a up+down profile using :
```
tmin, tmax = rbr.get_time_range(0)
```
As for CDTs and SVPs, you can scatter the temperature profile :
```
fig, ax = plt.subplots()
rbr.scatter_TP(ax, "up", 0)
```
But also all down profiles or all up profiles
```
rbr.scatter_TP_all_down(ax)
rbr.scatter_TP_all_up(ax)
ax2profile(ax, xlabel="Temperature (°C)", ylabel="Depth (m)", zlabel="", title="My graph", invert = True)
```
