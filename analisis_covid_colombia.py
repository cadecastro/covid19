#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 22:02:08 2021
ANÁLISIS CIFRAS COVID-19 COLOMBIA
Autor: Carlos Armando De Castro (cadecastro.com)
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#Input de región de interés:
depto=str(input('Departamento o distrito a analizar (todo en mayúsculas):'))
#Importar datos de Datos Abiertos Colombia:
columnas=['Nombre departamento','Edad','Sexo','Ubicación del caso','Estado','Fecha de inicio de síntomas','Fecha de muerte']
covid=pd.read_csv('https://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv',usecols=columnas)
#Convertir fechas de muerte a formato adecuado:
covid["Fecha de muerte"] = pd.to_datetime(covid["Fecha de muerte"],dayfirst=True)
covid["Fecha de inicio de síntomas"] = pd.to_datetime(covid["Fecha de inicio de síntomas"],dayfirst=True)
#COLOMBIA:
#Casos que fallecieron por COVID-19:
muertes=covid[covid['Estado']=='Fallecido']
#Conteo de muertes por fecha de ocurrencia:
fecha_muerte=muertes['Fecha de muerte'].value_counts()
fecha_muerte=fecha_muerte.sort_index()
#Conteo de casos por fecha de inicio de síntomas:
fecha_sint=covid['Fecha de inicio de síntomas'].value_counts()
fecha_sint=fecha_sint.sort_index()
#Muertes por sexo:
sexo_muerte=muertes.groupby(['Sexo'])[['Fecha de muerte']].count()
sexo_muerte=sexo_muerte.sort_values(by=['Fecha de muerte'],ascending=False)
#Muertes por edad:
edades_muerte=muertes.groupby(['Edad'])[['Fecha de muerte']].count()
#Casos por edad:
edades_casos=covid.groupby(['Edad'])[['Edad']].count()
#CFR por edad:
CFR_edad=edades_muerte['Fecha de muerte'].divide(edades_casos['Edad'])
#Estadísticas casos por edad:
stat_edad_casos=covid['Edad'].describe()
stat_edad_muertes=muertes['Edad'].describe()
#REGIÓN A ANALIZAR:
#Casos y muertes:
casos_dep=covid[covid['Nombre departamento']==depto]
muertes_dep=casos_dep[casos_dep['Estado']=='Fallecido']
#Conteo de casos por fecha de inicio de síntomas:
fecha_sint_dep=casos_dep['Fecha de inicio de síntomas'].value_counts()
fecha_sint_dep=fecha_sint_dep.sort_index()
#Conteo por fecha de ocurrencia:
fecha_muerte_dep=muertes_dep['Fecha de muerte'].value_counts()
fecha_muerte_dep=fecha_muerte_dep.sort_index()
#Muertes por edad:
edades_muerte_dep=muertes_dep.groupby(['Edad'])[['Fecha de muerte']].count()
#Casos por edad:
edades_casos_dep=casos_dep.groupby(['Edad'])[['Edad']].count()
#CFR por edad:
CFR_dep=edades_muerte_dep['Fecha de muerte'].divide(edades_casos_dep['Edad'])
#Estadísticas casos por edad:
stat_edad_casos_dep=casos_dep['Edad'].describe()
stat_edad_muertes_dep=muertes_dep['Edad'].describe()
#Salida estadísticas casos por edad:
print('Estadísticas de edad de los casos en COLOMBIA:')
print(stat_edad_casos)
print('Estadísticas de edad de las muertes en COLOMBIA:')
print(stat_edad_muertes)
print('Tasa de letalidad por caso =',np.format_float_positional(stat_edad_muertes['count']/stat_edad_casos['count']*100,precision=2),'%')
print('Estadísticas de edad de los casos en ',depto)
print(stat_edad_casos_dep)
print('Estadísticas de edad de las muertes en ',depto)
print(stat_edad_muertes_dep)
print('Tasa de letalidad por caso =',np.format_float_positional(stat_edad_muertes_dep['count']/stat_edad_casos_dep['count']*100,precision=2),'%')
#GRÁFICAS COLOMBIA:
#Gráfica de muertes diarias:
plt.figure(1)
plt.subplot(211)
plt.bar(fecha_muerte.index[:len(fecha_muerte)-2],fecha_muerte[:len(fecha_muerte)-2],color='blue')
plt.plot(fecha_muerte.index[:len(fecha_muerte)-2],fecha_muerte[:len(fecha_muerte)-2].rolling(window =7).mean(),'r')
plt.title('Cifras diarias COVID-19 en Colombia',loc='left')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.legend(['Media semanal','Datos'])
plt.ylabel('Muertes diarias')
plt.subplot(212)
plt.bar(fecha_sint.index[:len(fecha_sint)-8],fecha_sint[:len(fecha_sint)-8],color='blue')
plt.plot(fecha_sint.index[:len(fecha_sint)-8],fecha_sint[:len(fecha_sint)-8].rolling(window =7).mean(),'r')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.legend(['Media semanal','Datos'])
plt.ylabel('Inicio de síntomas diarios')
plt.xlabel('cadecastro.com')
#Gráfica por edades:
plt.figure(2)
plt.subplot(211)
plt.fill_between(edades_casos.index,edades_casos['Edad'],color='blue')
plt.fill_between(edades_muerte.index,edades_muerte['Fecha de muerte'],color='red')
plt.title('Casos y muertes COVID-19 Colombia por edad',loc='left')
plt.grid(True,'both','both')
plt.legend(['Casos','Muertes'])
plt.xlim(1,114)
plt.ylim(0,None)
plt.subplot(212)
plt.plot(CFR_edad,'b')
plt.ylabel('Muertes/Casos')
plt.xlabel('cadecastro.com')
plt.grid(True,'both','both')
plt.legend(['CFR'])
plt.xlim(1,90)
plt.ylim(0,0.4)
#Gráfica muertes por sexo:
plt.figure(3)
plt.pie(sexo_muerte['Fecha de muerte'],labels=sexo_muerte.index,colors=['red','blue'])
plt.title('Muertes COVID-19 Colombia por género',loc='left')
#Histograma edades:
plt.figure(4)
plt.subplot(121)
covid['Edad'].plot.hist(color='blue')
plt.title('Histograma casos COVID-19',loc='left')
plt.xlabel('Edad')
plt.subplot(122)
muertes['Edad'].plot.hist(color='red')
plt.title('Histograma muertes COVID-19',loc='left')
plt.xlabel('Edad - cadecastro.com')
plt.xlabel('cadecastro.com')
#GRÁFICAS DEPTO:
#Gráfica de muertes diarias:
plt.figure(5)
plt.subplot(211)
plt.bar(fecha_muerte_dep.index[:len(fecha_muerte_dep)-2],fecha_muerte_dep[:len(fecha_muerte_dep)-2],color='blue')
fecha_muerte_dep[:len(fecha_muerte_dep)-2].rolling(window =7).mean().plot(color='red')
plt.title('Cifras diarias COVID-19 '+depto,loc='left')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.legend(['Media semanal','Datos'])
plt.ylabel('Muertes diarias')
plt.subplot(212)
plt.bar(fecha_sint_dep.index[:len(fecha_sint_dep)-8],fecha_sint_dep[:len(fecha_sint_dep)-8],color='blue')
plt.plot(fecha_sint_dep.index[:len(fecha_sint_dep)-8],fecha_sint_dep[:len(fecha_sint_dep)-8].rolling(window =7).mean(),'r')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.legend(['Media semanal','Datos'])
plt.ylabel('Inicio síntomas diarios')
plt.xlabel('cadecastro.com')
#Gráfica por edades:
plt.figure(6)
plt.subplot(211)
plt.fill_between(edades_casos_dep.index,edades_casos_dep['Edad'],color='blue')
plt.fill_between(edades_muerte_dep.index,edades_muerte_dep['Fecha de muerte'],color='red')
plt.title('Casos y muertes COVID-19 por edad '+depto,loc='left')
plt.grid(True,'both','both')
plt.legend(['Casos','Muertes'])
plt.xlim(1,114)
plt.ylim(0,None)
plt.subplot(212)
plt.plot(CFR_dep,'b')
plt.ylabel('Muertes/Casos')
plt.xlabel('cadecastro.com')
plt.grid(True,'both','both')
plt.legend(['CFR'])
plt.xlim(1,90)
plt.ylim(0,0.4)

