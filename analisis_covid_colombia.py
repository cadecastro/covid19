print('-------------------------------------------------')
print('        ANÁLISIS CIFRAS COVID-19 COLOMBIA        ')
print('Carlos Armando De Castro - https://cadecastro.com')
print('-------------------------------------------------')
print(' ')

import pandas as pd , numpy as np , matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None  # default='warn'

#Importar datos de Datos Abiertos Colombia:
print('Cargando datos de casos positivos COVID-19 Colombia...')
columnas=['Nombre departamento','Nombre municipio','Edad','Sexo','Ubicación del caso','Estado','Fecha de inicio de síntomas','Fecha de muerte']
covid=pd.read_csv('https://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv',usecols=columnas)
#Convertir fechas de muerte a formato adecuado:
covid["Fecha de muerte"] = pd.to_datetime(covid["Fecha de muerte"],dayfirst=True)
covid["Fecha de inicio de síntomas"] = pd.to_datetime(covid["Fecha de inicio de síntomas"],dayfirst=True)
#Corrección datos:
covid['Nombre departamento']=covid['Nombre departamento'].replace(to_replace=['Tolima','Caldas','STA MARTA D.E.','Cundinamarca','Santander'],
                                                                  value=['TOLIMA','CALDAS','SANTA MARTA','CUNDINAMARCA','SANTANDER'])
covid['Sexo']=covid['Sexo'].replace(to_replace=['m','f'],value=['M','F'])
covid["Período"] = pd.DatetimeIndex(covid["Fecha de muerte"]).to_period('M').astype(str)
print('Datos COVID-19 cargados.')

#Importar datos de población:
print('Cargando datos población...')
poblacion=pd.read_csv('https://raw.githubusercontent.com/cadecastro/analisis_datos/main/poblacion_deptos_2021.csv')
poblacion=poblacion.set_index('DEPARTAMENTO')
poblacion=poblacion.rename(columns={'POBLACION 2021':'Población'})
#Lectura datos población municipal:
anho=2021
pob_mun=pd.read_excel('https://github.com/cadecastro/analisis_datos/blob/main/anexo-proyecciones-poblacion-Municipal_Area_2018-2035.xlsx?raw=true',sheet_name=0,skiprows=11)
pob_mun=pob_mun[(pob_mun['AÑO']==anho)&(pob_mun['ÁREA GEOGRÁFICA']=='Total')].set_index('MPIO').drop(columns=['DPMP',
                                                                                'DP','AÑO','ÁREA GEOGRÁFICA']).rename(columns={'Total':'Población 2021'})
pob_mun=pob_mun[pob_mun['Población '+str(anho)]>200000] #Sólo municipios con más de 200k habitantes.
pob_mun.index=pob_mun.index.str.title()
pob_mun=pob_mun.rename(index={'Bogotá, D.C.':'Bogota','Medellín':'Medellin','San José De Cúcuta':'Cucuta',
                              'Ibagué':'Ibague','Popayán':'Popayan','Montería':'Monteria','San Andrés De Tumaco':'Tumaco','Tuluá':'Tulua','Cartagena De Indias':'Cartagena'})
print('Datos población cargados.')
print('')
print('Continuar análisis.')

