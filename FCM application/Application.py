import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from FCM1 import FCM1
from PyQt5 import uic



class MyWindowClass(QMainWindow):
    def __init__(self):
        super(MyWindowClass, self).__init__()
        uic.loadUi("FCM application\main_window.ui", self)
        
        
        self.k_text.setText("fdfsdfdsf")






    def choose_data(self):
        try:
            file_filter = 'Data File (*.xlsx *.csv *.data);; Excel File (*.xlsx *.xls)'
            path, _ = QFileDialog.getOpenFileName(parent=self, caption='Select a Data File', filter=file_filter,
                                                  options=QFileDialog.DontUseNativeDialog)
            
            self.fcm1.read_data(path)
        except:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Please choose a data set !')
    def caculate_cluster():
        return
app = QApplication(sys.argv)
myWindow = MyWindowClass()
myWindow.show()
app.exec_()