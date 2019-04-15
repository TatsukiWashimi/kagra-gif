from gwpy.timeseries import TimeSeriesDict
from gwpy.time import tconvert
import numpy as np

start = tconvert('Apr 13 2019 14:00:00 JST')
end = tconvert('Apr 13 2019 14:00:01 JST')
chname = [
    'K1:GIF-X_ANGLE_IN1_DQ',
    'K1:GIF-X_PPOL_IN1_DQ',
    'K1:GIF-X_SPOL_IN1_DQ']
data = TimeSeriesDict.fetch(chname,start,end,
                            host='10.68.10.121',port=8088)

angle = data['K1:GIF-X_ANGLE_IN1_DQ']
print np.rad2deg(angle[0].value)
print np.rad2deg(angle[10].value)
angle = angle.value[:100]
angle = np.unwrap(angle)
angle = np.rad2deg(angle)
ppol = data['K1:GIF-X_PPOL_IN1_DQ']
ppol = ppol.value
spol = data['K1:GIF-X_SPOL_IN1_DQ']
spol = spol.value
time = np.arange(len(angle))/2048.0
print time
import matplotlib.pyplot as plt
if False:
    fig, ax = plt.subplots(1,1,figsize=(8,8),dpi=160)
    ax.plot(ppol,spol,'ko',markersize=1)
    ax.plot((0,ppol[0]),(0,spol[0]),'yo-',markersize=10,linewidth=2)
    ax.plot((0,ppol[10]),(0,spol[10]),'ro-',markersize=10,linewidth=2)
    ax.plot(0,0,'ko',markersize=10)
    ax.set_xlabel('s [counts]')
    ax.set_ylabel('p [counts]')
    plt.savefig('hoge.png')
    plt.close()
    
if True:
    _time = np.arange(len(angle)+3)/2048.0    
    _angle = -360.0/(1.0/64.0)*_time + angle[0]
    fig, ax = plt.subplots(1,1,figsize=(8,8),dpi=160)
    ax.plot(time,angle,'ko',markersize=3)
    ax.plot(_time,_angle,'r-')
    ax.set_xlabel('Time [sec]')
    ax.set_ylabel('Angle [degree]')
    ax.set_yticks(np.arange(-360*3,361,360))
    ax.legend(['Result','Expected'])
    plt.savefig('huge.png')
    plt.close()
    