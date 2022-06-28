import pandas as pd
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use('seaborn')

header_list = ["Record", "Date", "Time", "ms", "V1ac Min (V)", "V1ac Avg (V)", "V1ac Max (V)", "V2ac Min (V)",
               "V2ac Avg (V)", "V2ac Max (V)", "V1dc Min (V)", "V1dc Avg (V)", "V1dc Max (V)", "V2dc Min (V)",
               "V2dc Avg (V)", "V2dc Max (V)", "I1ac Min (A)", "I1ac Avg (A)", "I1ac Max (A)", "I2ac Min (A)",
               "I2ac Avg (A)", "I2ac Max (A)", "I4ac [m] Min (A)", "I4ac [m] Avg (A)", "I4ac [m] Max (A)",
               "I1dc Min (A)", "I1dc Avg (A)", "I1dc Max (A)", "I2dc Min (A)", "I2dc Avg (A)", "I2dc Max (A)",
               "I4dc [c] Min (A)", "I4dc [c] Avg (A)", "I4dc [c] Max (A)", "TDD1 (%)", "TDD2 (%)", "TDD4 [m] (%)",
               "It1 (%)", "It2 (%)", "It4 [m] (%)", "TIF1 (%)", "TIF2 (%)", "TIF4 [m] (%)", "Watts CH1 Avg (kW)",
               "Watts CH2 Avg (kW)", "Watts Total Avg (kW)", "Watts DC CH1 (kW)", "Watts DC CH2 (kW)", "VA CH1 (kVA)",
               "VA CH2 (kVA)", "VA Total (kVA)", "PF CH1 ", "PF CH2 ", "PF Total ", "Freq Min (Hz)", "Freq Avg (Hz)",
               "Freq Max (Hz)", "PST V1 ()", "PST V2 ()", "PLT V1 ()", "PLT V2 ()", "VAR CH1 Avg (kVar)",
               "VAR CH2 Avg (kVar)", "VAR Total Avg (kVar)", "THDV1 Min (%)", "THDV1 Avg (%)", "THDV1 Max (%)",
               "THDV2 Min (%)", "THDV2 Avg (%)", "THDV2 Max (%)", "THDI1 Min (%)", "THDI1 Avg (%)", "THDI1 Max (%)",
               "THDI2 Min (%)", "THDI2 Avg (%)", "THDI2 Max (%)", "THDI4 [c] Min (%)", "THDI4 [c] Avg (%)",
               "THDI4 [c] Max (%)", "V12 Min (V)", "V12 Avg (V)", "V12 Max (V)", "V1-H3 (V)", "V1-H3 ( Degrees)",
               "V1-H5 (V)", "V1-H5 ( Degrees)", "V1-H7 (V)", "V1-H7 ( Degrees)", "V1-H9 (V)", "V1-H9 ( Degrees)",
               "V2-H3 (V)", "V2-H3 ( Degrees)", "V2-H5 (V)", "V2-H5 ( Degrees)", "V2-H7 (V)", "V2-H7 ( Degrees)",
               "V2-H9 (V)", "V2-H9 ( Degrees)", "I1-H3 (A)", "I1-H3 ( Degrees)", "I1-H5 (A)", "I1-H5 ( Degrees)",
               "I1-H9 (A)", "I1-H9 ( Degrees)", "I2-H3 (A)", "I2-H3 ( Degrees)", "I2-H5 (A)", "I2-H5 ( Degrees)",
               "I2-H9 (A)", "I2-H9 ( Degrees)", "I3-H3 (A)", "I3-H3 ( Degrees)", "I3-H5 (A)", "I3-H5 ( Degrees)",
               "I3-H9 (A)", "I3-H9 ( Degrees)", "I4-H3 [m] (A)", "I4-H3 [m] ( Degrees)", "I4-H5 [m] (A)",
               "I4-H5 [m] ( Degrees)", "I4-H9 [m] (A)", "I4-H9 [m] ( Degrees)"]

bins_list = np.arange(105, 128, 1)

df = pd.read_csv('data/.csv', encoding="ISO-8859-1", skiprows=5, names=header_list, low_memory=False)

df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"])

df2 = df.resample('W', on='Datetime')


for _, g in df2:
    Abs_Frequency_V1, intervals = np.histogram(g['V1ac Avg (V)'], bins=bins_list)
    Abs_Frequency_V2, intervals = np.histogram(g['V2ac Avg (V)'], bins=bins_list)
    # Create dataframe
    df_x = pd.DataFrame(index=np.linspace(1, 91, len(bins_list)-1), columns=['start', 'end', 'Frec_abs_V1', 'Frec_perc_V1',
                                                               'Frec_abs_V2', 'Frec_perc_V2'])


    #print(g['V2ac Avg (V)'].quantile(0.95))
    # Assign the intervals
    df_x['start'] = intervals[:-1]
    df_x['end'] = intervals[1:]

    df_x = df_x.set_index("start")
    # Assing Absolute frecuency
    df_x['Frec_abs_V1'] = Abs_Frequency_V1
    df_x['Frec_abs_V2'] = Abs_Frequency_V2

    #converst it to a percentage of the total
    df_x['Frec_perc_V1'] = df_x['Frec_abs_V1'].div(df_x['Frec_abs_V1'].sum()).mul(100).round(2)
    df_x['Frec_perc_V2'] = df_x['Frec_abs_V2'].div(df_x['Frec_abs_V2'].sum()).mul(100).round(2)

    plt.figure(figsize=(9, 25))
    fig, axs = plt.subplots(1)
    #generates the histogram
    axs[0].hist(g['V1ac Avg (V)'], weights=np.ones(len(g['V1ac Avg (V)'])) / len(g['V1ac Avg (V)']) * 100, bins=bins_list, alpha=0.5, color='blue', ec='black', label='Phase A')
    axs[0].hist(g['V2ac Avg (V)'], weights=np.ones(len(g['V2ac Avg (V)'])) / len(g['V2ac Avg (V)']) * 100, bins=bins_list, alpha=0.5, color='green', ec='black', label='Phase B')
    # Labels
    axs[0].set(xlabel='Percentage Frequency', ylabel='Voltage (V)')

    # axs[0].ylabel('Percentage Frequency', fontsize=14)
    # axs[0].xlabel('Voltage (V)', fontsize=14)
    # axs[0].xticks(fontsize=14)
    # axs[0].yticks(fontsize=14)
    # Add Title
    fig.suptitle('Voltage Averages for the week of\n' + str(_.date()) + " & " + str((_ + datetime.timedelta(days=7)).date()), fontsize=16);

    axs[0].axvline(x=110, color='yellow')
    axs[0].axvline(x=125, color='yellow')
    axs[0].axvline(x=106, color='red')
    axs[0].axvline(x=127, color='red')

    # plt.table(cellText=df_x.values, colLabels=df_x.columns, loc='bottom')
    axs[0].legend()
    #plt.subplots_adjust(left=None, bottom=.45, right=None, top=.5, wspace=.4, hspace=None)
    axs[0].set_axis_off()
    axs[0].table(cellText=df_x.values, colLabels=df_x.columns,  loc='bottom')


    plt.show()

    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(df_x)
    #
    #     print(df_x['Frec_perc_V1'].sum(), df_x['Frec_perc_V2'].sum())
    #
    #     df_z = df_x.drop([105,106,107,108,109,110,126,125])
    #     print(df_z['Frec_perc_V1'].sum(), df_z['Frec_perc_V2'].sum())

