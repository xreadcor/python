import sys

import numpy as np

from PyQt5 import uic

from PyQt5 import QtGui, QtWidgets, QtCore

from PyQt5.QtWidgets import QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QTreeWidgetItem, QTreeWidget


class MainWindow(QtWidgets.QMainWindow):


# __counter_cliker_smpl и __counter_cliker_dcs приватные переменные флаги

__counter_cliker_smpl = False

__counter_cliker_dcs = False

minEl = 0


def __init__(self):


QtWidgets.QMainWindow.__init__(self)

self.ui = uic.loadUi('gui.ui', self)

self.pushButton.clicked.connect(self.defaultButton)

self.pushButton_2.clicked.connect(self.simplifyButton)

self.pushButton_3.clicked.connect(self.solveButton)

self.pushButton_4.clicked.connect(self.resetButton)

self.tableWidget_3.setVerticalHeaderLabels(["Задачи", "Узлы"])


def defaultButton(self):  # Задание исходных матриц


# Параметры задание исходной матрицы

# numGr - номер группы : 1 numTm - номер бригады : 2 i - номер строки матрицы

# формула определяющий первый столбец (numGr+numTm+i)/2, остальные столбцы статичны

k = []

numGr = 1

numTm = 5

for i in range(1, 6, 1):

k.append((numGr + numTm + i) / 2)

c = np.array([[k[0], 7, 2, 2], [k[1], 8, 1, 3], [k[2], 9, 6, 2], [k[3], 10, 7, 1], [k[4], 5, 3, 1]])

t = np.array([[k[0], 3, 2, 9], [k[1], 6, 5, 10], [k[2], 7, 6, 11], [k[3], 7.5, 7, 12], [k[4], 9, 8, 5]])

buttonReply = QMessageBox.question(self, 'Подтвердите действие',
                                   "Вы действительно хотите задать матрицы С,Т и Тз по умолчанию?",
                                   QMessageBox.Yes | QMessageBox.No)

if buttonReply == QMessageBox.Yes:

for i in range(5):

for j in range(4):

self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(c[i, j])))

self.tableWidget.setItem(i, j, QTableWidgetItem(str(t[i, j])))

self.lineEdit.setText('21')

self.pushButton.setEnabled(False)


def simplifyButton(self):  # Упрощение исходных матриц


if self.lineEdit.text() == '' or self.__counter_cliker_smpl:

buttonReply = QMessageBox.question(self, 'Предупреждение',
                                   "Пожалуйста,проверьте корректность ввода данных матриц С и Т", QMessageBox.Ok)

# нужна проверка заполнения массивов

else:  # Проход проверок, упрощение

# Чтение матриц

self.__counter_cliker_smpl = True

c = np.zeros((5, 4))

t = np.zeros((5, 4))

try:

for i in range(5):

for j in range(4):

c[i, j] = float(self.tableWidget_2.item(i, j).text())

if c[i, j] <= 0:

raise ValueError

t[i, j] = float(self.tableWidget.item(i, j).text())

if t[i, j] <= 0:

raise ValueError

# Первое упрощение исходной матрицы

minTi = np.sum(t.min(axis=1))

minCis = 10000

Tis = 0

k = 0

l = 0

for i in range(5):

minCis = c[i, 0]

for j in range(4):

if minCis > c[i, j]:

minCis = c[i, j]

k = i

l = j

Tis = t[k, l]

for j in range(4):

if c[i, j] > minCis and t[i, j] > Tis:

c[i, j] = -1

t[i, j] = -1

# Второе упрощение исходной матрицы

tz = float(self.lineEdit.text())

if minTi > tz:

raise ValueError

for i in range(5):

for j in range(4):

sum = 0

srminTij = 0

slminTij = 0

if t[i, j] != -1:

sum += t[i, j]

if i < 4 and i > 0:

for k in range(i):

minTi = 10000

for l in range(4):

if minTi > t[k, l] and t[k, l] != -1:

minTi = t[k, l]

slminTij += minTi

for k in range(i + 1, 5):

minTi = 10000

for l in range(4):

if minTi > t[k, l] and t[k, l] != -1:

minTi = t[k, l]

srminTij += minTi

if i == 0:

for k in range(1, 5):

for l in range(4):

if minTi > t[k, l] and t[k, l] != -1:

minTi = t[k, l]

srminTij += minTi

if i == 4:

for k in range(4):

minTi = 10000

for l in range(4):

if minTi > t[k, l] and t[k, l] != -1:

minTi = t[k, l]

slminTij += minTi

sum += srminTij

sum += slminTij

if sum > tz:

t[i, j] = -1

c[i, j] = -1

# Заполнение формы упрощенной матрицой

for i in range(5):

for j in range(4):

self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(c[i, j])))

self.tableWidget.setItem(i, j, QTableWidgetItem(str(t[i, j])))

self.pushButton_2.setEnabled(False)

self.pushButton_3.setEnabled(True)

self.tableWidget_2.setEnabled(False)

self.tableWidget.setEnabled(False)

self.lineEdit.setEnabled(False)

except ValueError:

