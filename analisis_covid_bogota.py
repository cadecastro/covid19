#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 18:39:14 2021
ANÁLISIS CIFRAS COVID-19 BOGOTÁ
Autor: Carlos Armando De Castro (cadecastro.com)
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
datos=pd.read_csv('https://datosabiertos.bogota.gov.co/dataset/44eacdb7-a535-45ed-be03-16dbbea6f6da/resource/b64ba3c4-9e41-41b8-b3fd-2da21d627558/download/osb_enftransm-covid-19_14012022.csv',sep=',')
datos['FECHA_DE_INICIO_DE_SINTOMAS']=pd.to_datetime(datos['FECHA_DE_INICIO_DE_SINTOMAS'],yearfirst=True)
FIS_bog=datos['FECHA_DE_INICIO_DE_SINTOMAS'].value_counts()
FIS_bog=FIS_bog.sort_index()
activos=datos.groupby('ESTADO').count()
activos=activos.drop(['Recuperado','Fallecido','Fallecido (No aplica No causa Directa)'])
activos=activos.sort_values('CASO',ascending=False)
localidades=pd.pivot_table(datos,values='CASO',index='FECHA_DE_INICIO_DE_SINTOMAS',columns='LOCALIDAD_ASIS',aggfunc=np.count_nonzero)
total_act=activos['CASO'].sum()
asint=activos['CASO'].sum()-activos['FECHA_DE_INICIO_DE_SINTOMAS'].sum()
leve=activos['CASO']['Leve']-asint
moderado=activos['CASO']['Moderado']
grave=activos['CASO']['Grave']
estados1=['Asintomático','Síntomas leves','Moderado','Grave']
estados2=np.array([asint,leve,moderado,grave])
activos=pd.DataFrame(estados2,estados1)
print('Casos activos en Bogotá: ',total_act)
print('Casos asintomáticos: ',np.format_float_positional(asint,precision=0),' Porcentaje: ',np.format_float_positional(asint/total_act*100,precision=2),'%')
print('Casos con síntomas leves: ',leve,' Porcentaje: ',np.format_float_positional(leve/total_act*100,precision=2),' %')
print('Casos con síntomas moderados: ',moderado,' Porcentaje: ',np.format_float_positional(moderado/total_act*100,precision=2),' %')
print('Casos con síntomas graves: ',grave,' Porcentaje: ',np.format_float_positional(grave/total_act*100,precision=2),' %')
plt.figure(1,figsize=(12,5))
#plt.bar(FIS_bog.index,FIS_bog,color='blue')
plt.plot(FIS_bog.index,FIS_bog.rolling(window=7).mean(),'b')
plt.title('Casos por fecha inicio síntomas COVID-19 en Bogotá',loc='left')
plt.title('cadecastro.com',loc='right')
plt.ylabel('Casos diarios')
plt.legend(['Media móvil 7 días','Casos diarios'])
plt.ylim(0,None)
plt.xlim(FIS_bog.index[0],FIS_bog.index[len(FIS_bog)-6])
localidad=str(input('Localidad: '))
plt.grid(True,'both','both')
plt.figure(2,figsize=(12,5))
#plt.bar(localidades.index,localidades[localidad],color='blue')
plt.plot(localidades.index,localidades[localidad].rolling(window=7).mean(),'b')
plt.title('Casos por fecha inicio síntomas COVID-19 en '+localidad,loc='left')
plt.title('cadecastro.com',loc='right')
plt.ylabel('Casos diarios')
plt.legend(['Media móvil 7 días','Casos diarios'])
plt.ylim(0,None)
plt.xlim(localidades.index[0],localidades.index[len(localidades[localidad])-6])
plt.grid(True,'both','both')
plt.figure(3)
plt.bar(activos.index,activos[0],color='blue')
plt.title('Casos activos COVID-19 Bogotá',loc='left')
plt.title('cadecastro.com',loc='right')
plt.figure(4,figsize=(12,5))
plt.plot(localidades.index,localidades['Sin dato'].rolling(window=7).mean(),'r')
plt.plot(localidades.index,localidades['Suba'].rolling(window=7).mean(),'b')
plt.plot(localidades.index,localidades['Kennedy'].rolling(window=7).mean(),'y')
plt.plot(localidades.index,localidades['Santa Fe'].rolling(window=7).mean(),'c')
plt.plot(localidades.index,localidades['Chapinero'].rolling(window=7).mean(),'m')
plt.plot(localidades.index,localidades['Usaquén'].rolling(window=7).mean(),'g')
plt.legend(['Sin dato','Suba','Kennedy','Santa Fe','Chapinero','Usaquén'])
plt.title('Media móvil 7 días casos COVID-19 localidades',loc='left')
plt.xlabel('cadecastro.com')
plt.ylabel('Inicios de síntomas')
plt.ylim(0,None)
plt.xlim(localidades.index[0],localidades.index[len(localidades[localidad])-6])
plt.grid(True,'both','both')
plt.figure(5,figsize=(12,5))
#plt.bar(localidades.index,localidades['Sin dato'],color='blue')
plt.plot(localidades.index,localidades['Sin dato'].rolling(window=7).mean(),'b')
plt.title('Casos COVID-19 localidad Sin dato',loc='left')
plt.title('cadecastro.com',loc='right')
plt.ylabel('Inicios de síntomas')
plt.ylim(0,None)
plt.xlim(localidades.index[0],localidades.index[len(localidades[localidad])-6])
plt.grid(True,'both','both')
plt.legend(['Media móvil semanal','Casos diarios'])