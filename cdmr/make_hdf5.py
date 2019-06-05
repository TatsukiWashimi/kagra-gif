import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from gwpy.plot import Plot
from gwpy.timeseries import TimeSeriesDict,TimeSeries
from gwpy.time import tconvert
from glue import lal
import sys
sys.path.insert(0,'../../miyopy')
from miyopy.utils.trillium import Trillium
from gwpy.frequencyseries import FrequencySeries
from astropy import units as u

'''
chname3_2.gwf data contains these bellow channels in JST Dec02 11:00 - Dec03 07.
chname3 list;
'K1:PEM-IXV_GND_TR120Q_X_IN1_DQ',
'K1:PEM-IXV_GND_TR120Q_Y_IN1_DQ',
'K1:PEM-IXV_GND_TR120Q_Z_IN1_DQ',
'K1:PEM-IXV_GND_TR120QTEST_X_IN1_DQ',
'K1:PEM-IXV_GND_TR120QTEST_Y_IN1_DQ',
'K1:PEM-IXV_GND_TR120QTEST_Z_IN1_DQ',
'K1:PEM-EXV_GND_TR120Q_X_IN1_DQ',
'K1:PEM-EXV_GND_TR120Q_Y_IN1_DQ',
'K1:PEM-EXV_GND_TR120Q_Z_IN1_DQ',
'K1:PEM-EYV_GND_TR120Q_X_IN1_DQ',
'K1:PEM-EYV_GND_TR120Q_Y_IN1_DQ',
'K1:PEM-EYV_GND_TR120Q_Z_IN1_DQ'

chname3_2_X.gwf data contains only X axis.

'''

def calc_asd(ts, fftlength=2**10):
    sg = ts.spectrogram2(fftlength=fftlength, overlap=fftlength/2., window='hanning') ** (1/2.)
    median_0,low_0,high_0 = sg.percentile(50), sg.percentile(5), sg.percentile(95)
    return median_0,low_0,high_0

chname3_x = ['K1:PEM-IXV_GND_TR120Q_X_IN1_DQ',
             'K1:PEM-IXV_GND_TR120QTEST_X_IN1_DQ',
             'K1:PEM-EXV_GND_TR120Q_X_IN1_DQ',]
chname4_x = [
    'K1:PEM-SEIS_IXV_GND_EW_IN1_DQ',
    'K1:PEM-SEIS_EXV_GND_EW_IN1_DQ',
    'K1:PEM-SEIS_EYV_GND_EW_IN1_DQ',
    ]



import argparse 
parser = argparse.ArgumentParser(description='description')
parser.add_argument('dataname', help='help')
parser.add_argument('--Plot')
args = parser.parse_args()


dataname = args.dataname
if dataname == 'chname3_1':
    start = tconvert('Dec 02 2018 11:00:00')
    end = start + 2**16
    chname = chname3_x
elif dataname == 'chname3_2':
    start = tconvert('Jan 01 2019 04:00:00')
    end = start + 2**16
    chname = chname3_x    
elif dataname == 'chname3_3':
    start = tconvert('Jan 02 2019 00:00:00')
    end = start + 2**16
    chname = chname3_x
elif dataname == 'chname4_1':
    start = tconvert('May 31 2019 00:00:00')    
    end = start + 2**16
    chname = chname4_x
elif dataname == 'chname4_2':
    start = tconvert('Jun 2 2019 00:00:00')    
    end = start + 2**16
    chname = chname4_x    
else:
    raise ValueError('Invalid data name')



    
data = TimeSeriesDict.read('./{dataname}/X.gwf'.format(dataname=dataname),chname,
                           format='gwf.lalframe',
                           start=start,
                           end=end,
                           pad=np.nan,
                           nproc=2,
                           verbose=True)
print('Read Done')

# Override unit of data from count to voltage.
c2v = (10.0/2**15)*u.V/u.ct # [1]

# [1] In the case of differential output.
if 'chname3' in dataname:
    exv_x = data['K1:PEM-EXV_GND_TR120Q_X_IN1_DQ']
    ixv1_x = data['K1:PEM-IXV_GND_TR120Q_X_IN1_DQ']
    ixv2_x = data['K1:PEM-IXV_GND_TR120QTEST_X_IN1_DQ']
elif 'chname4' in dataname:
    exv_x = data['K1:PEM-SEIS_EXV_GND_EW_IN1_DQ']
    ixv1_x = data['K1:PEM-SEIS_IXV_GND_EW_IN1_DQ']
    ixv2_x = data['K1:PEM-SEIS_EYV_GND_EW_IN1_DQ']
   
exv_x.override_unit('ct')#*c2v
ixv1_x.override_unit('ct')#*c2v
ixv2_x.override_unit('ct')#*c2v    
exv_x = exv_x*c2v
ixv1_x = ixv1_x*c2v
ixv2_x = ixv2_x*c2v
    

# Calc differential and common components.
diff12 = ixv1_x - ixv2_x
comm12 = ixv1_x + ixv2_x
diff13 = ixv1_x - exv_x
comm13 = ixv1_x + exv_x
print('calc in timeseries')

# Calc asd
median_0,low_0,high_0 = calc_asd(exv_x,fftlength=2**10)
print('calc asd done 1')
median_1,low_1,high_1 = calc_asd(ixv1_x,fftlength=2**10)
print('calc asd done 2')
median_2,low_2,high_2 = calc_asd(ixv2_x,fftlength=2**10)
print('calc asd done 3')
median_d12,low_d12,high_d12 = calc_asd(diff12,fftlength=2**10)
print('calc asd done 4')
median_c12,low_c12,high_c12 = calc_asd(comm12,fftlength=2**10)
print('calc asd done 5')
median_d13,low_d13,high_d13 = calc_asd(diff13,fftlength=2**10)
print('calc asd done 6')
median_c13,low_c13,high_c13 = calc_asd(comm13,fftlength=2**10)
print('calc asd done')

