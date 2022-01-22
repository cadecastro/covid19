#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 15:23:30 2022
ANÁLISIS REDUCCIÓN MOVILIDAD VS. MUERTES PER CÁPITA COVID-19 COLOMBIA
Autor: Carlos Armando De Castro (cadecastro.com)
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#Leer datos:
datos=pd.read_csv('https://raw.githubusercontent.com/cadecastro/covid19/main/muertes_covid_2020y2021.csv')
df=datos.dropna()
df=df.set_index(np.arange(len(df.index)))

#Recreación 2020:
x=df['Recreación 2020']
y=df['Per capita 2020']
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
R2 = correlation_xy**2
R2=str(np.format_float_positional(R2,precision=3))
d=np.polyfit(x,y,1)
f= np.poly1d(d)
y1=f(x)
fig, ax = plt.subplots(figsize=(12,6))
plt.plot(x,y,'b.')
plt.plot(x,y1,'r')
plt.xlabel("Cambio movilidad Recreación 2020 (%)", size=12)
plt.ylabel("Muertes covid / Habitantes", size=12)
plt.title("Muertes per cápita vs. Cambio movilidad Recreación 2020 - R²="+R2,loc='left',size=12)
plt.title('Análisis: cadecastro.com',loc='right')
for index in range(len(x)):
  ax.text(x[index], y[index], df['Departamento'][index], size=6)
plt.grid()
plt.legend(['Datos','Reg. Lineal'])

#Recreación 2021:
x=df['Recreación 2021']
y=df['Per capita 2021']
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
R2 = correlation_xy**2
R2=str(np.format_float_positional(R2,precision=3))
d=np.polyfit(x,y,1)
f= np.poly1d(d)
y1=f(x)
fig, ax = plt.subplots(figsize=(12,6))
plt.plot(x,y,'b.')
plt.plot(x,y1,'r')
plt.xlabel("Cambio movilidad Recreación 2021 (%)", size=12)
plt.ylabel("Muertes covid / Habitantes", size=12)
plt.title("Muertes per cápita vs. Cambio movilidad Recreación 2021 - R²="+R2,loc='left',size=12)
plt.title('Análisis: cadecastro.com',loc='right')
for index in range(len(x)):
  ax.text(x[index], y[index], df['Departamento'][index], size=6)
plt.grid()
plt.legend(['Datos','Reg. Lineal'])

#Mercados y farmacias 2020:
x=df['Mercados y farmacias 2020']
y=df['Per capita 2020']
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
R2 = correlation_xy**2
R2=str(np.format_float_positional(R2,precision=3))
d=np.polyfit(x,y,1)
f= np.poly1d(d)
y1=f(x)
fig, ax = plt.subplots(figsize=(12,6))
plt.plot(x,y,'b.')
plt.plot(x,y1,'r')
plt.xlabel("Cambio movilidad Mercados y farmacias 2020 (%)", size=12)
plt.ylabel("Muertes covid / Habitantes", size=12)
plt.title("Muertes per cápita vs. Cambio movilidad Mercados y farmacias 2020 - R²="+R2,loc='left',size=12)
plt.title('Análisis: cadecastro.com',loc='right')
for index in range(len(x)):
  ax.text(x[index], y[index], df['Departamento'][index], size=6)
plt.grid()
plt.legend(['Datos','Reg. Lineal'])

#Mercados y farmacias 2021:
x=df['Mercados y farmacias 2021']
y=df['Per capita 2021']
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
R2 = correlation_xy**2
R2=str(np.format_float_positional(R2,precision=3))
d=np.polyfit(x,y,1)
f= np.poly1d(d)
y1=f(x)
fig, ax = plt.subplots(figsize=(12,6))
plt.plot(x,y,'b.')
plt.plot(x,y1,'r')
plt.xlabel("Cambio movilidad Mercados y farmacias 2021 (%)", size=12)
plt.ylabel("Muertes covid / Habitantes", size=12)
plt.title("Muertes per cápita vs. Cambio movilidad Mercados y farmacias 2021 - R²="+R2,loc='left',size=12)
plt.title('Análisis: cadecastro.com',loc='right')
for index in range(len(x)):
  ax.text(x[index], y[index], df['Departamento'][index], size=6)
