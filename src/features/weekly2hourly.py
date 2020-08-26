import pandas as pd
import os

#%% Read excel file

dir_data_raw = 'data/data_raw/'
dir_data_processed = "data/data_processed/"
file_name = 'Data 18 months Outlook/12-01-2018/12012018.xlsx'
df_outlook = pd.read_excel(os.path.join(dir_data_raw, file_name), sheet_name='Feuil1')

# correspond to ['HOEP', 'Ontario.Demand', 'Temp', 'CDD', 'HDD', 'NUCLEAR', 'GAS', 'HYDRO', 'WIND', 'SOLAR', 'BIOFUEL'] in our dataset
independ_vars = ['HOEP', 'Ontario ED', 'Normal Average Temperature (°C)', 'Expected Nuclear Output', 'Expected Hydro Output', 'Expected Wind Output', 'Expected Self-Scheduling & Intermittent Output']
# keep only useful variables
df = df_outlook[['Date (week ending)'] + independ_vars]

#%% Pad to hourly

# add one dummy raw to the beginning
extra_weekending = df['Date (week ending)'][0] - pd.Timedelta('7 day')
extra_row = df[:1].copy()
extra_row['Date (week ending)'] = extra_weekending

df = pd.concat([extra_row, df])

# pad to hourly
df_hourly = df.set_index('Date (week ending)').shift(-1).resample(rule='H').pad().shift().dropna()
# output
df_hourly.to_csv(os.path.join(dir_data_processed, '12012018_outlook_hourly.csv'))