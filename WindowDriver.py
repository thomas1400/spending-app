import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, qApp, QMessageBox,
                             QTabWidget, QWidget, QVBoxLayout, QPushButton, QSizePolicy)
from PyQt5.QtGui import QIcon

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from Spending import SpendingAnalyzer

import random


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        self.tw = TabWidget(self)
        self.setCentralWidget(self.tw)

        # spendingAct = QAction('Spending Analysis', self)
        # spendingAct.setShortcut('Ctrl+1')
        # spendingAct.triggered.connect(self.on_spending_clicked)
        #
        # budgetAct = QAction('Budget Planning', self)
        # budgetAct.setShortcut('Ctrl+2')
        # budgetAct.triggered.connect(self.on_budget_clicked)

        # self.toolbar = self.addToolBar('Navigation')
        # self.toolbar.setMovable(False)
        # self.toolbar.addAction(spendingAct)
        # self.toolbar.addAction(budgetAct)

        self.setGeometry(100, 100, 1200, 600)
        self.setWindowTitle("Spending Analysis")
        self.show()

    def on_spending_clicked(self):
        # display spending screen
        pass

    def on_budget_clicked(self):
        # display budget screen
        pass


class TabWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.spending_tab = QWidget()
        self.budget_tab = QWidget()

        self.tabs.addTab(self.spending_tab, "Spending")
        self.tabs.addTab(self.budget_tab, "Budget")

        self.init_spending_tab()
        self.init_budget_tab()

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def init_spending_tab(self):
        self.spending_tab.layout = QVBoxLayout(self)
        sa = SpendingAnalyzer('data/AccountHistory.csv')
        plot = PlotCanvas(sa.generate_figure())
        plot.move(0, 0)

        self.spending_tab.layout.addWidget(plot)

        # self.pushButton1 = QPushButton("Spending Button")
        # self.spending_tab.layout.addWidget(self.pushButton1)
        self.spending_tab.setLayout(self.spending_tab.layout)

    def init_budget_tab(self):
        pass


class PlotCanvas(FigureCanvas):

    def __init__(self, figure, parent=None, width=5, height=4, dpi=100):
        # fig = Figure(figsize=(width, height), dpi=dpi)
        # self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, figure)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.draw()
    #
    # def plot(self, data, style, title):
    #     self.axes.plot(data, style)
    #     self.axes.set_title(title)
    #     self.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
