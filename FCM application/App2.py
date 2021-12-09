import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from FCM1 import FCM1


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


class App(QMainWindow):

    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        
        self.fcm1 = FCM1()

        self.jaccard_value_box = QLineEdit()
        self.adjusted_value_box = QLineEdit()
        self.rand_value_box = QLineEdit()
        self.resize(900, 800)
        self.setStyleSheet("QMainWindow {background: '#DCEAE0';}")
        frame = QFrame()

        self.topLayout = QHBoxLayout()
        self.midWidget = QWidget()
        self.bottomLayout = QHBoxLayout()
        self.randIndex = QGroupBox()
        self.table_x = QTableView()
        self.table_u_ngang = QTableView()
        self.table_u = QTableView()
        self.table_v = QTableView()
        self.u_Table = QTabWidget()
        self.x_Table = QTabWidget()
        self.v_table = QTabWidget()
        self.textEdit = QLineEdit()

        self.calculate()
        self.U_Table()
        self.X_Table()
        self.Input_Section()
        self.V_table()
        self.rand_index_box()
        self.randIndex.setMinimumWidth(300)
        self.midWidget.setMaximumWidth(300)
        self.u_Table.setMaximumWidth(500)
        self.v_table.setMinimumWidth(600)
        self.v_table.setMaximumWidth(700)
        self.bottomLayout.addWidget(self.v_table)
        self.bottomLayout.addStretch(1)
        self.bottomLayout.addWidget(self.randIndex)

        mainLayout = QGridLayout()
        mainLayout.addLayout(self.topLayout, 0, 0, 1, 4)
        mainLayout.addWidget(self.x_Table, 1, 0, 3, 3)
        mainLayout.addWidget(self.midWidget, 1, 3, 1, 1)
        mainLayout.addWidget(self.u_Table, 1, 4, 3, 6)
        mainLayout.addLayout(self.bottomLayout, 4, 0, 2, 10)

        self.table_u_ngang.setStyleSheet("QTableView {border: 1px solid #000}")
        self.table_u.setStyleSheet("QTableView {border: 1px solid #000}")
        self.table_x.setStyleSheet("QTableView {border: 1px solid #000}")
        self.table_v.setStyleSheet("QTableView {border: 1px solid #000}")
        self.randIndex.setStyleSheet("QGroupBox {border: 1px solid #000}")

        frame.setLayout(mainLayout)
        self.setCentralWidget(frame)
        self.setWindowTitle("Semi-Supervised Fuzzy C-means Clustering")

    def rand_index_box(self):

        rand_label = QLabel("Rand Index")
        adjusted_rand_label = QLabel("Adjusted Rand Index")
        jaccard_label = QLabel("Jaccard Coefficient")

        layout = QFormLayout()
        layout.addRow(rand_label, self.rand_value_box)
        layout.addRow(adjusted_rand_label, self.adjusted_value_box)
        layout.addRow(jaccard_label, self.jaccard_value_box)

        self.randIndex.setLayout(layout)

    def Input_Section(self):
        button = QPushButton("Choose Data")
        button.clicked.connect(self.get_data_file)

        self.topLayout.addWidget(button, 2)
        self.topLayout.addWidget(self.textEdit, 7)

    def calculate(self):

        label3 = QLabel("Number of k1")
        label1 = QLabel("Input the parameter m")
        label2 = QLabel("Number of clusters")
        label4 = QLabel("Epsilon")

        self.input1 = QLineEdit()
        self.input2 = QLineEdit()
        self.input3 = QLineEdit()
        self.input4 = QLineEdit()

        cal_button1 = QPushButton("Calculate clusters (1 Pha)")
        cal_button1.clicked.connect(self.generate_clusters_1)
        cal_button2 = QPushButton("Calculate clusters (2 Pha)")
        cal_button2.clicked.connect(self.generate_clusters_2)

        midLayout = QFormLayout()

        midLayout.addRow(label3, self.input3)
        midLayout.addRow(label2, self.input2)
        midLayout.addRow(label1, self.input1)
        midLayout.addRow(label4, self.input4)
        midLayout.addWidget(cal_button1)
        midLayout.addWidget(cal_button2)
        midLayout.setContentsMargins(1, 40, 1, 1)
        self.midWidget.setLayout(midLayout)

    def get_data_file(self):
        try:
            file_filter = 'Data File (*.xlsx *.csv *.data);; Excel File (*.xlsx *.xls)'
            path, _ = QFileDialog.getOpenFileName(parent=self, caption='Select a Data File', filter=file_filter,
                                                  options=QFileDialog.DontUseNativeDialog)
            self.textEdit.setText(path)
            self.fcm1.read_data(path)
            model_x = TableModel(self.fcm1.X)
            self.table_x.setModel(model_x)
            self.table_x.resizeColumnsToContents()
        except:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Please choose a data set !')

    def generate_clusters_1(self):
        
        self.rand_value_box.clear()
        self.adjusted_value_box.clear()
        self.jaccard_value_box.clear()
        
        if self.input1.text() != '' and (self.input3.text() != '') and (self.input2.text() != '') and self.input4.text() !='':
            value_m = int(self.input1.text())
            value_epsilon = float(self.input4.text())
            value_k1 = int(self.input3.text())
            value_c = int(self.input2.text())
            self.fcm1.thuat_toan_1_pha(value_epsilon, value_m, value_c, value_k1)    
            cluster_model = TableModel(self.fcm1.V)
            u_model = TableModel(self.fcm1.U)

            self.table_u.setModel(u_model)
            self.table_u.resizeColumnsToContents()
            self.table_v.setModel(cluster_model)
            self.table_v.resizeColumnsToContents()
            
            model = TableModel(self.fcm1.U_ngang)
            self.table_u_ngang.setModel(model)
            self.table_u_ngang.resizeColumnsToContents()

            self.rand_value_box.insert(str(self.fcm1.w1))
            self.adjusted_value_box.insert(str(self.fcm1.w2))
            self.jaccard_value_box.insert(str(self.fcm1.w3))
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Missing Input")
            msg.setInformativeText("Please, input the all field")
            msg.setWindowTitle("Error")
            msg.exec_()
    
    
    
    def generate_clusters_2(self):
            
        self.rand_value_box.clear()
        self.adjusted_value_box.clear()
        self.jaccard_value_box.clear()
        
        if self.input1.text() != '' and (self.input3.text() != '') and (self.input2.text() != '') and self.input4.text() !='':
            value_m = int(self.input1.text())
            value_epsilon = float(self.input4.text())
            value_k1 = int(self.input3.text())
            value_c = int(self.input2.text())
            
            self.fcm1.thuat_toan_2_pha(value_epsilon, value_m, value_c, value_k1)  
              
            cluster_model = TableModel(self.fcm1.V)
            u_model = TableModel(self.fcm1.U)

            self.table_u.setModel(u_model)
            self.table_u.resizeColumnsToContents()
            self.table_v.setModel(cluster_model)
            self.table_v.resizeColumnsToContents()
            
            model = TableModel(self.fcm1.U_ngang)
            self.table_u_ngang.setModel(model)
            self.table_u_ngang.resizeColumnsToContents()

            self.rand_value_box.insert(str(self.fcm1.w1))
            self.adjusted_value_box.insert(str(self.fcm1.w2))
            self.jaccard_value_box.insert(str(self.fcm1.w3))
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Missing Input")
            msg.setInformativeText("Please, input the all field")
            msg.setWindowTitle("Error")
            msg.exec_()
    
    def V_table(self):
        self.v_table.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)

        tab = QWidget()

        tabBox = QHBoxLayout()
        tabBox.setContentsMargins(3, 3, 3, 3)
        tabBox.addWidget(self.table_v)

        tab.setLayout(tabBox)
        self.table_v.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.table_v.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        self.v_table.addTab(tab, "Cluster centroids")

    def X_Table(self):
        self.x_Table.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)

        tab = QWidget()

        tabBox = QHBoxLayout()
        tabBox.setContentsMargins(3, 3, 3, 3)
        tabBox.addWidget(self.table_x)

        tab.setLayout(tabBox)
        self.table_x.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.table_x.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        header = self.table_x.horizontalHeader()
        header.setFrameStyle(QFrame.Box | QFrame.Plain)

        self.table_x.setHorizontalHeader(header)

        self.x_Table.addTab(tab, "X value")

    def U_Table(self):
        self.u_Table.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)

        tab1 = QWidget()

        tab1box = QHBoxLayout()
        tab1box.setContentsMargins(3, 3, 3, 3)
        tab1box.addWidget(self.table_u)
        tab1.setLayout(tab1box)
        self.table_u.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.table_u.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        tab2 = QWidget()

        tab2box = QHBoxLayout()
        tab2box.setContentsMargins(3, 3, 3, 3)
        tab2box.addWidget(self.table_u_ngang)
        tab2.setLayout(tab2box)
        self.table_u_ngang.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.table_u_ngang.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        self.u_Table.addTab(tab2, "Ma trận U ngang")
        self.u_Table.addTab(tab1, "Ma trận U")


def main():
    app = QApplication([])
    mainWindow = App()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