#RESUMEN REGIONES:
casos_regiones=pd.pivot_table(covid,values='Edad',index='Nombre departamento',aggfunc=np.count_nonzero).fillna(0)
casos_regiones=casos_regiones.rename(columns={'Edad':'Casos'})
muertes_regiones=pd.pivot_table(covid[covid['Estado']=='Fallecido'],values='Edad',index='Nombre departamento',aggfunc=np.count_nonzero).fillna(0)
muertes_regiones=muertes_regiones.rename(columns={'Edad':'Muertes'})
regiones=pd.merge(casos_regiones,muertes_regiones,left_index=True,right_index=True)
regiones=pd.merge(regiones,poblacion,left_index=True,right_index=True)
del casos_regiones,muertes_regiones,poblacion
regiones['MPC']=regiones['Muertes']/regiones['Población']*100
regiones=regiones.sort_values(by='MPC',ascending=False)
#Conteo de muertes por fecha de ocurrencia:
fecha_muerte=pd.pivot_table(data=covid[covid['Estado']=='Fallecido'],values='Edad',index='Fecha de muerte',columns='Nombre departamento',aggfunc=np.count_nonzero).fillna(0)
fecha_muerte['COLOMBIA']=fecha_muerte.sum(axis=1)
fecha_muerte['Semana']=pd.DatetimeIndex(fecha_muerte.index).to_period('W').astype(str)
#Conteo de casos por fecha de inicio de síntomas:
fecha_sint=pd.pivot_table(data=covid,values='Edad',index='Fecha de inicio de síntomas',columns='Nombre departamento',aggfunc=np.count_nonzero).fillna(0)
fecha_sint['COLOMBIA']=fecha_sint.sum(axis=1)
#Cifras por sexo:
sexo=pd.pivot_table(data=covid,values='Nombre departamento',index='Sexo',aggfunc=np.count_nonzero).fillna(0).rename(columns={'Nombre departamento':'Casos'})
sexo2=pd.pivot_table(data=covid[covid['Estado']=='Fallecido'],values='Nombre departamento',index='Sexo',aggfunc=np.count_nonzero).fillna(0).rename(columns={'Nombre departamento':'Muertes'})
sexo=pd.merge(left=sexo,right=sexo2,left_index=True,right_index=True)
sexo['CFR']=sexo['Muertes']/sexo['Casos']*100
sexo=sexo.sort_values(by='Muertes',ascending=False)
del sexo2
#Casos, muertes y CFR por edad:
edades=pd.pivot_table(data=covid,values='Nombre departamento',index='Edad',aggfunc=np.count_nonzero).fillna(0).rename(columns={'Nombre departamento':'Casos'})
edades2=pd.pivot_table(data=covid[covid['Estado']=='Fallecido'],values='Nombre departamento',index='Edad',aggfunc=np.count_nonzero).fillna(0).rename(columns={'Nombre departamento':'Muertes'})
edades=pd.merge(left=edades,right=edades2,left_index=True,right_index=True)
edades['CFR']=edades['Muertes']/edades['Casos']*100
del edades2
#Edades y sexo:
edades_c=pd.pivot_table(data=covid,values='Nombre departamento',index='Edad',
                        columns='Sexo',aggfunc=np.count_nonzero).fillna(0).rename(columns={'F':'Casos F','M':'Casos M'})
edades_m=pd.pivot_table(data=covid[covid['Estado']=='Fallecido'],values='Nombre departamento',index='Edad',
                        columns='Sexo',aggfunc=np.count_nonzero).fillna(0).rename(columns={'F':'Muertes F','M':'Muertes M'})
edades_sexo=pd.merge(left=edades_c,right=edades_m,left_index=True,right_index=True)
edades_sexo['CFR M']=edades_sexo['Muertes M']/edades_sexo['Casos M']*100
edades_sexo['CFR F']=edades_sexo['Muertes F']/edades_sexo['Casos F']*100
del edades_c,edades_m

#Muertes per cápita en deptos. y distritos:
mpc=pd.DataFrame(index=fecha_muerte.index)
for depto in regiones.index:
  mpc[depto]=fecha_muerte[depto]/regiones['Población'][depto]

#MUERTES MENSUALES:
muertes_mensuales=pd.pivot_table(data=covid[covid['Estado']=='Fallecido'],values='Edad',index='Período',columns='Nombre departamento',aggfunc=np.count_nonzero).fillna(0)
muertes_mensuales['COLOMBIA']=muertes_mensuales.sum(axis=1)
#Muertes semanales:
muertes_semanales=fecha_muerte.groupby(by='Semana').sum()
#Muertes per cápita mensuales:
mpc_mensuales=pd.DataFrame(index=muertes_mensuales.index)
for depto in regiones.index:
  mpc_mensuales[depto]=muertes_mensuales[depto]/regiones['Población'][depto]

#Muertes municipios:
muertes_mun=pd.pivot_table(covid[covid['Estado']=='Fallecido'],values='Edad',index='Nombre municipio',aggfunc=np.count_nonzero).fillna(0)
muertes_mun.index=muertes_mun.index.str.title()
muertes_mun=pob_mun.join(muertes_mun).dropna().rename(columns={'Edad':'Muertes covid'})
muertes_mun['Muertes per capita (%)']=muertes_mun['Muertes covid']/muertes_mun['Población 2021']*100
muertes_mun=muertes_mun.sort_values(by='Muertes per capita (%)',ascending=False)

