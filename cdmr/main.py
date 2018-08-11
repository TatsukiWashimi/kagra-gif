#
#! coding:utf-8
from __future__ import print_function
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['agg.path.chunksize'] = 1000000
import numpy as np
from scipy.signal import butter, lfilter
from scipy import signal, interpolate
from control import matlab
from trillium import selfnoise,V2Vel
from tips import *
from plot import *
import os
import re
import platform
try:
    import nds2
    import gwpy    
    from miyopy.timeseries import TimeSeries as ts
    from gwpy.timeseries import TimeSeries
except:
    pass

c2V = 10.0/2**15
deGain_compact = 10.0**(-45.0/20.0)
deGain_120QA = 10.0**(-30.0/20.0)

system = platform.system()
if system=='Darwin':
    prefix = '/Users/miyo/data/'
elif system=='Linux':
    prefix = './'
else:
    raise UserWarning('Invalid computer system; {}'.format(system))


tlen = 2**13

def rm_nandata(data_fname):
    print('Finding nan data file...')
    for fname in data_fname:
        with open(prefix+fname,'rb') as f:
            data = np.load(f)
            if True in np.isnan(data):
                os.remove(prefix+fname)
                print('remove {}'.format(prefix+fname))
    print('Done.')

def does_data_exist(start,end,startlist,endlist):
    if start not in startlist:
        errortxt = 'Invalid start time; {0}\n'\
                   'Please choose start time in \n {1}'\
                   .format(start,(startlist))
        raise ValueError(errortxt)
    if end not in endlist or end<start:
        endlist = filter(lambda x:x>start,endlist)
        errortxt = 'Invalid end time; {0}\n'\
                   'Please choose end time in \n {1}'\
                   .format(end,(endlist))
        raise ValueError(errortxt)
    if end-start!=2**13:
        raise UserWarning('tlen is not 2**13.')
    
    return start,end
        
    
def get_time(rm_nandata=False):
    list = os.listdir(prefix)
    data_fname = filter(lambda x :re.match("121.*121.",x) ,list)
    start_end = np.array(map(lambda x:re.findall('[0-9]{10}',x),data_fname),
                         dtype=np.int32)
    startlist = np.unique(start_end[:,0])
    startlist = np.sort(startlist)
    endlist = np.unique(start_end[:,1])   
    endlist = np.sort(endlist)    
    if len(startlist)!=len(endlist):
        raise UserWarning('!')
    
    if rm_nandata:
        rm_nandata(data_fname)

    argvs = sys.argv  
    argc = len(argvs)
    if (argc == 3):
        start = int(argvs[1])
        end = int(argvs[2])
    else:
        raise ValueError('Usage:python {} <starttime> <endtime>'.format(argvs[0]))
    
    start, end = does_data_exist(start,end,startlist,endlist)
    return start,end


def download_gifdata(start,end,chname='CALC_STRAIN'):
    print('taking data from gif')
    data = ts.read(start,end-start,chname)
    value = data.value
    print('done')
    print('saving data')
    fname = prefix+'{0}_{1}_{2}'.format(start,end,chname[3:])        
    with open(fname,'w') as f:
        np.save(f,value)
    print('done')
    return value


chnames = ['K1:PEM-EXV_SEIS_WE_SENSINF_IN1_DQ',
           'K1:PEM-EXV_SEIS_NS_SENSINF_IN1_DQ',
           'K1:PEM-EXV_SEIS_Z_SENSINF_IN1_DQ',
           'K1:PEM-EYV_SEIS_WE_SENSINF_IN1_DQ',
           'K1:PEM-EYV_SEIS_NS_SENSINF_IN1_DQ',
           'K1:PEM-EYV_SEIS_Z_SENSINF_IN1_DQ',
           'K1:PEM-IXV_SEIS_WE_SENSINF_IN1_DQ',
           'K1:PEM-IXV_SEIS_NS_SENSINF_IN1_DQ',
           'K1:PEM-IXV_SEIS_Z_SENSINF_IN1_DQ',
           #'K1:PEM-IY0_SEIS_WE_SENSINF_OUT16',
           #'K1:PEM-IY0_SEIS_NS_SENSINF_OUT16',
           'K1:PEM-IMC_SEIS_MCI_NS_SENSINF_IN1_DQ',
           'K1:PEM-IMC_SEIS_MCE_NS_SENSINF_IN1_DQ',
           'K1:PEM-IMC_SEIS_MCI_WE_SENSINF_IN1_DQ',
           'K1:PEM-IMC_SEIS_MCE_WE_SENSINF_IN1_DQ',
           'K1:PEM-IMC_SEIS_MCI_Z_SENSINF_IN1_DQ',
           'K1:PEM-IMC_SEIS_MCE_Z_SENSINF_IN1_DQ', 
           'K1:PEM-IXV_SENSOR1_OUT_DQ',
           ]

    
