# -*- coding: utf-8 -*-
"""
Created on Wed March 18 2020

@author: Timothee Klein
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
import requests
import csv
import os
import pandas as pd	
import datetime as dt
import matplotlib.dates as mdates


#-------------------------------- READ INPUT -------------------------------------

#Read time series csv files from GitHub (confirmed cases)
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'#os.path.join(os.getcwd(),   )
with requests.Session() as s:
    download = s.get(url)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    data = list(cr)


#Read time series csv files (nbr of deaths)
# Path2 = os.path.join(os.getcwd(),'time_series_19-covid-Deaths.csv')
# data2 = list(csv.reader(open(Path2)))
url2 = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
with requests.Session() as s:
    download2 = s.get(url2)
    decoded_content2 = download2.content.decode('utf-8')
    cr2 = csv.reader(decoded_content2.splitlines(), delimiter=',')
    data2 = list(cr2)



#Data array for confirmed cases
data_array = np.asarray(data)
data_array=np.transpose(data_array)

#Data array nbr of deaths 
data_array2 = np.asarray(data2)
data_array2=np.transpose(data_array2)

#Dates
Dates = data_array[:,0]
Dates = Dates[4:].flatten()
Dates = [dt.datetime.strptime(date, '%m/%d/%y').date() for date in Dates]

#Array of countries' names
Country = data_array[1,:]


#-------------------------------- DATASET PARSING FUNCTION -------------------------------------
def country_data(CountryName, CountryPopulation):
	#Find column corresponding to a specific country 
	Country_index = np.where(Country == str(CountryName))
	Country_index = np.asarray(Country_index).flatten()
	Country_population = CountryPopulation

	#Append confirmed Country cases
	Country_cases=[]
	Country_confirmed=[]

	for index in Country_index:
		Country_cases = data_array[4:,index].astype(int)
		Country_confirmed = np.append(Country_confirmed, Country_cases, axis=0)

	Country_confirmed = Country_confirmed.reshape((len(Country_index), len(data_array)-4))
	Country_confirmed = np.sum(a=Country_confirmed, axis=0)	

	#Append nbr of deaths Country
	Country_cases=[]
	Country_deaths=[]

	for index in Country_index:
		Country_cases = data_array2[4:,index].astype(int)
		Country_deaths = np.append(Country_deaths, Country_cases, axis=0)

	Country_deaths = Country_deaths.reshape((len(Country_index), len(data_array2)-4))
	Country_deaths = np.sum(a=Country_deaths, axis=0)

	Country_cases = Country_confirmed / Country_population * 100
	
	return Country_cases, Country_deaths

#-----------------------------------------------------------------------------------------------

France_population = 66*10**6
France_cases, France_deaths = country_data('France', France_population)

UK_population = 66.44*10**6
UK_cases, UK_deaths = country_data('United Kingdom', UK_population)

Italy_population = 60.48*10**6
Italy_cases, Italy_deaths = country_data('Italy', Italy_population)

Korea_population = 51.47*10**6
Korea_cases, Korea_deaths = country_data('Korea, South', Korea_population)

US_population = 327.2*10**6
US_cases, US_deaths = country_data('US', US_population)

China_population = 1.386*10**9
China_cases, China_deaths = country_data('China', China_population)

Canada_population = 37.59*10**6
Canada_cases, Canada_deaths = country_data('Canada', Canada_population)

Germany_population = 82.79*10**6
Germany_cases, Germany_deaths = country_data('Germany', Germany_population)


#-------------------------------- PLOT GRAPH ---------------------------------------------------
fig, ax = plt.subplots()
ax.plot(Dates, France_cases, label="France", alpha=.8, color='b')
ax.plot(Dates, Canada_cases,label="Canada", alpha=.8, color='purple')
ax.plot(Dates, Italy_cases, label="Italy", alpha=.8, color='orange')
ax.plot(Dates, US_cases, label="US", alpha=.8, color='c')
ax.plot(Dates, China_cases, label="China", color='r', alpha=.8)
ax.plot(Dates, UK_cases,label="UK", alpha=.8, c='slategray')
ax.plot(Dates, Korea_cases,label="South Korea", alpha=.8, c='green')
ax.plot(Dates, Germany_cases,label="Germany", alpha=.8, c='pink')
ax.grid(True, color='silver', linestyle=':')
ax.grid(True, which='minor', linestyle=':', linewidth=0.5, color='lightgray')
ax.set_xlabel('Date', fontsize='small')
ax.tick_params(axis='both', which='major', labelsize=8)
ax.set_ylabel('Confirmed Cases (% Population)', fontsize='small')
fig.autofmt_xdate()
plt.xticks(np.arange(min(Dates), max(Dates), 7))
plt.legend(fontsize='small')
plt.title('Confirmed Cases COVID-19')
plt.savefig(os.path.join(os.getcwd(),('Covid19' + '.png')), dpi=300, edgecolor='k', bbox_inches='tight')
plt.show()    

