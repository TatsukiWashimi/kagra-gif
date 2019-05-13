from gwpy.timeseries import TimeSeries
from gwpy.plot import Plot

'''
Fetch seismometer data from nds.

'''


# - data1 -----------------------------
start = '2019 May 12 00:00:00 JST'
end = '2019 May 12 06:00:00 JST'
chname = 'K1:PEM-SEIS_IXV_GND_X_OUT_DQ'
# -------------------------------------

# fetch data
data = TimeSeries.fetch(chname,start,end,host='k1nds0',port=8088)

# calc spectrum
fftlength = 2**10
sg = data.spectrogram2(fftlength=fftlength,
                       overlap=fftlength/2,
                       nproc=2,
                       window='hanning') ** (1/2.)
# percentile
median = sg.percentile(50)
low = sg.percentile(5)
high = sg.percentile(95)

# plot TimeSeries
plot = data.plot()
plot.savefig('result_timeseries.png')
plot.close()

# plot Spectrum
plot = Plot()
ax = plot.gca(xscale='log', xlim=(1e-3, 200), xlabel='Frequency [Hz]',
              yscale='log',# ylim=(3e-24, 2e-20),
              ylabel=r'Ground Velocity [um/sec/\rtHz]')
ax.plot_mmm(median, low, high, color='gwpy:ligo-hanford')
ax.set_title('No title',fontsize=16)
plot.savefig('result_asd.png')

# write data
low.write('data1_ixv_x_5pct.hdf5',format='hdf5')
median.write('data1_ixv_x_50pct.hdf5',format='hdf5')
high.write('data1_ixv_x_95pct.hdf5',format='hdf5')