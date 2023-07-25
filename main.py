from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sqlite3 ,os
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Settings")
        Dialog.resize(400, 211)
        Dialog.setWindowFlags(Qt.WindowTitleHint)
        Dialog.setStyleSheet("QDialog{background-color:'#fff';}")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(20, 30, 350, 141))
        self.widget.setObjectName("widget")
        self.widget.setStyleSheet("*{background-color:'#fff';}")
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setPlaceholderText("eg:- 'word1 word2 word3'")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.pushButton_2 = QtWidgets.QCheckBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        # self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setStyleSheet("QPushButton{background-color#eee;border-radius:10px}")
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.done)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(1, QtWidgets.QFormLayout.FieldRole, spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(3, QtWidgets.QFormLayout.FieldRole, spacerItem1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(5, QtWidgets.QFormLayout.FieldRole, spacerItem1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate 
        Dialog.setWindowIcon(QIcon('src/static/m/icon.png'))
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))
        self.label.setText(_translate("Dialog", "Enter URL"))
        self.label_2.setText(_translate("Dialog", "Keywords    "))
        self.pushButton_2.setText(_translate("Dialog", "Recursive Scanning"))
        self.pushButton.setText(_translate("Dialog", "Submit"))

    def getInteger(self):
        i, okPressed = QtWidgets.QInputDialog.getInt(Dialog, "Window Title","Recursion Level", 1, 1, 10, 1,flags=Qt.FramelessWindowHint)
        if okPressed:
            return i

    def done(self):
        self.val1 = self.lineEdit.text().strip(" ")
        self.val2 = self.lineEdit_2.text()
        if self.pushButton_2.isChecked():
            self.rLevel = self.getInteger()
        if 'https://' == self.val1[:8] or 'http://' == self.val1[:7]:
            # self.val1.strip("https://").strip("http://")
            try:
                sqliteConnection = sqlite3.connect('src/SQLite_Python.db')
                cursor = sqliteConnection.cursor()
                table_name = "tb_config"
                sql = 'drop table if exists '+table_name
                cursor.execute(sql)
                sql = 'create table if not exists ' + table_name + ' (url , keywords, recur, recurLevel)'
                cursor.execute(sql)
                print("Connected to SQLite")
                sqlite_insert_query = ''' INSERT INTO tb_config VALUES (?,?,?,?)'''
                if self.pushButton_2.isChecked():
                    cursor.execute(sqlite_insert_query,(self.val1,self.val2,str(self.pushButton_2.isChecked()),self.rLevel))
                    print("{}\n{}\n{}\n{}".format(self.val1,self.val2,str(self.pushButton_2.isChecked()),self.rLevel))
                else:
                    cursor.execute(sqlite_insert_query,(self.val1,self.val2,str(self.pushButton_2.isChecked()),-1))
                    print("{}\n{}\n{}\n{}".format(self.val1,self.val2,str(self.pushButton_2.isChecked()),-1))
                sqliteConnection.commit()
                cursor.close()
                print("Starting Filter...")
                os.system('start cmd /k "cd src && python app.py" & exit')
                QtWidgets.QApplication.quit()
            except Exception as e: 
                print(e)
        elif len(self.val1)+len(self.val2) == 0:
            os.system('start cmd /k "cd src && python app.py" & exit')
            QtWidgets.QApplication.quit()


# class getData():
#     def __init__(self):
#         import sys
#         app = QtWidgets.QApplication(sys.argv)
#         Dialog = QtWidgets.QDialog()
#         ui = Ui_Dialog()
#         ui.setupUi(Dialog)
#         Dialog.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


