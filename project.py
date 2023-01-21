from PyQt5 import QtGui, QtCore, QtTest
from PyQt5.QtWidgets import (
    QApplication,
    QPushButton,
    QLabel,
    QWidget,
    QGridLayout,
    QDesktopWidget,
)
import sys
import re
import csv
from datetime import date

GREY_200 = "rgb(235,235,235)"
GREY_400 = "rgb(220,220,220)"
GREY_600 = "rgb(180,180,180)"
BLUE_700 = "rgb(57,73,98)"
BLUE_800 = "rgb(27,53,78)"

history = list()


class InitWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "pyCalc"
        self.left = 450
        self.top = 100
        self.width = 450
        self.height = 150
        self.iconName = "calculator-variant.png"
        self.initUI()

    def initUI(self):
        self.center()
        self.resize(self.width, self.height)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setWindowTitle(self.title)

        self.gridLayout()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

    def gridLayout(self):

        grid = QGridLayout()
        self.setLayout(grid)

        # set a label where numbers will appear
        label = QLabel()
        font = QtGui.QFont("Calibri", 12)
        label.setFont(font)
        label.setText("Welcome to pyCalc! Chose your favourite mode:")
        label.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(label, 0, 0, 1, 4)
        label.setWordWrap(True)

        b_dark = Button("Dark mode", BLUE_800)
        grid.addWidget(b_dark, 1, 1)
        b_dark.clicked.connect(self.setDark)

        b_light = Button("Light mode", GREY_400)
        grid.addWidget(b_light, 1, 2)
        b_light.clicked.connect(self.setLight)

    def setDark(self):
        color = BLUE_800
        self.win = Calculator(color)
        self.win.show()
        self.hide()

    def setLight(self):
        color = GREY_200
        self.win = Calculator(color)
        self.win.show()
        self.hide()


class Button(QPushButton):
    def __init__(self, text, color):
        super().__init__()
        self.setText(text)
        self.setMinimumHeight(60)
        font = QtGui.QFont("Calibri", 13)
        self.setFont(font)
        d_color = BLUE_800

        if color == d_color:
            self.setStyleSheet(
                """ QPushButton 
                {
                    border: 0.5px solid rgb(180,180,180); 
                    border-radius: 5px; 
                    border-style: outset; 
                    background-color: rgb(7,33,58); 
                    color: white;
                }
                    QPushButton:pressed 
                {
                    border-style: inset; 
                }   
                    QPushButton:hover
                {
                    background-color: rgb(47,63,88);
                }

                """
            )

        else:
            self.setStyleSheet(
                """
                    QPushButton {
                        border: 0.5px solid rgb(180,180,180);
                        border-radius: 5px;
                        border-style: outset;
                        background-color: rgb(185,185,185);
                    }
                    QPushButton:pressed {
                        border-style: inset;
                    }
                    QPushButton:hover {
                        background-color: rgb(215,215,215);
                    }
                """
            )


class Label(QLabel):
    def __init__(self, color):
        super().__init__()
        self.color = color
        if color == BLUE_800:
            self.setStyleSheet(
                """
                QLabel {
                    border: 1px solid rgb(150,150,150); 
                    border-radius: 5px;
                    background-color: rgb(7,33,58);
                    border-style: inset;
                    color: white;
                }
            """
            )
        else:
            self.setStyleSheet(
                """
                QLabel {
                    border: 1px solid rgb(150,150,150); 
                    border-radius: 5px;
                    background-color: rgb(195,195,195);
                    border-style: inset;
                }
            """
            )
        self.setMinimumWidth(300)
        self.setMaximumWidth(400)
        self.setMinimumHeight(60)
        self.setWordWrap(True)
        font = QtGui.QFont("Calibri", 30)
        self.setFont(font)
        self.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignRight
        )