#Salida respuestas:
print('_______________________________________________________________________')
print('|                  ANÁLISIS CIFRAS COVID-19 COLOMBIA                  |')
print('|          Autor: Carlos Armando De Castro - cadecastro.com           |')
print('_______________________________________________________________________')
print('-------------------------------------------------------------------')
print('         POBLACIÓN EN COLOMBIA: ',np.format_float_positional(regiones['Población'].sum(),precision=0))
print('             CASOS EN COLOMBIA: ',np.format_float_positional(regiones['Casos'].sum(),precision=0))
print('           MUERTES EN COLOMBIA: ',np.format_float_positional(regiones['Muertes'].sum(),precision=0))
print('MUERTES PER CÁPITA EN COLOMBIA:',np.format_float_positional(regiones['Muertes'].sum()/regiones['Población'].sum()*100,precision=3),'%')
print('LETALIDAD POR CASO EN COLOMBIA:',np.format_float_positional(regiones['Muertes'].sum()/regiones['Casos'].sum()*100,precision=3),'%')
print('-------------------------------------------------------------------')
print('Estadísticas de edad de los casos en COLOMBIA:')
print(covid['Edad'].describe())
print('Estadísticas de edad de las muertes en COLOMBIA:')
print(covid['Edad'][covid['Estado']=='Fallecido'].describe())
print('-------------------------------------------------------------------')
print('AVISO: LAS CURVAS DE *CASOS* DEPENDEN DE LAS PRUEBAS Y')
print('POR CAMBIOS EN SU MUESTREO NO SON CONFIABLES')
print('*LA ATENCIÓN DEBE CENTRARSE EN LAS CURVAS DE MUERTES DIARIAS*')

cdc=1
plt.figure(cdc,figsize=(15,15))
plt.subplot(311)
plt.plot(fecha_muerte.index[:len(fecha_muerte)-1],fecha_muerte['COLOMBIA'][:len(fecha_muerte)-1].rolling(window =7).mean(),color='lime')
plt.title('Cifras diarias COVID-19 en Colombia',loc='left')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(fecha_muerte.index[0],fecha_muerte.index[len(fecha_muerte)-2])
plt.legend(['Media móvil 7 días'])
plt.ylabel('Muertes diarias')
plt.subplot(312)
plt.plot(fecha_sint.index[:len(fecha_sint)-6],fecha_sint['COLOMBIA'][:len(fecha_sint)-6].rolling(window =7).mean(),color='navy')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(fecha_sint.index[0],fecha_sint.index[len(fecha_sint)-7])
plt.legend(['Media móvil 7 días'])
plt.ylabel('Inicio de síntomas diarios')
plt.subplot(313)
plt.title('Muertes per cápita - media móvil 7 días')
plt.ylabel('Muertes diarias / Habitantes')
plt.plot(mpc.index[:len(mpc.index)-1],mpc['BOGOTA'][:len(mpc.index)-1].rolling(window=7).mean(),'b')
plt.plot(mpc.index[:len(mpc.index)-1],mpc['BARRANQUILLA'][:len(mpc.index)-1].rolling(window=7).mean(),'r')
plt.plot(mpc.index[:len(mpc.index)-1],mpc['VALLE'][:len(mpc.index)-1].rolling(window=7).mean(),'g')
plt.legend(['Bogotá','Barranquilla','Valle'])
plt.grid(True,which='both',axis='both')
plt.ylim(0,None)
plt.xlim(mpc.index[0],mpc.index[len(mpc.index)-2])
plt.xlabel('cadecastro.com')
cdc+=1

plt.figure(cdc,figsize=(15,15))
plt.subplot(211)
plt.bar(muertes_mensuales.index,muertes_mensuales['COLOMBIA'],color='navy')
plt.plot(muertes_mensuales.index,muertes_mensuales['COLOMBIA'].rolling(window =2).mean(),color='lime')
plt.title('Muertes mensuales COVID-19 en COLOMBIA')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xticks(rotation=90)
plt.xlim(muertes_mensuales.index[0],muertes_mensuales.index[len(muertes_mensuales.index)-1])
plt.legend(['Media móvil 2 meses','Datos'])
plt.ylabel('Muertes mensuales')
plt.subplot(212)
plt.bar(muertes_semanales.index,muertes_semanales['COLOMBIA'],color='navy',label='Dato semanal')
plt.plot(muertes_semanales.index,muertes_semanales['COLOMBIA'].rolling(window =2).mean(),color='lime',label='Media móvil 2 semanas')
plt.title('Muertes semanales COVID-19 en COLOMBIA')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xticks(rotation=90,size=6)
plt.legend()
plt.ylabel('Muertes semanales')
plt.xlabel('cadecastro.com')
cdc+=1

