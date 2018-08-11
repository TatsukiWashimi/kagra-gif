#
#! coding:utf-8

import sys 
import numpy as np
from scipy import signal
from miyopy.types import Seismometer,Timeseries
import miyopy.io.reader as reader
import miyopy.plot as mpplot
import subprocess
from scipy.signal import spectral
from miyopy.parse.arg import get_gpstime
import pickle


EQ_name = {
    'Tottori':[1207240372,2**12],
    'Tottori_P-Wave':[1207240372,2**12],
    'Kimbe':[1206093078,32*2*64],
    'Kimbe_P-Wave':[1206093078+440,2**7],
    'Kimbe_S-Wave':[1206093078+800,2**11],
    'Kimbe_S-Wave':[1206093078+1200,2**9],
    'Kimbe_Other-Wave':[1206093078+1200,2**11],        
    'Saumlaki':[1206044105,32*2*32],
    'Hachijo-jima':[1206027402,32*2*64],
    'Example_MidNight':[1207407618,2**10], # 4/10 24:00
    'Example_MidNight':[1207407618,2**10], # 4/10 24:00
    'Example_MidNight2':[1207411218,2**10], # 4/10 25:00
    'Example_MidNight_Long':[1207234818,2**15], # 4/08 24:00        
    'Example_MidNight_Long2':[1207152018,2**16], # 4/08 24:00
    'Example_Night_Long':[1207213218,2**15], # 4/08 24:00
    'Example_Long_1day':[1207440018,2**16], # 04/11 09:00, 18hour
    #'Example_Long_1day':[1207440018,2**10], # 04/11 09:00, 18hour
    '0413_20h00m':[1207652418,2**16], # 04-13-20:00 - 
    # - 28000,52000ごろにひずみが飛んでいる箇所がある。
    # - 34000から50000なら歪は線形にみなせる。
    '0413_20h00m_LinearTidal':[1207652418+34000,2**14], #
    #
    '0413_20h00m_Tidal':[1207652418,2**14], #
    # ひずみは上に凸になっているけど、飛んでる箇所はない  
    #'0413_20h00m':[1207652418,2**13], # 2**13 Ok KAGRA,GIF, 2**16made
    # - 
    '0416_00h00m':[1207839618,2**13], #2**15made
    '0416_13h00m':[1207886418,2**13], # 2**13 ok 
    '0416_16h00m':[1207897218,2**13], # OK
    '0416_19h00m':[1207908018,2**13], # OK
    '0416_22h00m':[1207918818,2**13], # OK
    '0417_01h00m':[1207929618,2**13], # OK 
    '0417_17h00m':[1207987218,2**13], # OK,2**16 made
    '0417_20h00m':[1207998018,2**13], # OK ,2**16 made
    '0417_23h00m':[1208008818,2**13], # OK ,2**16 made
    '0421chiba_all':[1208339257-2**10+100,2**11],
    '0421chiba_p':[1208339257+45,2**4],
    '0421chiba_pslove':[1208339257+45,2**7],
    '0421chiba_ps':[1208339257+40,2**6],
    '0421chiba':[1208339257-2**10,2**7],
    '0423shimane':[1208448078-2**6,2**9],
    '0425_heavy_rain':[],
    '0425_00':[1208617218,2**16], # 04-25-00:00
    # - cRIO02_data/2018/04/25/10/1804251042.AD02 lack
    # - cRIO02_data/2018/04/25/11/1804251109.AD02 lack
    '0425_00_1':[1208617218,2**15], # 04-25-00:00    
    '0425_00_1_LinearTidal':[1208617218+15000,2**14], # 04-25-00:00
    # 
    # 
    '0424_23':[1208617218-3600,2**10],
    '0424_18':[1208595618,2**17], # start 04-24-18:00
    # 大雨で地面が揺れ始めた頃のデータ
    # - cRIO02_data/2018/04/25/10/1804251042.AD02 0が空
    # - cRIO02_data/2018/04/25/11/1804251109.AD02 0が空
    '0426_18':[1208769618,2**17], # start 04-26-18:20 
    # - cRIO02_data/2018/04/26/20/1804262055.AD02 が空
    # - cRIO02_data/2018/04/27/06/1804270627.AD02 が空
    # - cRIO02_data/2018/04/27/07/1804270725.AD02 が空
    # - cRIO02_data/2018/04/27/19/1804271943.AD02 が空
    '0426_18_1':[1208769618,2**16], # start 04-26-18:20
    # - cRIO02_data/2018/04/26/20/1804262055.AD02 が空
    # - cRIO02_data/2018/04/27/06/1804270627.AD02 が空
    # - cRIO02_data/2018/04/27/07/1804270725.AD02 が空    
    #
    '0426_18_2':[1208769618,2**15], # start 04-26-18:20
    # - cRIO02_data/2018/04/26/20/1804262055.AD02 が空
    #
    '0426_18_3':[1208769618,2**13], # start 04-26-18:20
    #
    '0428_09':[1208908938,2**17], # start04-28-09:02
    #'0428_09_':[1208908938+92400,1000], # start04-28-09:02,
    '0428_09_1':[1208908938,2**16], # start04-28-09:02,
    # 大雨が過ぎた頃のデータ
    # - cRIO03_data/2018/04/28/15/1804281554.AD00 が空
    # - cRIO03_data/2018/04/28/15/1804281559.AD00 が空
    '0428_09_2':[1208908938+93400,2**16], # JST start04-29-10:58
    # 開始手前1000秒前から200秒間データがおかしい。DAQのメンテナンスが原因。
    # - 欠損無し。
    '0428_09_2_LinearTidal':[1208908938+93400+10000,2**14], # JST start04-29-10:58    
    # 1208908938+92400から200秒データがおかしい
    # 2018-04-29 JST 10:42:00から200秒
    #'0430_09_2':[1208908938,2**16], # start04-28-
    #'0430_22':[1209128418,2**14] #[data] JST 04-30-22:00 many lockloss!
    '0429_22':[1209042018,2**14], #[data] JST 04-29-22:00
    '0418_00_STRAIN':[1208044818,2**20], #[data] JST
    '0502_12':[1209267078,2**17], # [data] JST 05-02-12:31
    '0502_15':[1209267078+3600*3,2**15], # [data] JST 05-02-12:31
    '0502_10':[1209258738,2**13], # [data] JST 05-02-10:12
    '0504_00':[1209427218,2**7], # [data] JST 05-04-09:00
    '0502_09-10':[1209254418,2**13], # [data] JST 05-02-09:00 (include lack of data)
    'Phase1':[1208908818,2**20] # JST04-28-09:00 about 12days
    }
    
