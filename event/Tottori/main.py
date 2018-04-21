#
#! coding:utf-8

import sys 
import numpy as np
import miyopy.io.reader as reader
import miyopy.plot as mpplot

'''
memo
M5.8, 2018-04-08-14:32:34(UTC), 1207240372, W of Tottori, Japan
M5.2, 2018-03-27-06:39:10(UTC), 1206167968, WS of Iwo Jima, Japan
M6.6, 2018-03-26-09:51:00(UTC), 1206093078, Kimbe, Papua New Guinea
M6.4, 2018-03-25-20:14:47(UTC), 1206044105, NW of Saumlaki, Indonesia
M5.0, 2018-03-25-15:36:24(UTC), 1206027402, SE of Hachijo-jima, Japan
'''    

def getKimbeDataGIFseis(start,tlen):
    fs = 8.0
    TR240_EW = reader.gif(start,tlen,'X1500_TR240velEW',fs=fs)*1.0/1196.5
    TR240_NS = reader.gif(start,tlen,'X1500_TR240velNS',fs=fs)*1.0/1196.5
    TR240_UD = reader.gif(start,tlen,'X1500_TR240velUD',fs=fs)*1.0/1196.5
    CMG3T_EW = reader.gif(start,tlen,'X1500_CMG3TvelEW',fs=fs)*1.0/2000.0
    CMG3T_NS = reader.gif(start,tlen,'X1500_CMG3TvelNS',fs=fs)*1.0/2000.0
    CMG3T_UD = reader.gif(start,tlen,'X1500_CMG3TvelUD',fs=fs)*1.0/2000.0
    GIF_X = reader.gif(start,tlen,'CALC_STRAIN',fs=fs)*3000.0
    #GIF_SQ = reader.gif(start,tlen,'CALC_SQRT',fs=fs)
    #CLIO_LIN = reader.gif(start,tlen,'CLO_CALC_STRAIN_LIN',fs=fs)
    #CLIO_SHR = reader.gif(start,tlen,'CLO_CALC_STRAIN_SHR',fs=fs)
    time = np.arange(len(TR240_EW))/fs
    data = [[time,TR240_EW],[time,TR240_NS],[time,TR240_UD],
            #[time,GIF_X],[time,CLIO_LIN],[time,CLIO_SHR],
            [time,GIF_X],[time,GIF_X],[time,GIF_X],
            [time,CMG3T_EW],[time,CMG3T_NS],[time,CMG3T_UD],
            ]
    label = ['X1500_TR240velEW','X1500_TR240velNS','X1500_TR240velUD',
             'GIF_X','GIF_SQ','None',
             'X1500_CMG3TvelEW','X1500_CMG3TvelNS','X1500_CMG3TvelUD',
             ]
    return data,label
    
def get3seis3axis(start,tlen):
    '''
    3つの地震計の3つの軸の信号を取得してくる。
    '''
    fs = 8.0    
    EX1_SEIS = reader.kagra(start,tlen,['K1:PEM-EX1_SEIS_NS_SENSINF_OUT16','K1:PEM-EX1_SEIS_WE_SENSINF_OUT16','K1:PEM-EX1_SEIS_Z_SENSINF_OUT16']).T    
    EY1_SEIS = reader.kagra(start,tlen,['K1:PEM-EY1_SEIS_WE_SENSINF_OUT16','K1:PEM-EY1_SEIS_NS_SENSINF_OUT16','K1:PEM-EY1_SEIS_Z_SENSINF_OUT16']).T
    IY0_SEIS = reader.kagra(start,tlen,['K1:PEM-IY0_SEIS_NS_SENSINF_OUT16','K1:PEM-IY0_SEIS_WE_SENSINF_OUT16','K1:PEM-IY0_SEIS_Z_SENSINF_OUT16']).T 
    #
    R_xend = np.array([[-1.,0.,0.],[0.,-1.,0.],[0.,0.,1.]])
    R_yend = np.array([[-1.,0.,0.],[0.,-1.,0.],[0.,0.,1.]])
    R_cent = np.array([[-1.,0.,0.],[0.,-1.,0.],[0.,0.,1.]])
    #
    Xend_NSEW = np.array(map(lambda x:np.dot(x,R_xend),EX1_SEIS))
    Yend_NSEW = np.array(map(lambda x:np.dot(x,R_yend),EY1_SEIS))
    Cent_NSEW = np.array(map(lambda x:np.dot(x,R_cent),IY0_SEIS))
    #
    Xend_EW, Xend_NS, Xend_UD = Xend_NSEW.T
    Cent_EW, Cent_NS, Cent_UD = Cent_NSEW.T
    Yend_EW, Yend_NS, Yend_UD = Yend_NSEW.T
    time = np.arange(len(Xend_EW))/fs
    data = [[time,Xend_EW],[time,Xend_NS],[time,Xend_UD],
            [time,Cent_EW],[time,Cent_NS],[time,Cent_UD],
            [time,Yend_EW],[time,Yend_NS],[time,Yend_UD]]    
    label = ['Xend2F_EW','Xend1F_NS','Xend1F_UD',
             'Cent1F_EW','Cent1F_NS','Cent1F_UD',
             'Yend2F_EW','Yend2F_NS','Yend2F_UD']    
    return data,label
    
