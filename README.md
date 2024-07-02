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
The file "Readers.py"
