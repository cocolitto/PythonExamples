# python_live_plot.py

import random
import math
import numpy
from itertools import count
import tkinter
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('ggplot')

x_values = []
y_values = []
FahrTorq =      0;
FahrTorq_Filt = 0;
FahrRPM =       0;
FahrRPMFilt =   0;
FahrOmega =     0;
FahrPower =     0;
time_x =        0;
StreckTorq =    0;
StreckTorqFilt = 0;         
StreckRPM =     0;
StreckRPMFilt = 0;
StreckOmega =   0; 
StreckPower =   0; 
StreckPowerUnfiltered = 0; 
motorPower = 0;
motorPowerCorr = 0;
BikeSpeed = 0;
motorTorque = 0;
csv_path = 0;

index = count()
trackNMOffset=0.2752;#%0.3653;%0; % 0.4
driverNMOffset =-0.4935;#%-0.414;% 0;% -0.55
rRoll = 0.5/2;#%m


def livePlot(i):
    #data = pd.read_csv('eBike_Riese&Müller/191222/rawdata/TC_0009_3_78_04.1.23-16.37.csv',sep=';')
    data = pd.read_csv(csv_path.name,sep=';')
    data.columns = ["TimeStamp","Track_VOLT","Track_AMP","Track_CTRLVAL","Track_TIME","Track_C_DIST","Track_T_DIST","Track_F_TORQUE","Track_TORQUE","Track_RPM","Track_VELOC","Driver_VOLT","Driver_AMP","Driver_CTRLVAL","Driver_TIME","Driver_C_DIST","Driver_T_DIST","Driver_F_TORQUE","Driver_TORQUE","Driver_RPM","Driver_VELOC", "Driver_FRICTION_T","Driver_TRACK_T","Driver_WIND_T","Driver_ACC", " "]
    print(data.columns)
    print(data.dtypes)
    extractData(data=data)

    # clear axis
    ax1.cla()
    ax2.cla()
    ax3.cla()
    ax4.cla()

    #plt.plot(x_values, y_values)
    ax1.set_title("Driver Power [W]")
    ax1.plot(time_x, FahrPower, 'm') #row=0, col=0
    ax1.set_ylim(0,500)
    ax2.set_title("Driver Cadence [RPM]")
    ax2.plot(time_x, FahrRPM, 'b') #row=1, col=0
    ax2.set_ylim(0,150)
    ax3.set_title("eBike Motor Power ~ [W]")
    ax3.plot(time_x, motorPowerCorr, 'r') #row=0, col=1
    ax3.set_ylim(0,600)
    ax4.set_title("eBike Speed [km/h] RPM")
    ax4.plot(time_x, BikeSpeed, 'y') #row=1, col=1
    ax4.set_ylim(0,45)




def extractData(data):
    global FahrTorq      
    global FahrTorq_Filt 
    global FahrRPM     
    global FahrRPMFilt 
    global FahrOmega     
    global FahrPower     
    global time_x       
    global FahrPowerFilt
    global StreckTorq
    global StreckTorqFilt      
    global StreckRPM    
    global StreckRPMFilt
    global StreckOmega  
    global StreckPower
    global StreckPowerUnfiltered
    global motorPower
    global motorPowerCorr
    global BikeSpeed
    global motorTorque

    #Driverdata
    FahrTorq = data['Driver_TORQUE']/1000-driverNMOffset;
    FahrTorq_Filt = data['Driver_F_TORQUE']/1000-driverNMOffset;
    FahrRPM = data['Driver_RPM']/10;
    FahrRPMFilt = 0
    FahrOmega = FahrRPM*(2*math.pi*(1/60));
    FahrPower = FahrOmega * FahrTorq;
    FahrPowerFilt = FahrOmega * FahrTorq_Filt;
    time_x = numpy.cumsum(data['Track_TIME'])

    #Trackdata
    StreckTorq = -1*data['Track_TORQUE']/1000-trackNMOffset;
    StreckTorqFilt = -1*data['Track_F_TORQUE']/1000-trackNMOffset;  
    StreckRPM = data['Track_RPM']/10;
    StreckRPMFilt = 0
    StreckOmega = StreckRPM*(2*math.pi*(1/60));
    StreckPower = StreckOmega * StreckTorqFilt;
    StreckPowerUnfiltered = StreckOmega * StreckTorqFilt;

    #EBike Consumption                                        
    # motorTorque = motorPowerCorr./(2*pi*checkRawData.FahrRPMFilt/60);                                                                                  
    rRoll = 0.5/2;
    fac = 3.6;
    BikeSpeed = abs(StreckOmega)*rRoll*fac;

    #SystemLossData from Riese&Müller with FAZUA-Drive
    #systemlossResult(3).fitParam = [-1.79360544985198e-07,9.19506519498592e-05,-0.158336274055139,-0.793907546287248]
    motorPower = StreckPower - FahrPower;
    motorPowerCorr = motorPower + numpy.polyval([-1.79360544985198e-07,9.19506519498592e-05,-0.158336274055139,-0.793907546287248],StreckRPM); 
    motorTorque = motorPowerCorr/(2*math.pi*FahrRPM/60);    



fig = plt.figure()
ax1 = plt.subplot(2, 2, 1)
ax2 = plt.subplot(2, 2, 2)
ax3 = plt.subplot(2, 2, 3)
ax4 = plt.subplot(2, 2, 4)
tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
csv_path = filedialog.askopenfile()

ani = FuncAnimation(fig, livePlot, 1000)

plt.show()
