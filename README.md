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
You can then access the data (Temperature, Pressure, PSalinity, Depths, Timestamps, coordinates, etc): 
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
ctd.scatter_SP(ax, s=2, marker="+", color="purple", label=" CTD n°1")
```
Or the same graphs on the depth
```
fig, ax = plt.subplots()
ctd.scatter_TD(ax, s=2, marker="+", color="purple", label=" CTD n°1")
ctd.scatter_SD(ax, s=2, marker="+", color="purple", label=" CTD n°1")
```
You can then format the figures as an ocean profile using :
```
fig, ax = plt.subplots()
```
#### SVP
SVPs are represented by the class SVP_cnv. It is close to a CTD_cnv object. The only difference reside in the data you can extract. as Temperature, Salinity and Pressure are used to calculate the Sound speed, you cannot acces those informations. But you can acces Soundspeed
```
ax2profile(ax, xlabel="Temperature (°C)", ylabel="Depth (m)", zlabel="", title="My graph", invert = True)
```
(NB : The invert attribute descide if the Y axis should be inverted (positive pressure/depth) or not)
