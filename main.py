import pandas as pd
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
import datetime

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

bins_list = np.arange(105, 128, 0.25)

df = pd.read_csv('data/.csv', encoding="ISO-8859-1", skiprows=5, names=header_list, low_memory=False)

df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"])

df2 = df.resample('W', on='Datetime')


for _, g in df2:
    # x = plt.hist(g['V1ac Avg (V)'], density=True, histtype='bar', facecolor='b', alpha=0.5, bins=bins_list, label='Phase A')
    # plt.hist(g['V2ac Avg (V)'], density=True, histtype='bar', facecolor='y', alpha=0.5, bins=bins_list, label='Phase B')
    # plt.title('Voltage Averages for the week of\n' + str(_.date()) + " & " + str((_ + datetime.timedelta(days=7)).date()))
    # plt.axvline(x=110, color='yellow')
    # plt.axvline(x=125, color='yellow')
    # plt.axvline(x=106, color='red')
    # plt.axvline(x=127, color='red')
    # plt.xlabel("Voltage Bins")
    # plt.ylabel("Probability")
    # plt.legend()
    Abs_frecuency, intervals = np.histogram(g['V1ac Avg (V)'], bins = bins_list)
    # Create dataframe
    df_x = pd.DataFrame(index=np.linspace(1, 91, 91), columns=['start', 'end', 'V1ac', 'Frec_abs', 'Frec_perc'])
    # Assign the intervals
    df_x['start'] = intervals[:-1]
    df_x['end'] = intervals[1:]
    # Calculate class marks
    df_x['V1ac'] = (df_x['start'] + df_x['end']) / 2
    # Assing Absolute frecuency
    df_x['Frec_abs'] = Abs_frecuency

    df_x['Frec_perc'] = df_x['Frec_abs'].div(df_x['Frec_abs'].sum()).mul(100).round(2)




    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df_x)




    plt.hist(g['V1ac Avg (V)'], bins=bins_list, alpha=0.5, color='blue', ec='black', label='Phase A')
    plt.hist(g['V2ac Avg (V)'], bins=bins_list, alpha=0.5, color='green', ec='black', label='Phase B')
    # Labels
    plt.ylabel('Absolute Frequency', fontsize=14)
    plt.xlabel('Voltage (V)', fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    # Add Title
    plt.title('Voltage Averages for the week of\n' + str(_.date()) + " & " + str((_ + datetime.timedelta(days=7)).date()), fontsize=16);

    plt.axvline(x=110, color='yellow')
    plt.axvline(x=125, color='yellow')
    plt.axvline(x=106, color='red')
    plt.axvline(x=127, color='red')


    # plt.table(cellText=df_x)
    plt.legend()

    plt.show()

