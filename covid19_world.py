import pandas as pd
# source data from my raspberry
# the original csv comes from here https://www.kaggle.com/imdevskp/corona-virus-report/download
df = pd.read_csv("http://g0mesp1res.dynip.sapo.pt/covid_19_clean_complete.csv")
df = df.drop(labels=None, axis=0, index=None, columns=['Province/State','Lat','Long'], level=None, inplace=False, errors='raise')
df['Date'] = pd.to_datetime(df['Date'])
pd.set_option("display.precision", 2)


# aggregation of data in countries which report data per state or region
df = df.groupby(['Date','Country/Region']).agg(sum).reset_index()

# TOTAL data set
df_total = df.groupby(df['Date'])['Deaths','Recovered','Confirmed'].sum().reset_index()
# DRate is the % deaths / cases
df_total["DRate"] = 100* df_total.Deaths / df_total.Confirmed
# DConfirmed is the new daily cases
df_total['DConfirmed'] = df_total['Confirmed'] - df_total['Confirmed'].shift(1)
# DDeaths is the new daily deaths
df_total['DDeaths'] = df_total['Deaths'] - df_total['Deaths'].shift(1)
# df_total.to_csv(r'drive/My Drive/PythonFiles/df_total.csv', index = False)
# R0, probably not well calculated
df_total['R0'] = df_total['DConfirmed'] / df_total['DConfirmed'].shift(1)

# TOTAL data set graphics
# from plotly.subplots import make_subplots
import plotly.graph_objects as go
# import plotly.express as px
import os

fig = go.Figure( go.Scatter(x=df_total.Date, y=df_total.Confirmed, name='World', stackgroup='one', line=dict(width =2)))
fig.update_layout(title_text='Total cases, world', xaxis_rangeslider_visible=False, yaxis_type="log")
# fig.show()
fig.write_image('world_cases_total.png')

fig = go.Figure( go.Scatter(x=df_total.Date, y=df_total.DConfirmed, line_shape='spline', name='World', line=dict(width =2)))
fig.update_layout(title_text='New daily cases, world', xaxis_rangeslider_visible=False, yaxis_type="log")
# fig.show()
fig.write_image('world_cases_daily.png')

fig = go.Figure( go.Scatter(x=df_total.Date, y=df_total.R0, line_shape='spline', name='World', line=dict(width =2)))
fig.update_layout(title_text='R0', xaxis_rangeslider_visible=False)
# fig.show()
fig.write_image('world_R0.png')

fig = go.Figure( go.Scatter(x=df_total.Date, y=df_total.Deaths, name='World', stackgroup='one', line=dict(width =2)))
fig.update_layout(title_text='Total deaths, world', xaxis_rangeslider_visible=False, yaxis_type="log")
# fig.show()
fig.write_image('world_deaths_total.png')

fig = go.Figure( go.Scatter(x=df_total.Date, y=df_total.DRate, name='World'))
fig.update_layout(title_text='Death rate %, world', xaxis_rangeslider_visible=False)
# fig.show()
fig.write_image('world_death_rate.png')

fig = go.Figure( go.Scatter(x=df_total.Date, y=df_total.DDeaths, line_shape='spline', name='World', line=dict(width =2)))
fig.update_layout(title_text='Daily deaths, world', xaxis_rangeslider_visible=False, yaxis_type="log")
# fig.show()
fig.write_image('world_deaths_daily.png')

fig = go.Figure( go.Scatter(x=df_total.Confirmed, y=df_total.DConfirmed, line_shape='spline', name='Daily cases', line=dict(width =2)))
fig.add_scatter(x=df_total.Confirmed, y=df_total.DDeaths, line_shape='spline', name='Daily deaths', line=dict(width =2))
fig.update_layout(title_text='Daily cases and daily deaths Vs total cases, world', xaxis_rangeslider_visible=False, yaxis_type="log")
# fig.show()
fig.write_image('world_cases_deaths_daily_Vs_total_cases_world.png')

