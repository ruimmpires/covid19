#data source, removing unused columns and cleaning-up date format
import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/data.csv")
#df['data']=pd.to_datetime(df['data'])
df=df.drop(labels=None, axis=0, index=None, columns=['data_dados'], level=None, inplace=False, errors='raise')
pd.set_option("display.precision", 2)


#DRate is the % deaths / cases
df["DRate"] = 100* df.obitos / df.confirmados
#DRate_80_plus_m is the % deaths / cases _80_plus_m
df["DRate_80_plus_m"] = 100* df.obitos_80_plus_m / df.confirmados_80_plus_m
#DRate_80_plus_f is the % deaths / cases _80_plus_f
df["DRate_80_plus_f"] = 100* df.obitos_80_plus_f / df.confirmados_80_plus_f
#DRate_70_79_m is the % deaths / cases 70_79_m
df["DRate_70_79_m"] = 100* df.obitos_70_79_m / df.confirmados_70_79_m
#DRate_70_79_f is the % deaths / cases 70_79_f
df["DRate_70_79_f"] = 100* df.obitos_70_79_f/ df.confirmados_70_79_f
#DRate_60_69_m is the % deaths / cases 60_69_m
df["DRate_60_69_m"] = 100* df.obitos_60_69_m / df.confirmados_60_69_m
#DRate_60_69_f is the % deaths / cases _60_69_f
df["DRate_60_69_f"] = 100* df.obitos_60_69_f/ df.confirmados_60_69_f
#DRate_50_59_m is the % deaths / cases 50_59_m
df["DRate_50_59_m"] = 100* df.obitos_50_59_m / df.confirmados_50_59_m
#DRate_50_59_f is the % deaths / cases _50_59_f
df["DRate_50_59_f"] = 100* df.obitos_50_59_f/ df.confirmados_50_59_f
#DRate_40_49_m is the % deaths / cases 40_49_m
df["DRate_40_49_m"] = 100* df.obitos_40_49_m / df.confirmados_40_49_m
#DRate_40_49_f is the % deaths / cases _40_49_f
df["DRate_40_49_f"] = 100* df.obitos_40_49_f/ df.confirmados_40_49_f
#DRate_30_39_m is the % deaths / cases 30_39_m
df["DRate_30_39_m"] = 100* df.obitos_30_39_m / df.confirmados_30_39_m
#DRate_30_39_f is the % deaths / cases _30_39_f
df["DRate_30_39_f"] = 100* df.obitos_30_39_f/ df.confirmados_30_39_f
#DRate_20_29_m is the % deaths / cases 20_29_m
df["DRate_20_29_m"] = 100* df.obitos_20_29_m / df.confirmados_20_29_m
#DRate_20_29_f is the % deaths / cases _20_29_f
df["DRate_20_29_f"] = 100* df.obitos_20_29_f/ df.confirmados_20_29_f
#DRate_10_19_m is the % deaths / cases 10_19_m
df["DRate_40_49_m"] = 100* df.obitos_40_49_m / df.confirmados_10_19_m
#DRate_10_19_f is the % deaths / cases _10_19_f
df["DRate_10_19_f"] = 100* df.obitos_10_19_f/ df.confirmados_10_19_f
#DRate_0_9_m is the % deaths / cases 0_9_m
df["DRate_0_9_m"] = 100* df.obitos_0_9_m / df.confirmados_0_9_m
#DRate_0_9_f is the % deaths / cases _0_9_f
df["DRate_0_9_f"] = 100* df.obitos_0_9_f/ df.confirmados_0_9_f
#DCases is the daily cases
df['DCases'] = df['confirmados'] - df['confirmados'].shift(1)
#DDeaths is the daily deaths
df['DDeaths'] = df['obitos'] - df['obitos'].shift(1)
#DRecovered is the daily recovered
df['DRecovered'] = df['recuperados'] - df['recuperados'].shift(1)
#Dn_confirmados is the daily non confirmed
df['Dn_confirmados'] = df['n_confirmados'] - df['n_confirmados'].shift(1)
#DTests is the daily tests
df['DTests'] = df['DCases'] + df['Dn_confirmados']
# R0, probably not well calculated
df['R0'] = df['DCases'] / df['DCases'].shift(1)


import plotly.graph_objects as go
#import plotly.express as px
import os
import datetime