buttonReply = QMessageBox.question(self, 'Предупреждение',
                                   "Пожалуйста,проверьте корректность ввода данных исходных матриц С и Т",
                                   QMessageBox.Ok)

self.__counter_cliker_smpl = False


def solveButton(self):  # Решение задачи и построение дерева


# Нужна проверка корректности данных в таблице и поле

# Считывание упрощенных матриц С и Т

c = np.zeros((5, 4))

t = np.zeros((5, 4))

for i in range(5):

for j in range(4):

c[i, j] = float(self.tableWidget_2.item(i, j).text())

t[i, j] = float(self.tableWidget.item(i, j).text())

# Решение задачи в опредеденном узле

cs = np.zeros((5, 4))

ts = np.zeros((5, 4))

for i in range(5):  # Обход по всей матрице

for j in range(4):

if c[i, j] == -1:

cs[i, j] = -1

ts[i, j] = -1

continue

if i == 0:

SumMinCij = 0

SumMinTij = 0

for k in range(1, 5):

MinCij = 10000

MinTij = 10000

for l in range(4):

if c[k, l] < MinCij and c[k, l] != -1:

MinCij = c[k, l]

if t[k, l] < MinTij and t[k, l] != -1:

MinTij = t[k, l]

SumMinCij += MinCij

SumMinTij += MinTij

cs[i, j] = c[i, j] + SumMinCij

ts[i, j] = t[i, j] + SumMinTij

elif i == 4:

SumPathCij = 0

SumPathTij = 0

for k in range(i):

minCSi = 10000

indK = k

indL = 0

for l in range(4):

if cs[k, l] < minCSi and cs[k, l] != -1:

minCSi = cs[k, l]

indL = l

SumPathCij += c[indK, indL]  # Нахождение минимального пути в задаче

SumPathTij += t[indK, indL]

cs[i, j] = c[i, j] + SumPathCij

ts[i, j] = t[i, j] + SumPathTij

else:

SumPathCij = 0

SumPathTij = 0

for k in range(i):

minCSij = 10000

indK = k

indL = 0

for l in range(4):

if cs[k, l] < minCSij and cs[k, l] != -1:

minCSij = cs[k, l]

indL = l

SumPathCij += c[indK, indL]  # Нахождение минимального пути в задаче

SumPathTij += t[indK, indL]

SumMinCij = 0

SumMinTij = 0

for k in range(i + 1, 5):

MinCij = 10000

MinTij = 10000

for l in range(4):

if c[k, l] < MinCij and c[k, l] != -1:

MinCij = c[k, l]

if t[k, l] < MinTij and t[k, l] != -1:

MinTij = t[k, l]

SumMinCij += MinCij

SumMinTij += MinTij

cs[i, j] = c[i, j] + SumPathCij + SumMinCij

ts[i, j] = t[i, j] + SumPathTij + SumMinTij

# print(cs)

# print(ts)

# пример заполения дерева

answ = []

min5 = 0

for i in range(5):

minCi = 10000

minTi = 10000

indJ = 0

for j in range(4):

if minCi > cs[i, j] and c[i, j] != -1:

minCi = cs[i, j]

min5 = cs[i, j]

indJ = j

minTi = ts[i, j]

self.tableWidget_3.setItem(0, i, QTableWidgetItem(str(i + 1)))

self.tableWidget_3.setItem(1, i, QTableWidgetItem(str(indJ + 1)))

st = str(minCi) + '||' + str(minTi)

answ.append(st)

self.lineEdit_2.setText(str(min5))

it1 = QTreeWidgetItem([answ[0]])

it2 = QTreeWidgetItem([answ[1]])

it3 = QTreeWidgetItem([answ[2]])

it4 = QTreeWidgetItem([answ[3]])

it5 = QTreeWidgetItem([answ[4]])

it1.addChild(it2)

it2.addChild(it3)

it3.addChild(it4)

it4.addChild(it5)

self.treeWidget.addTopLevelItem(it1)

self.pushButton_3.setEnabled(False)


def resetButton(self):  # Сброс решения и исходных данных


buttonReply = QMessageBox.question(self, 'Подтвердите действие',
                                   "Вы действительно хотите очистить матрицы С,Т значение Тз и решение задачи?",
                                   QMessageBox.Yes | QMessageBox.No)

if buttonReply == QMessageBox.Yes:

self.__counter_cliker_smpl = False

self.__counter_cliker_dcs = False

self.lineEdit.setText('')

self.lineEdit_2.setText('')

self.tableWidget.clear()

self.treeWidget.clear()

self.lineEdit.setEnabled(True)

self.pushButton.setEnabled(True)

self.pushButton_2.setEnabled(True)

self.pushButton_3.setEnabled(False)

self.tableWidget_3.clear()

self.tableWidget_2.setEnabled(True)

self.tableWidget.setEnabled(True)

self.tableWidget_2.clear()

self.tableWidget_3.setVerticalHeaderLabels(["Задачи", "Узлы"])

if __name__ == '__main__':

app = QtWidgets.QApplication(sys.argv)

w = MainWindow()

w.show()

sys.exit(app.exec_())
