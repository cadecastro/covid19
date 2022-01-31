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
muertes_diarias['Year']=pd.DatetimeIndex(muertes_diarias.index).year
print('ANALYSIS OF COVID-19 DATA WORLDWIDE')
print('Author: Carlos Armando De Castro - cadecastro.com (Analysis and Engineering Services)')
print('----------------------------------')
pais=str(input('SPECIFIC COUNTRY TO ANALYSE: '))
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

#Comparativo Latinoamérica:
comparativo_latam=pd.DataFrame(data=[muertes_diarias['Colombia'].sum()/pob2021['PopTotal']['Colombia'],muertes_diarias['Mexico'].sum()/pob2021['PopTotal']['Mexico'],
                               muertes_diarias['Argentina'].sum()/pob2021['PopTotal']['Argentina'],muertes_diarias['Peru'].sum()/pob2021['PopTotal']['Peru'],
                               muertes_diarias['Ecuador'].sum()/pob2021['PopTotal']['Ecuador'],muertes_diarias['Panama'].sum()/pob2021['PopTotal']['Panama'],
                               muertes_diarias['Brazil'].sum()/pob2021['PopTotal']['Brazil'],muertes_diarias['Chile'].sum()/pob2021['PopTotal']['Chile'],
                               muertes_diarias['Uruguay'].sum()/pob2021['PopTotal']['Uruguay'],muertes_diarias['Paraguay'].sum()/pob2021['PopTotal']['Paraguay']],
                         index=['Colombia','México','Argentina','Perú','Ecuador','Panamá','Brasil','Chile','Uruguay','Paraguay'])
comparativo_latam=comparativo_latam.rename(columns={0:'Deaths per capita'})
comparativo_latam=comparativo_latam.sort_values(by='Deaths per capita',ascending=False)

#Comparativo Europa:
comparativo_eur=pd.DataFrame(data=[muertes_diarias['Portugal'].sum()/pob2021['PopTotal']['Portugal'],muertes_diarias['Germany'].sum()/pob2021['PopTotal']['Germany'],
                               muertes_diarias['France'].sum()/pob2021['PopTotal']['France'],muertes_diarias['Italy'].sum()/pob2021['PopTotal']['Italy'],
                               muertes_diarias['Austria'].sum()/pob2021['PopTotal']['Austria'],muertes_diarias['Poland'].sum()/pob2021['PopTotal']['Poland'],
                               muertes_diarias['Sweden'].sum()/pob2021['PopTotal']['Sweden'],muertes_diarias['Spain'].sum()/pob2021['PopTotal']['Spain'],
                               muertes_diarias['Greece'].sum()/pob2021['PopTotal']['Greece'],muertes_diarias['Denmark'].sum()/pob2021['PopTotal']['Denmark'],
                               muertes_diarias['Netherlands'].sum()/pob2021['PopTotal']['Netherlands'],muertes_diarias['Belgium'].sum()/pob2021['PopTotal']['Belgium'],
                               muertes_diarias['Russia'].sum()/pob2021['PopTotal']['Russian Federation'],muertes_diarias['Finland'].sum()/pob2021['PopTotal']['Finland']],
                         index=['Portugal','Germany','France','Italy','Austria','Poland','Sweden','Spain','Greece','Denmark','Netherlands','Belgium','Russia','Finland'])
comparativo_eur=comparativo_eur.rename(columns={0:'Deaths per capita'})
comparativo_eur=comparativo_eur.sort_values(by='Deaths per capita',ascending=False)

#Comparativo países anglos:
comparativo_ang=pd.DataFrame(data=[muertes_diarias['United Kingdom'].sum()/pob2021['PopTotal']['United Kingdom'],muertes_diarias['US'].sum()/pob2021['PopTotal']['United States of America'],
                               muertes_diarias['Ireland'].sum()/pob2021['PopTotal']['Ireland'],muertes_diarias['Australia'].sum()/pob2021['PopTotal']['Australia'],
                               muertes_diarias['New Zealand'].sum()/pob2021['PopTotal']['New Zealand'],muertes_diarias['Canada'].sum()/pob2021['PopTotal']['Canada']],
                         index=['United Kingdom','United States','Ireland','Australia','New Zealand','Canada'])
comparativo_ang=comparativo_ang.rename(columns={0:'Deaths per capita'})
comparativo_ang=comparativo_ang.sort_values(by='Deaths per capita',ascending=False)