# ----------------------------------------------------------
#new columns
df["DRate"] = 100* df.Deaths / df.Confirmed
#new delta deaths and delta confirmed, have to sort per country first
df = df.sort_values(['Country/Region','Date'])
#new columns for Delta Confirmed and Delta Deaths
df['DConfirmed'] = df['Confirmed'] - df['Confirmed'].shift(1)
df['DDeaths'] = df['Deaths'] - df['Deaths'].shift(1)

# reducing the dataset
list_countries = ['Portugal','Brazil','Spain','Italy','Germany','South Korea','Japan','France','US','United Kingdom','China']
df = df[df['Country/Region'].isin(list_countries)]

# Graphics per country
fig = go.Figure( go.Scatter(x=df[df['Country/Region'] == 'Portugal'].Date, y=df[df['Country/Region'] == 'Portugal'].Deaths, name='Portugal', stackgroup='one', line=dict(width =2)))
list = ['Brazil','Spain','Italy','Germany','South Korea','Japan','France','US','United Kingdom','China']
for i in list:
    fig.add_scatter(x=df[df['Country/Region'] == i].Date, y=df[df['Country/Region'] == i].Deaths, name=i, stackgroup='one')
fig.update_layout(title_text='Deaths per country', xaxis_rangeslider_visible=False)
# fig.show()
fig.write_image('country_deaths.png')

fig = go.Figure( go.Scatter(x=df[df['Country/Region'] == 'Portugal'].Date, y=df[df['Country/Region'] == 'Portugal'].DRate, line_shape='spline', name='Portugal', line=dict(width =5)))
list = ['Brazil','Spain','Italy','Germany','South Korea','Japan','France','US','United Kingdom','China']
for i in list:
    fig.add_scatter(x=df[df['Country/Region'] == i].Date, y=df[df['Country/Region'] == i].DRate, line_shape='spline', name=i)
fig.add_scatter(x=df_total.Date, y=df_total.DRate, line_shape='spline', name='Total')
fig.update_layout(title_text='DRate % per country', xaxis_rangeslider_visible=False)
# fig.show()
fig.write_image('country_death_rate.png')

# --------------------------------------------------------------------------
#new data set starting on the 10th death, and dropping the date
df1 = df[df.Deaths >9]
df_total1 = df_total.drop(labels=None, axis=0, index=None, columns=['Date'], level=None, inplace=False, errors='raise')
df_total1['DConfirmed'] = df_total1['Confirmed'] - df_total1['Confirmed'].shift(1)
df_total1['DDeaths'] = df_total1['Deaths'] - df_total1['Deaths'].shift(1)

# don't know how to calculate the difference between rows based on the country
# one idea is to reorganized the df1 per country, and remove the 1st row of each country
# df1 = df1.groupby('Country/Region', sort=True['Country/Region']).agg(sum).reset_index()
df1 = df1.sort_values(['Country/Region','Date'])
# new columns for Delta Confirmed and Delta Deaths
df1['DConfirmed'] = df1['Confirmed'] - df1['Confirmed'].shift(1)
df1['DDeaths'] = df1['Deaths'] - df1['Deaths'].shift(1)
df1 = df1.drop(labels=None, axis=0, index=None, columns=['Date'], level=None, inplace=False, errors='raise')

fig = go.Figure( go.Scatter(y=df1[df1['Country/Region'] == 'Portugal'].Deaths, line_shape='spline', name='Portugal', line=dict(width =5)))
list = ['Brazil','Spain','Italy','Germany','South Korea','Japan','France','US','United Kingdom','China']
for i in list:
    fig.add_scatter(y=df1[df1['Country/Region'] == i].Deaths, line_shape='spline', name=i)
#fig.add_scatter(y=df_total1.Deaths, line_shape='spline', name='Total')
fig.update_layout(title_text='Deaths per country since 10th death', xaxis_rangeslider_visible=False,yaxis_type="log")
# fig.show()
fig.write_image('country_deaths_since_10th_death.png')

