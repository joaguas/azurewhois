# azurewhois
Find if a/which service is associated with a particular Azure IP

# Why and how?

Azure updates (on a weekly basis give or take) a file that contains the IP address ranges for Public Azure (https://www.microsoft.com/en-us/download/details.aspx?id=56519)

While this file helps finding out what service an IP address is associated with, it can be tedious searching in which range a particular IP address fits (specially with overlapping masks) and periodically checking for a new version.

This script aims to solve both issues by automatically downloading the latest file available and doing the heavy-lifting work of matching an IP address to the prefix with the highest mask.

The file scraps the latest date from the page above and then uses the `pandas` library to build a dataframe from the dated .json file. It then uses `ipaddress` to check if your IP address is contained within a prefix and returns the associated Service Tag and region (when applicable).

# Installation and Usage

Portable binary (Linux distros / WSL only):
```
wget https://github.com/joaguas/azurewhois/raw/main/dist/azurewhois
chmod +x azurewhois
sudo mv azurewhois /usr/local/bin/
azurewhois 123.132.213.231
(if you don't want to make it globally available/have no permissions just run ./azurewhois 123.132.213.231 after the chmod command)
```

Running the script (All OS - requires pip to install necessary libraries):
```
wget https://raw.githubusercontent.com/joaguas/azurewhois/main/azurewhois.py -P azurewhois/
wget https://raw.githubusercontent.com/joaguas/azurewhois/main/requirements.txt -P azurewhois/
cd azurewhois
pip install -r requirements.txt
python azurewhois.py 123.132.213.231
```

