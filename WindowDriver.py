import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, qApp, QMessageBox,
                             QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QSizePolicy, QInputDialog, QFileDialog, QLineEdit, QLabel)
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Spending import SpendingAnalyzer


class Window(QMainWindow):

    layout = None
    tw = None

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        tw = TabWidget(self)
        self.setCentralWidget(tw)

        self.setGeometry(100, 100, 1200, 600)
        self.setWindowTitle("Spending Analysis")
        self.show()


class TabWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        # Get file to analyze
        self.filename = self.open_file()

        # Create and initialize tabs
        self.tabs = QTabWidget()
        self.spending_tab = QWidget()
        self.budget_tab = QWidget()
        self.tabs.addTab(self.spending_tab, "Spending")
        self.tabs.addTab(self.budget_tab, "Budget")
        self.init_spending_tab()
        self.init_budget_tab()

        # Display filename
        self.file_display = QLabel()
        self.file_display.setText('Analyzing ' + str(self.filename))
        self.file_display.setAlignment(Qt.AlignCenter)
        # self.file_open_button = QPushButton('Open File')
        # self.file_open_button.clicked.connect(self.open_file)

        # Create layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tabs)
        lower_hbox = QHBoxLayout()
        lower_hbox.addWidget(self.file_display)
        #lower_hbox.addWidget(self.file_open_button)
        self.layout.addLayout(lower_hbox)
        self.setLayout(self.layout)

    def init_spending_tab(self):

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        sa = SpendingAnalyzer(self.filename)
        (fig1, fig2, fig3) = sa.generate_figures()
        plot1 = PlotCanvas(fig1)
        plot2 = PlotCanvas(fig2)
        plot3 = PlotCanvas(fig3)

        hbox.addWidget(plot1)
        hbox.addWidget(plot2)
        hbox.addWidget(plot3)

        vbox.addLayout(hbox)

        print('got plots')

        self.spending_tab.setLayout(vbox)

        print('init')
        print(self.spending_tab.layout())
        self.spending_tab.update()

    def init_budget_tab(self):
        pass

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Select a file to analyze.", "",
                                                  "CSV Files (*.csv)", options=options)

        return filename


class PlotCanvas(FigureCanvas):

    def __init__(self, figure, parent=None, width=5, height=4, dpi=100):
        FigureCanvas.__init__(self, figure)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
