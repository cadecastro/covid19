#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 13:27:22 2021
ANÁLISIS CIFRAS COVID-19 GLOBALES
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
#POBLACIÓN MUNDIAL:
#Lectura base de datos de la ONU:
pob_mundial=pd.read_csv('https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/CSV_FILES/WPP2019_TotalPopulationBySex.csv',
                        usecols=['Location','Variant','Time','PopTotal'])
pob_mundial['PopTotal']=1000*pob_mundial['PopTotal']
pob_mundial=pob_mundial[pob_mundial['Variant']=='Medium'].drop(columns='Variant')
pob2021=pob_mundial[pob_mundial['Time']==2021].drop(columns='Time')
pob2021=pob2021.set_index('Location')

#GRÁFICAS:
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
plt.plot(muertes_diarias.index,muertes_diarias['Mundo'].rolling(window =7).mean(),'r')
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
plt.plot(muertes_diarias.index,muertes_diarias[pais].rolling(window =7).mean(),'r')
plt.ylabel('Daily Deaths')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(muertes_diarias.index[0],muertes_diarias.index[len(muertes_diarias.index)-1])
plt.legend(['Rolling average 7 days','Daily data'])

plt.figure(3,figsize=(18,9))
plt.plot(muertes_diarias.index,muertes_diarias['Colombia'].rolling(window =7).mean()/pob2021['PopTotal']['Colombia'],'gold')
plt.plot(muertes_diarias.index,muertes_diarias['Mexico'].rolling(window =7).mean()/pob2021['PopTotal']['Mexico'],'b')
plt.plot(muertes_diarias.index,muertes_diarias['Israel'].rolling(window =7).mean()/pob2021['PopTotal']['Israel'],'r')
plt.plot(muertes_diarias.index,muertes_diarias['US'].rolling(window =7).mean()/pob2021['PopTotal']['United States of America'],'g')
plt.plot(muertes_diarias.index,muertes_diarias['South Africa'].rolling(window =7).mean()/pob2021['PopTotal']['South Africa'],'m')
plt.plot(muertes_diarias.index,muertes_diarias['United Kingdom'].rolling(window =7).mean()/pob2021['PopTotal']['United Kingdom'],'c')
plt.plot(muertes_diarias.index,muertes_diarias['Brazil'].rolling(window =7).mean()/pob2021['PopTotal']['Brazil'],'k')
plt.plot(muertes_diarias.index,muertes_diarias['Sweden'].rolling(window =7).mean()/pob2021['PopTotal']['Sweden'],'slategrey')
plt.title('Daily COVID-19 Deaths per Capita',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Daily Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(muertes_diarias.index[0],muertes_diarias.index[len(muertes_diarias.index)-1])
plt.legend(['Colombia','México','Israel','USA','South Africa','United Kingdom','Brazil','Sweden'])

#Comparativo países de interés:
comparativo=pd.DataFrame(data=[muertes_diarias['Colombia'].sum()/pob2021['PopTotal']['Colombia'],muertes_diarias['Mexico'].sum()/pob2021['PopTotal']['Mexico'],
                               muertes_diarias['Israel'].sum()/pob2021['PopTotal']['Israel'],muertes_diarias['US'].sum()/pob2021['PopTotal']['United States of America'],
                               muertes_diarias['South Africa'].sum()/pob2021['PopTotal']['South Africa'],muertes_diarias['United Kingdom'].sum()/pob2021['PopTotal']['United Kingdom'],
                               muertes_diarias['Brazil'].sum()/pob2021['PopTotal']['Brazil'],muertes_diarias['Sweden'].sum()/pob2021['PopTotal']['Sweden']],
                         index=['Colombia','México','Israel','USA','South Africa','United Kingdom','Brazil','Sweden'])
comparativo=comparativo.rename(columns={0:'Deaths per capita'})
comparativo=comparativo.sort_values(by='Deaths per capita',ascending=False)
print(comparativo)

plt.figure(4,figsize=(10,5))
plt.bar(comparativo.index,comparativo['Deaths per capita'],color='blue')
plt.title('Total COVID-19 Deaths per Capita',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Total Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.xticks(rotation=90)
plt.grid(True,'both','both')
plt.ylim(0,None)

#Comparativo Latinoamérica:
comparativo_latam=pd.DataFrame(data=[muertes_diarias['Colombia'].sum()/pob2021['PopTotal']['Colombia'],muertes_diarias['Mexico'].sum()/pob2021['PopTotal']['Mexico'],
                               muertes_diarias['Argentina'].sum()/pob2021['PopTotal']['Argentina'],muertes_diarias['Peru'].sum()/pob2021['PopTotal']['Peru'],
                               muertes_diarias['Ecuador'].sum()/pob2021['PopTotal']['Ecuador'],muertes_diarias['Panama'].sum()/pob2021['PopTotal']['Panama'],
                               muertes_diarias['Brazil'].sum()/pob2021['PopTotal']['Brazil'],muertes_diarias['Chile'].sum()/pob2021['PopTotal']['Chile']],
                         index=['Colombia','México','Argentina','Perú','Ecuador','Panamá','Brasil','Chile'])
comparativo_latam=comparativo_latam.rename(columns={0:'Muertes per capita'})
comparativo_latam=comparativo_latam.sort_values(by='Muertes per capita',ascending=False)
print(comparativo_latam)

plt.figure(5,figsize=(12,6))
plt.bar(comparativo_latam.index,comparativo_latam['Muertes per capita'],color='blue')
plt.title('Muertes per capita COVID-19 Latinoamérica',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Total Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.xticks(rotation=90)
plt.grid(True,'both','both')
plt.ylim(0,None)
