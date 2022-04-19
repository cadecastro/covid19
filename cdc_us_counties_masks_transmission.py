# -*- coding: utf-8 -*-
import pandas as pd, numpy as np, matplotlib.pyplot as plt, scipy as sp
from scipy import stats
pd.options.mode.chained_assignment = None  # default='warn'

#Read Data from CDC website - Mask Mandates:
masks=pd.read_csv('https://data.cdc.gov/api/views/42jj-z7fa/rows.csv',usecols=['FIPS_Code',
                                            'Date','Masks_Order_Code', 'Face_Masks_Required_in_Public'])
masks['Date']=pd.to_datetime(masks['Date'],yearfirst=True)
#Read Data from CDC website - Community Transmission Levels:
transmission=pd.read_csv('https://data.cdc.gov/api/views/nra9-vzzn/rows.csv',usecols=['fips_code',
                                            'date','cases_per_100K_7_day_count_change','percent_test_results_reported_positive_last_7_days']).rename(columns={'fips_code':'FIPS_Code','date':'Date'})
transmission['Date']=pd.to_datetime(transmission['Date'],yearfirst=False,dayfirst=False)

#Counties in the same Data Frame by Date to compare:
df=pd.merge(masks,transmission)
df=df[df['cases_per_100K_7_day_count_change']!='suppressed']
df['cases_per_100K_7_day_count_change'] = df['cases_per_100K_7_day_count_change'].str.replace(",","").astype(float)

del masks, transmission

dates=pd.pivot_table(data=df,values='cases_per_100K_7_day_count_change',index='Date',columns='Masks_Order_Code',aggfunc=np.nanmean)

#Test to see difference in means:
T,p=sp.stats.ttest_ind(dates[1],dates[2], axis=0, equal_var=False, nan_policy='omit')
print('t-test p-value = ',p)
if p<0.05:
  cdc='Yes'
else:
  cdc='No'
tabla=pd.DataFrame([dates[1].mean(),dates[2].mean(),T,p,cdc],index=['Mean of Cases/100k with Mask Mandate',
                                                                'Mean of Cases/100k without Mask Mandate','t-Statistic','p-value','Significant Difference']).rename(columns={0:'Values'})
print('_______________________________________________________________________')
print('Value of COVID-19 Community Transmission in All US Counties')
print('         separating by Mask Mandates or Not.               ')
print(' ')
print('Dates from '+str(dates.index[0])+' to '+str(dates.index[len(dates.index)-1]))
print(' ')
print(tabla)
print('_______________________________________________________________________')
print('            Analysis: https://cadecastro.com')
print('Mask Mandates Source: https://data.cdc.gov/api/views/42jj-z7fa/rows.csv')
print(' Transmission Source: https://data.cdc.gov/api/views/8396-v7yb/rows.csv')
print('_______________________________________________________________________')

#PLOTS:
plt.figure(1,figsize=(10,5))
plt.plot(dates.index,dates[1],label='Mask Mandate',color='navy')
plt.plot(dates.index,dates[2],label='No Mask Mandate',color='lime')
plt.ylabel('Cases per 100k')
plt.xlabel('Analysis: cadecastro.com - Sources: CDC Data Sets 42jj-z7fa & 8396-v7yb',size=8)
plt.title('COVID-19 Community Transmission in Counties separated by Mask Mandate')
plt.legend()
plt.grid()

plt.figure(2,figsize=(8,5))
plt.boxplot([dates[1].dropna(),dates[2].dropna()])
plt.xticks(ticks=np.array([1,2]),labels=['Mask Mandate','No Mask Mandate'])
plt.ylabel('Cases per 100k')
plt.xlabel('Analysis: cadecastro.com - Sources: CDC Data Sets 42jj-z7fa & 8396-v7yb',size=10)
plt.title('COVID-19 Community Transmission in US Counties by Mask Mandate')
plt.grid(axis='y')