#Comparativo países asiáticos:
comparativo_asia=pd.DataFrame(data=[muertes_diarias['Japan'].sum()/pob2021['PopTotal']['Japan'],muertes_diarias['Vietnam'].sum()/pob2021['PopTotal']['Viet Nam'],
                               muertes_diarias['India'].sum()/pob2021['PopTotal']['India'],muertes_diarias['Philippines'].sum()/pob2021['PopTotal']['Philippines'],
                               muertes_diarias['Thailand'].sum()/pob2021['PopTotal']['Thailand'],muertes_diarias['Korea, South'].sum()/pob2021['PopTotal']['Republic of Korea'],
                               muertes_diarias['Mongolia'].sum()/pob2021['PopTotal']['Mongolia'],muertes_diarias['Indonesia'].sum()/pob2021['PopTotal']['Indonesia']],
                         index=['Japan','Vietnam','India','Philippines','Thailand','South Korea','Mongolia','Indonesia'])
comparativo_asia=comparativo_asia.rename(columns={0:'Deaths per capita'})
comparativo_asia=comparativo_asia.sort_values(by='Deaths per capita',ascending=False)

#Comparativo medio oriente:
comparativo_med=pd.DataFrame(data=[muertes_diarias['Israel'].sum()/pob2021['PopTotal']['Israel'],muertes_diarias['Turkey'].sum()/pob2021['PopTotal']['Turkey'],
                               muertes_diarias['Jordan'].sum()/pob2021['PopTotal']['Jordan'],muertes_diarias['Saudi Arabia'].sum()/pob2021['PopTotal']['Saudi Arabia'],
                               muertes_diarias['Iran'].sum()/pob2021['PopTotal']['Iran (Islamic Republic of)'],muertes_diarias['Iraq'].sum()/pob2021['PopTotal']['Iraq'],
                               muertes_diarias['Lebanon'].sum()/pob2021['PopTotal']['Lebanon'],muertes_diarias['Egypt'].sum()/pob2021['PopTotal']['Egypt'],
                               muertes_diarias['Libya'].sum()/pob2021['PopTotal']['Libya'],muertes_diarias['Pakistan'].sum()/pob2021['PopTotal']['Pakistan']],
                         index=['Israel','Turkey','Jordan','Saudi Arabia','Iran','Iraq','Lebanon','Egypt','Libya','Pakistan'])
comparativo_med=comparativo_med.rename(columns={0:'Deaths per capita'})
comparativo_med=comparativo_med.sort_values(by='Deaths per capita',ascending=False)

#Comparativo África:
comparativo_africa=pd.DataFrame(data=[muertes_diarias['Nigeria'].sum()/pob2021['PopTotal']['Nigeria'],muertes_diarias['South Africa'].sum()/pob2021['PopTotal']['South Africa'],
                               muertes_diarias['Kenya'].sum()/pob2021['PopTotal']['Kenya'],muertes_diarias['Malawi'].sum()/pob2021['PopTotal']['Malawi'],
                               muertes_diarias['Mozambique'].sum()/pob2021['PopTotal']['Mozambique'],muertes_diarias['Ethiopia'].sum()/pob2021['PopTotal']['Ethiopia'],
                               muertes_diarias['Namibia'].sum()/pob2021['PopTotal']['Namibia'],muertes_diarias['Rwanda'].sum()/pob2021['PopTotal']['Rwanda']],
                         index=['Nigeria','South Africa','Kenya','Malawi','Mozambique','Ethiopia','Namibia','Rwanda'])
comparativo_africa=comparativo_africa.rename(columns={0:'Deaths per capita'})
comparativo_africa=comparativo_africa.sort_values(by='Deaths per capita',ascending=False)

#Comparativo mundial:
comparativo_mund=comparativo_latam.append([comparativo_eur,comparativo_ang,comparativo_asia,
                                           comparativo_med,comparativo_africa]).sort_values(by='Deaths per capita',ascending=False)