fig = go.Figure( go.Scatter(x=df.data, y=df.DRate, line_shape='spline', name='Death rate overall', line=dict(width =5)))
fig.add_scatter(x=df.data, y=df.DRate_80_plus_m,line_shape='spline', name='Death rate 80+m', line=dict(width =2))
fig.add_scatter(x=df.data, y=df.DRate_80_plus_f, line_shape='spline', name='Death rate 80+f', line=dict(width =2))
fig.add_scatter(x=df.data, y=df.DRate_70_79_m, line_shape='spline', name='Death rate 70_79_m', line=dict(width =2))
fig.add_scatter(x=df.data, y=df.DRate_70_79_f, line_shape='spline', name='Death rate 70_79_f', line=dict(width =2))
fig.add_scatter(x=df.data, y=df.DRate_60_69_m, line_shape='spline', name='Death rate 60_69_m', line=dict(width =2))
fig.add_scatter(x=df.data, y=df.DRate_60_69_f, line_shape='spline', name='Death rate 60_69_g', line=dict(width =2))
fig.add_scatter(x=df.data, y=df.DRate_50_59_m, line_shape='spline', name='Death rate 50_59_m', line=dict(width =2))
fig.add_scatter(x=df.data, y=df.DRate_50_59_f, line_shape='spline', name='Death rate 50_59_f', line=dict(width =2))
fig.add_scatter(x=df.data, y=df.DRate_40_49_m, line_shape='spline', name='Death rate 40_49_m', line=dict(width =2))
fig.add_scatter(x=df.data, y=df.DRate_40_49_f, line_shape='spline', name='Death rate 40_49_g', line=dict(width =2))
fig.add_scatter(x=df.data, y=df.DRate_30_39_m, line_shape='spline', name='Death rate 30_39_m', line=dict(width =2))
fig.add_scatter(x=df.data, y=df.DRate_30_39_f, line_shape='spline', name='Death rate 30_39_f', line=dict(width =2))
fig.add_scatter(x=df.data, y=df.DRate_20_29_m, line_shape='spline', name='Death rate 20_29_m', line=dict(width =2))
fig.add_scatter(x=df.data, y=df.DRate_20_29_f, line_shape='spline', name='Death rate 20_29_g', line=dict(width =2))
# fig.update_layout(title_text='Death rate per age, portugal', xaxis_rangeslider_visible=False, yaxis_type="log")
#fig.update_layout(title_text='Death rate per age, portugal', xaxis_rangeslider_visible=False, xaxis_range=[datetime.datetime(2020, 5, 5),datetime.datetime(2020, 12, 31)])
fig.update_layout(title_text='Death rate per age, portugal', xaxis_rangeslider_visible=False,
                  xaxis_range=['1-4-2020','31-12-2020'])
# fig.show()
fig.write_image('portugal_death_rate_age.png')

fig = go.Figure( go.Scatter(x=df.data, y=df.confirmados, line_shape='spline', name='cases', line=dict(width =5)))
fig.add_scatter(x=df.data, y=df.obitos,line_shape='spline', name='deaths', line=dict(width =2))
# fig.add_scatter(x=df.data, y=df.recuperados, line_shape='spline', name='recovered', line=dict(width =2))
fig.update_layout(title_text='Cases and deaths, Portugal', xaxis_rangeslider_visible=False, yaxis_type="log")
# fig.show()
fig.write_image('portugal_cases_deaths.png')

fig = go.Figure( go.Scatter(x=df.data, y=df.R0, line_shape='spline', name='R0', line=dict(width =5)))
fig.update_layout(title_text='R0, Portugal')
# fig.show()
fig.write_image('portugal_R0.png')


fig = go.Figure( go.Scatter(x=df.data, y=df.DCases, line_shape='spline', name='cases', line=dict(width =5)))
fig.add_scatter(x=df.data, y=df.DDeaths,line_shape='spline', name='deaths', line=dict(width =2))
# fig.add_scatter(x=df.data, y=df.DRecovered, line_shape='spline', name='recovered', line=dict(width =2))
fig.update_layout(title_text='Daily cases and deaths, Portugal', xaxis_rangeslider_visible=False, yaxis_type="log")
# fig.show()
fig.write_image('portugal_cases_deaths_daily.png')

fig = go.Figure( go.Scatter(x=df.confirmados, y=df.DCases, line_shape='spline', name='cases', line=dict(width =5)))
fig.add_scatter(x=df.confirmados, y=df.DDeaths,line_shape='spline', name='deaths', line=dict(width =2))
# fig.add_scatter(x=df.confirmados, y=df.DRecovered, line_shape='spline', name='recovered', line=dict(width =2))
fig.update_layout(title_text='Daily cases and deaths Vs total cases, Portugal', xaxis_rangeslider_visible=False, yaxis_type="log")
# fig.show()
fig.write_image('portugal_cases_deaths_daily_vs_cases.png')

fig = go.Figure( go.Bar(x=df.data, y=df.DCases,  name='confimed'))
# fig.add_trace(go.Bar(x=df.data, y=df.DTests, name='tests'))
fig.add_trace(go.Bar(x=df.data, y=df.Dn_confirmados, name='non-confirmed'))
fig.update_layout(title_text='Daily tests, Portugal', barmode='stack', xaxis_rangeslider_visible=False)
# fig.show()
fig.write_image('portugal_cases_tests_nconf_daily.png')

fig = go.Figure( go.Scatter(x=df.data, y=df.internados, line_shape='spline', name='Hospital', line=dict(width =2)))
fig.add_scatter(x=df.data, y=df.internados_uci,line_shape='spline', name='UCI', line=dict(width =2))
fig.add_scatter(x=df.data, y=df.obitos, line_shape='spline', name='deaths', line=dict(width =2))
fig.add_trace(go.Bar(x=df.data, y=df.DDeaths*10, name='daily deaths x 10'))
fig.update_layout(title_text='Hospital, UCI and daily deaths, Portugal', xaxis_rangeslider_visible=False)
# fig.show()
fig.write_image('portugal_hospital_uci_deaths_daily.png')
