import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import csv
from datetime import date
from collections import Counter

class SpendingAnalyzer:

    AVG_LEN = 5
    DISP_RANGE = 40

    LABEL_NAMES = ['Food', 'Travel', 'Activities', 'Wants', 'Needs', 'Savings', 'Income']

    def __init__(self, file_path):
        matplotlib.rcParams.update({'figure.autolayout': True})

        with open(file_path) as file:
            reader = csv.reader(file, delimiter=',')

            self.dates = []
            self.balances = []
            self.trans_amounts = []
            self.labels = []

            # Account Number, Post Date, Check, Description,
            # Debit, Credit, Status, Balance, Label

            next(reader)  # skip the column names
            for row in reader:
                # Read dates and balances
                if row[7]:
                    date_split = row[1].split('/')
                    d = matplotlib.dates.date2num(date(int(date_split[2]), int(date_split[0]), int(date_split[1])))
                    if len(self.dates) > 0:
                        if d == self.dates[-1]:
                            self.balances[-1] = float(row[7])
                        else:
                            while self.dates[-1] - d > 1:
                                self.dates.append(self.dates[-1]-1)
                                self.balances.append(self.balances[-1])
                                self.dates.append(d)
                            self.balances.append(float(row[7]))
                    else:
                        self.dates.append(d)
                        self.balances.append(float(row[7]))

                # Read debits and labels
                if row[8]and row[4]:
                        self.trans_amounts.append(float(row[4]))
                        self.labels.append(int(row[8]))
                # if row[8] and row[5]:
                #     self.trans_amounts.append(float(row[5]))
                #     self.labels.append(int(row[8])) # uncomment to include income in breakdown

        self.averages = []
        for i in range(0, len(self.balances)-self.AVG_LEN):
            self.averages.append(sum(self.balances[i:i+self.AVG_LEN])/self.AVG_LEN)
        for i in range(0, self.AVG_LEN):
            self.averages.append(self.averages[-1])

        self.differences = [0]
        for i in range(1, len(self.balances)):
            d = self.balances[i]-self.balances[i-1]
            if d < 0:
                d = 0
            self.differences.append(d)

        self.label_sums = {}
        for i, label in enumerate(self.labels):
            if label not in self.label_sums.keys():
                self.label_sums[label] = 0
            self.label_sums[label] += self.trans_amounts[i]

    def generate_figures(self, width=5, height=4, dpi=100):
        fig1 = Figure(figsize=(width, height), dpi=dpi)
        ax1 = fig1.add_subplot(111)
        fig2 = Figure(figsize=(width, height), dpi=dpi)
        ax2 = fig2.add_subplot(111)
        fig3 = Figure(figsize=(width, height), dpi=dpi)
        ax3 = fig3.add_subplot(111)


        # fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
        fig1.set_size_inches(width, height)
        ax1.plot_date(self.dates[0:self.DISP_RANGE], self.balances[0:self.DISP_RANGE], '-')
        ax1.plot_date(self.dates[0:self.DISP_RANGE], self.averages[0:self.DISP_RANGE], 'r--')
        ax1.set(title='Balance vs. Time')
        plt.setp(ax1.get_xticklabels(), rotation=75)
        plt.subplots_adjust(bottom=0.15)


        #ax2.plot(self.dates[0:self.DISP_RANGE], self.balances[0:self.DISP_RANGE], '--')
        ax2.bar(self.dates[0:self.DISP_RANGE], self.differences[0:self.DISP_RANGE])
        ax2.xaxis_date()
        ax2.set(title='Spending vs. Time')
        plt.setp(ax2.get_xticklabels(), rotation=75)
        plt.gcf().subplots_adjust(bottom=0.15)


        counts = Counter(self.label_sums)
        ax3.pie([v for v in counts.values()],
                labels=[self.LABEL_NAMES[k-1] for k in counts], autopct="%d%%")
        ax3.set(title='Spending Breakdown')
        plt.gcf().subplots_adjust(bottom=0.15)

        # plt.tight_layout()
        # plt.show()

        return fig1, fig2, fig3


if __name__ == '__main__':
    sa = SpendingAnalyzer('data/AccountHistory.csv')
