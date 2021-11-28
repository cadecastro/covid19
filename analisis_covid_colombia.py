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
#Importar datos de Datos Abiertos Colombia:
columnas=['Nombre departamento','Edad','Sexo','Estado','Fecha de muerte']
datos=pd.read_csv('https://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv',usecols=columnas)
#Convertir fechas de muerte a formato adecuado:
datos["Fecha de muerte"] = pd.to_datetime(datos["Fecha de muerte"],dayfirst=True)
#COLOMBIA:
#Casos que fallecieron por COVID-19:
muertes=datos[datos['Estado']=='Fallecido']
#Conteo de muertes por fecha de ocurrencia:
fecha_muerte=muertes['Fecha de muerte'].value_counts()
fecha_muerte=fecha_muerte.sort_index()
#Muertes por sexo:
sexo_muerte=muertes.groupby(['Sexo'])[['Fecha de muerte']].count()
sexo_muerte=sexo_muerte.sort_values(by=['Fecha de muerte'],ascending=False)
#Muertes por edad:
edades_muerte=muertes.groupby(['Edad'])[['Fecha de muerte']].count()
#Casos por edad:
edades_casos=datos.groupby(['Edad'])[['Edad']].count()
#CFR por edad:
CFR_edad=edades_muerte['Fecha de muerte'].divide(edades_casos['Edad'])
#Estadísticas casos por edad:
stat_edad_casos=datos['Edad'].describe()
stat_edad_muertes=muertes['Edad'].describe()
#BOGOTÁ:
#Casos y muertes:
casos_bog=datos[datos['Nombre departamento']=='BOGOTA']
muertes_bog=casos_bog[casos_bog['Estado']=='Fallecido']
#Conteo de muertes por fecha de ocurrencia:
fecha_muerte_bog=muertes_bog['Fecha de muerte'].value_counts()
fecha_muerte_bog=fecha_muerte_bog.sort_index()
#Muertes por edad:
edades_muerte_bog=muertes_bog.groupby(['Edad'])[['Fecha de muerte']].count()
#Casos por edad:
edades_casos_bog=casos_bog.groupby(['Edad'])[['Edad']].count()
#CFR por edad:
CFR_bog=edades_muerte_bog['Fecha de muerte'].divide(edades_casos_bog['Edad'])
#Estadísticas casos por edad:
stat_edad_casos_bog=casos_bog['Edad'].describe()
stat_edad_muertes_bog=muertes_bog['Edad'].describe()
#GRÁFICAS COLOMBIA:
#Gráfica de muertes diarias:
plt.figure(1)
plt.bar(fecha_muerte.index,fecha_muerte,color='blue')
fecha_muerte.rolling(window =7).mean().plot(color='red')
plt.title('Muertes diarias COVID-19 en Colombia',loc='left')
plt.title('cadecastro.com',loc='right')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.legend(['Media semanal','Datos'])
#Gráfica por edades:
plt.figure(2)
plt.fill_between(edades_casos.index,edades_casos['Edad'],color='blue')
plt.fill_between(edades_muerte.index,edades_muerte['Fecha de muerte'],color='red')
plt.title('Casos y muertes COVID-19 Colombia por edad',loc='left')
plt.xlabel('cadecastro.com')
plt.grid(True,'both','both')
plt.legend(['Casos','Muertes'])
plt.xlim(1,114)
plt.ylim(0,None)
#Gráfica CFR nacional:
plt.figure(3)
plt.plot(CFR_edad,'b')
plt.title('Letalidad por caso por edad Colombia',loc='left')
plt.title('cadecastro.com',loc='right')
plt.grid(True,'both','both')
plt.legend(['CFR'])
plt.xlim(1,90)
plt.ylim(0,0.4)
#Gráfica muertes por sexo:
plt.figure(4)
plt.pie(sexo_muerte,labels=sexo_muerte.index,colors=['red','blue'])
plt.title('Muertes COVID-19 Colombia por género',loc='left')
plt.xlabel('cadecastro.com')
#Salida estadísticas casos por edad:
print('COLOMBIA:')
print('Estadísticas de edad de los casos:')
print(stat_edad_casos)
print('Estadísticas de edad de las muertes:')
print(stat_edad_muertes)
print('Tasa de letalidad por caso =',np.format_float_positional(stat_edad_muertes['count']/stat_edad_casos['count']*100,precision=2),'%')
#GRÁFICAS BOGOTÁ:
#Gráfica de muertes diarias:
plt.figure(5)
plt.bar(fecha_muerte_bog.index,fecha_muerte_bog,color='blue')
fecha_muerte_bog.rolling(window =7).mean().plot(color='red')
plt.title('Muertes diarias COVID-19 en Bogotá',loc='left')
plt.title('cadecastro.com',loc='right')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.legend(['Media semanal','Datos'])
#Gráfica por edades:
plt.figure(6)
plt.fill_between(edades_casos_bog.index,edades_casos_bog['Edad'],color='blue')
plt.fill_between(edades_muerte_bog.index,edades_muerte_bog['Fecha de muerte'],color='red')
plt.title('Casos y muertes COVID-19 Bogotá por edad',loc='left')
plt.grid(True,'both','both')
plt.legend(['Casos','Muertes'])
plt.xlim(1,114)
plt.ylim(0,None)
plt.xlabel('cadecastro.com')
#Gráfica CFR Bogotá:
plt.figure(7)
plt.plot(CFR_bog,'b')
plt.title('Letalidad por caso por edad Bogotá',loc='left')
plt.title('cadecastro.com',loc='right')
plt.grid(True,'both','both')
plt.legend(['CFR'])
plt.xlim(1,90)
plt.ylim(0,0.4)
#Salida estadísticas casos por edad:
print('BOGOTÁ:')
print('Estadísticas de edad de los casos:')
print(stat_edad_casos_bog)
print('Estadísticas de edad de las muertes:')
print(stat_edad_muertes_bog)
print('Tasa de letalidad por caso =',np.format_float_positional(stat_edad_muertes_bog['count']/stat_edad_casos_bog['count']*100,precision=2),'%')
#DEPARTAMENTO ADICIONAL A ANALIZAR:
depto=str(input('Departamento o distrito adicional a analizar:'))
#Casos y muertes:
casos_dep=datos[datos['Nombre departamento']==depto]
muertes_dep=casos_dep[casos_dep['Estado']=='Fallecido']
#Conteo de muertes por fecha de ocurrencia:
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
print(depto)
print('Estadísticas de edad de los casos:')
print(stat_edad_casos_dep)
print('Estadísticas de edad de las muertes:')
print(stat_edad_muertes_dep)
print('Tasa de letalidad por caso =',np.format_float_positional(stat_edad_muertes_dep['count']/stat_edad_casos_dep['count']*100,precision=2),'%')
#GRÁFICAS DEPTO:
#Gráfica de muertes diarias:
plt.figure(8)
plt.bar(fecha_muerte_dep.index,fecha_muerte_dep,color='blue')
fecha_muerte_dep.rolling(window =7).mean().plot(color='red')
plt.title('Muertes diarias COVID-19 departamento',loc='left')
plt.title('cadecastro.com',loc='right')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.legend(['Media semanal','Datos'])
#Gráfica por edades:
plt.figure(9)
plt.fill_between(edades_casos_dep.index,edades_casos_dep['Edad'],color='blue')
plt.fill_between(edades_muerte_dep.index,edades_muerte_dep['Fecha de muerte'],color='red')
plt.title('Casos y muertes COVID-19 por edad Depto. seleccionado',loc='left')
plt.grid(True,'both','both')
plt.legend(['Casos','Muertes'])
plt.xlim(1,114)
plt.ylim(0,None)
plt.xlabel('cadecastro.com')
#Gráfica CFR Depto:
plt.figure(10)
plt.plot(CFR_dep,'b')
plt.title('Letalidad por caso por edad Depto. seleccionado',loc='left')
plt.title('cadecastro.com',loc='right')
plt.grid(True,'both','both')
plt.legend(['CFR'])
plt.xlim(1,90)
plt.ylim(0,0.4)
#Histograma edades muerte:
plt.figure(11)
muertes['Edad'].plot.hist(color='blue')
plt.title('Histograma muertes COVID-19 por edad',loc='left')
plt.title('cadecastro.com',loc='right')
plt.xlabel('Edad')