# Calibrate to velocity.    
amp = 10**(30/20.)
_v2vel = 1/1202.5*u.m/u.s/u.V
tr120q = Trillium('120QA')
v2vel = tr120q.v2vel
median_0,low_0,high_0 = v2vel(median_0)/amp, v2vel(low_0)/amp, v2vel(high_0)/amp
median_1,low_1,high_1 = v2vel(median_1)/amp, v2vel(low_1)/amp, v2vel(high_1)/amp
median_2,low_2,high_2 = v2vel(median_2)/amp, v2vel(low_2)/amp, v2vel(high_2)/amp
median_d12,low_d12,high_d12 = v2vel(median_d12)/amp, v2vel(low_d12)/amp, v2vel(high_d12)/amp
median_c12,low_c12,high_c12 = v2vel(median_c12)/amp, v2vel(low_c12)/amp, v2vel(high_c12)/amp
median_d13,low_d13,high_d13 = v2vel(median_d13)/amp, v2vel(low_d13)/amp, v2vel(high_d13)/amp
median_c13,low_c13,high_c13 = v2vel(median_c13)/amp, v2vel(low_c13)/amp, v2vel(high_c13)/amp



# Save data
def save(data,fname='tmp.hdf5',overwrite=True):
    data.write(fname,format='hdf5',overwrite=True)
    
if True:
    print('save')
    hdf5_fmt = './{dataname}/Xaxis_{sensor}_{pct}.hdf5'.replace("{dataname}",dataname)
    
    exv_fmt = hdf5_fmt.replace('{sensor}','exv')
    median_0.name = 'exv_x_50pct'
    low_0.name = 'exv_x_5pct'
    high_0.name = 'exv_x_95pct'    
    save(median_0, fname=exv_fmt.format(pct='50pct'),overwrite=True)
    save(low_0, fname=exv_fmt.format(pct='5pct'),overwrite=True)
    save(high_0, fname=exv_fmt.format(pct='95pct'),overwrite=True)
    
    ixv1_fmt = hdf5_fmt.replace('{sensor}','ixv1')    
    median_1.name = 'ixv1_x_50pct'
    low_1.name = 'ixv1_x_5pct'
    high_1.name = 'ixv1_x_95pct'
    save(median_1, fname=ixv1_fmt.format(pct='50pct'),overwrite=True)
    save(low_1, fname=ixv1_fmt.format(pct='5pct'),overwrite=True)
    save(high_1, fname=ixv1_fmt.format(pct='95pct'),overwrite=True)

    ixv2_fmt = hdf5_fmt.replace('{sensor}','ixv2')    
    median_2.name = 'ixv2_x_50pct'
    low_2.name = 'ixv2_x_5pct'
    high_2.name = 'ixv2_x_95pct'
    save(median_2, fname=ixv2_fmt.format(pct='50pct'),overwrite=True)
    save(low_2, fname=ixv2_fmt.format(pct='5pct'),overwrite=True)
    save(high_2, fname=ixv2_fmt.format(pct='95pct'),overwrite=True)    
    
    diff12_fmt = hdf5_fmt.replace('{sensor}','diff12')    
    median_d12.name = 'diff12_x_50pct'
    low_d12.name = 'diff12_x_5pct'
    high_d12.name = 'diff12_x_95pct'
    save(median_d12, fname=diff12_fmt.format(pct='50pct'),overwrite=True)
    save(low_d12, fname=diff12_fmt.format(pct='5pct'),overwrite=True)
    save(high_d12, fname=diff12_fmt.format(pct='95pct'),overwrite=True)    

    comm12_fmt = hdf5_fmt.replace('{sensor}','comm12')    
    median_c12.name = 'comm12_x_50pct'
    low_c12.name = 'comm12_x_5pct'
    high_c12.name = 'comm12_x_95pct'
    save(median_c12, fname=comm12_fmt.format(pct='50pct'),overwrite=True)
    save(low_c12, fname=comm12_fmt.format(pct='5pct'),overwrite=True)
    save(high_c12, fname=comm12_fmt.format(pct='95pct'),overwrite=True)    

    diff13_fmt = hdf5_fmt.replace('{sensor}','diff13')    
    median_d13.name = 'diff13_x_50pct'
    low_d13.name = 'diff13_x_5pct'
    high_d13.name = 'diff13_x_95pct'
    save(median_d13, fname=diff13_fmt.format(pct='50pct'),overwrite=True)
    save(low_d13, fname=diff13_fmt.format(pct='5pct'),overwrite=True)
    save(high_d13, fname=diff13_fmt.format(pct='95pct'),overwrite=True)    

    comm13_fmt = hdf5_fmt.replace('{sensor}','comm13')    
    median_c13.name = 'comm13_x_50pct'
    low_c13.name = 'comm13_x_5pct'
    high_c13.name = 'comm13_x_95pct'
    save(median_c13, fname=comm13_fmt.format(pct='50pct'),overwrite=True)
    save(low_c13, fname=comm13_fmt.format(pct='5pct'),overwrite=True)
    save(high_c13, fname=comm13_fmt.format(pct='95pct'),overwrite=True)
