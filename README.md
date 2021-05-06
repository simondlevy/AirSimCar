# AirSimCar
Quickstart for driving the car in Microsoft AirSim on Windows computers

## 1. Get the AirSim executable for Windows

Download the following three files:

[CityEnviron.zip.001](https://github.com/microsoft/AirSim/releases/download/v1.4.0-windows/CityEnviron.zip.001) 

[CityEnviron.zip.002](https://github.com/microsoft/AirSim/releases/download/v1.4.0-windows/CityEnviron.zip.002) 

[CityEnviron.zip.003](https://github.com/microsoft/AirSim/releases/download/v1.4.0-windows/CityEnviron.zip.003) 

If you've installed a program like [WinRar](https://www.rarlab.com/download.htm), you should be able to double-click
on the CityEnviron.zip.001 to start the unzipping.  The clickable EXE file and support will be in a folder 
<b>CityEnviron/WindowsNoEditor</b>.

## 2. Install Python packages

```
pip install msgpack-rpc-python

pip install airsim

pip install opencv-python
```

## 3. Clone and drive

```
git clone https://github.com/simondlevy/AirSimCar
cd AirSimCar
python hello_car.py
```

## Tips

If your cursor disappears, you can recover it by hitting the F10 key to get
the Settings dialog, then clicking Close in the dialog.