def main_plotSeismometerSepctrogram(*args,**kwargs):
    '''X,Y,Centerそれぞれの3軸についてスペクトログラムを描く。       
    
    Parameter
    ---------
    args : t0, tlen, title
    
    '''
    from miyopy.plot.plotspectrogram import plotspectrogram
    theta = 0.0
    ex1 = Seismometer(t0,tlen,'EX1')    
    ey1 = Seismometer(t0,tlen,'EY1')
    cen = Seismometer(t0,tlen,'IY0')    
    ave = 16
    ex1._rotate(theta)
    ey1._rotate(theta)
    cen._rotate(theta)
    for seismo in [ex1,ey1,cen]:
        for axis in ['x','y','z']:
            fname_fmt = '{0}Spectrogram_{1}_{2}_{3}_{4:03d}.png'
            fname = fname_fmt.format(title,
                                     t0,
                                     tlen,
                                     getattr(seismo,axis)._name,
                                     int(theta))
            plotspectrogram(getattr(seismo,axis).timeseries,
                            getattr(seismo,axis)._fs,
                            outfile=fname,
                            wlen=512,
                            log=True,
                            clip=[0,1],
                            per_lap=0.9)
                

def main_Lock(*args):
    channels = ['K1:VIS-BS_TM_OPLEV_SERVO_PIT_OFFSET',
                #'K1:VIS-BS_TM_OPLEV_SERVO_YAW_OFFSET',
                'K1:VIS-BS_IM_LOCK_L_OUT16',
                'K1:GRD-LSC_MICH_STATE_N']
    data = reader.kagra.readKAGRAdata(t0,tlen,channels)
    label=['Time','Value']
    filename = '{0}/TimeseriesMultPlot_{1}_{2}.png'.format(title,t0,tlen)
    legend = [d_._name for d_ in data]
    mpplot.MultiPlot_new(data,label,filename,legend)
    

