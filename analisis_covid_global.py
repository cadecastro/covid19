#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 13:27:22 2021
ANALYSIS OF COVID-19 WORLD DATA
Autor: Carlos Armando De Castro (cadecastro.com)
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
#MUERTES TOTALES:
#Importar datos de GitHub:
covid_global=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
#Retirar coordenadas:
covid_global=covid_global.drop(labels=['Lat','Long'],axis=1)
#Agrupar por país:
covid_global=covid_global.groupby(['Country/Region']).sum()
covid_global=covid_global.transpose()
#Muertes diarias:
muertes_diarias=covid_global.diff(periods=1,axis=0)
muertes_diarias.index=pd.to_datetime(muertes_diarias.index,dayfirst=False,yearfirst=False)
muertes_diarias['Mundo']=muertes_diarias.sum(axis=1)
pais=str(input('COUNTRY TO ANALYSE: '))
#CASOS CONFIRMADOS:
casos_global=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
#Retirar coordenadas:
casos_global=casos_global.drop(labels=['Lat','Long'],axis=1)
#Agrupar por país:
casos_global=casos_global.groupby(['Country/Region']).sum()
casos_global=casos_global.transpose()
#Casos diarios:
casos_diarias=casos_global.diff(periods=1,axis=0)
casos_diarias.index=pd.to_datetime(casos_diarias.index,dayfirst=False,yearfirst=False)
casos_diarias['Mundo']=casos_diarias.sum(axis=1)
#Salida resultados:
print('Confirmed cases at ',pais,'= ',np.format_float_positional(casos_diarias[pais].sum(),precision=0))
print('Reported deaths at ',pais,'= ',np.format_float_positional(muertes_diarias[pais].sum(),precision=0))
print('Case Fatality Rate at ',pais,'= ',np.format_float_positional(muertes_diarias[pais].sum()/casos_diarias[pais].sum()*100,precision=2),'%')
print('Confirmed cases World = ',np.format_float_positional(casos_diarias['Mundo'].sum(),precision=0))
print('Reported deaths Worldwide = ',np.format_float_positional(muertes_diarias['Mundo'].sum(),precision=0))
print('Case Fatality Rate Worldwide = ',np.format_float_positional(muertes_diarias['Mundo'].sum()/casos_diarias['Mundo'].sum()*100,precision=2),'%')
#Gráficas:
plt.figure(1,figsize=(12,6))
plt.subplot(211)
#plt.bar(casos_diarias.index,casos_diarias['Mundo'],color='blue')
plt.plot(casos_diarias.index,casos_diarias['Mundo'].rolling(window =7).mean(),'b')
plt.title('Daily COVID-19 report Worldwide')
plt.title('cadecastro.com',loc='right')
plt.ylabel('Daily Cases')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(casos_diarias.index[0],casos_diarias.index[len(casos_diarias.index)-1])
plt.legend(['Rolling average 7 days','Daily data'])
plt.subplot(212)
#plt.bar(muertes_diarias.index,muertes_diarias['Mundo'],color='blue')
plt.plot(muertes_diarias.index,muertes_diarias['Mundo'].rolling(window =7).mean(),'b')
plt.ylabel('Daily Deaths')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(muertes_diarias.index[0],muertes_diarias.index[len(muertes_diarias.index)-1])
plt.legend(['Rolling average 7 days','Daily data'])
plt.figure(2,figsize=(12,6))
plt.subplot(211)
#plt.bar(casos_diarias.index,casos_diarias[pais],color='blue')
plt.plot(casos_diarias.index,casos_diarias[pais].rolling(window =7).mean(),'b')
plt.title('Daily COVID-19 report at '+pais)
plt.title('cadecastro.com',loc='right')
plt.ylabel('Daily Cases')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(casos_diarias.index[0],casos_diarias.index[len(casos_diarias.index)-1])
plt.legend(['Rolling average 7 days','Daily data'])
plt.subplot(212)
#plt.bar(muertes_diarias.index,muertes_diarias[pais],color='blue')
plt.plot(muertes_diarias.index,muertes_diarias[pais].rolling(window =7).mean(),'b')
plt.ylabel('Daily Deaths')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(muertes_diarias.index[0],muertes_diarias.index[len(muertes_diarias.index)-1])
plt.legend(['Rolling average 7 days','Daily data'])
