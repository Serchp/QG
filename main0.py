

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from v11 import Ui_MainWindow
from GV import MiGraphicsView
import cv2
import qimage2ndarray
from matplotlib import pyplot as plt


class About(QtWidgets.QLabel):

    def __init__(self):
        QtWidgets.QLabel.__init__(self,
                                  "CuantiGel 1.0\n\nPor Servando Chinchón Payá, 2023\n\nPor favor no dude en comentar cualquier sugerencia\n\nservando@ietcc.csic.es\n\n¡Gracias!")
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

    # def binarizar_antiguo(self):
    #     self.im = cv2.imread('960px-Gray_scale.jpg')
    #     self.th, self.im_th = cv2.threshold(self.im, 128, 255, cv2.THRESH_BINARY)
    #     Qim = qimage2ndarray.array2qimage(self.im_th)
    #     h, w = self.im_th.shape[:2]
    #     q_pixmap = QtGui.QPixmap.fromImage(Qim).scaled(w, h)
    #     self.gv.setPhoto(q_pixmap)

    def histograma(self):
        # img = cv2.imread('prueba.jpeg', cv2.IMREAD_GRAYSCALE)
        img = cv2.imread('P1.png', cv2.IMREAD_GRAYSCALE)
        # # gray = cv2. cvtColor(img, cv2.COLOR_BGR5552GRAY)
        hist = cv2.calcHist([img], [0], None, [256], [0, 256])
        hist /= hist.sum()
        plt.figure()
        plt.title('Grayscale histogram')
        plt.xlabel('Bins')
        plt.ylabel('# of pixels')
        plt.plot(hist)
        plt.xlim([0, 256])
        # plt.ylim([0, 2000])
        plt.show()

        cv2.waitKey(0)

        Qim = qimage2ndarray.array2qimage(img)
        h, w = img.shape[:2]
        q_pixmap = QtGui.QPixmap.fromImage(Qim).scaled(w, h)
        self.gv.setPhoto(q_pixmap)

    def pasar_a_grises(self):
        print('imagen gris')
        if self.existe_imagen:
            self.gv2.setEnabled(True)
            self.imagen_grises = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2GRAY)
            """fundiona, pero me quedo con el método y función cortos"""
            # frame = cv2.cvtColor(self.imagen_grises, cv2.COLOR_BGR2RGB)
            # h, w = self.imagen_grises.shape[:2]
            # bytesPerLine = 3 * w
            # qimage = QImage(frame.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)
            # q_pixmap = QtGui.QPixmap.fromImage(qimage)

            """funciona pero prefiero quitar este código por una línea más simple con una nueva función"""
            # qimage = qimage2ndarray.gray2qimage(self.imagen_grises)
            # self.q_pixmap_gv2 = QtGui.QPixmap.fromImage(qimage)
            # self.gv2.setPhoto(self.q_pixmap_gv2)
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

        # qimage = qimage2ndarray.gray2qimage(self.B)
        # self.q_pixmap_gv2 = QtGui.QPixmap.fromImage(qimage)
        # self.gv2.setPhoto(self.q_pixmap_gv2)

        # self.imagen_gv2 = self.R
        # self.gv2.setPhoto(self.cv2_a_qpixmap(self.imagen_gv2))

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
            # qimage = qimage2ndarray.array2qimage(self.im_th)
            # qimage = qimage2ndarray.gray2qimage(self.im_th)
            # self.q_pixmap_gv2 = QtGui.QPixmap.fromImage(qimage)
            # self.gv2.setPhoto(self.q_pixmap_gv2)
            self.gv2.setPhoto(self.cv2_a_qpixmap(self.im_th))
        if not self.cb_invertir.isChecked():
            self.th, self.im_th = cv2.threshold(imagen, umbral, 255, cv2.THRESH_BINARY)
            # qimage = qimage2ndarray.array2qimage(self.im_th)
            # qimage = qimage2ndarray.gray2qimage(self.im_th)
            # self.q_pixmap_gv2 = QtGui.QPixmap.fromImage(qimage)
            # self.gv2.setPhoto(self.q_pixmap_gv2)
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

    # def prueba(self):
    #     """quiero comprobar el cv2.imread vs self.abris"""
    #     name, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Abrir imagen')
    #     self.img = QtGui.QPixmap(name)
    #     print(self.img)
    #     self.im = cv2.imread(name)
    #     print(self.im)
    #     q_pixmap = self.imagen_a_QPixmap(self.im)
    #     if q_pixmap == self.img:
    #         print('iguales')
    #     else:
    #         print('no iguales')
    #     self.gv.setPhoto(self.img)
    #     cv2.waitKey(10000)
    #     print('la otra')
    #     self.gv.setPhoto(q_pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = mainProgram()
    window.show()

    sys.exit(app.exec_())
