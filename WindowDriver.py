import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, qApp, QMessageBox
from PyQt5.QtGui import QIcon


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):

        spendingAct = QAction('Spending Analysis', self)
        spendingAct.setShortcut('Ctrl+1')
        spendingAct.triggered.connect(self.on_spending_clicked)

        budgetAct = QAction('Budget Planning', self)
        budgetAct.setShortcut('Ctrl+2')
        budgetAct.triggered.connect(self.on_budget_clicked)

        self.toolbar = self.addToolBar('Navigation')
        self.toolbar.setMovable(False);
        self.toolbar.addAction(spendingAct)
        self.toolbar.addAction(budgetAct)

        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle("Spending Analysis")
        self.show()

    def on_spending_clicked(self):
        # display spending screen
        pass

    def on_budget_clicked(self):
        # display budget screen
        pass



if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
