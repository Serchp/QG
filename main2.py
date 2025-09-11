

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from v11 import Ui_MainWindow
from GV import MiGraphicsView
import cv2
import qimage2ndarray
# from matplotlib import pyplot as plt
import numpy as np


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
        """
        Quito todo lo relativo al GraphicsView de Main.py y lo traigo aquí
        """
        # self.gv = MiGraphicsView()
        # self.gv.setObjectName("gv")
        # self.verticalLayout.addWidget(self.gv)

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
        self.actionSeparar_canales.triggered.connect(self.separar_canales)

        self.cb_invertir.clicked.connect(self.invertir_threshold)
        self.pb_calcular.clicked.connect(self.calcular)

        self.existe_imagen = False
        self.existe_imagen_qpixmap = False

        self.hs.setMinimum(0)
        self.hs.setMaximum(255)
        self.hs.valueChanged.connect(self.cambio_valor_slider)

        self.rb_b.clicked.connect(self.canal_a_gv2)
        self.rb_g.clicked.connect(self.canal_a_gv2)
        self.rb_r.clicked.connect(self.canal_a_gv2)

    def sobre_programa(self):
        self.pop = About()
        self.pop.resize(555, 333)
        self.pop.setWindowTitle("Sobre CuantiGel")
        self.pop.show()

    def abrir(self):
        name, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Abrir imagen')
        self.imagen_qpixmap = QtGui.QPixmap(name)
        self.imagen = cv2.imread(name)
        self.gv.setPhoto(self.imagen_qpixmap)
        self.filename = QFileInfo(name).fileName()

        self.actionTransformar_a_escala_grises.setEnabled(True)
        self.actionSeparar_canales.setEnabled(True)
        self.existe_imagen = True

    # def histograma(self):
    #     # img = cv2.imread('prueba.jpeg', cv2.IMREAD_GRAYSCALE)
    #     img = cv2.imread('P1.png', cv2.IMREAD_GRAYSCALE)
    #     # # gray = cv2. cvtColor(img, cv2.COLOR_BGR5552GRAY)
    #     hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    #     hist /= hist.sum()
    #     plt.figure()
    #     plt.title('Grayscale histogram')
    #     plt.xlabel('Bins')
    #     plt.ylabel('# of pixels')
    #     plt.plot(hist)
    #     plt.xlim([0, 256])
    #     # plt.ylim([0, 2000])
    #     plt.show()
    #
    #     cv2.waitKey(0)
    #
    #     Qim = qimage2ndarray.array2qimage(img)
    #     h, w = img.shape[:2]
    #     q_pixmap = QtGui.QPixmap.fromImage(Qim).scaled(w, h)
    #     self.gv.setPhoto(q_pixmap)

    def pasar_a_grises(self):
        print('imagen gris')
        if self.existe_imagen:
            self.gv2.setEnabled(True)
            self.imagen_grises = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2GRAY)
            self.gv2.setPhoto(self.cv2_a_qpixmap((self.imagen_grises)))
            self.imagen_gv2 = self.imagen_grises
        else:
            print('falta imagen')
        self.hs.setEnabled(True)
        self.hs.setValue(0)
        self.pb_calcular.setEnabled(True)
        self.cb_invertir.setEnabled(True)
        self.rb_b.setEnabled(False)
        self.rb_g.setEnabled(False)
        self.rb_r.setEnabled(False)
        if self.rb_b.isChecked():
            self.rb_b.setChecked(False)
        if self.rb_g.isChecked():
            self.rb_g.setChecked(False)
        if self.rb_r.isChecked():
            self.rb_r.setChecked(False)

    def pasar_a_grises(self):
        print('imagen gris')
        if self.existe_imagen:
            self.gv2.setEnabled(True)
            altura, ancho = self.imagen.shape[:2]
            self.imagen_grises = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2GRAY)
            # self.gv2.setPhoto(self.cv2_a_qpixmap((self.imagen_grises)))
            self.imagen_gv2 = self.imagen_grises

            # self.imagen_gv = self.imagen

            ret, thresh = cv2.threshold(self.imagen_grises, 127, 255, 0)
            self.contornos, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        else:
            print('falta imagen')

        if len(self.contornos) >= 2:
            # Ordenar los contornos por área, de mayor a menor
            self.contornos = sorted(self.contornos, key=cv2.contourArea, reverse=True)

            # Dibujar el segundo mayor contorno
            segundo_mayor_contorno = self.contornos[1]  # Segundo mayor
            # cv.drawContours(im, [segundo_mayor_contorno], -1, (0, 255, 0), 3)

            # Crear una máscara con el mismo tamaño que la imagen, inicialmente negra
            mascara = np.zeros_like(self.imagen_gv2)

            # Dibujar el segundo mayor contorno en la máscara, llenándolo (blanco en el área del contorno)
            cv2.drawContours(mascara, [segundo_mayor_contorno], -1, (255, 255, 255), thickness=cv2.FILLED)

            # Aplicar la máscara a la imagen original
            self.imagen_mascara = cv2.bitwise_and(self.imagen_gv2, mascara)

            # self.imagen_mascara_original = cv2.bitwise_and(self.imagen_gv2, mascara)

            # Encontrar el bounding box (rectángulo que encierra el contorno)
            x, y, w, h = cv2.boundingRect(segundo_mayor_contorno)

            # Recortar la imagen usando las coordenadas del bounding box
            self.imagen_recortada = self.imagen_mascara[y:y + h, x:x + w]

            # Reescalar la imagen recortada para que ocupe el tamaño original de la imagen
            # self.imagen_reescalada = cv2.resize(self.imagen_recortada, (ancho, altura), interpolation=cv2.INTER_AREA)
            self.imagen_reescalada = cv2.resize(self.imagen_recortada, (w, h), interpolation=cv2.INTER_AREA)

            # Mostrar la imagen con solo el área dentro del segundo mayor contorno
            self.gv2.setPhoto(self.cv2_a_qpixmap((self.imagen_reescalada)))

            # self.gv.setPhoto(self.cv2_a_qpixmap(self.imagen_mascara_original))

            self.imagen_gv2 = self.imagen_reescalada


            # cv.imshow('Imagen Recortada', imagen_recortada)
            # cv.waitKey(0)
            # cv.destroyAllWindows()
        else:
            print("No hay suficientes contornos rectangulares detectados.")

        self.hs.setEnabled(True)
        self.hs.setValue(0)
        self.pb_calcular.setEnabled(True)
        self.cb_invertir.setEnabled(True)
        self.rb_b.setEnabled(False)
        self.rb_g.setEnabled(False)
        self.rb_r.setEnabled(False)
        if self.rb_b.isChecked():
            self.rb_b.setChecked(False)
        if self.rb_g.isChecked():
            self.rb_g.setChecked(False)
        if self.rb_r.isChecked():
            self.rb_r.setChecked(False)

    def cv2_a_qpixmap(selfself, imagen):
        qimage = qimage2ndarray.gray2qimage(imagen)
        qpixmap = QtGui.QPixmap.fromImage(qimage)
        return qpixmap

    def cambio_valor_slider(self):
        valor = self.hs.value()
        self.lb1.setText(str(valor))
        self.binarizar(self.imagen_gv2, valor)

    def separar_canales(self):
        self.B, self.G, self.R = cv2.split(self.imagen)
        print('canales separados')

        self.rb_r.setChecked(True)
        self.canal_a_gv2()
        self.rb_b.setEnabled(True)
        self.rb_g.setEnabled(True)
        self.rb_r.setEnabled(True)

        self.hs.setValue(0)
        self.hs.setEnabled(True)
        self.cb_invertir.setEnabled(True)
        self.pb_calcular.setEnabled(True)

    def canal_a_gv2(self):
        if self.rb_b.isChecked():
            self.imagen_gv2 = self.B
            self.gv2.setPhoto(self.cv2_a_qpixmap(self.imagen_gv2))
        if self.rb_g.isChecked():
            self.imagen_gv2 = self.G
            self.gv2.setPhoto(self.cv2_a_qpixmap(self.imagen_gv2))
        if self.rb_r.isChecked():
            self.imagen_gv2 = self.R
            self.gv2.setPhoto(self.cv2_a_qpixmap(self.imagen_gv2))

    def binarizar(self, imagen, umbral):
        if self.cb_invertir.isChecked():
            print('inversión')
            self.th, self.im_th = cv2.threshold(imagen, umbral, 255, cv2.THRESH_BINARY_INV)
            self.gv2.setPhoto(self.cv2_a_qpixmap(self.im_th))
        if not self.cb_invertir.isChecked():
            self.th, self.im_th = cv2.threshold(imagen, umbral, 255, cv2.THRESH_BINARY)
            self.gv2.setPhoto(self.cv2_a_qpixmap(self.im_th))

    def invertir_threshold(self):
        if self.gv2.hasPhoto():
            print('gv2 tiene foto')
            self.cambio_valor_slider()
        else:
            print('falto foto en gv2')

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
            print(n_px_blancos)
            h, w = self.im_th.shape[:2]
            n_px_totales = h*w
            print(n_px_totales)
            porcentaje = n_px_blancos/n_px_totales*100
            print(porcentaje)
            self.lb2.setText(str(porcentaje) + ' %')


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = mainProgram()
    window.show()

    sys.exit(app.exec_())