fig = go.Figure( go.Scatter(y=df1[df1['Country/Region'] == 'Portugal'].DRate, line_shape='spline', name='Portugal', line=dict(width =5)))
list = ['Brazil','Spain','Italy','Germany','South Korea','Japan','France','US','United Kingdom','China']
for i in list:
    fig.add_scatter(y=df1[df1['Country/Region'] == i].DRate, line_shape='spline', name=i)
#fig.add_scatter(y=df_total1.Deaths, line_shape='spline', name='Total')
fig.update_layout(title_text='Death rate per country since 10th death', xaxis_rangeslider_visible=False)
# fig.show()
fig.write_image('country_death_rate_since_10th_death.png')

fig = go.Figure( go.Scatter(y=df1[df1['Country/Region'] == 'Portugal'].DDeaths, line_shape='spline', name='Portugal', line=dict(width =5)))
list = ['Brazil','Spain','Italy','Germany','South Korea','Japan','France','US','United Kingdom','China']
for i in list:
    fig.add_scatter(y=df1[df1['Country/Region'] == i].DDeaths, line_shape='spline', name=i)
#fig.add_scatter(y=df_total1.Deaths, line_shape='spline', name='Total')
fig.update_layout(title_text='Daily deaths per country since 10th death', xaxis_rangeslider_visible=False,yaxis_type="log")
# fig.show()
fig.write_image('country_deaths_since_10th_death.png')


fig = go.Figure( go.Scatter(x=df1[df1['Country/Region'] == 'Portugal'].Deaths, y=df1[df1['Country/Region'] == 'Portugal'].DDeaths, line_shape='spline', name='Portugal', line=dict(width =5)))
list = ['Brazil','Spain','Italy','Germany','South Korea','Japan','France','US','United Kingdom','China']
for i in list:
    fig.add_scatter(x=df1[df1['Country/Region'] == i].Deaths, y=df1[df1['Country/Region'] == i].DDeaths, line_shape='spline', name=i)
fig.add_scatter(x=df_total1.Deaths, y=df_total1.DDeaths, line_shape='spline', name='Total')
fig.update_layout(title_text='Daily deaths Vs total cases, per country', xaxis_rangeslider_visible=False,xaxis_type="log",yaxis_type="log")
# fig.show()
fig.write_image('country_deaths_daily_Vs_total_cases.png')


fig = go.Figure( go.Scatter(x=df1[df1['Country/Region'] == 'Portugal'].Confirmed, y=df1[df1['Country/Region'] == 'Portugal'].DConfirmed, line_shape='spline', name='Portugal', line=dict(width =5)))
list = ['Brazil','Spain','Italy','Germany','South Korea','Japan','France','US','United Kingdom','China']
for i in list:
    fig.add_scatter(x=df1[df1['Country/Region'] == i].Confirmed, y=df1[df1['Country/Region'] == i].DConfirmed, line_shape='spline', name=i)
fig.add_scatter(x=df_total1.Confirmed, y=df_total1.DConfirmed, line_shape='spline', name='Total')
fig.update_layout(title_text='Daily cases Vs total cases, per country', xaxis_rangeslider_visible=False,xaxis_type="log",yaxis_type="log")
# fig.show()
fig.write_image('country_cases_daily_Vs_total_cases.png')


fig = go.Figure( go.Scatter(y=df1[df1['Country/Region'] == 'Portugal'].DConfirmed, line_shape='spline', name='Portugal', line=dict(width =5)))
list = ['Brazil','Spain','Italy','Germany','South Korea','Japan','France','US','United Kingdom','China']
for i in list:
    fig.add_scatter(y=df1[df1['Country/Region'] == i].DConfirmed, line_shape='spline', name=i)
#fig.add_scatter(y=df_total1.Deaths, line_shape='spline', name='Total')
fig.update_layout(title_text='Daily cases per country since 10th death', xaxis_rangeslider_visible=False,yaxis_type="log")
# fig.show()
fig.write_image('country_cases_daily_since_10th_death.png')