plt.figure(cdc,figsize=(12,10))
plt.subplot(211)
plt.bar(fecha_muerte.index[len(fecha_muerte)-31:len(fecha_muerte)-1],fecha_muerte['COLOMBIA'][len(fecha_muerte)-31:len(fecha_muerte)-1],color='navy')
plt.plot(fecha_muerte.index[len(fecha_muerte)-31:len(fecha_muerte)-1],fecha_muerte['COLOMBIA'][len(fecha_muerte)-31:len(fecha_muerte)-1].rolling(window=7).mean(),color='lime')
plt.title('Muertes COVID-19 en Colombia último mes',loc='left')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(fecha_muerte.index[len(fecha_muerte)-31],fecha_muerte.index[len(fecha_muerte)-2])
plt.ylabel('Muertes diarias')
plt.subplot(212)
plt.bar(fecha_sint.index[len(fecha_sint)-36:len(fecha_sint)-6],fecha_sint['COLOMBIA'][len(fecha_sint)-36:len(fecha_sint)-6],color='navy')
plt.plot(fecha_sint.index[len(fecha_sint)-36:len(fecha_sint)-6],fecha_sint['COLOMBIA'][len(fecha_sint)-36:len(fecha_sint)-6].rolling(window=7).mean(),color='lime')
plt.title('Casos por inicio de síntomas en Colombia último mes',loc='left')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(fecha_sint.index[len(fecha_sint)-36],fecha_sint.index[len(fecha_sint)-7])
plt.ylabel('Casos diarios')
plt.xlabel('cadecastro.com')
cdc+=1

plt.figure(cdc,figsize=(15,6))
plt.bar(regiones.index,regiones['MPC'],color='navy')
plt.title('Muertes COVID-19 per cápita')
plt.ylabel('Muertes/Habitantes (%)')
plt.grid(True,which='both',axis='y')
plt.xticks(rotation=90)
cdc+=1

plt.figure(cdc,figsize=(15,6))
plt.bar(muertes_mun.index,muertes_mun['Muertes per capita (%)'],color='navy')
plt.grid(axis='y')
plt.title('Muertes por COVID-19 per cápita en ciudades de Colombia',loc='left',size=14)
plt.title('Análisis: cadecastro.com',loc='right')
plt.ylabel('Muertes/Habitantes (%)')
plt.grid(True,which='both',axis='y')
plt.xticks(rotation=90)
cdc+=1

plt.figure(cdc,figsize=(20,12))
plt.subplot(231)
plt.fill_between(edades.index,edades['Casos'],color='navy')
plt.fill_between(edades.index,edades['Muertes'],color='lime')
plt.title('Casos y muertes COVID-19 Colombia por edad')
plt.grid(True,'both','both')
plt.legend(['Casos','Muertes'])
plt.xlim(1,114)
plt.ylim(0,None)
plt.subplot(232)
plt.plot(edades.index,edades['CFR'].rolling(window=3).mean(),'orange')
plt.plot(edades_sexo.index,edades_sexo['CFR M'].rolling(window=3).mean(),'navy')
plt.plot(edades_sexo.index,edades_sexo['CFR F'].rolling(window=3).mean(),'violet')
plt.title('Tasa de letalidad por caso y género')
plt.ylabel('Muertes/Casos (%)')
plt.xlabel('cadecastro.com')
plt.grid(True,'both','both')
plt.legend(['Global','Masculino','Femenino'])
plt.xlim(1,90)
plt.ylim(0,40)
plt.subplot(233)
plt.violinplot(covid['Edad'])
plt.violinplot(covid['Edad'][covid['Estado']=='Fallecido'])
plt.title('Distribución casos y muertes por edad',size=10)
plt.ylabel('Edad')
plt.legend(['Casos','_no label_','_no label_','_no label_','Muertes'])
plt.subplot(234)
plt.pie(sexo['Muertes'],labels=sexo.index,colors=['navy','violet'])
plt.title('Muertes COVID-19 Colombia',loc='left')
plt.subplot(235)
plt.pie(sexo['Casos'],labels=sexo.index,colors=['navy','violet'])
plt.title('Casos COVID-19 Colombia')
plt.xlabel('cadecastro.com')
plt.subplot(236)
plt.bar(sexo.index,sexo['CFR'],color='lime')
plt.title('Letalidad COVID-19 por género')
plt.ylabel('Muertes/Casos (%)')
cdc+=1