plt.grid()
plt.legend(['Datos','Reg. Lineal'])

#Parques 2020:
x=df['Parques 2020']
y=df['Per capita 2020']
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
R2 = correlation_xy**2
R2=str(np.format_float_positional(R2,precision=3))
d=np.polyfit(x,y,1)
f= np.poly1d(d)
y1=f(x)
fig, ax = plt.subplots(figsize=(12,6))
plt.plot(x,y,'b.')
plt.plot(x,y1,'r')
plt.xlabel("Cambio movilidad Parques 2020 (%)", size=12)
plt.ylabel("Muertes covid / Habitantes", size=12)
plt.title("Muertes per cápita vs. Cambio movilidad Parques 2020 - R²="+R2,loc='left',size=12)
plt.title('Análisis: cadecastro.com',loc='right')
for index in range(len(x)):
  ax.text(x[index], y[index], df['Departamento'][index], size=6)
plt.grid()
plt.legend(['Datos','Reg. Lineal'])

#Parques 2021:
x=df['Parques 2021']
y=df['Per capita 2021']
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
R2 = correlation_xy**2
R2=str(np.format_float_positional(R2,precision=3))
d=np.polyfit(x,y,1)
f= np.poly1d(d)
y1=f(x)
fig, ax = plt.subplots(figsize=(12,6))
plt.plot(x,y,'b.')
plt.plot(x,y1,'r')
plt.xlabel("Cambio movilidad Parques 2021 (%)", size=12)
plt.ylabel("Muertes covid / Habitantes", size=12)
plt.title("Muertes per cápita vs. Cambio movilidad Parques 2021 - R²="+R2,loc='left',size=12)
plt.title('Análisis: cadecastro.com',loc='right')
for index in range(len(x)):
  ax.text(x[index], y[index], df['Departamento'][index], size=6)
plt.grid()
plt.legend(['Datos','Reg. Lineal'])

#Estaciones de tránsito 2020:
x=df['Estaciones de tránsito 2020']
y=df['Per capita 2020']
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
R2 = correlation_xy**2
R2=str(np.format_float_positional(R2,precision=3))
d=np.polyfit(x,y,1)
f= np.poly1d(d)
y1=f(x)
fig, ax = plt.subplots(figsize=(12,6))
plt.plot(x,y,'b.')
plt.plot(x,y1,'r')
plt.xlabel("Cambio movilidad Estaciones de tránsito 2020 (%)", size=12)
plt.ylabel("Muertes covid / Habitantes", size=12)
plt.title("Muertes per cápita vs. Cambio movilidad Estaciones de tránsito 2020 - R²="+R2,loc='left',size=12)
plt.title('Análisis: cadecastro.com',loc='right')
for index in range(len(x)):
  ax.text(x[index], y[index], df['Departamento'][index], size=6)
plt.grid()
plt.legend(['Datos','Reg. Lineal'])

#Estaciones de tránsito 2021:
x=df['Estaciones de tránsito 2021']
y=df['Per capita 2021']
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
R2 = correlation_xy**2
R2=str(np.format_float_positional(R2,precision=3))
d=np.polyfit(x,y,1)
f= np.poly1d(d)
y1=f(x)
fig, ax = plt.subplots(figsize=(12,6))
plt.plot(x,y,'b.')
plt.plot(x,y1,'r')
plt.xlabel("Cambio movilidad Estaciones de tránsito 2021 (%)", size=12)
plt.ylabel("Muertes covid / Habitantes", size=12)
plt.title("Muertes per cápita vs. Cambio movilidad Estaciones de tránsito 2021 - R²="+R2,loc='left',size=12)
plt.title('Análisis: cadecastro.com',loc='right')
for index in range(len(x)):
  ax.text(x[index], y[index], df['Departamento'][index], size=6)
