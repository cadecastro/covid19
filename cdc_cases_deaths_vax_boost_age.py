# -*- coding: utf-8 -*-

import pandas as pd, numpy as np, matplotlib.pyplot as plt, scipy as sp
from scipy import stats
pd.options.mode.chained_assignment = None  # default='warn'

#Read Data from CDC website - Cases and Deaths by Vacc. and Age Group:
df=pd.read_csv('https://data.cdc.gov/api/views/d6p8-wqjm/rows.csv')

vaccines=['Janssen','Moderna','Pfizer']
ages=['12-17', '18-49', '50-64', '65+']
months=['DEC 2021','JAN 2022','FEB 2022']

#Monthly CFR per status at All Age Groups Adjusted:
#df1=pd.DataFrame(index=months)
monthly1={}
monthly1['Unvaccinated']=pd.pivot_table(data=df[(df['vaccine_product']=='all_types')&(df['age_group']=='all_ages')],
                    values='unvaccinated_with_outcome',index='month',columns='outcome',aggfunc=np.sum).fillna(0)
monthly1['Unvaccinated']['CFR (%)']=monthly1['Unvaccinated']['death']/monthly1['Unvaccinated']['case']*100
monthly1['Unvaccinated']=monthly1['Unvaccinated'].loc[months,:]
for vax in vaccines:
  monthly1[vax]=pd.pivot_table(data=df[(df['vaccine_product']==vax)&(df['age_group']=='all_ages')],
                      values='primary_series_only_with_outcome',index='month',columns='outcome',aggfunc=np.sum).fillna(0)
  monthly1[vax]['CFR (%)']=monthly1[vax]['death']/monthly1[vax]['case']*100
  monthly1[vax]=monthly1[vax].loc[months,:]
  monthly1['Boosted '+vax]=pd.pivot_table(data=df[(df['vaccine_product']==vax)&(df['age_group']=='all_ages')],
                      values='boosted_with_outcome',index='month',columns='outcome',aggfunc=np.sum).fillna(0)
  monthly1['Boosted '+vax]['CFR (%)']=monthly1['Boosted '+vax]['death']/monthly1['Boosted '+vax]['case']*100
  monthly1['Boosted '+vax]=monthly1['Boosted '+vax].loc[months,:]

#Unvaccinated by Age Group:
ages_unvax={}
for age in ages:
  ages_unvax[age]=pd.pivot_table(data=df[df['age_group']==age],values='unvaccinated_with_outcome',index='month',
                    columns='outcome',aggfunc=np.sum).fillna(0)
  ages_unvax[age]['CFR (%)']=ages_unvax[age]['death']/ages_unvax[age]['case']*100
  ages_unvax[age]=ages_unvax[age].loc[months,:]

#Vaccinated by Age Group:
ages_vax={}
for age in ages:
  ages_vax[age]=pd.pivot_table(data=df[df['age_group']==age],values='primary_series_only_with_outcome',index='month',
                    columns='outcome',aggfunc=np.sum).fillna(0)
  ages_vax[age]['CFR (%)']=ages_vax[age]['death']/ages_vax[age]['case']*100
  ages_vax[age]=ages_vax[age].loc[months,:]

#Boosted by Age Group:
ages_boost={}
for age in ages:
  ages_boost[age]=pd.pivot_table(data=df[df['age_group']==age],values='boosted_with_outcome',index='month',
                    columns='outcome',aggfunc=np.sum).fillna(0)
  ages_boost[age]['CFR (%)']=ages_boost[age]['death']/ages_boost[age]['case']*100
  ages_boost[age]=ages_boost[age].loc[months,:]


t_tests=pd.DataFrame(index=['CFR Unvaxxed (%)','CFR Vaxxed (%)','CFR Boosted (%)','CFR Reduction Vax-Unvax (%)','CFR Reduction Boosted-Unvax (%)',
                            'p-value Vax-Unvax','Significant Vax-Unvax','p-value Vax-Boosted','Significant Vax-Boosted'],columns=ages)
