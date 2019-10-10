import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import date
import math


class SpendingAnalyzer:

    def __init__(self, file_path):
        with open(file_path) as file:
            reader = csv.reader(file, delimiter=',')
            line = 0
            dates = []
            balances = []
            averages = []

            # Account Number, Post Date, Check, Description,
            # Debit, Credit, Status, Balance, Label
            for row in reader:
                if line == 0:
                    print(row)
                elif row[7]:
                    date_split = row[1].split('/')
                    d = date(int(date_split[2]), int(date_split[0]), int(date_split[1]))
                    if len(dates) > 0 and d == dates[-1]:
                        balances[-1] = float(row[7])
                    else:
                        dates.append(d)
                        balances.append(float(row[7]))
                line += 1

        dates = matplotlib.dates.date2num(dates)

        AVG_LEN = 3
        for i in range(0, len(balances)-AVG_LEN):
            averages.append(sum(balances[i:i+AVG_LEN])/AVG_LEN)
        for i in range(0, AVG_LEN):
            averages.append(averages[-1])

        # for i in range(0, 60):
        #     print(str(dates[i]) + " " + str(balances[i]))

        DISP_LEN = 27
        plt.plot_date(dates[0:DISP_LEN], balances[0:DISP_LEN], '-')
        plt.plot_date(dates[0:DISP_LEN-AVG_LEN], averages[0:DISP_LEN-AVG_LEN], 'r-')
        plt.xticks(rotation=60)
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    sa = SpendingAnalyzer('data/AccountHistory.csv')