plt.figure(7)
plt.bar(fecha_muerte.index[len(fecha_muerte)-31:len(fecha_muerte)-2],fecha_muerte[len(fecha_muerte)-31:len(fecha_muerte)-2],color='blue')
plt.plot(fecha_muerte.index[len(fecha_muerte)-31:len(fecha_muerte)-2],fecha_muerte[len(fecha_muerte)-31:len(fecha_muerte)-2].rolling(window=7).mean(),'r')
plt.title('Muertes COVID-19 en Colombia último mes',loc='left')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.ylabel('Muertes diarias')
plt.xlabel('cadecastro.com')

plt.figure(8)
plt.bar(fecha_muerte_dep.index[len(fecha_muerte_dep)-31:len(fecha_muerte_dep)-2],fecha_muerte_dep[len(fecha_muerte_dep)-31:len(fecha_muerte_dep)-2],color='blue')
plt.plot(fecha_muerte_dep.index[len(fecha_muerte_dep)-31:len(fecha_muerte_dep)-2],fecha_muerte_dep[len(fecha_muerte_dep)-31:len(fecha_muerte_dep)-2].rolling(window=7).mean(),'r')
plt.title('Muertes COVID-19 en '+depto+' último mes',loc='left')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.ylabel('Muertes diarias')
plt.xlabel('cadecastro.com')

plt.figure(9)
plt.bar(fecha_sint.index[len(fecha_sint)-39:len(fecha_sint)-8],fecha_sint[len(fecha_sint)-39:len(fecha_sint)-8],color='blue')
plt.plot(fecha_sint.index[len(fecha_sint)-39:len(fecha_sint)-8],fecha_sint[len(fecha_sint)-39:len(fecha_sint)-8].rolling(window=7).mean(),'r')
plt.title('Casos por inicio de síntomas en Colombia último mes',loc='left')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.ylabel('Casos diarios')
plt.xlabel('cadecastro.com')

plt.figure(10)
plt.bar(fecha_sint_dep.index[len(fecha_sint_dep)-39:len(fecha_sint_dep)-8],fecha_sint_dep[len(fecha_sint_dep)-39:len(fecha_sint_dep)-8],color='blue')
plt.plot(fecha_sint_dep.index[len(fecha_sint_dep)-39:len(fecha_sint_dep)-8],fecha_sint_dep[len(fecha_sint_dep)-39:len(fecha_sint_dep)-8].rolling(window=7).mean(),'r')
plt.title('Casos por inicio de síntomas en '+depto+' último mes',loc='left')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.ylabel('Casos diarios')
plt.xlabel('cadecastro.com')