if __name__ == '__main__':
    EQ_name = {
        'Tottori':[1207240372,2**12],
        #'Tottori_P-Wave':[1207240372,2**12],
        'Tottori_P-Wave':[1207240372,2**7],
        'Kimbe':[1206093078,32*2*64],
        'Kimbe_':[1206093078,2**8],
        'Kimbe_P-Wave':[1206093078+440,2**7],
        'Kimbe_S-Wave':[1206093078+800,2**11],
        'Kimbe_S-Wave':[1206093078+1200,2**9],
        'Kimbe_Other-Wave':[1206093078+1200,2**11],        
        'Saumlaki':[1206044105,32*2*32],
        'Hachijo-jima':[1206027402,32*2*64],
    }
    #
    try:
        option = sys.argv[1]
        start, tlen = EQ_name[option]
        title = '{0}_{1}_{2}'.format(option,start,tlen)
    except IndexError as e:
        print type(e),e
        print 'Please add option. ex, python main.py <EQname>'
        print 'exit...'
        exit()
    except KeyError as e:
        print type(e),e
        print '{0} is not in EQ_name.'.format(e)
        print 'Please use argvs bellow;'
        print '\n'.join(EQ_name.keys())
        exit()        
    #'''
    import matplotlib.pyplot as plt
    strain = reader.gif(start,tlen,'CALC_STRAIN')
    lin = reader.gif(start,tlen,'CLIO_CALC_STRAIN_LIN')   
    xarm = strain*3000.0
    ex1_ew = reader.kagra(start,tlen,['K1:PEM-EX1_SEIS_NS_SENSINF_OUT16'])[0]
    xend_ew = -1*ex1_ew*np.cos(np.deg2rad(120))
    iy0_ew = reader.kagra(start,tlen,['K1:PEM-IY0_SEIS_NS_SENSINF_OUT16'])[0]
    cent_ew = -1*iy0_ew*np.cos(np.deg2rad(120))
    xarm_seis_ = ex1_ew-iy0_ew
    xarm_seis = xend_ew-cent_ew
    time = np.arange(len(ex1_ew))/8.0
    print ex1_ew
    print time
    plt.figure(num=None, figsize=(14, 6), dpi=80)
    plt.plot(time,xarm,label='x-arm')
    plt.plot(time,xarm_seis,label='x-arm_seis')
    plt.plot(time,xarm_seis_,label='x-arm_seis_')
    plt.legend()
    plt.savefig('huge.png')
    plt.close()    
#'''
    title = '{0}_{1}_{2}'.format(option,start,tlen)
    #
    data,label = get3seis3axis(start,tlen)
    fname = '3SEIS_{0}.png'.format(title)
    print fname
    mpplot.subplot33(data,fname,label)
    #
    data,label = getKimbeDataGIFseis(start, tlen)
    fname = 'GIF_{0}.png'.format(title)    
    mpplot.subplot33(data,fname,label)   
    print fname
    