import sys
import random
import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


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

        label3 = QLabel("Input number of labels")
        label1 = QLabel("Input the parameter m")
        label2 = QLabel("Number of clusters")

        self.input1 = QLineEdit()
        self.input2 = QLineEdit()
        self.input3 = QLineEdit()

        gen_button = QPushButton("Generate U_ngang")
        gen_button.clicked.connect(self.generate_U_ngang)

        cal_button = QPushButton("Calculate clusters")
        cal_button.clicked.connect(self.generate_clusters)

        midLayout = QFormLayout()

        midLayout.addRow(label3, self.input3)
        midLayout.addRow(label2, self.input2)
        midLayout.addWidget(gen_button)
        midLayout.addRow(label1, self.input1)
        midLayout.addWidget(cal_button)
        midLayout.setContentsMargins(1, 40, 1, 1)
        self.midWidget.setLayout(midLayout)

    def get_data_file(self):
        try:
            file_filter = 'Data File (*.xlsx *.csv *.data);; Excel File (*.xlsx *.xls)'
            path, _ = QFileDialog.getOpenFileName(parent=self, caption='Select a Data File', filter=file_filter,
                                                  options=QFileDialog.DontUseNativeDialog)
            self.textEdit.setText(path)
            data = pd.read_csv(path, header=None)
            data = data.select_dtypes(include=["float64", "int64"])
            self.X = np.array(data)
            self.n_rows = self.X.shape[0]
            self.n_cols = self.X.shape[1]
            model_x = TableModel(self.X)
            self.table_x.setModel(model_x)
            self.table_x.resizeColumnsToContents()
        except:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Please choose a data set !')

    def generate_U_ngang(self):
        if (self.input3.text() != '') and (self.input2.text() != ''):
            text1 = self.input3.text()
            self.number_labels = int(text1)
            self.number_of_cluster = int(self.input2.text())

            index_x_giamsat = random.sample(range(self.n_rows),
                                            self.number_labels)  # CHọn k1 vector x từ n vector x ban đầu
            index_x_giamsat = np.sort(index_x_giamsat)
            U_ngang = np.zeros((self.n_rows, self.number_of_cluster))
            for i in range(self.number_labels):
                c1 = random.randint(0, self.number_of_cluster - 1)  # Chọn vị trí cụm giám sát
                U_ngang[index_x_giamsat[i]][c1] = 0.5
            self.sum_i = sum(U_ngang.T)

            self.index_x_supervised = index_x_giamsat
            self.u_ngang = U_ngang
            model = TableModel(U_ngang)
            self.table_u_ngang.setModel(model)
            self.table_u_ngang.resizeColumnsToContents()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Do not let input fields empty!")
            msg.setInformativeText('More information')
            msg.setWindowTitle("Error")
            msg.exec_()

    def generate_clusters(self):

        if self.input1.text() != '':
            value_m = int(self.input1.text())
            self.V_var = np.random.rand(self.number_of_cluster, self.n_cols)
            self.U_var = np.zeros((self.n_rows, self.number_of_cluster))
            self.count_class_cluster = np.zeros((2, self.number_of_cluster), dtype="int64")
            self.w1 = 0
            self.w2 = 0
            self.w3 = 0

            def d_ki(k, i):
                kq = sum(pow(self.X[k] - self.V_var[i], 2))
                return kq

            def funtion_6(m):
                Z = np.zeros((self.n_rows, self.number_of_cluster))

                D = np.zeros((self.n_rows, self.number_of_cluster))
                for k in range(self.n_rows):
                    for i in range(self.number_of_cluster):
                        D[k][i] = pow(d_ki(k, i), 1 / (1 - m))
                    D[k] = D[k] / sum(D[k])

                for i in range(self.n_rows):
                    Z[i] = (1 - self.sum_i[i]) * D[i]

                return self.u_ngang + Z  # tuc la U

            def function_4(m):
                V_temp = np.zeros((self.number_of_cluster, self.n_cols))
                U_temp = abs(self.U_var - self.u_ngang)
                U_temp = pow(U_temp, m)
                for i in range(self.number_of_cluster):
                    tu_so = np.zeros(self.n_cols)
                    for k in range(self.n_rows):
                        tu_so += U_temp[k][i] * self.X[k]
                    V_temp[i] = tu_so / sum((U_temp.T)[i])
                print("V_sau:")
                print(V_temp)
                return V_temp

            def count(c):

                for k in range(self.n_rows):
                    if k in self.index_x_supervised:
                        k_class = 0
                    else:
                        k_class = 1
                    max_u = np.amax(self.U_var[k])
                    index_max = np.where(self.U_var[k] == max_u)

                    self.count_class_cluster[k_class][index_max] += 1

            num_class = 2

            def external_validity(c):
                a1 = b1 = c1 = d1 = 0
                for i in range(num_class):
                    a1 += sum((self.count_class_cluster[i] - 1) * self.count_class_cluster[i] / 2)
                    b1 += (pow(sum(self.count_class_cluster[i]), 2) - sum(pow(self.count_class_cluster[i], 2))) / 2
                for i in range(c):
                    c1 += self.count_class_cluster[0][i] * self.count_class_cluster[1][i]
                for j in range(c):
                    if i != j:
                        d1 += self.count_class_cluster[0][i] * self.count_class_cluster[1][j]

                self.w1 = (a1 + d1) / (a1 + b1 + c1 + d1)

                # Adjusted Rand Index
                M = a1 + b1 + c1 + d1
                self.w2 = (a1 - (a1 + c1) * (a1 + b1) / M) / ((2 * a1 + b1 + c1) / 2 - (a1 + c1) * (a1 + b1) / M)

                # Jaccard Coefficient
                self.w3 = a1 / (a1 + b1 + c1)

            def thuat_toan(epsilon, m):
                Epsilon = np.zeros((self.number_of_cluster, self.n_cols)) + epsilon
                i = 1
                while True:
                    print("-----------------------\nChay lan " + str(i) + "\n")
                    i += 1
                    self.U_var = funtion_6(m)
                    V_truoc = self.V_var
                    self.V_var = function_4(m)
                    delta_V = abs(self.V_var - V_truoc)
                    ktra = np.less_equal(delta_V, Epsilon)
                    if np.all(ktra):
                        break
                print("\n------------------------------------\nKetqua\n")
                count(self.number_of_cluster)
                external_validity(self.number_of_cluster)

            thuat_toan(1e-6, value_m)

            cluster_model = TableModel(self.V_var)
            u_model = TableModel(self.U_var)

            self.table_u.setModel(u_model)
            self.table_u.resizeColumnsToContents()
            self.table_v.setModel(cluster_model)
            self.table_v.resizeColumnsToContents()

            self.rand_value_box.insert(str(self.w1))
            self.adjusted_value_box.insert(str(self.w2))
            self.jaccard_value_box.insert(str(self.w3))
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Missing Input")
            msg.setInformativeText("Please, input the m value")
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
