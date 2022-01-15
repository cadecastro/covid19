#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 20:10:03 2021
COVID-19 DEATHS IN US STATES
Author: Carlos Armando De Castro (cadecastro.com)
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
muertes_us=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')
muertes_us=muertes_us.drop(labels=['UID','iso2','iso3','code3','FIPS','Admin2','Country_Region','Combined_Key','Lat','Long_'],axis=1)
muertes_us=muertes_us.groupby(['Province_State']).sum()
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
estado=str(input('STATE TO ANALYSE: '))
print('Deaths with COVID-19 at '+estado+' : ',np.format_float_positional(muertes[0][estado],precision=0))
print('Population at '+estado+' : ',np.format_float_positional(muertes['Population'][estado],precision=0))
print('Deaths per capita at '+estado+' : ',np.format_float_positional(muertes['Per capita'][estado],precision=3),'%')
plt.figure(1,figsize=(12,6))
#plt.bar(muertes_us.index,muertes_us[estado],color='blue')
plt.plot(muertes_us.index,muertes_us[estado].rolling(window=7).mean(),'b')
plt.title('Daily deaths with COVID-19 at '+estado,loc='left')
plt.title('cadecastro.com',loc='right')
plt.ylabel('Daily deaths')
plt.legend(['Rolling average 7 days','Daily deaths'])
plt.ylim(0,None)
plt.xlim(muertes_us.index[0],muertes_us.index[len(muertes_us[estado])-1])
plt.grid(True,'both','both')
plt.figure(2,figsize=(12,6))
muertes['Per capita'][:len(muertes['Per capita'])-46].plot.bar(color='blue')
plt.ylabel('Deaths/Population (%)')
plt.title('Reported COVID-19 deaths per capita',loc='left')
plt.title('cadecastro.com',loc='right')