for age in ages:
  t_tests[age]['CFR Unvaxxed (%)']=ages_unvax[age]['CFR (%)'].mean()
  t_tests[age]['CFR Vaxxed (%)']=ages_vax[age]['CFR (%)'].mean()
  t_tests[age]['CFR Boosted (%)']=ages_boost[age]['CFR (%)'].mean()
  t_tests[age]['CFR Reduction Vax-Unvax (%)']=(t_tests[age]['CFR Unvaxxed (%)']-t_tests[age]['CFR Vaxxed (%)'])/t_tests[age]['CFR Unvaxxed (%)']*100
  t_tests[age]['CFR Reduction Boosted-Unvax (%)']=(t_tests[age]['CFR Unvaxxed (%)']-t_tests[age]['CFR Boosted (%)'])/t_tests[age]['CFR Unvaxxed (%)']*100
  T,p=sp.stats.ttest_ind(ages_unvax[age]['CFR (%)'],ages_vax[age]['CFR (%)'], axis=0, equal_var=False, nan_policy='omit')
  t_tests[age]['p-value Vax-Unvax']=p
  if p<0.05:
    t_tests[age]['Significant Vax-Unvax']='Yes'
  else:
    t_tests[age]['Significant Vax-Unvax']='No'
  T,p=sp.stats.ttest_ind(ages_vax[age]['CFR (%)'],ages_boost[age]['CFR (%)'], axis=0, equal_var=False, nan_policy='omit')
  t_tests[age]['p-value Vax-Boosted']=p
  if p<0.05:
    t_tests[age]['Significant Vax-Boosted']='Yes'
  else:
    t_tests[age]['Significant Vax-Boosted']='No' 

print('____________________________________________________________________________________________')
print('t-Test on CFR by Vax. Status per Age Range in Winter 21-22:')
print(' ')
print(t_tests)
print(' ')
print('Analysis: https://cadecastro.com')
print('Source: https://data.cdc.gov/api/views/d6p8-wqjm/rows.csv')
print('____________________________________________________________________________________________')


#PLOTS:
#Monthly in Winter by vaccine:
plt.figure(1,figsize=(10,5))
plt.plot(monthly1['Unvaccinated'].index,monthly1['Unvaccinated']['CFR (%)'],color='lime',label='Unvaccinated',marker='.')
plt.plot(monthly1['Pfizer'].index,monthly1['Pfizer']['CFR (%)'],color='navy',label='Pfizer',marker='.',linestyle='-')
plt.plot(monthly1['Boosted Pfizer'].index,monthly1['Boosted Pfizer']['CFR (%)'],color='navy',label='Boosted Pfizer',marker='.',linestyle='--')
plt.plot(monthly1['Moderna'].index,monthly1['Moderna']['CFR (%)'],color='maroon',label='Moderna',marker='.',linestyle='-')
plt.plot(monthly1['Boosted Moderna'].index,monthly1['Boosted Moderna']['CFR (%)'],color='maroon',label='Boosted Moderna',marker='.',linestyle='--')
plt.plot(monthly1['Janssen'].index,monthly1['Janssen']['CFR (%)'],color='orange',label='Janssen',marker='.',linestyle='-')
plt.plot(monthly1['Boosted Janssen'].index,monthly1['Boosted Janssen']['CFR (%)'],color='orange',label='Boosted Janssen',marker='.',linestyle='--')
plt.title('COVID-19 Monthly Case Fatality Rate by Vaccine in US - All Ages Adjusted')
plt.xlabel('Analysis: https://cadecastro.com - Source: https://data.cdc.gov/api/views/d6p8-wqjm/rows.csv',size=10)
plt.ylabel('Deaths/Cases (%)')
plt.ylim(0,None)
plt.legend()
plt.grid()
#Monthly in Winter by vaccination status and Age Group:
cdc=2
for age in ages:
  plt.figure(cdc,figsize=(10,5))
  plt.plot(ages_unvax[age].index,ages_unvax[age]['CFR (%)'],color='lime',marker='.',label='Unvaccinated')
  plt.plot(ages_vax[age].index,ages_vax[age]['CFR (%)'],color='navy',marker='.',label='Vaccinated')
  plt.plot(ages_boost[age].index,ages_boost[age]['CFR (%)'],color='orange',marker='.',label='Boosted')
  plt.legend()
  plt.title('Monthly Case Fatality Rate by Vaccination Status on '+age+' Age Group')
  plt.grid()
  plt.ylim(0,None)
  plt.xlabel('Analysis: https://cadecastro.com - Source: https://data.cdc.gov/api/views/d6p8-wqjm/rows.csv',size=10)
  plt.ylabel('Deaths/Cases (%)')
  cdc+=1

for age in ages:
  plt.figure(cdc,figsize=(10,5))
  plt.boxplot([ages_unvax[age]['CFR (%)'],ages_vax[age]['CFR (%)'],ages_boost[age]['CFR (%)']])
  plt.xticks(ticks=np.array([1,2,3]),labels=['Unvaccinated','Vaccinated','Boosted'])
  plt.title('Winter 21-22 Case Fatality Rate by Vaccination Status on '+age+' Age Group')
  plt.xlabel('Analysis: https://cadecastro.com - Source: https://data.cdc.gov/api/views/d6p8-wqjm/rows.csv',size=10)
  plt.ylim(0,None)
  cdc+=1