plt.grid()
plt.legend(['Datos','Reg. Lineal'])

#Puestos de trabajo 2020:
x=df['Puestos de trabajo 2020']
y=df['Per capita 2020']
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
R2 = correlation_xy**2
R2=str(np.format_float_positional(R2,precision=3))
d=np.polyfit(x,y,1)
f= np.poly1d(d)
y1=f(x)
fig, ax = plt.subplots(figsize=(12,6))
plt.plot(x,y,'b.')
plt.plot(x,y1,'r')
plt.xlabel("Cambio movilidad Puestos de trabajo 2020 (%)", size=12)
plt.ylabel("Muertes covid / Habitantes", size=12)
plt.title("Muertes per cápita vs. Cambio movilidad Puestos de trabajo 2020 - R²="+R2,loc='left',size=12)
plt.title('Análisis: cadecastro.com',loc='right')
for index in range(len(x)):
  ax.text(x[index], y[index], df['Departamento'][index], size=6)
plt.grid()
plt.legend(['Datos','Reg. Lineal'])

#Puestos de trabajo 2021:
x=df['Puestos de trabajo 2021']
y=df['Per capita 2021']
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
R2 = correlation_xy**2
R2=str(np.format_float_positional(R2,precision=3))
d=np.polyfit(x,y,1)
f= np.poly1d(d)
y1=f(x)
fig, ax = plt.subplots(figsize=(12,6))
plt.plot(x,y,'b.')
plt.plot(x,y1,'r')
plt.xlabel("Cambio movilidad Puestos de trabajo 2021 (%)", size=12)
plt.ylabel("Muertes covid / Habitantes", size=12)
plt.title("Muertes per cápita vs. Cambio movilidad Puestos de trabajo 2021 - R²="+R2,loc='left',size=12)
plt.title('Análisis: cadecastro.com',loc='right')
for index in range(len(x)):
  ax.text(x[index], y[index], df['Departamento'][index], size=6)
plt.grid()
plt.legend(['Datos','Reg. Lineal'])

#Residencial 2020:
x=df['Residencial 2020']
y=df['Per capita 2020']
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
R2 = correlation_xy**2
R2=str(np.format_float_positional(R2,precision=3))
d=np.polyfit(x,y,1)
f= np.poly1d(d)
y1=f(x)
fig, ax = plt.subplots(figsize=(12,6))
plt.plot(x,y,'b.')
plt.plot(x,y1,'r')
plt.xlabel("Cambio movilidad Residencial 2020 (%)", size=12)
plt.ylabel("Muertes covid / Habitantes", size=12)
plt.title("Muertes per cápita vs. Cambio movilidad Residencial 2020 - R²="+R2,loc='left',size=12)
plt.title('Análisis: cadecastro.com',loc='right')
for index in range(len(x)):
  ax.text(x[index], y[index], df['Departamento'][index], size=6)
plt.grid()
plt.legend(['Datos','Reg. Lineal'])

#Residencial 2021:
x=df['Residencial 2021']
y=df['Per capita 2021']
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
R2 = correlation_xy**2
R2=str(np.format_float_positional(R2,precision=3))
d=np.polyfit(x,y,1)
f= np.poly1d(d)
y1=f(x)
fig, ax = plt.subplots(figsize=(12,6))
plt.plot(x,y,'b.')
plt.plot(x,y1,'r')
plt.xlabel("Cambio movilidad Residencial 2021 (%)", size=12)
plt.ylabel("Muertes covid / Habitantes", size=12)
plt.title("Muertes per cápita vs. Cambio movilidad Residencial 2021 - R²="+R2,loc='left',size=12)
plt.title('Análisis: cadecastro.com',loc='right')
for index in range(len(x)):
  ax.text(x[index], y[index], df['Departamento'][index], size=6)
plt.grid()
plt.legend(['Datos','Reg. Lineal'])