def download_kagradata(start,end,chname=None):
    if chname==None:
        raise ValueError('Invalid chname name; {}'.format(chname))
    
    fname = prefix+'{0}_{1}_{2}'.format(start,end,chname[3:])
    print('data taking {}'.format(chname))
    data = TimeSeries.fetch(chname,
                            start, end,
                            host='10.68.10.121', port=8088)
    data =  data.value 
    print('done')
    print('save')
    fname = prefix+'{0}_{1}_{2}'.format(start,end,chname[3:])        
    with open(fname,'w') as f:
        np.save(f,data)
    return data


def read(chname):
    fname = prefix+'{0}_{1}_{2}'.format(start,end,chname[3:])
    try:
        with open(fname,'rb') as f:
            value = np.load(f)
    except Exception as e:
        print(e)
        if 'K1' not in chname:
            value = download_gifdata(start,end,chname=chname)
        else:
            value = download_kagradata(start,end,chname=chname)
    return value





if __name__ == '__main__':
    #start,end = get_time()
    start,end = 1217926818, 1217926818+2**13
    if start==1214784018:
        #adc = read('K1:PEM-IXV_SENSOR1_OUT_DQ')            
        exx = read('K1:PEM-EX1_SEIS_WE_SENSINF_OUT_DQ') # vel
        exy = read('K1:PEM-EX1_SEIS_NS_SENSINF_OUT_DQ') # vel
        ixx = -1.0*read('K1:PEM-IX1_SEIS_WE_SENSINF_OUT_DQ') # vel
        ixy = -1.0*read('K1:PEM-IX1_SEIS_NS_SENSINF_OUT_DQ') # vel
    else:
        #adc = read('K1:PEM-IXV_SENSOR1_OUT_DQ')
        #gifx = read('CALC_STRAIN')
        exx = read('K1:PEM-EXV_SEIS_WE_SENSINF_IN1_DQ')*deGain_120QA*c2V
        exy = read('K1:PEM-EXV_SEIS_NS_SENSINF_IN1_DQ')*deGain_120QA*c2V
        exz = read('K1:PEM-EXV_SEIS_Z_SENSINF_IN1_DQ')*deGain_120QA*c2V
        eyx = read('K1:PEM-EYV_SEIS_WE_SENSINF_IN1_DQ')*c2V
        eyy = read('K1:PEM-EYV_SEIS_NS_SENSINF_IN1_DQ')*c2V
        eyz = read('K1:PEM-EYV_SEIS_Z_SENSINF_IN1_DQ')*c2V
        ixx = read('K1:PEM-IXV_SEIS_WE_SENSINF_IN1_DQ')*c2V
        ixy = read('K1:PEM-IXV_SEIS_NS_SENSINF_IN1_DQ')*c2V
        ixz = read('K1:PEM-IXV_SEIS_Z_SENSINF_IN1_DQ')*c2V
        mcey = read('K1:PEM-IMC_SEIS_MCE_NS_SENSINF_IN1_DQ')*deGain_compact*c2V
        mciy = read('K1:PEM-IMC_SEIS_MCI_NS_SENSINF_IN1_DQ')*deGain_compact*c2V
        mcez = read('K1:PEM-IMC_SEIS_MCE_Z_SENSINF_IN1_DQ')*deGain_compact*c2V
        mciz = read('K1:PEM-IMC_SEIS_MCI_Z_SENSINF_IN1_DQ')*deGain_compact*c2V      
    
    # --------------------
    # プロットするデータセットの準備
    # --------------------           
    if True:
        # Xアームの基線長伸縮を比較するためのデータセット
        diff = (exx-ixx)/np.sqrt(2.0) # V
        comm = (exx+ixx)/np.sqrt(2.0) # V
        data1 = [diff,comm,gifx*3.0e3/np.sqrt(2.0)] # [V, V, m] に注意
        labels11 = ['(Xend-Center)/sqrt(2) : Diff','(Xend+Center)/sqrt(2) : Com','GIFx']
        labels12 = ['Com/Diff','Com/GIFx']
        
    if True:
        # Xアームの基線長伸縮を比較するためのデータセット
        data9 = [exx/5500,ixx/5500,gifx] # [V, V, m] に注意
        labels91 = ['(Xend-Center)/sqrt(2) : Diff','(Xend+Center)/sqrt(2) : Com','GIFx']
        labels92 = ['Com/Diff','Com/GIFx']        
    if False:
        # Yアームの基線長伸縮
        diff = (eyy-ixy)/np.sqrt(2.0)
        comm = (eyy+ixy)/np.sqrt(2.0)
        data5 = [diff, # V
                 comm, # V
                 #adc # V
                ]
        labels51 = ['(Yend-Center)/sqrt(2) : Diff','(Yend+Center)/sqrt(2) : Com','--']
        labels52 = ['Com/Diff', 'None','ADC']
    if False:
        # IMCの基線長伸縮を比較するためのデータセット        
        diff = (mciy-mcey)/np.sqrt(2.0)
        comm = (mciy+mcey)/np.sqrt(2.0)
        data2 = [diff, # V
                 comm, # V
                 #adc*c2V # V
                ] 
        labels21 = ['(MCiy-MCey)/sqrt(2) : Diff','(MCiy+MCey)/sqrt(2) : Com','---']
        labels22 = ['Com/Diff','Com/GIF','---']
    if True:
        # Xエンドとセンターの地震計
        fs = float(len(exx)/tlen)
        data3 = [exx, # V
                 ixx, # V
                 #adc, # V
                 ]
        labels31 = ['Xend','Center','ADC(Center)','ADC(Xend)']
        labels32 = ['Xend','Center','ADC(Center)','ADC(Xend)']
    if True:
        # Yエンドとセンターの地震計
        fs = float(len(eyy)/tlen)
        data6 = [eyy,
                 ixy,
                 #adc*c2V
                ]
        labels61 = ['Yend','Center','ADC(Center)']
        labels62 = ['Yend','Center','ADC(Center)']
    if True:
        # MCi,MCeの地震計
        fs = float(len(mciy)/tlen)
        data4 = [mciy, # V
                 mcey, # V
                 #adc # V
                 ]
        labels41 = ['MCi','MCe','ADC']
        labels42 = ['MCi','MCe','ADC']
    # ---------------
    # プロット
    # ---------------
    
    if True:
        # -----------------
        # プロット : 時系列
        # -----------------
        plot41_blrms_timeseries(ixx/749.1,
            tlen=tlen,
            title='IXVx',
            fname='Timeseries-IXVx',
            unit='m/s'
            )
        #exit()        
        plot41_blrms_timeseries(exx/1202.5,
            tlen=tlen,
            title='EXVx',
            fname='Timeseries-EXVx',
            unit='m/s'
            )
        exit()
        plot_timeseries(data4,
            tlen=tlen,
            title='Timeseries',
            fname='Timeseries-MCi_MCe',
            labels1=labels41,
            labels2=labels42,
            )
        exit()
    if False:
        # ---------------- 
        # プロット : CDMR  
        # ----------------
        plot21_cdmr(data1,
            start=start,
            tlen=tlen,            
            title='Common Differential Mode Rate (CDMR) on the X-Arm Bedrock',
            fname='cdmr_xarm_gifx',
            labels1=labels11,
            labels2=labels12,
            model='comm/gifx',
            linestyle=['k-','k:','r-'],
            adcnoise=True,
            selfnoiseplot=True,
            trillium='120QA',            
            )
        print('cdmr_xarm_gif done')
        exit()
        plot21_cdmr(data1,
            start=start,                    
            tlen=tlen,
            title='Common Differential Mode Rate (CDMR) on the X-Arm Bedrock',
            fname='cdmr_xarm_seis',
            labels1=labels11,
            labels2=labels12,
            model='comm/diff',
            linestyle=['k-','k:','r-'],            
            adcnoise=True,
            selfnoiseplot=True,
            trillium='120QA',          
            )
        plot21_cdmr(data2,
            start=start,                    
            tlen=tlen,
            title='Common Differential Mode Rate (CDMR) on the IMC Bedrock',
            fname='cdmr_imc',
            labels1=labels21,
            labels2=labels22,
            L=20,
            linestyle=['k-','k:','r-'],            
            adcnoise=True,
            selfnoiseplot=True,
            trillium='compact',            
            )        
        plot21_cdmr(data5,
            start=start,                    
            tlen=tlen,
            title='Common Differential Mode Rate (CDMR) on the Y-Arm Bedrock',
            fname='cdmr_yarm',
            labels1=labels51,
            labels2=labels52,
            linestyle=['k-','k:','r-'],            
            adcnoise=True,
            selfnoiseplot=True,
            trillium='120QA',           
           )
        #exit()    
    if True:
        # ----------------
        # プロット : ASD
        # ----------------
        plot(data1,
            start=start,             
            tlen=tlen,
            title='Seismometer at the EXV and IXV, and GIFx',
            fname='ASD-EXV_IXV_GIFX',
            labels1=labels11,
            labels2=labels12,
            adcnoise=True,
            selfnoise=True,
            trillium='120QA',
            unit='m'
            )
        #exit()        
        print('asd exv,ixv,gifx')
        plot(data9,
            start=start,             
            tlen=tlen,
            title='Seismometer at the EXV and IXV, and GIFx',
            fname='ASD-EXV_IXV_GIFX_strain',
            labels1=labels11,
            labels2=labels12,
            adcnoise=True,
            selfnoise=True,
            unit='strain',
            trillium='120QA'                        
            )
        exit()
        print('asd exv,ixv,gifx')        
        plot(data3,
            start=start,             
            tlen=tlen,
            title='Seismometer at the EXV and IXV',
            fname='ASD-EXV_IXV',
            labels1=labels31,
            labels2=labels32,
            adcnoise=True,
            selfnoise=True,
            trillium='120QA'                        
            )
        print('asd exv,ixv')
        plot(data6,
            start=start,             
            tlen=tlen,
            title='Seismometer at the EYV and IXV',
            fname='ASD-EYV_IXV',         
            labels1=labels61,
            labels2=labels62,
            adcnoise=True,
            selfnoise=True,
            trillium='120QA'            
            )    
        print('asd eyv,ixv')
        plot(data4,
            start=start,             
            tlen=tlen,
            title='Seismometer at the MCi and MCe',
            fname='ASD-MCi_MCe',
            labels1=labels41,
            labels2=labels42,
            adcnoise=True,
            selfnoise=True,
            linestyle=['r-','b-'],
            trillium='compact'
            )
        print('asd mci,mce')  
    if True:
        # ---------------------
        # プロット : Coherence
        # ---------------------        
        plot21_coherence(data3,
            start=start,                         
            tlen=tlen,
            title='Seismometer at the EXV and IXV',
            fname='Coherence-EXV_IXV',
            labels1=labels31,
            labels2=labels32,
            adcnoise=True,            
            )        
        plot21_coherence(data6,
            start=start,                         
            tlen=tlen,
            title='Seismometer at the EYV and IXV',
            fname='Coherence-EYV_IXV',         
            labels1=labels61,
            labels2=labels62,
            adcnoise=True,            
            )            
        plot21_coherence(data4,
            start=start,                         
            tlen=tlen,
            title='Seismometer at the MCi and MCe',
            fname='Coherence-MCi_MCe',         
            labels1=labels41,
            labels2=labels42,
            adcnoise=True,            
            )   