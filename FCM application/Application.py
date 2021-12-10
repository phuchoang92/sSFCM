import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from FCM1 import FCM1
from PyQt5 import uic

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

class MyWindowClass(QMainWindow):
    
    def __init__(self):
        super(MyWindowClass, self).__init__()
        uic.loadUi("FCM application\main_window.ui", self)
        
        self.fcm1 = FCM1()
        self.fcm2 = FCM2()
        self.run_btn.clicked.connect(self.caculate_cluster)


    def choose_data(self):
        try:
            file_filter = 'Data File (*.xlsx *.csv *.data);; Excel File (*.xlsx *.xls)'
            path, _ = QFileDialog.getOpenFileName(parent=self, caption='Select a Data File', filter=file_filter,
                                                  options=QFileDialog.DontUseNativeDialog)
            
            self.data_path.setText(path)
            self.fcm1.read_data(path)
            model_x = TableModel(self.fcm1.X)
            self.X_table.setModel(model_x)
            self.X_table.resizeColumnsToContents()
            
        except:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Please choose a data set !')
    def caculate_cluster():
        
        if self.number_of_label.text() != '' and (self.number_of_cluster.text() != '') and (self.epsilon.text() != ''):
            number_of_label = int(self.k_text.text())
            number_of_cluster = int(self.k_text.text())
            epsilon = float(self.epsilon_text.text())

            if self.algo1_check.isChecked(): #Kiểm tra có chạy thuật toán 1 hay ko
                value_of_m = int(self.m_text.text())
                if self.check_2pha_algo1.isChecked():
                    self.fcm1.thuat_toan_2_pha(epsilon, value_of_m, number_of_cluster, number_of_label)
                else:
                    self.fcm1.thuat_toan_1_pha(epsilon,value_of_m,number_of_cluster,number_of_label)

            if self.algo2_check.isChecked(): #Kiểm tra có chạy thuật toán 2 hay ko
                value_of_M = int(self.M_text.text())
                value_of_M1 = int(self.M1_text.text())

                if self.check_2pha_algo2.isChecked():
       
def main():
    app = QApplication([])
    mainWindow = App()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