print('------------------------------------------------------------')

#REGIÓN A ANALIZAR:
depto=str(input('Departamento o distrito a analizar (todo en mayúsculas):'))
#Casos y muertes:
casos_dep=covid[covid['Nombre departamento']==depto]
muertes_dep=casos_dep[casos_dep['Estado']=='Fallecido']
#Cifras por edad:
#Casos, muertes y CFR por edad:
edades_dep=pd.pivot_table(data=casos_dep,values='Nombre departamento',index='Edad',aggfunc=np.count_nonzero).fillna(0).rename(columns={'Nombre departamento':'Casos'})
edades_dep2=pd.pivot_table(data=muertes_dep,values='Nombre departamento',index='Edad',aggfunc=np.count_nonzero).fillna(0).rename(columns={'Nombre departamento':'Muertes'})
edades_dep=pd.merge(left=edades_dep,right=edades_dep2,left_index=True,right_index=True)
edades_dep['CFR']=edades_dep['Muertes']/edades_dep['Casos']*100
del edades_dep2
#Cifras por sexo:
sexo_dep=pd.pivot_table(data=casos_dep,values='Nombre departamento',index='Sexo',aggfunc=np.count_nonzero).fillna(0).rename(columns={'Nombre departamento':'Casos'})
sexo_dep2=pd.pivot_table(data=muertes_dep,values='Nombre departamento',index='Sexo',aggfunc=np.count_nonzero).fillna(0).rename(columns={'Nombre departamento':'Muertes'})
sexo_dep=pd.merge(left=sexo_dep,right=sexo_dep2,left_index=True,right_index=True)
sexo_dep['CFR']=sexo_dep['Muertes']/sexo_dep['Casos']*100
sexo_dep=sexo_dep.sort_values(by='Muertes',ascending=False)
del sexo_dep2

print('-------------------------------------------------------------------')
print('          POBLACIÓN EN '+depto+': ',np.format_float_positional(regiones['Población'][depto].sum(),precision=0))
print('              CASOS EN '+depto+': ',np.format_float_positional(regiones['Casos'][depto].sum(),precision=0))
print('            MUERTES EN '+depto+': ',np.format_float_positional(regiones['Muertes'][depto].sum(),precision=0))
print('MUERTES PER CÁPITA EN '+depto+' :',np.format_float_positional(regiones['Muertes'][depto].sum()/regiones['Población'][depto].sum()*100,precision=3),'%')
print('LETALIDAD POR CASO EN '+depto+' :',np.format_float_positional(regiones['Muertes'][depto].sum()/regiones['Casos'][depto].sum()*100,precision=3),'%')
print('-------------------------------------------------------------------')
print('Estadísticas de edad de los casos en ',depto)
print(casos_dep['Edad'].describe())
print('Estadísticas de edad de las muertes en ',depto)
print(muertes_dep['Edad'].describe())
print('-------------------------------------------------------------------')
print('AVISO: LAS CURVAS DE *CASOS* DEPENDEN DE LAS PRUEBAS Y')
print('POR CAMBIOS EN SU MUESTREO NO SON CONFIABLES')
print('*LA ATENCIÓN DEBE CENTRARSE EN LAS CURVAS DE MUERTES DIARIAS*')

plt.figure(cdc,figsize=(12,10))
plt.subplot(211)
plt.plot(fecha_muerte[depto][:len(fecha_muerte.index)-1].rolling(window =7).mean(),color='lime')
plt.title('Cifras diarias COVID-19 '+depto,loc='left')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(fecha_muerte.index[0],fecha_muerte.index[len(fecha_muerte.index)-2])
plt.legend(['Media móvil 7 días'])
plt.ylabel('Muertes diarias')
plt.subplot(212)
plt.plot(fecha_sint.index[:len(fecha_sint.index)-6],fecha_sint[depto][:len(fecha_sint.index)-6].rolling(window =7).mean(),color='navy')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(fecha_sint.index[0],fecha_sint.index[len(fecha_sint.index)-7])
plt.legend(['Media móvil 7 días'])
plt.ylabel('Inicio síntomas diarios')
plt.xlabel('cadecastro.com')
cdc+=1

