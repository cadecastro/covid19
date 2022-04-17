# -*- coding: utf-8 -*-
"""
ANALYSIS OF COVID-19 DATA WORLDWIDE  
Author: Carlos Armando De Castro (cadecastro.com)
"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None  # default='warn'
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#REPORTED DEATHS:
#Data from GitHub:
covid_global=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
#Remove coordinates:
covid_global=covid_global.drop(labels=['Lat','Long'],axis=1)
#Group by country:
covid_global=covid_global.groupby(['Country/Region']).sum().transpose()
#Daily deaths:
muertes_diarias=covid_global.diff(periods=1,axis=0).rename(columns={'US':'United States','Korea, South':'South Korea'})
muertes_diarias.index=pd.to_datetime(muertes_diarias.index,dayfirst=False,yearfirst=False)
muertes_diarias['World']=muertes_diarias.sum(axis=1)
muertes_diarias['Year']=pd.DatetimeIndex(muertes_diarias.index).year
muertes_diarias['Month']=pd.DatetimeIndex(muertes_diarias.index).month
muertes_diarias['Period']=pd.DatetimeIndex(muertes_diarias.index).to_period('M').astype(str)
muertes_diarias['Week']=pd.DatetimeIndex(muertes_diarias.index).to_period('W').astype(str)
#Monthly deaths:
muertes_mensuales=muertes_diarias.groupby('Period').sum()
#Weekly:
muertes_semanales=muertes_diarias.groupby('Week').sum()

#CONFIRMED CASES:
casos_global=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
#Remove coordinates:
casos_global=casos_global.drop(labels=['Lat','Long'],axis=1)
#Group by country:
casos_global=casos_global.groupby(['Country/Region']).sum().transpose()
#Daily cases:
casos_diarias=casos_global.diff(periods=1,axis=0).rename(columns={'US':'United States','Korea, South':'South Korea'})
casos_diarias.index=pd.to_datetime(casos_diarias.index,dayfirst=False,yearfirst=False)
casos_diarias['World']=casos_diarias.sum(axis=1)
casos_diarias['Period']=pd.DatetimeIndex(casos_diarias.index).to_period('M').astype(str)
casos_diarias['Year']=pd.DatetimeIndex(casos_diarias.index).year
casos_diarias['Week']=pd.DatetimeIndex(casos_diarias.index).to_period('W').astype(str)
casos_mensuales=casos_diarias.groupby('Period').sum()
casos_semanales=casos_diarias.groupby('Week').sum()

#POPULATION OF THE WORLD:
#UN Data:
pob_mundial=pd.read_csv('https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/CSV_FILES/WPP2019_TotalPopulationBySex.csv',
                        usecols=['Location','Variant','Time','PopTotal']).replace(to_replace={'United States of America':'United States',
                                                                                              'Viet Nam':'Vietnam','Republic of Korea':'South Korea',
                                                                                              'Iran (Islamic Republic of)':'Iran','Russian Federation':'Russia'})
pob_mundial['PopTotal']=1000*pob_mundial['PopTotal']
pob_mundial=pob_mundial[pob_mundial['Variant']=='Medium'].drop(columns='Variant')
#Pop. in year 2021:
pob_mundial=pob_mundial[pob_mundial['Time']==2021].drop(columns='Time')
pob_mundial=pob_mundial.set_index('Location')

#VACCINATION DATA:
vacunas=pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv',
                    usecols=['location','date','people_vaccinated_per_hundred','people_fully_vaccinated_per_hundred','total_boosters_per_hundred'])#.replace(to_replace={'South Korea':'Korea, South'})
vacunas['date']=pd.to_datetime(vacunas['date'],yearfirst=True)
vacunas['year']=pd.DatetimeIndex(vacunas['date']).year
vacunas['month']=pd.DatetimeIndex(vacunas['date']).month
vacunas['Period']=pd.DatetimeIndex(vacunas['date']).to_period('M').astype(str)
#Vacunación mensual por país:
doses=pd.pivot_table(data=vacunas,values='people_vaccinated_per_hundred',
                        index='Period',columns='location',aggfunc=np.nanmax).fillna(0)
full=pd.pivot_table(data=vacunas,values='people_fully_vaccinated_per_hundred',
                        index='Period',columns='location',aggfunc=np.nanmax).fillna(0)
boost=pd.pivot_table(data=vacunas,values='total_boosters_per_hundred',
                        index='location',columns='Period',aggfunc=np.nanmax).fillna(0)

#RESIDENTIAL MOBILITY CHANGE:
mov_global=pd.read_csv('https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv',usecols=['date','country_region','residential_percent_change_from_baseline'])
mov_global['date']=pd.to_datetime(mov_global['date'],yearfirst=True)
mov_global=pd.pivot_table(data=mov_global,values='residential_percent_change_from_baseline',index='date',columns='country_region',aggfunc=np.mean)
mov_global['Year']=pd.DatetimeIndex(mov_global.index).year
mov_global['Period']=pd.DatetimeIndex(mov_global.index).to_period('M').astype(str)
mov_month=mov_global.groupby('Period').mean()
mov_year=mov_global.groupby('Year').mean()

#Countries to analyze:
countries=set(vacunas['location']).intersection(set(muertes_diarias.columns))
countries=countries.intersection(set(pob_mundial.index))
countries=countries.intersection(set(mov_global.columns))

#Comparison DataFrame:
comparison=pd.DataFrame(index=countries,columns=['Deaths per capita (%)','Cases per capita (%)'])
for country in countries:
  comparison['Deaths per capita (%)'][country]=muertes_mensuales[country].sum()/pob_mundial['PopTotal'][country]*100
  comparison['Cases per capita (%)'][country]=casos_mensuales[country].sum()/pob_mundial['PopTotal'][country]*100
comparison=comparison.sort_values(by='Deaths per capita (%)',ascending=False)

#MONTHLY SUMMARY:
monthly={}
for country in countries:
  monthly[country]=pd.DataFrame(muertes_mensuales[country]).rename(columns={country:'Deaths'})
  monthly[country]['Cases']=pd.DataFrame(casos_mensuales[country]).rename(columns={country:'Cases'})
  monthly[country]['Fully Vax (%)']=pd.DataFrame(full[country])
  monthly[country]['Fully Vax (%)']=monthly[country]['Fully Vax (%)'].fillna(0)
  monthly[country]['Cases per capita (%)']=monthly[country]['Cases']/pob_mundial['PopTotal'][country]*100
  monthly[country]['Deaths per capita (%)']=monthly[country]['Deaths']/pob_mundial['PopTotal'][country]*100
  monthly[country]['Residential mobility change (%)']=mov_month[country]
  monthly[country]['Residential mobility change (%)']=monthly[country]['Residential mobility change (%)'].fillna(0)

#YEARLY SUMMARY:
yearly={}
for country in countries:
  yearly[country]=pd.DataFrame(muertes_diarias.groupby('Year').sum()[country]).rename(columns={country:'Deaths'})
  yearly[country]['Cases']=pd.DataFrame(casos_diarias.groupby('Year').sum()[country]).rename(columns={country:'Cases'})
  yearly[country]['Fully Vax (%)']=full=pd.pivot_table(data=vacunas[vacunas['location']==country],values='people_fully_vaccinated_per_hundred',
                        index='year',aggfunc=np.nanmax).fillna(0)
  yearly[country]['Fully Vax (%)']=yearly[country]['Fully Vax (%)'].fillna(0)
  yearly[country]['Cases per capita (%)']=yearly[country]['Cases']/pob_mundial['PopTotal'][country]*100
  yearly[country]['Deaths per capita (%)']=yearly[country]['Deaths']/pob_mundial['PopTotal'][country]*100
  yearly[country]['Residential mobility change (%)']=mov_year[country]
  yearly[country]['Residential mobility change (%)']=yearly[country]['Residential mobility change (%)'].fillna(0)

def aproximacion_polinomial(x,y,n):
    p=np.polyfit(x,y,n)
    y_pred=np.polyval(p,x)
    y_m=np.mean(y)
    SST=0
    SSR=0
    for i in range(0,len(y)):
        SSR=SSR+(y[i]-y_pred[i])**2
        SST=SST+(y[i]-y_m)**2
    R2=1-SSR/SST
    R2s=str(np.format_float_positional(R2,precision=3))
    
    return R2,y_pred, R2s


print('_____________________________________________________________________________________')
print('                         ANALYSIS OF COVID-19 DATA WORLDWIDE                         ')
print('                  Author: Carlos Armando De Castro - cadecastro.com                  ')
print('                          Analysis and Engineering Services                          ')
print('_____________________________________________________________________________________')
print(' ')
print('-----------------------------------------------------------------------')
print('       Confirmed cases World : ',np.format_float_positional(casos_diarias['World'].sum(),precision=0))
print('   Reported deaths Worldwide : ',np.format_float_positional(muertes_diarias['World'].sum(),precision=0))
print('Case Fatality Rate Worldwide : ',np.format_float_positional(muertes_diarias['World'].sum()/casos_diarias['World'].sum()*100,precision=2),'%')
print('-----------------------------------------------------------------------')
print(' ')
print('_____________________________________________________________________________')
print('Selected countries to analyze:')
print(' ')
print(comparison)
print('_____________________________________________________________________________')
print(' ')

#PLOTS:
plt.figure(1,figsize=(15,15))
plt.subplot(411)
#plt.bar(casos_diarias.index,casos_diarias['World'],color='blue')
plt.plot(casos_diarias.index,casos_diarias['World'].rolling(window =7).mean(),'navy')
plt.title('Daily and Weekly COVID-19 report Worldwide')
plt.title('cadecastro.com',loc='right')
plt.ylabel('Daily Cases')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(casos_diarias.index[0],casos_diarias.index[len(casos_diarias.index)-1])
plt.legend(['Rolling average 7 days','Daily data'])
plt.subplot(412)
#plt.bar(muertes_diarias.index,muertes_diarias['World'],color='blue')
plt.plot(muertes_diarias.index,muertes_diarias['World'].rolling(window =7).mean(),'lime')
plt.ylabel('Daily Deaths')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(muertes_diarias.index[0],muertes_diarias.index[len(muertes_diarias.index)-1])
plt.legend(['Rolling average 7 days','Daily data'])
plt.subplot(413)
plt.bar(casos_semanales.index,casos_semanales['World'],color='navy')
plt.plot(casos_semanales.index,casos_semanales['World'].rolling(window =2).mean(),'lime')
plt.ylabel('Weekly Cases')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xticks(rotation=90,size=6)
plt.legend(['Rolling average 2 weeks','Weekly data'])
plt.subplot(414)
plt.bar(muertes_semanales.index,muertes_semanales['World'],color='navy')
plt.plot(muertes_semanales.index,muertes_semanales['World'].rolling(window =2).mean(),'lime')
plt.ylabel('Weekly Deaths')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xticks(rotation=90,size=6)
plt.legend(['Rolling average 2 weeks','Weekly data'])

plt.figure(2,figsize=(12,11))
plt.subplot(211)
plt.bar(casos_mensuales.index,casos_mensuales['World'],color='navy')
plt.plot(casos_mensuales.index,casos_mensuales['World'].rolling(window =2).mean(),'lime')
plt.title('Monthly COVID-19 report Worldwide')
plt.title('cadecastro.com',loc='right')
plt.ylabel('Monthly Cases')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xticks(rotation=90)
plt.legend(['Rolling average 2 months','Monthly data'])
plt.subplot(212)
plt.bar(muertes_mensuales.index,muertes_mensuales['World'],color='navy')
plt.plot(muertes_mensuales.index,muertes_mensuales['World'].rolling(window =2).mean(),'lime')
plt.ylabel('Monthly Deaths')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xticks(rotation=90)
plt.legend(['Rolling average 2 months','Monthly data'])

plt.figure(3,figsize=(18,6))
plt.bar(comparison.index,comparison['Deaths per capita (%)'],color='navy')
plt.title('Total COVID-19 Deaths per Capita',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('COVID-19 Deaths per Capita (%)')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.xticks(rotation=90,size=8)
plt.grid(True,'both','both')
plt.ylim(0,None)

country=str(input('Country to analyze: '))

print(' ')
print('-----------------------------------------------------------------------')
print('|   Confirmed cases at ',country,': ',np.format_float_positional(casos_diarias[country].sum(),precision=0))
print('|   Reported deaths at ',country,': ',np.format_float_positional(muertes_diarias[country].sum(),precision=0))
print('|Case Fatality Rate at ',country,': ',np.format_float_positional(muertes_diarias[country].sum()/casos_diarias[country].sum()*100,precision=2),'%')
print('-----------------------------------------------------------------------')

plt.figure(4,figsize=(15,15))
plt.subplot(411)
#plt.bar(casos_diarias.index,casos_diarias[country],color='blue')
plt.plot(casos_diarias.index,casos_diarias[country].rolling(window =7).mean(),'navy')
plt.title('Daily and Weekly COVID-19 report at '+country)
plt.title('cadecastro.com',loc='right')
plt.ylabel('Daily Cases')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(casos_diarias.index[0],casos_diarias.index[len(casos_diarias.index)-1])
plt.legend(['Rolling average 7 days','Daily data'])
plt.subplot(412)
#plt.bar(muertes_diarias.index,muertes_diarias[country],color='blue')
plt.plot(muertes_diarias.index,muertes_diarias[country].rolling(window =7).mean(),'lime')
plt.ylabel('Daily Deaths')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(muertes_diarias.index[0],muertes_diarias.index[len(muertes_diarias.index)-1])
plt.legend(['Rolling average 7 days','Daily data'])
plt.subplot(413)
plt.bar(casos_semanales.index,casos_semanales[country],color='navy')
plt.plot(casos_semanales.index,casos_semanales[country].rolling(window =2).mean(),'lime')
plt.ylabel('Weekly Cases')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xticks(rotation=90,size=6)
plt.legend(['Rolling average 2 weeks','Weekly data'])
plt.subplot(414)
plt.bar(muertes_semanales.index,muertes_semanales[country],color='navy')
plt.plot(muertes_semanales.index,muertes_semanales[country].rolling(window =2).mean(),'lime')
plt.ylabel('Weekly Deaths')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xticks(rotation=90,size=6)
plt.legend(['Rolling average 2 weeks','Weekly data'])

plt.figure(5,figsize=(12,22))
plt.subplot(411)
plt.title('Monthly COVID-19 numbers at '+country,size=13,loc='center')
plt.title('cadecastro.com',loc='right')
plt.bar(monthly[country].index,monthly[country]['Deaths'],color='lime')
plt.ylabel('COVID-19 Deaths')
plt.xticks(rotation=90,size=8)
plt.grid()
plt.subplot(412)
plt.bar(monthly[country].index,monthly[country]['Cases'],color='navy')
plt.ylabel('COVID-19 Cases')
plt.xticks(rotation=90,size=8)
plt.grid()
plt.subplot(413)
plt.bar(monthly[country].index,monthly[country]['Fully Vax (%)'],color='violet')
plt.ylabel('Population fully vaccinated (%)')
plt.xticks(rotation=90,size=8)
plt.grid()
plt.subplot(414)
plt.bar(monthly[country].index,monthly[country]['Residential mobility change (%)'],color='gold')
plt.ylabel('Residential mobility change (%)')
plt.xticks(rotation=90,size=8)
plt.grid()

#Correlation between Residential Mobility and Deaths per capita:
x=monthly[country]['Residential mobility change (%)']
y=monthly[country]['Deaths per capita (%)']
R2,y_pred, R2s=aproximacion_polinomial(x,y,1)
fig, ax = plt.subplots(figsize=(12,6)) #Figure 6
plt.plot(x,y,'bo')
plt.plot(x,y_pred,'lime')
plt.title(country+' COVID-19 Deaths vs. Residential Mobility Change, Monthly - R²='+R2s,size=12,loc='left')
plt.title('cadecastro.com',size=8,loc='right')
plt.ylabel('Monthly COVID-19 Deaths per capita (%)',size=12)
plt.xlabel('Residential Mobility Change (%)',size=12)
plt.grid(True,'both','both')
plt.ylim(0,None)
for j in range(len(x)):
  ax.text(x[j], y[j], x.index[j], size=10)

period=str(input('Period to compare countries (YYYY-MM): '))

comparison2=pd.DataFrame(index=countries,columns=['Deaths per capita (%)','Fully Vax (%)','Residential mobility change (%)'])
for country in countries:
  for j in comparison2.columns:
    comparison2[j][country]=monthly[country][j][period]

comparison2=comparison2.sort_values(by='Deaths per capita (%)',ascending=False)
#Correlation between Boosters Rate and Deaths per capita:
comparison3=pd.merge(left=comparison2,right=boost[period],left_index=True,right_index=True).rename(columns={period:'Boosted (%)'})

#Correlation between Residential Mobility and Deaths per capita:
x=comparison2['Residential mobility change (%)'].astype(float)
y=comparison2['Deaths per capita (%)'].astype(float)
R2,y_pred, R2s=aproximacion_polinomial(x,y,1)
fig, ax = plt.subplots(figsize=(12,6)) #Figure 7
plt.plot(x,y,'bo')
plt.plot(x,y_pred,'lime')
plt.title('COVID-19 Deaths vs. Residential Mobility Change in '+period+' - R²='+R2s,size=12,loc='left')
plt.title('cadecastro.com',size=8,loc='right')
plt.ylabel('Monthly COVID-19 Deaths per capita (%)',size=12)
plt.xlabel('Residential Mobility Change (%)',size=12)
plt.grid(True,'both','both')
plt.ylim(0,None)
for j in range(len(x)):
  ax.text(x[j], y[j], x.index[j], size=10)


#Correlation between Vaccination Rate and Deaths per capita:
x=comparison2['Fully Vax (%)'].astype(float)
y=comparison2['Deaths per capita (%)'].astype(float)
R2,y_pred, R2s=aproximacion_polinomial(x,y,1)
fig, ax = plt.subplots(figsize=(12,6)) #Figure 8
plt.plot(x,y,'bo')
plt.plot(x,y_pred,'lime')
plt.title('COVID-19 Deaths vs. Fully Vax (%) in '+period+' - R²='+R2s,size=12,loc='left')
plt.title('cadecastro.com',size=8,loc='right')
plt.ylabel('Monthly COVID-19 Deaths per capita (%)',size=12)
plt.xlabel('Fully Vax (%)',size=12)
plt.grid(True,'both','both')
plt.ylim(0,None)
for j in range(len(x)):
  ax.text(x[j], y[j], x.index[j], size=10)

#Correlation between Boosters Rate and Deaths per capita:
x=comparison3['Boosted (%)'].astype(float)
y=comparison3['Deaths per capita (%)'].astype(float)
R2,y_pred, R2s=aproximacion_polinomial(x,y,1)
fig, ax = plt.subplots(figsize=(12,6)) #Figure 8
plt.plot(x,y,'bo')
plt.plot(x,y_pred,'lime')
plt.title('COVID-19 Deaths vs. Boosted (%) in '+period+' - R²='+R2s,size=12,loc='left')
plt.title('cadecastro.com',size=8,loc='right')
plt.ylabel('Monthly COVID-19 Deaths per capita (%)',size=12)
plt.xlabel('Boosted (%)',size=12)
plt.grid(True,'both','both')
plt.ylim(0,None)
for j in range(len(x)):
  ax.text(x[j], y[j], x.index[j], size=10)