print('----------------------------------')
print('DEATHS PER CAPITA COMPARISON:')
print(comparativo_mund)

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
plt.plot(muertes_diarias.index,muertes_diarias['Argentina'].rolling(window =7).mean()/pob2021['PopTotal']['Argentina'],'r')
plt.plot(muertes_diarias.index,muertes_diarias['Peru'].rolling(window =7).mean()/pob2021['PopTotal']['Peru'],'m')
plt.plot(muertes_diarias.index,muertes_diarias['Chile'].rolling(window =7).mean()/pob2021['PopTotal']['Chile'],'c')
plt.plot(muertes_diarias.index,muertes_diarias['Brazil'].rolling(window =7).mean()/pob2021['PopTotal']['Brazil'],'lime')
plt.plot(muertes_diarias.index,muertes_diarias['Panama'].rolling(window =7).mean()/pob2021['PopTotal']['Panama'],'brown')
plt.plot(muertes_diarias.index,muertes_diarias['Uruguay'].rolling(window =7).mean()/pob2021['PopTotal']['Uruguay'],'k')
plt.plot(muertes_diarias.index,muertes_diarias['Paraguay'].rolling(window =7).mean()/pob2021['PopTotal']['Paraguay'],'grey')
plt.title('Daily COVID-19 Deaths per Capita Latin America',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Daily Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(muertes_diarias.index[0],muertes_diarias.index[len(muertes_diarias.index)-1])
plt.legend(['Colombia','México','Argentina','Perú','Chile','Brasil','Panamá','Uruguay','Paraguay'])

plt.figure(4,figsize=(18,9))
plt.plot(muertes_diarias.index,muertes_diarias['United Kingdom'].rolling(window =7).mean()/pob2021['PopTotal']['United Kingdom'],'gold')
plt.plot(muertes_diarias.index,muertes_diarias['Germany'].rolling(window =7).mean()/pob2021['PopTotal']['Germany'],'b')
plt.plot(muertes_diarias.index,muertes_diarias['France'].rolling(window =7).mean()/pob2021['PopTotal']['France'],'r')
plt.plot(muertes_diarias.index,muertes_diarias['Spain'].rolling(window =7).mean()/pob2021['PopTotal']['Spain'],'g')
plt.plot(muertes_diarias.index,muertes_diarias['Greece'].rolling(window =7).mean()/pob2021['PopTotal']['Greece'],'m')
plt.plot(muertes_diarias.index,muertes_diarias['Denmark'].rolling(window =7).mean()/pob2021['PopTotal']['Denmark'],'c')
plt.plot(muertes_diarias.index,muertes_diarias['Netherlands'].rolling(window =7).mean()/pob2021['PopTotal']['Netherlands'],'lime')
plt.plot(muertes_diarias.index,muertes_diarias['Belgium'].rolling(window =7).mean()/pob2021['PopTotal']['Belgium'],'brown')
plt.plot(muertes_diarias.index,muertes_diarias['Italy'].rolling(window =7).mean()/pob2021['PopTotal']['Italy'],'k')
plt.plot(muertes_diarias.index,muertes_diarias['Poland'].rolling(window =7).mean()/pob2021['PopTotal']['Poland'],'grey')
plt.title('Daily COVID-19 Deaths per Capita Europe',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Daily Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(muertes_diarias.index[0],muertes_diarias.index[len(muertes_diarias.index)-1])
plt.legend(['UK','Germany','France','Spain','Greece','Denmark','Netherlands','Belgium','Italy','Poland'])


plt.figure(5,figsize=(18,9))
plt.plot(muertes_diarias.index,muertes_diarias['US'].rolling(window =7).mean()/pob2021['PopTotal']['United States of America'],'b')
plt.plot(muertes_diarias.index,muertes_diarias['United Kingdom'].rolling(window =7).mean()/pob2021['PopTotal']['United Kingdom'],'r')
plt.plot(muertes_diarias.index,muertes_diarias['Ireland'].rolling(window =7).mean()/pob2021['PopTotal']['Ireland'],'g')
plt.plot(muertes_diarias.index,muertes_diarias['Australia'].rolling(window =7).mean()/pob2021['PopTotal']['Australia'],'c')
plt.plot(muertes_diarias.index,muertes_diarias['New Zealand'].rolling(window =7).mean()/pob2021['PopTotal']['New Zealand'],'m')
plt.plot(muertes_diarias.index,muertes_diarias['Canada'].rolling(window =7).mean()/pob2021['PopTotal']['Canada'],'y')
plt.title('Daily COVID-19 Deaths per Capita Anglo',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Daily Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(muertes_diarias.index[0],muertes_diarias.index[len(muertes_diarias.index)-1])
plt.legend(['United States','United Kingdom','Ireland','Australia','New Zealand','Canada'])

plt.figure(6,figsize=(18,9))
plt.plot(muertes_diarias.index,muertes_diarias['Japan'].rolling(window =7).mean()/pob2021['PopTotal']['Japan'],'b')
plt.plot(muertes_diarias.index,muertes_diarias['Vietnam'].rolling(window =7).mean()/pob2021['PopTotal']['Viet Nam'],'r')
plt.plot(muertes_diarias.index,muertes_diarias['India'].rolling(window =7).mean()/pob2021['PopTotal']['India'],'g')
plt.plot(muertes_diarias.index,muertes_diarias['Philippines'].rolling(window =7).mean()/pob2021['PopTotal']['Philippines'],'c')
plt.plot(muertes_diarias.index,muertes_diarias['Thailand'].rolling(window =7).mean()/pob2021['PopTotal']['Thailand'],'m')
plt.plot(muertes_diarias.index,muertes_diarias['Korea, South'].rolling(window =7).mean()/pob2021['PopTotal']['Republic of Korea'],'y')
plt.title('Daily COVID-19 Deaths per Capita East Asia',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Daily Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(muertes_diarias.index[0],muertes_diarias.index[len(muertes_diarias.index)-1])
plt.legend(['Japan','Vietnam','India','Philippines','Thailand','South Korea'])

plt.figure(7,figsize=(12,6))
plt.bar(comparativo_latam.index,comparativo_latam['Deaths per capita'],color='blue')
plt.title('Deaths per Capita COVID-19 Latin America',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Total Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.xticks(rotation=90)
plt.grid(True,'both','both')
plt.ylim(0,None)

plt.figure(8,figsize=(12,6))
plt.bar(comparativo_eur.index,comparativo_eur['Deaths per capita'],color='blue')
plt.title('Deaths per capita COVID-19 Europe',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Total Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.xticks(rotation=90)
plt.grid(True,'both','both')
plt.ylim(0,None)

plt.figure(9,figsize=(12,6))
plt.bar(comparativo_ang.index,comparativo_ang['Deaths per capita'],color='blue')
plt.title('Deaths per capita COVID-19 Anglo',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Total Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.xticks(rotation=90)
plt.grid(True,'both','both')
plt.ylim(0,None)

plt.figure(10,figsize=(12,6))
plt.bar(comparativo_asia.index,comparativo_asia['Deaths per capita'],color='blue')
plt.title('Deaths per capita COVID-19 Asia',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Total Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.xticks(rotation=90)
plt.grid(True,'both','both')
plt.ylim(0,None)

plt.figure(11,figsize=(10,5))
plt.bar(comparativo_med.index,comparativo_med['Deaths per capita'],color='blue')
plt.title('Total COVID-19 Deaths per Capita Middle East',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Total Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.xticks(rotation=90)
plt.grid(True,'both','both')
plt.ylim(0,None)

plt.figure(12,figsize=(10,5))
plt.bar(comparativo_africa.index,comparativo_africa['Deaths per capita'],color='blue')
plt.title('Total COVID-19 Deaths per Capita Africa (Sub Sahara)',size=15,loc='left')
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Total Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.xticks(rotation=90)
plt.grid(True,'both','both')
plt.ylim(0,None)

plt.figure(13,figsize=(13,6))
plt.bar(comparativo_mund.index,comparativo_mund['Deaths per capita'],color='blue')
plt.title('Total COVID-19 Deaths per Capita',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Total Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.xticks(rotation=90)
plt.grid(True,'both','both')
plt.ylim(0,None)

#Datos de cambio de movilidad global:
mov_global=pd.read_csv('https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv',usecols=['date','country_region','residential_percent_change_from_baseline'])
mov_global['date']=pd.to_datetime(mov_global['date'],yearfirst=True)
mov_medio=pd.pivot_table(data=mov_global,values='residential_percent_change_from_baseline',index='country_region',aggfunc=np.mean)

#Cambio movilidad residencial por regiones en países seleccionados:
mov_latam=pd.DataFrame(data=[mov_medio['residential_percent_change_from_baseline']['Colombia'],mov_medio['residential_percent_change_from_baseline']['Mexico'],
                             mov_medio['residential_percent_change_from_baseline']['Argentina'],mov_medio['residential_percent_change_from_baseline']['Peru'],
                             mov_medio['residential_percent_change_from_baseline']['Ecuador'],mov_medio['residential_percent_change_from_baseline']['Panama'],
                             mov_medio['residential_percent_change_from_baseline']['Brazil'],mov_medio['residential_percent_change_from_baseline']['Chile'],
                             mov_medio['residential_percent_change_from_baseline']['Uruguay'],mov_medio['residential_percent_change_from_baseline']['Paraguay']],
                       index=['Colombia','México','Argentina','Perú','Ecuador','Panamá','Brasil','Chile','Uruguay','Paraguay'])
mov_latam=mov_latam.rename(columns={0:'Residential mobility average change'})
mov_latam=mov_latam.sort_values(by='Residential mobility average change',ascending=False)

mov_eur=pd.DataFrame(data=[mov_medio['residential_percent_change_from_baseline']['Poland'],mov_medio['residential_percent_change_from_baseline']['Italy'],
                             mov_medio['residential_percent_change_from_baseline']['Portugal'],mov_medio['residential_percent_change_from_baseline']['France'],
                             mov_medio['residential_percent_change_from_baseline']['Greece'],mov_medio['residential_percent_change_from_baseline']['Spain'],
                             mov_medio['residential_percent_change_from_baseline']['Austria'],mov_medio['residential_percent_change_from_baseline']['Germany'],
                             mov_medio['residential_percent_change_from_baseline']['Denmark'],mov_medio['residential_percent_change_from_baseline']['Sweden'],
                           mov_medio['residential_percent_change_from_baseline']['Netherlands'],mov_medio['residential_percent_change_from_baseline']['Belgium'],
                           mov_medio['residential_percent_change_from_baseline']['Russia'],mov_medio['residential_percent_change_from_baseline']['Finland']],
                       index=['Poland','Italy','Portugal','France','Greece','Spain','Austria','Germany','Denmark','Sweden','Netherlands','Belgium','Russia','Finland'])
mov_eur=mov_eur.rename(columns={0:'Residential mobility average change'})
mov_eur=mov_eur.sort_values(by='Residential mobility average change',ascending=False)

mov_ang=pd.DataFrame(data=[mov_medio['residential_percent_change_from_baseline']['United States'],mov_medio['residential_percent_change_from_baseline']['Australia'],
                             mov_medio['residential_percent_change_from_baseline']['United Kingdom'],mov_medio['residential_percent_change_from_baseline']['Ireland'],
                             mov_medio['residential_percent_change_from_baseline']['Canada'],mov_medio['residential_percent_change_from_baseline']['New Zealand']],
                       index=['United States','Australia','United Kingdom','Ireland','Canada','New Zealand'])
mov_ang=mov_ang.rename(columns={0:'Residential mobility average change'})
mov_ang=mov_ang.sort_values(by='Residential mobility average change',ascending=False)

mov_asia=pd.DataFrame(data=[mov_medio['residential_percent_change_from_baseline']['Japan'],mov_medio['residential_percent_change_from_baseline']['Vietnam'],
                             mov_medio['residential_percent_change_from_baseline']['India'],mov_medio['residential_percent_change_from_baseline']['Philippines'],
                             mov_medio['residential_percent_change_from_baseline']['Thailand'],mov_medio['residential_percent_change_from_baseline']['South Korea'],
                            mov_medio['residential_percent_change_from_baseline']['Mongolia'],mov_medio['residential_percent_change_from_baseline']['Indonesia']],
                       index=['Japan','Vietnam','India','Philippines','Thailand','South Korea','Mongolia','Indonesia'])
mov_asia=mov_asia.rename(columns={0:'Residential mobility average change'})
mov_asia=mov_asia.sort_values(by='Residential mobility average change',ascending=False)

mov_med=pd.DataFrame(data=[mov_medio['residential_percent_change_from_baseline']['Israel'],mov_medio['residential_percent_change_from_baseline']['Turkey'],
                             mov_medio['residential_percent_change_from_baseline']['Jordan'],mov_medio['residential_percent_change_from_baseline']['Saudi Arabia'],
                             mov_medio['residential_percent_change_from_baseline']['Iraq'],
                            mov_medio['residential_percent_change_from_baseline']['Lebanon'],mov_medio['residential_percent_change_from_baseline']['Egypt'],
                           mov_medio['residential_percent_change_from_baseline']['Libya'],mov_medio['residential_percent_change_from_baseline']['Pakistan']],
                       index=['Israel','Turkey','Jordan','Saudi Arabia','Iraq','Lebanon','Egypt','Libya','Pakistan'])
mov_med=mov_med.rename(columns={0:'Residential mobility average change'})
mov_med=mov_med.sort_values(by='Residential mobility average change',ascending=False)

mov_africa=pd.DataFrame(data=[mov_medio['residential_percent_change_from_baseline']['Nigeria'],mov_medio['residential_percent_change_from_baseline']['South Africa'],
                             mov_medio['residential_percent_change_from_baseline']['Kenya'],
                             mov_medio['residential_percent_change_from_baseline']['Mozambique'],mov_medio['residential_percent_change_from_baseline']['Namibia'],
                              mov_medio['residential_percent_change_from_baseline']['Rwanda']],
                       index=['Nigeria','South Africa','Kenya','Mozambique','Namibia','Rwanda'])
mov_africa=mov_africa.rename(columns={0:'Residential mobility average change'})
mov_africa=mov_africa.sort_values(by='Residential mobility average change',ascending=False)

#Movilidad residencial mundial:
mov_mund=mov_latam.append([mov_eur,mov_ang,mov_asia,
                                           mov_med,mov_africa]).sort_values(by='Residential mobility average change',ascending=False)
mov_mund=mov_mund.drop_duplicates()
print('----------------------------------')
print('RESIDENTIAL MOBILITY CHANGE COMPARISON:')
print(mov_mund)

comparativo_latam=pd.merge(left=comparativo_latam,right=mov_latam,left_index=True,right_index=True)
comparativo_eur=pd.merge(left=comparativo_eur,right=mov_eur,left_index=True,right_index=True)
comparativo_ang=pd.merge(left=comparativo_ang,right=mov_ang,left_index=True,right_index=True)
comparativo_asia=pd.merge(left=comparativo_asia,right=mov_asia,left_index=True,right_index=True)
comparativo_med=pd.merge(left=comparativo_med,right=mov_med,left_index=True,right_index=True)
comparativo_africa=pd.merge(left=comparativo_africa,right=mov_africa,left_index=True,right_index=True)

comparativo_mund=pd.merge(left=comparativo_mund,right=mov_mund,left_index=True,right_index=True)
comparativo_mund=comparativo_mund.drop_duplicates()
print(comparativo_mund)

x=comparativo_latam['Residential mobility average change']
y=comparativo_latam['Deaths per capita']
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
R2 = correlation_xy**2
R2=str(np.format_float_positional(R2,precision=3))
d=np.polyfit(x,y,1)
f= np.poly1d(d)
y1=f(x)
fig, ax = plt.subplots(figsize=(12,6))
plt.plot(x,y,'bo')
plt.plot(x,y1,'r')
plt.title('LATIN AMERICA Deaths per capita vs. Residential mobility change - R²='+R2,size=12,loc='left')
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Deaths/Population')
plt.xlabel('Residential mobility average change (%)',size=10)
plt.grid(True,'both','both')
plt.ylim(0,None)
for index in range(len(x)):
  ax.text(x[index], y[index], comparativo_latam.index[index], size=10)

x=comparativo_eur['Residential mobility average change']
y=comparativo_eur['Deaths per capita']
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
R2 = correlation_xy**2
R2=str(np.format_float_positional(R2,precision=3))
d=np.polyfit(x,y,1)
f= np.poly1d(d)
y1=f(x)
fig, ax = plt.subplots(figsize=(12,6))
plt.plot(x,y,'bo')
plt.plot(x,y1,'r')
plt.title('EUROPE Deaths per capita vs. Residential mobility change - R²='+R2,size=12,loc='left')
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Deaths/Population')
plt.xlabel('Residential mobility average change (%)',size=10)
plt.grid(True,'both','both')
plt.ylim(0,None)
for index in range(len(x)):
  ax.text(x[index], y[index], comparativo_eur.index[index], size=10)

x=comparativo_ang['Residential mobility average change']
y=comparativo_ang['Deaths per capita']
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
R2 = correlation_xy**2
R2=str(np.format_float_positional(R2,precision=3))
d=np.polyfit(x,y,1)
f= np.poly1d(d)
y1=f(x)
fig, ax = plt.subplots(figsize=(12,6))
plt.plot(x,y,'bo')
plt.plot(x,y1,'r')
plt.title('ANGLO Deaths per capita vs. Residential mobility change - R²='+R2,size=12,loc='left')
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Deaths/Population')
plt.xlabel('Residential mobility average change (%)',size=10)
plt.grid(True,'both','both')
plt.ylim(0,None)
for index in range(len(x)):
  ax.text(x[index], y[index], comparativo_ang.index[index], size=10)


x=comparativo_mund['Residential mobility average change']
y=comparativo_mund['Deaths per capita']
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
R2 = correlation_xy**2
R2=str(np.format_float_positional(R2,precision=3))
d=np.polyfit(x,y,1)
f= np.poly1d(d)
y1=f(x)
fig, ax = plt.subplots(figsize=(12,6))
plt.plot(x,y,'bo')
plt.plot(x,y1,'r')
plt.title('Global Deaths per capita vs. Residential mobility change - R²='+R2,size=12,loc='left')
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Deaths/Population')
plt.xlabel('Residential mobility average change (%)',size=10)
plt.grid(True,'both','both')
plt.ylim(0,None)
for index in range(len(x)):
  ax.text(x[index], y[index], comparativo_mund.index[index], size=10)

#Datos de vacunación mundial:
vacunas=pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv',
                    usecols=['location','date','people_vaccinated_per_hundred','people_fully_vaccinated_per_hundred','total_boosters_per_hundred'])
vacunas['date']=pd.to_datetime(vacunas['date'],yearfirst=True)
vacunas['year']=pd.DatetimeIndex(vacunas['date']).year
#Vacunación al final de 2021:
vac2021=vacunas[vacunas['year']==2021]
vac=pd.pivot_table(data=vac2021,values='people_vaccinated_per_hundred',index='location',aggfunc=np.max).sort_values(by='people_vaccinated_per_hundred',ascending=False)
vac_full=pd.pivot_table(data=vac2021,values='people_fully_vaccinated_per_hundred',index='location',aggfunc=np.max).sort_values(by='people_fully_vaccinated_per_hundred',ascending=False)
vac_boost=pd.pivot_table(data=vac2021,values='total_boosters_per_hundred',index='location',aggfunc=np.max).sort_values(by='total_boosters_per_hundred',ascending=False)

#Muertes año 2021:
m2021=muertes_diarias.groupby(by='Year').sum()
m2021=m2021.transpose()
m2021=m2021[[2021]].rename(columns={2021:'Deaths 2021'})

#Muertes per capita 2021:
#Muertes per capita 2021 Latinoamérica:
mpc2021_latam=pd.DataFrame(data=[m2021['Deaths 2021']['Colombia']/pob2021['PopTotal']['Colombia'],m2021['Deaths 2021']['Mexico']/pob2021['PopTotal']['Mexico'],
                               m2021['Deaths 2021']['Argentina']/pob2021['PopTotal']['Argentina'],m2021['Deaths 2021']['Peru']/pob2021['PopTotal']['Peru'],
                               m2021['Deaths 2021']['Ecuador']/pob2021['PopTotal']['Ecuador'],m2021['Deaths 2021']['Panama']/pob2021['PopTotal']['Panama'],
                               m2021['Deaths 2021']['Brazil']/pob2021['PopTotal']['Brazil'],m2021['Deaths 2021']['Chile']/pob2021['PopTotal']['Chile'],
                               m2021['Deaths 2021']['Uruguay']/pob2021['PopTotal']['Uruguay'],m2021['Deaths 2021']['Paraguay']/pob2021['PopTotal']['Paraguay']],
                         index=['Colombia','Mexico','Argentina','Peru','Ecuador','Panama','Brazil','Chile','Uruguay','Paraguay'])
mpc2021_latam=mpc2021_latam.rename(columns={0:'Deaths per capita'})
mpc2021_latam=mpc2021_latam.sort_values(by='Deaths per capita',ascending=False)

#Muertes per capita 2021 Europa:
mpc2021_eur=pd.DataFrame(data=[m2021['Deaths 2021']['Portugal']/pob2021['PopTotal']['Portugal'],m2021['Deaths 2021']['Germany']/pob2021['PopTotal']['Germany'],
                               m2021['Deaths 2021']['France']/pob2021['PopTotal']['France'],m2021['Deaths 2021']['Italy']/pob2021['PopTotal']['Italy'],
                               m2021['Deaths 2021']['Austria']/pob2021['PopTotal']['Austria'],m2021['Deaths 2021']['Poland']/pob2021['PopTotal']['Poland'],
                               m2021['Deaths 2021']['Sweden']/pob2021['PopTotal']['Sweden'],m2021['Deaths 2021']['Spain']/pob2021['PopTotal']['Spain'],
                               m2021['Deaths 2021']['Greece']/pob2021['PopTotal']['Greece'],m2021['Deaths 2021']['Denmark']/pob2021['PopTotal']['Denmark'],
                               m2021['Deaths 2021']['Netherlands']/pob2021['PopTotal']['Netherlands'],m2021['Deaths 2021']['Belgium']/pob2021['PopTotal']['Belgium'],
                               m2021['Deaths 2021']['Russia']/pob2021['PopTotal']['Russian Federation'],m2021['Deaths 2021']['Finland']/pob2021['PopTotal']['Finland']],
                         index=['Portugal','Germany','France','Italy','Austria','Poland','Sweden','Spain','Greece','Denmark','Netherlands','Belgium','Russia','Finland'])
mpc2021_eur=mpc2021_eur.rename(columns={0:'Deaths per capita'})
mpc2021_eur=mpc2021_eur.sort_values(by='Deaths per capita',ascending=False)

#Muertes per capita 2021 países anglos:
mpc2021_ang=pd.DataFrame(data=[m2021['Deaths 2021']['United Kingdom']/pob2021['PopTotal']['United Kingdom'],m2021['Deaths 2021']['US']/pob2021['PopTotal']['United States of America'],
                               m2021['Deaths 2021']['Ireland']/pob2021['PopTotal']['Ireland'],m2021['Deaths 2021']['Australia']/pob2021['PopTotal']['Australia'],
                               m2021['Deaths 2021']['New Zealand']/pob2021['PopTotal']['New Zealand'],m2021['Deaths 2021']['Canada']/pob2021['PopTotal']['Canada']],
                         index=['United Kingdom','United States','Ireland','Australia','New Zealand','Canada'])
mpc2021_ang=mpc2021_ang.rename(columns={0:'Deaths per capita'})
mpc2021_ang=mpc2021_ang.sort_values(by='Deaths per capita',ascending=False)

#Muertes per capita 2021 países asiáticos:
mpc2021_asia=pd.DataFrame(data=[m2021['Deaths 2021']['Japan']/pob2021['PopTotal']['Japan'],m2021['Deaths 2021']['Vietnam']/pob2021['PopTotal']['Viet Nam'],
                               m2021['Deaths 2021']['India']/pob2021['PopTotal']['India'],m2021['Deaths 2021']['Philippines']/pob2021['PopTotal']['Philippines'],
                               m2021['Deaths 2021']['Thailand']/pob2021['PopTotal']['Thailand'],m2021['Deaths 2021']['Korea, South']/pob2021['PopTotal']['Republic of Korea'],
                               m2021['Deaths 2021']['Mongolia']/pob2021['PopTotal']['Mongolia'],m2021['Deaths 2021']['Indonesia']/pob2021['PopTotal']['Indonesia']],
                         index=['Japan','Vietnam','India','Philippines','Thailand','South Korea','Mongolia','Indonesia'])
mpc2021_asia=mpc2021_asia.rename(columns={0:'Deaths per capita'})
mpc2021_asia=mpc2021_asia.sort_values(by='Deaths per capita',ascending=False)

#Muertes per capita 2021 medio oriente:
mpc2021_med=pd.DataFrame(data=[m2021['Deaths 2021']['Israel']/pob2021['PopTotal']['Israel'],m2021['Deaths 2021']['Turkey']/pob2021['PopTotal']['Turkey'],
                               m2021['Deaths 2021']['Jordan']/pob2021['PopTotal']['Jordan'],m2021['Deaths 2021']['Saudi Arabia']/pob2021['PopTotal']['Saudi Arabia'],
                               m2021['Deaths 2021']['Iran']/pob2021['PopTotal']['Iran (Islamic Republic of)'],m2021['Deaths 2021']['Iraq']/pob2021['PopTotal']['Iraq'],
                               m2021['Deaths 2021']['Lebanon']/pob2021['PopTotal']['Lebanon'],m2021['Deaths 2021']['Egypt']/pob2021['PopTotal']['Egypt'],
                               m2021['Deaths 2021']['Libya']/pob2021['PopTotal']['Libya'],m2021['Deaths 2021']['Pakistan']/pob2021['PopTotal']['Pakistan']],
                         index=['Israel','Turkey','Jordan','Saudi Arabia','Iran','Iraq','Lebanon','Egypt','Libya','Pakistan'])
mpc2021_med=mpc2021_med.rename(columns={0:'Deaths per capita'})
mpc2021_med=mpc2021_med.sort_values(by='Deaths per capita',ascending=False)

#Muertes per capita 2021 África:
mpc2021_africa=pd.DataFrame(data=[m2021['Deaths 2021']['Nigeria']/pob2021['PopTotal']['Nigeria'],m2021['Deaths 2021']['South Africa']/pob2021['PopTotal']['South Africa'],
                               m2021['Deaths 2021']['Kenya']/pob2021['PopTotal']['Kenya'],m2021['Deaths 2021']['Malawi']/pob2021['PopTotal']['Malawi'],
                               m2021['Deaths 2021']['Mozambique']/pob2021['PopTotal']['Mozambique'],m2021['Deaths 2021']['Ethiopia']/pob2021['PopTotal']['Ethiopia'],
                               m2021['Deaths 2021']['Namibia']/pob2021['PopTotal']['Namibia'],m2021['Deaths 2021']['Rwanda']/pob2021['PopTotal']['Rwanda']],
                         index=['Nigeria','South Africa','Kenya','Malawi','Mozambique','Ethiopia','Namibia','Rwanda'])
mpc2021_africa=mpc2021_africa.rename(columns={0:'Deaths per capita'})
mpc2021_africa=mpc2021_africa.sort_values(by='Deaths per capita',ascending=False)

#Muertes per capita 2021 mundial:
mpc2021_mund=mpc2021_latam.append([mpc2021_eur,mpc2021_ang,mpc2021_asia,
                                           mpc2021_med,mpc2021_africa]).sort_values(by='Deaths per capita',ascending=False)

print('-------------------------------------')
print('DEATHS AND VACCINATION 2021:')

#DataFrame con vacunas totales en 2021:
comp2021=pd.merge(left=mpc2021_mund,right=vac_full,left_index=True,right_index=True)
print(comp2021)


x=comp2021['people_fully_vaccinated_per_hundred']
y=comp2021['Deaths per capita']
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
R2 = correlation_xy**2
R2=str(np.format_float_positional(R2,precision=3))
d=np.polyfit(x,y,1)
f= np.poly1d(d)
y1=f(x)
fig, ax = plt.subplots(figsize=(15,7))
plt.plot(x,y,'bo')
plt.plot(x,y1,'r')
plt.title('Deaths per capita in 2021 vs. People Fully Vaccinated in 2021 - R²='+R2,size=14,loc='left')
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Total Deaths/Population in 2021',size=12)
plt.xlabel('People Fully Vaccinated at the end of 2021 (%)',size=12)
plt.grid(True,'both','both')
plt.ylim(0,None)
for index in range(len(x)):
  ax.text(x[index], y[index], comp2021.index[index], size=11)