plt.figure(cdc,figsize=(15,15))
plt.subplot(211)
plt.bar(muertes_mensuales.index,muertes_mensuales[depto],color='navy')
plt.plot(muertes_mensuales.index,muertes_mensuales[depto].rolling(window =2).mean(),color='lime')
plt.title('Muertes mensuales COVID-19 en '+depto)
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xticks(rotation=90)
plt.xlim(muertes_mensuales.index[0],muertes_mensuales.index[len(muertes_mensuales.index)-1])
plt.legend(['Media móvil 2 meses','Datos'])
plt.ylabel('Muertes mensuales')
plt.subplot(212)
plt.bar(muertes_semanales.index,muertes_semanales[depto],color='navy',label='Dato semanal')
plt.plot(muertes_semanales.index,muertes_semanales[depto].rolling(window =2).mean(),color='lime',label='Media móvil 2 semanas')
plt.title('Muertes semanales COVID-19 en '+depto)
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xticks(rotation=90,size=6)
plt.legend()
plt.ylabel('Muertes semanales')
plt.xlabel('cadecastro.com')
cdc+=1

plt.figure(cdc,figsize=(12,12))
plt.subplot(211)
plt.bar(fecha_muerte.index[len(fecha_muerte.index)-31:len(fecha_muerte.index)-1],fecha_muerte[depto][len(fecha_muerte.index)-31:len(fecha_muerte.index)-1],color='navy')
plt.plot(fecha_muerte.index[len(fecha_muerte.index)-31:len(fecha_muerte.index)-1],fecha_muerte[depto][len(fecha_muerte.index)-31:len(fecha_muerte.index)-1].rolling(window=7).mean(),color='lime')
plt.title('Muertes COVID-19 en '+depto+' último mes',loc='left')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(fecha_muerte.index[len(fecha_muerte)-31],fecha_muerte.index[len(fecha_muerte.index)-2])
plt.ylabel('Muertes diarias')
plt.subplot(212)
plt.bar(fecha_sint.index[len(fecha_sint.index)-36:len(fecha_sint.index)-6],fecha_sint[depto][len(fecha_sint.index)-36:len(fecha_sint.index)-6],color='navy')
plt.plot(fecha_sint.index[len(fecha_sint.index)-36:len(fecha_sint.index)-6],fecha_sint[depto][len(fecha_sint.index)-36:len(fecha_sint.index)-6].rolling(window=7).mean(),color='lime')
plt.title('Casos por inicio de síntomas en '+depto+' último mes',loc='left')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(fecha_sint.index[len(fecha_sint.index)-36],fecha_sint.index[len(fecha_sint.index)-7])
plt.ylabel('Casos diarios')
plt.xlabel('cadecastro.com')
cdc+=1

plt.figure(cdc,figsize=(16,12))
plt.subplot(231)
plt.fill_between(edades_dep.index,edades_dep['Casos'],color='navy')
plt.fill_between(edades_dep.index,edades_dep['Muertes'],color='lime')
plt.title('Casos y muertes COVID-19 por edad '+depto,loc='left')
plt.grid(True,'both','both')
plt.legend(['Casos','Muertes'])
plt.xlim(1,114)
plt.ylim(0,None)
plt.subplot(232)
plt.plot(edades_dep.index,edades_dep['CFR'].rolling(window=3).mean(),'orange')
plt.ylabel('Muertes/Casos (%)')
plt.xlabel('cadecastro.com')
plt.grid(True,'both','both')
plt.legend(['CFR'])
plt.xlim(1,90)
plt.ylim(0,40)
plt.subplot(233)
plt.violinplot(casos_dep['Edad'])
plt.violinplot(muertes_dep['Edad'])
plt.title('Distribución casos y muertes por edad',size=10)
plt.ylabel('Edad')
plt.legend(['Casos','_no label_','_no label_','_no label_','Muertes'])
plt.subplot(234)
plt.pie(sexo_dep['Muertes'],labels=sexo_dep.index,colors=['navy','violet'])
plt.title('Muertes COVID-19 '+depto,loc='left')
plt.subplot(235)
plt.pie(sexo_dep['Casos'],labels=sexo_dep.index,colors=['navy','violet'])
plt.title('Casos COVID-19 '+depto,loc='left')
plt.xlabel('cadecastro.com')
plt.subplot(236)
plt.bar(sexo_dep.index,sexo_dep['CFR'],color='lime')
plt.title('Letalidad COVID-19 por género',loc='left')
plt.ylabel('Muertes/Casos (%)')
cdc+=1
