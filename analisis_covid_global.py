#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 13:27:22 2021
ANÁLISIS MUERTES COVID-19 GLOBALES
Autor: Carlos Armando De Castro (cadecastro.com)
"""
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
#Importar datos de GitHub:
covid_global=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
#Retirar coordenadas:
covid_global=covid_global.drop(labels=['Lat','Long'],axis=1)
#Agrupar por país:
covid_global=covid_global.groupby(['Country/Region']).sum()
covid_global=covid_global.transpose()
muertes_diarias=covid_global.diff(periods=1,axis=0)
muertes_diarias.index=pd.to_datetime(muertes_diarias.index,dayfirst=False,yearfirst=False)
pais=str(input('País a graficar muertes diarias: '))
plt.figure(1)
plt.bar(muertes_diarias.index,muertes_diarias[pais],color='blue')
plt.plot(muertes_diarias.index,muertes_diarias[pais].rolling(window =7).mean(),'r')
plt.title('Muertes diarias COVID-19 reportadas en '+pais,loc='left')
plt.title('cadecastro.com',loc='right')
plt.ylim(0,None)
muertes_mundo=muertes_diarias.sum(axis=1)
plt.figure(2)
plt.bar(muertes_mundo.index,muertes_mundo,color='blue')
plt.plot(muertes_mundo.index,muertes_mundo.rolling(window =7).mean(),'r')
plt.title('Muertes diarias COVID-19 global',loc='left')
plt.title('cadecastro.com',loc='right')
plt.ylim(0,None)