class Calculator(QWidget):
    def __init__(self, color):
        super().__init__()
        self.color = color
        if self.color == BLUE_800:
            self.b_color = BLUE_800
        else:
            self.b_color = color
        self.title = "pyCalc"
        self.left = 450
        self.top = 100
        self.width = 350
        self.height = 450
        self.iconName = "calculator-variant.png"
        self.errors = ["Cannot divide by 0"]
        self.history = list()
        self.initUI()

    def initUI(self):
        self.center()
        self.setMaximumWidth(400)
        self.resize(self.width, self.height)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setWindowTitle(self.title)
        self.setStyleSheet(f"background-color: {self.color}")

        self.gridLayout()

    def gridLayout(self):

        grid = QGridLayout()
        self.setLayout(grid)

        # set a label where numbers will appear
        self.label = Label(self.color)
        self.label.setWordWrap(True)
        grid.addWidget(self.label, 0, 0, 1, 4)

        # top row
        top_row = 1

        b_percentage = Button("%", self.b_color)
        grid.addWidget(b_percentage, top_row, 0)
        b_percentage.clicked.connect(self.percentage)

        b_plusminus = Button("+ / -", self.b_color)
        grid.addWidget(b_plusminus, top_row, 1)
        b_plusminus.clicked.connect(self.change_plusminus)

        b_ce = Button("CE", self.b_color)
        grid.addWidget(b_ce, top_row, 2)
        b_ce.clicked.connect(self.eraseLabel)

        b_del = Button("DEL", self.b_color)
        grid.addWidget(b_del, top_row, 3)
        b_del.clicked.connect(self.delete)

        # first row
        first_row = 2

        b7 = Button("7", self.b_color)
        grid.addWidget(b7, first_row, 0)
        b7.clicked.connect(self.clicked)

        b8 = Button("8", self.b_color)
        grid.addWidget(b8, first_row, 1)
        b8.clicked.connect(self.clicked)

        b9 = Button("9", self.b_color)
        grid.addWidget(b9, first_row, 2)
        b9.clicked.connect(self.clicked)

        b_plus = Button("+", self.b_color)
        grid.addWidget(b_plus, first_row, 3)
        b_plus.clicked.connect(self.clicked)

        # second row
        second_row = 3
        b4 = Button("4", self.b_color)
        grid.addWidget(b4, second_row, 0)
        b4.clicked.connect(self.clicked)

        b5 = Button("5", self.b_color)
        grid.addWidget(b5, second_row, 1)
        b5.clicked.connect(self.clicked)

        b6 = Button("6", self.b_color)
        grid.addWidget(b6, second_row, 2)
        b6.clicked.connect(self.clicked)

        b_minus = Button("-", self.b_color)
        grid.addWidget(b_minus, second_row, 3)
        b_minus.clicked.connect(self.clicked)

        # third row
        third_row = 4
        b1 = Button("1", self.b_color)
        grid.addWidget(b1, third_row, 0)
        b1.clicked.connect(self.clicked)

        b2 = Button("2", self.b_color)
        grid.addWidget(b2, third_row, 1)
        b2.clicked.connect(self.clicked)

        b3 = Button("3", self.b_color)
        grid.addWidget(b3, third_row, 2)
        b3.clicked.connect(self.clicked)

        b_multiply = Button("x", self.b_color)
        grid.addWidget(b_multiply, third_row, 3)
        b_multiply.clicked.connect(self.clicked)

        # bottom row
        bottom_row = 5

        b_equal = Button("=", self.b_color)
        grid.addWidget(b_equal, bottom_row, 0)
        b_equal.clicked.connect(self.equal)
        if self.b_color != BLUE_800:
            b_equal.setStyleSheet(
                """
            QPushButton {
                border: 0.5px solid rgb(180,180,180);
                border-radius: 5px;
                border-style: outset;
                background-color: rgb(27,53,78);
                color: white;
            }
            QPushButton:pressed {
                border-style: inset;
                background-color: rgb(57,73,98);
            }
            QPushButton:hover {
                background-color: rgb(57,73,98);
            }
        """
            )
        else:
            b_equal.setStyleSheet(
                """
                    QPushButton {
                        border: 0.5px solid rgb(180,180,180);
                        border-radius: 5px;
                        border-style: outset;
                        background-color: rgb(165,165,165);
                    }
                    QPushButton:pressed {
                        border-style: inset;
                    }
                    QPushButton:hover {
                        background-color: rgb(195,195,195);
                    }
                """
            )

        b0 = Button("0", self.b_color)
        grid.addWidget(b0, bottom_row, 1)
        b0.clicked.connect(self.clicked)

        b_float = Button(".", self.b_color)
        grid.addWidget(b_float, bottom_row, 2)
        b_float.clicked.connect(self.setFloat)

        b_divide = Button("/", self.b_color)
        grid.addWidget(b_divide, bottom_row, 3)
        b_divide.clicked.connect(self.clicked)

    def keyPressEvent(self, e: QtGui.QKeyEvent):
        modifiers = QtGui.QGuiApplication.keyboardModifiers()

        if e.text() in [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "+",
            "-",
            "x",
            "/",
        ]:
            self.clicked(e.text())
        elif e.text() == ".":
            self.setFloat()
        # equal sign
        elif e.key() == 16777220:
            self.equal()
        # del sign
        elif e.key() == 16777219:
            self.delete()
        # canc sign
        elif e.key() == 16777223:
            self.eraseLabel()
        # shift sign
        elif modifiers == QtCore.Qt.ShiftModifier:
            # n. 5
            if e.key() == 37:
                self.percentage()
        else:
            pass

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

    def eraseLabel(self):
        self.label.clear()

    def delete(self):
        text = self.label.text()
        self.label.setText(text[:-1])

    def clicked(self, e=""):

        widget = self.sender()
        if widget is not None:
            widget_text = widget.text()
        else:
            widget_text = e

        text = self.label.text()
        regex = r"^-?[0-9]+(.?[0-9]+)?[-+\/x][0-9]+(.?[0-9]+)?$"

        if re.match(regex, text) is not None:
            if widget_text in ["+", "-", "x", "/", "."]:
                self.equal()
                text = self.label.text()
                self.label.setText(text + widget_text)
            else:
                self.label.setText(text + widget_text)
        elif text == "":
            if widget_text in ["+", "-", "x", "/", "."]:
                pass
            else:
                self.label.setText(widget_text)
        elif text == "0":
            if widget_text in ["+", "-", "x", "/", "."]:
                self.label.setText(text + widget_text)
            else:
                pass
        elif text in self.errors:
            self.label.setText(widget_text)
        elif "+" in text[1:] or "-" in text[1:] or "x" in text[1:] or "/" in text[1:]:
            if widget_text in ["+", "-", "x", "/"]:
                pass
            else:
                self.label.setText(text + widget_text)
        else:
            self.label.setText(text + widget_text)

    def percentage(self):
        regex = r"^-?[0-9]+(.?[0-9]+)?$"
        text = self.label.text()

        if re.match(regex, text) is not None:
            n = float(self.label.text())
            perc = int(n * 100)
            self.label.setText(str(perc))
        else:
            pass

    def setFloat(self):
        regex = r"^-?[0-9]+$"
        text = self.label.text()

        if re.match(regex, text) is not None:
            self.label.setText(text + ".")
        elif "+" in text[1:] or "-" in text[1:] or "x" in text[1:] or "/" in text[1:]:
            if text[-1] in ["x", "/", "+", "-"]:
                pass
            elif text.count(".") == 2:
                pass
            else:
                self.label.setText(text + ".")
        elif text == "":
            pass
        else:
            pass

    def equal(self):

        text = self.label.text()
        regex = r"^-?[0-9]+(.?[0-9]+)?[-+\/x][0-9]+(.?[0-9]+)?$"

        if re.match(regex, text) is not None:
            if "+" in text and text[0] != "-":
                a, b = text.split("+")
                if "." in a or "." in b:
                    result = float(a) + float(b)
                    self.label.setText(str(f"{result:.1f}"))
                    history.append(f"{float(a)} + {float(b)} = {result:.1f}")
                else:
                    result = int(a) + int(b)
                    self.label.setText(str(result))
                    history.append(f"{int(a)} + {int(b)} = {result}")
            elif "+" in text and text[0] == "-":
                a, b = text[1:].split("+")
                if "." in a or "." in b:
                    result = -float(a) + float(b)
                    self.label.setText(str(f"{result:.1f}"))
                    history.append(f"{-float(a)} + {float(b)} = {result:.1f}")
                else:
                    result = -int(a) + int(b)
                    self.label.setText(str(result))
                    history.append(f"{-int(a)} + {int(b)} = {result}")

            elif "x" in text and text[0] != "-":
                a, b = text.split("x")
                if "." in a or "." in b:
                    result = float(a) * float(b)
                    self.label.setText(str(f"{result:.1f}"))
                    history.append(f"{float(a)} * {float(b)} = {result:.1f}")
                else:
                    result = int(a) * int(b)
                    self.label.setText(str(result))
                    history.append(f"{int(a)} * {int(b)} = {result}")
            elif "x" in text and text[0] == "-":
                a, b = text[1:].split("x")
                if "." in a or "." in b:
                    result = -float(a) * float(b)
                    self.label.setText(str(f"{result:.1f}"))
                    history.append(f"{-float(a)} * {float(b)} = {result:.1f}")
                else:
                    result = -int(a) * int(b)
                    self.label.setText(str(result))
                    history.append(f"{-int(a)} * {int(b)} = {result}")

            elif "/" in text and text[0] != "-":
                a, b = text.split("/")
                try:
                    if "." in a or "." in b:
                        result = float(a) / float(b)
                        self.label.setText(str(f"{result:.1f}"))
                        history.append(f"{float(a)} / {float(b)} = {result:.1f}")
                    else:
                        result = int(a) / int(b)
                        if int(a) % int(b) == 0:
                            self.label.setText(str(int(result)))
                            history.append(f"{int(a)} / {int(b)} = {result}")
                        else:
                            self.label.setText(str(f"{result:.1f}"))
                            history.append(f"{int(a)} / {int(b)} = {result:.1f}")
                except ZeroDivisionError:
                    history.append(f"Error when calculating {text}: cannot divide by 0")
                    self.label.setText(self.errors[0])
                    self.sleep()
                    if self.clicked() is True:
                        self.label.setText(a)
                    else:
                        self.label.setText(a)

            elif "/" in text and text[0] == "-":
                a, b = text[1:].split("/")
                try:
                    if "." in a or "." in b:
                        result = -float(a) / float(b)
                        self.label.setText(str(f"{result:.1f}"))
                        history.append(f"{-float(a)} / {float(b)} = {result:.1f}")
                    else:
                        result = -int(a) / int(b)
                        if int(a) % int(b) == 0:
                            self.label.setText(str(int(result)))
                            history.append(f"{-int(a)} / {int(b)} = {result}")
                        else:
                            self.label.setText(str(f"{result:.1f}"))
                            history.append(f"{-int(a)} / {int(b)} = {result:.1f}")
                except ZeroDivisionError:
                    history.append(f"Error when calculating {text}: cannot divide by 0")
                    self.label.setText(self.errors[0])
                    self.sleep()
                    if self.clicked() is True:
                        self.label.setText(a)
                    else:
                        self.label.setText(a)

            elif "-" in text and text[0] != "-":
                a, b = text.split("-")
                if "." in a or "." in b:
                    result = float(a) - float(b)
                    self.label.setText(str(f"{result:.1f}"))
                    history.append(f"{float(a)} - {float(b)} = {result:.1f}")
                else:
                    result = int(a) - int(b)
                    self.label.setText(str(result))
                    history.append(f"{int(a)} - {int(b)} = {result}")
            elif "-" in text and text[0] == "-":
                a, b = text[1:].split("-")
                if "." in a or "." in b:
                    result = -float(a) - float(b)
                    self.label.setText(str(f"{result:.1f}"))
                    history.append(f"{-float(a)} - {float(b)} = {result:.1f}")
                else:
                    result = -int(a) - int(b)
                    self.label.setText(str(result))
                    history.append(f"{-int(a)} - {int(b)} = {result}")

            else:
                pass
        else:
            pass

    def change_plusminus(self):
        regex = r"^-?[0-9]+(.?[0-9]+)?[-+\/x][0-9]+(.?[0-9]+)?$"
        text = self.label.text()

        if text == "":
            pass
        elif re.match(regex, text):
            pass
        else:
            if "." in text:
                n = float(text)
                n_change = n * -1
                history.append(f"Change of sign: {str(n)} -> {str(n_change)}")
                self.label.setText(str(n_change))

            else:
                n = int(text)
                n_change = n * -1
                history.append(f"Change of sign: {str(n)} -> {str(n_change)}")
                self.label.setText(str(n_change))

    def sleep(self):
        QtTest.QTest.qWait(1000)


