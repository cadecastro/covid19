#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 10:52:33 2022
COVID-19 DEATHS IN US - COUNTY
Author: Carlos Armando De Castro (cadecastro.com)
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
muertes_us=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')
muertes_us=muertes_us.drop(labels=['UID','iso2','iso3','code3','FIPS','Admin2','Country_Region','Lat','Long_'],axis=1)
muertes_us=muertes_us.groupby(['Combined_Key']).sum()
poblacion=muertes_us['Population']
muertes_us=muertes_us.drop(labels=['Population'],axis=1)
muertes_us=muertes_us.diff(periods=1,axis=1)
muertes=muertes_us.sum(axis=1)
muertes=pd.concat([muertes,poblacion],axis=1)
#muertes=muertes.rename(columns={'0':'Muertes','Population':'Poblacion'})
muertes_us=muertes_us.transpose()
muertes_us.index=pd.to_datetime(muertes_us.index,dayfirst=False,yearfirst=False)
muertes_us.dropna()
muertes['Per capita']=muertes[0]/muertes['Population']*100
muertes=muertes[np.isfinite(muertes).all(1)]
muertes=muertes.sort_values(by=['Per capita'],ascending=False)
condado=str(input('COUNTY TO ANALYSE: '))
print('Deaths with COVID-19 at '+condado+' : ',np.format_float_positional(muertes[0][condado],precision=0))
print('Population at '+condado+' : ',np.format_float_positional(muertes['Population'][condado],precision=0))
print('Deaths per capita at '+condado+' : ',np.format_float_positional(muertes['Per capita'][condado],precision=3),'%')
plt.figure(1,figsize=(12,6))
plt.bar(muertes_us.index,muertes_us[condado],color='blue')
plt.plot(muertes_us.index,muertes_us[condado].rolling(window=7).mean(),'r')
plt.title('Daily deaths with COVID-19 at '+condado,loc='left')
plt.title('cadecastro.com',loc='right')
plt.ylabel('Daily deaths')
plt.legend(['Daily deaths','Rolling average 7 days'])
plt.ylim(0,None)
plt.figure(2,figsize=(12,6))
muertes['Per capita'][:len(muertes['Per capita'])-3200].plot.bar(color='blue')
plt.title('Deaths per capita by county')
plt.ylabel('Deaths/Population (%)')
