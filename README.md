# Introduction
This projects aim is to replace the stock firmware and software of persistance of vision spoke light displays, commonly named YQ8803.

# bSpokeLight
This project is heavily inspired by the awesome nomeata and his [bSpokeLight](https://github.com/nomeata/bSpokeLight) project.
This Repo would not exist without his work. The microcontroller firmware is his work with a few improvements.

# Installation
## Firmware
First of, compile the firmware with **sdcc**
If you are running ubuntu or debian, use
```
sudo apt install sdcc
```

Navigate to the ```firmware``` directory and run
```
make
```

## Tools
Use pip to install the python requirements
```
pip3 install -r requirements.txt
```

# Usage
Navigate to the ```src``` directory and run
```
python3 bikePovTool.py
```