def main_StrainmeterSignalBudjet(theta=0.0,*args):
    X1500_TR = Seismometer(t0,tlen,
                             'X1500_TR240',
                             plot=True,
                             detrend=True,
                             title=title,
                                 )
    X1500_TR_X = X1500_TR.x
    X1500_TR_Z = X1500_TR.z
    GIF_X = reader.gif.readGIFdata(t0,tlen,
                                   'CALC_STRAIN',
                                   name='X_strainmeter',
                                   plot=True,
                                   detrend=True,
                                   title=title,
                                       )
    X500_BARO = reader.gif.readGIFdata(t0,tlen,
                                       'X500_BARO',
                                       name='x500_pressure',
                                       plot=True,detrend=True,
                                       title=title,
                                           )
    X2000_BARO = reader.gif.readGIFdata(t0,tlen,
                                        'X2000_BARO',
                                        name='x2000_pressure',
                                        plot=True,detrend=True,
                                        title=title,
                                            )
    #
    # 1. 0413_20h00m_LinearTidal
    # 2. 0425_00_1_LinearTidal    
    # 3. 0428_09_2_LinearTidal
    # convert
    X1500_TR_X = X1500_TR_X/5500.0
    X1500_TR_Z = X1500_TR_Z/5500.0
    X500_BARO = X500_BARO*0.55e-9
    X2000_BARO = X2000_BARO*0.55e-9
    # psd
    ave = 16
    GIF_X.get_psd(ave=ave,plot=False)
    X1500_TR_X.get_psd(ave=ave,plot=False,TF_240=True)
    X1500_TR_Z.get_psd(ave=ave,plot=False,TF_240=True)
    X500_BARO.get_psd(ave=ave,plot=False)
    X2000_BARO.get_psd(ave=ave,plot=False)
    #
    datalist = [GIF_X,
                X1500_TR_X,
                X1500_TR_Z,
                X500_BARO,
                ]
    mpplot.plotspectrum(datalist,label=['Frequency [Hz]','Strain [1/rtHz]'],lim=([1e-3,6],[1e-13,1e-8]),filename='{0}StrainmeterSignalBudget_{1:03d}'.format(title,theta))
    
    
def main_coherence(*args):
    GIF_X = reader.gif.readGIFdata(t0,tlen,
                                   'CALC_STRAIN',
                                   name='X_strainmeter',
                                   plot=True,
                                   detrend=True,
                                       title=title,                                   
                                       )
    X500_BARO = reader.gif.readGIFdata(t0,tlen,
                                       'X500_BARO',
                                       name='x500_pressure',
                                       plot=True,detrend=False,
                                       title=title,
                                           )                                           
    X2000_BARO = reader.gif.readGIFdata(t0,tlen,
                                       'X2000_BARO',
                                       name='x2000_pressure',
                                       plot=True,detrend=True,
                                       title=title,
                                            )
    X1500_TR_X = Seismometer(t0,tlen,
                             'X1500_TR240',
                             plot=True,
                             detrend=True,
                             title=title,
                                 ).x    
    GIF_X.get_coherence(X500_BARO,ave=16,plot=True,title=title)
    GIF_X.get_coherence(X1500_TR_X,ave=16,plot=True,title=title)
    X2000_BARO.get_coherence(X500_BARO,ave=16,plot=True,title=title)
    X2000_BARO.get_coherence(X1500_TR_X,ave=16,plot=True,title=title)


def main_GIFspectrogram(*args):
    GIF_X = reader.gif.readGIFdata(t0,tlen,
                                   'CALC_STRAIN',
                                   name='X_strainmeter',
                                   plot=False,
                                   detrend=True)
    X500_BARO = reader.gif.readGIFdata(t0,tlen,
                                       'X500_BARO',
                                       name='x500_pressure',
                                       plot=False,detrend=True)
    for data in [GIF_X,X500_BARO]:
        fname_fmt = '{0}Spectrogram_{1}_{2}_{3}.png'
        fname = fname_fmt.format(title,
                                 t0,
                                 tlen,
                                 data._name,
                                    )
        mpplot.plotspectrogram(data.timeseries,
                               data._fs,
                               outfile=fname,
                               wlen=256,
                               log=True,
                               auto_frange=True,
                                   clip=[0,1],
                                   flim=[1e-13,1e-8],
                                   per_lap=0.9)  
    pass    


def main_strain(init=False,save=False,load=True):
    EQ_name = {'0418_00_STRAIN':[1208044818,2**20]}
    event = '0418_00_STRAIN'
    t0,tlen = EQ_name[event]
    title = '../event/{0}'.format(event)
    #
    if init:
        GIF_X = reader.gif.readGIFdata(t0,tlen,
                                    'CALC_STRAIN',
                                    name='X_strainmeter',
                                    plot=True,
                                    detrend=True)    
    if save:
        print 'saving...'
        with open('0418_00_STRAIN.pickle', mode='wb') as f:
            pickle.dump(GIF_X, f)
    if load:
        print 'loading...'
        with open('0418_00_STRAIN.pickle', mode='rb') as f:
            GIF_X = pickle.load(f)
    #
    gotic = reader.gotic.readGOTICdata(t0,tlen,'Xarm',plot=True,detrend=False)
    #
    import matplotlib.pyplot as plt
    plt.plot(GIF_X._time,GIF_X.timeseries,label=GIF_X._name)
    plt.plot(gotic._time,gotic.timeseries,label=gotic._name)
    plt.savefig('hoge.png')
    plt.close()


def main_compare(*args):
    #data = reader.kagra.readKAGRAdata(t0,tlen,channels)
    ex1 = Seismometer(t0,tlen,'EX1')
    ex1.x.plot()

    
