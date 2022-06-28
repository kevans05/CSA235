import pandas as pd
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
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

bins_list = np.arange(105, 128, 0.25)

df = pd.read_csv('data/.CSV', encoding="ISO-8859-1", skiprows=5, names=header_list, low_memory=False)

df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"])

df2 = df.resample('W', on='Datetime')


for _, g in df2:
    count_normal_a = g['V1ac Avg (V)'].between(left=110, right=125).sum()
    count_extreme_a = g['V1ac Avg (V)'].between(left=106, right=127).sum()
    count_total_a = g['V2ac Avg (V)'].size

    count_normal_b = g['V2ac Avg (V)'].between(left=110, right=125).sum()
    count_extreme_b = g['V2ac Avg (V)'].between(left=106, right=127).sum()
    count_total_b = g['V2ac Avg (V)'].size

    normal_percent_a = round((count_normal_a/count_total_a)*100, 2)
    normal_pass_fail_a = 'Pass' if normal_percent_a > 95 else 'Fail'
    extreme_percent_a = round((count_extreme_a/count_total_a)*100, 2)
    extreme_pass_fail_a = 'Pass' if extreme_percent_a > 99 else 'Fail'

    normal_percent_b = round((count_normal_b/count_total_b)*100, 2)
    normal_pass_fail_b = 'Pass' if normal_percent_b > 95 else 'Fail'
    extreme_percent_b = round((count_extreme_b/count_total_b)*100, 2)
    extreme_pass_fail_b = 'Pass' if extreme_percent_b > 99 else 'Fail'

    title = 'Voltage Averages for the week of\n' + str(_.date()) + " & " + str((_ + datetime.timedelta(days=7)).date())
    stat_table = "Phase A\n" \
                 "   Percentage in Normal Operating Conditions: {normal_percent_a}%\n"\
                 "   Pass\Fail (95% of the time):             : {normal_pass_fail_a}\n"\
                 "   Percentage in Extreme Operating Conditions: {extreme_percent_a}%\n"\
                 "   Pass\Fail (99% of the time):             : {extreme_pass_fail_a}\n"\
                 "---------------------------------------------------------------\n\n\n" \
                 "Phase B\n" \
                 "   Percentage in Normal Operating Conditions: {normal_percent_b}%\n" \
                 "   Pass\Fail (95% of the time):             : {normal_pass_fail_b}\n" \
                 "   Percentage in Extreme Operating Conditions: {extreme_percent_b}%\n" \
                 "   Pass\Fail (99% of the time):             : {normal_pass_fail_b}\n".\
        format(normal_percent_a=normal_percent_a, normal_pass_fail_a=normal_pass_fail_a,
               extreme_percent_a=extreme_percent_a, extreme_pass_fail_a=extreme_pass_fail_a,
               normal_percent_b=normal_percent_b, normal_pass_fail_b=normal_pass_fail_b,
               extreme_percent_b=extreme_percent_b, extreme_pass_fail_b=extreme_pass_fail_b)


    fig, ax = plt.subplots(3,1)
    fig.suptitle(title)
    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=1,
                        hspace=0.4)

    fig.set_size_inches(10.5, 10.5)

    n_a, bins_a, patches_a = ax.ravel()[0].hist(g['V1ac Avg (V)'], bins_list, density=1, facecolor='r',
                                                label='Phase A')
    n_b, bins_b, patches_b = ax.ravel()[1].hist(g['V2ac Avg (V)'], bins_list, density=1, facecolor='y',
                                                label='Phase B')


    ax.ravel()[0].set_title('Phase A')
    ax.ravel()[0].set_xlabel('Voltage')
    ax.ravel()[0].set_ylabel('Percentage')
    ax.ravel()[0].axvline(x=110, color='g')
    ax.ravel()[0].axvline(x=125, color='g')
    ax.ravel()[0].axvline(x=106, color='b')
    ax.ravel()[0].axvline(x=127, color='b')
    ax.ravel()[0].set_ylim([0, 1])
    ax.ravel()[0].yaxis.set_major_formatter(PercentFormatter(xmax=1))

    ax.ravel()[1].set_title('Phase B')
    ax.ravel()[1].set_xlabel('Voltage')
    ax.ravel()[1].set_ylabel('Percentage')
    ax.ravel()[1].axvline(x=110, color='g')
    ax.ravel()[1].axvline(x=125, color='g')
    ax.ravel()[1].axvline(x=106, color='b')
    ax.ravel()[1].axvline(x=127, color='b')
    ax.ravel()[1].set_ylim([0, 1])
    ax.ravel()[1].yaxis.set_major_formatter(PercentFormatter(xmax=1))

    ax.ravel()[2].set_axis_off()

    ax.ravel()[2].text(0, 00, stat_table ,wrap=True)

    plt.show()
    fig.savefig(title + '.png', dpi=300, bbox_inches='tight')


