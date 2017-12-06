#!/usr/bin/python
#coding=utf-8 

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset
import cmaps

lon_0 =  116.75
lat_0 =  37.25



filename = './emiss_27.ncf'
#filename = './wrfchemi_d01'
print(filename)
readfile = Dataset(filename, mode='r', open=True)
no2    = np.squeeze(readfile.variables['NO2'][:][:][:])
no2_units = readfile.variables['NO2'].units
#no2 = readfile.variables['NO2'][:]

m = Basemap(lat_0=lat_0, lon_0=lon_0, llcrnrlat=24.75 ,urcrnrlat=49.75,\
            llcrnrlon=104.25,urcrnrlon=129.25,\
            rsphere=6371200.,resolution='l') 

lons = np.arange(104.25,129.25,0.25)
lats = np.arange(24.75,49.75,0.25)

lon, lat = np.meshgrid(lons, lats)
xi, yi = m(lon, lat)

######  提取NO 网格信息COL,ROW 
#for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
for i in [0,]:
    print(u"第一个是", i)
    no2_0 = no2[i:i+1, 0:1, :, :]
    no2_0 = np.squeeze(no2_0)
    clevs = np.arange(0,1.3,0.1)
    #clevs = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    #cs = m.pcolor(xi, yi, np.squeeze(no2_0))
    #cs = m.contourf(xi, yi, no2_0, cmap=cm.s3pcpn, levels=clevs)
    #print(xi.shape,yi.shape,no2_0.shape)
    fig, ax = plt.subplots(1, 1, figsize=(8,6))
    cs = plt.contourf(xi, yi, no2_0, cmap=cmaps.WhiteBlueGreenYellowRed, levels=clevs)
    ######  画网格-经纬度线
    #m.drawparallels(np.arange(0,80,0.25))
    #m.drawmeridians(np.arange(100,150,0.25))

    # Add Colorbar
    #cbar = m.colorbar(cs, location='bottom', pad="10%")
    cbar = m.colorbar(cs, location='right', pad="5%")
    cbar.set_label(no2_units)

    # Add Coastlines, States, and Country Boundaries
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()   
    m.drawparallels(np.arange(-90.,120.,10.),labels=[1,0,0,0])
    m.drawmeridians(np.arange(-180.,180.,10.),labels=[0,0,0,1])
    #m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
    plt.title('NO2 emission rate')
    plt.savefig('emiss.png', dpi=300)
    plt.show()

    #plt.savefig('current_'+str(i)+'.png', dpi=75)
    #plt.savefig('current_{0}_.png'.format(i), dpi=75)
    #plt.close()
    
    del no2_0; del cs
    
readfile.close()