def main_plotlongtime(*args):
    print args
    chname = ['K1:PEM-EX1_SEIS_NS_SENSINF_OUT16']
    ex1_ns_rms = reader.kagra.readKAGRAdata(t0,tlen,chname)[0]
    ex1_ns_rms.plot()

    
def main_CMMR(*args):
    pass


def main_cmrr(*args):
    ex1 = Seismometer(t0,tlen,'EX1',title=title)
    cen = Seismometer(t0,tlen,'IY0',title=title)
    hoge = Seismometer(t0,tlen,'IY0',title=title)
    hoge.x.timeseries = ex1.x.timeseries-cen.x.timeseries
    hoge.x._name='Xend-Center'
    X500_BARO = reader.gif.readGIFdata(t0,tlen,
                                       'X500_BARO',
                                       name='x500_pressure',
                                       plot=True,detrend=False,
                                       title=title,
                                           )                                           
    X2000_BARO = reader.gif.readGIFdata(t0,tlen,
                                       'X2000_BARO',
                                       name='x2000_pressure',
                                       plot=True,detrend=True,
                                       title=title,
                                            )    
    gif_x = reader.gif.readGIFdata(t0,tlen,
                                   'CALC_STRAIN',
                                   name='X_strainmeter',
                                   plot=True,
                                   detrend=True)
    X1500_TR = Seismometer(t0,tlen,
                             'X1500_TR240',
                             plot=True,
                             detrend=True)
    X1500_TR_X = X1500_TR.x
    X1500_TR_Z = X1500_TR.z 
    X1500_TR_X = X1500_TR_X#/5500.0#*3000.0
    ex1.x = ex1.x/5500.0
    ex1.z = ex1.z/5500.0
    cen.x = cen.x/5500.0
    cen.z = cen.z/5500.0
    X1500_TR_Z = X1500_TR_Z/5500.0#*3000.0
    X500_BARO = X500_BARO*0.55e-9
    X2000_BARO = X2000_BARO*0.55e-9    
    gif_x.timeseries = gif_x.timeseries*3000.0
    hoge.x.timeseries = hoge.x.timeseries#/3000.0
    #
    ave = 16    
    #
    integ=True
    hoge.x.get_psd(ave=ave,integ=integ)
    ex1.x.get_psd(ave=ave,integ=integ,TF_120=True)
    ex1.z.get_psd(ave=ave,integ=integ,TF_120=True)
    cen.x.get_psd(ave=ave,integ=integ,TF_120=True)
    cen.z.get_psd(ave=ave,integ=integ,TF_120=True)
    X1500_TR_X.get_psd(ave=ave,integ=integ,TF_240=True)
    X1500_TR_Z.get_psd(ave=ave,integ=integ,TF_240=True)
    gif_x.get_psd(ave=ave)
    X500_BARO.get_psd(ave=ave)
    #mpplot.plotspectrum([gif_x,hoge.x,X500_BARO],[None,None])
    #mpplot.plotspectrum([gif_x,hoge.x,X1500_TR_X],[[1e-3,6],[1e-9,1e-5]],label=['Frequency [Hz]','Displacement [m/sqrt(Hz)]'])
    filename = './Strain_GIF_Xend_Cent_x1500_x500'
    mpplot.plotspectrum([gif_x,ex1.x,cen.x,ex1.z,cen.z,X1500_TR_X,X1500_TR_Z,X500_BARO],[[1e-3,6],[1e-13,1e-8]],label=['Frequency [Hz]','Strain [1/sqrt(Hz)]'],filename=filename)
    filename = './Strain_GIF_Xend-Cent'
    mpplot.plotspectrum([gif_x,hoge.x],[[1e-3,6],[1e-13,1e-8]],label=['Frequency [Hz]','Strain [1/sqrt(Hz)]'],filename=filename)
    filename = './Displacement_GIF_x1500'
    mpplot.plotspectrum([gif_x,hoge.x,X1500_TR_X],[[1e-3,6],[1e-9,1e-5]],label=['Frequency [Hz]','Displacement [m/sqrt(Hz)]'],filename=filename)



def main_longterm(*args):
    X2000_BARO = reader.gif.readGIFdata(t0,tlen,
                                       'X2000_BARO',
                                       name='x2000_pressure',
                                       plot=True,detrend=True,
                                       title=title,
                                            )
    
if __name__ == '__main__':
    t0,tlen,title = get_gpstime(EQ_name)
    #main_plotSeismometerSepctrogram(t0,tlen,title,theta=0)
    #main_Lock(t0,tlen,title)
    #main_GIFspectrogram(t0,tlen,title)
    #exit()
    #main_StrainmeterSignalBudjet(t0,tlen,title)
    #main_coherence(t0,tlen,title)
    #main_strain(t0,tlen,title)
    #main_compare(t0,tlen,title)
    #main_plotlongtime()
    #main_cmrr(t0,tlen,title)
    main_longterm(t0,tlen,title)