def main():

    if len(sys.argv) > 1:
        startApp(sys.argv[1])
    else:
        print("Missing argument")
        sys.exit()

    generateHistory(
        input(
            "Would you like to generate the history of your calculation in Excel file? (Y/N) "
        )
    )

    openFile(input(
        "Would you like to print here the history calculation file? (Y/N) "
        )
    )


def startApp(s):
    
    if s == '-exe':
        app = QApplication(sys.argv)

        win = InitWindow()
        win.show()

        app.exec()
    else:
        print("Wrong argument")
        sys.exit()


def generateHistory(s):

    if s.strip().lower() == "y":
        today = date.today()
        d = today.strftime("[%y-%m-%d]")
        with open(f"{d} Calculator History.xls", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["History"])
            writer.writeheader()
            for i in history:
                writer.writerow({"History": i})

        print("File generated succesfully!")
    else:
        print("Thank you for using pyCalc!")
        sys.exit()


def openFile(s):
    if s.strip().lower() == "y":
        today = date.today()
        d = today.strftime("[%y-%m-%d]")
        with open(f"{d} Calculator History.xls", "r", newline="") as file:
            print("----- Reading starts here ----")
            for line in file:
                print(line.rstrip())
            print("----- Reading ends here ----")
    else:
        print("Your file will be available in this folder. Thank you for using pyCalc!")
        sys.exit()


if __name__ == "__main__":
    main()