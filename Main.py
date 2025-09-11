"""
Script con las funciones
"""
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
from v12 import Ui_MainWindow
from GV import MiGraphicsView
import cv2
import qimage2ndarray
import numpy as np


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class About(QtWidgets.QLabel):

    def __init__(self):
        QtWidgets.QLabel.__init__(self,
                                  "CuantiGel 1.0\n\nPor Servando Chinchón Payá, 2024\n\nPor favor no dude en comentar cualquier sugerencia\n\nservando@ietcc.csic.es\n\n¡Gracias!")
        self.setAlignment(QtCore.Qt.AlignCenter)

    def initUI(self):
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = app.desktop().availableGeometry().centre()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class mainProgram(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mainProgram, self).__init__()
        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon(resource_path("Icono.png")))

        self.gv = MiGraphicsView()
        self.gv.setObjectName("gv")
        self.verticalLayout_2.addWidget(self.gv)

        self.gv2 = MiGraphicsView()
        self.gv2.setEnabled(False)
        self.gv2.setObjectName("gv2")
        self.verticalLayout_3.insertWidget(0, self.gv2)

        self.actionInformacion.triggered.connect(self.sobre_programa)
        self.actionAbrir.triggered.connect(self.abrir)
        self.actionTransformar_a_escala_grises.triggered.connect(self.pasar_a_grises)
        self.actionAyuda.triggered.connect(self.Ayuda)
        self.actionSalir.triggered.connect(self.salir)

        self.pb_calcular.clicked.connect(self.calcular)

        self.existe_imagen = False
        self.existe_imagen_qpixmap = False

        self.hs.setMinimum(0)
        self.hs.setMaximum(255)
        self.hs.valueChanged.connect(self.cambio_valor_slider)

    def sobre_programa(self):
        self.pop = About()
        self.pop.resize(555, 333)
        self.pop.setWindowTitle("Sobre CuantiGel")
        self.pop.show()

    def Ayuda(self):
        os.startfile("Guía de usuario.pdf")

    def salir(self):
        choice = QMessageBox.information(None, 'Información',
                                         "¿Estás seguro de que quieres salir?", QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def abrir(self):
        name, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Abrir imagen')
        self.imagen_qpixmap = QtGui.QPixmap(name)
        self.imagen = cv2.imread(name)
        self.gv.setPhoto(self.imagen_qpixmap)
        self.filename = QFileInfo(name).fileName()

        self.actionTransformar_a_escala_grises.setEnabled(True)
        self.actionSeparar_canales.setEnabled(True)
        self.existe_imagen = True

    def pasar_a_grises(self):
        if self.existe_imagen:
            self.gv2.setEnabled(True)
            altura, ancho = self.imagen.shape[:2]
            self.imagen_grises = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2GRAY)
            self.imagen_gv2 = self.imagen_grises

            ret, thresh = cv2.threshold(self.imagen_grises, 127, 255, 0)
            self.contornos, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(self.contornos) >= 2:
            self.contornos = sorted(self.contornos, key=cv2.contourArea, reverse=True)

            segundo_mayor_contorno = self.contornos[1]  # Segundo mayor
            mascara = np.zeros_like(self.imagen_gv2)
            cv2.drawContours(mascara, [segundo_mayor_contorno], -1, (255, 255, 255), thickness=cv2.FILLED)
            self.imagen_mascara = cv2.bitwise_and(self.imagen_gv2, mascara)

            x, y, w, h = cv2.boundingRect(segundo_mayor_contorno)

            self.imagen_recortada = self.imagen_mascara[y:y + h, x:x + w]

            self.imagen_reescalada = cv2.resize(self.imagen_recortada, (w, h), interpolation=cv2.INTER_AREA)

            self.gv2.setPhoto(self.cv2_a_qpixmap((self.imagen_reescalada)))

            self.imagen_gv2 = self.imagen_reescalada

        self.hs.setEnabled(True)
        self.hs.setValue(0)
        self.pb_calcular.setEnabled(True)

    def cv2_a_qpixmap(selfself, imagen):
        qimage = qimage2ndarray.gray2qimage(imagen)
        qpixmap = QtGui.QPixmap.fromImage(qimage)
        return qpixmap

    def cambio_valor_slider(self):
        valor = self.hs.value()
        self.lb1.setText(str(valor))
        self.binarizar(self.imagen_gv2, valor)

    def binarizar(self, imagen, umbral):
        self.th, self.im_th = cv2.threshold(imagen, umbral, 255, cv2.THRESH_BINARY)
        self.gv2.setPhoto(self.cv2_a_qpixmap(self.im_th))

    def imagen_a_QPixmap(self, imagen):
        (B, G, R) = cv2.split(imagen)
        imagen = cv2.merge([R, G, B])
        Qim = qimage2ndarray.rgb_view(imagen)
        h, w = imagen.shape[:2]
        q_pixmap = QtGui.QPixmap.fromImage(Qim).scaled(w, h)
        return q_pixmap

    def calcular(self):
        if self.gv2.hasPhoto():
            n_px_blancos = cv2.countNonZero(self.im_th)
            h, w = self.im_th.shape[:2]
            n_px_totales = h*w
            porcentaje = n_px_blancos/n_px_totales*100
            self.lb2.setText(str(porcentaje) + ' %')


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = mainProgram()
    window.show()

    sys.exit(app.exec_())
