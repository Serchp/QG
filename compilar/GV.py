from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt


class MiGraphicsView(QtWidgets.QGraphicsView):

    def __init__(self):
        QtWidgets.QGraphicsView.__init__(self)

        self._zoom = 0
        self.scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self._photo)
        self.setScene(self.scene)

        self.empty = True

    def hasPhoto(self):
        return not self.empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self.empty = False
            self._photo.setPixmap(pixmap)
        else:
            self.empty = True
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self._dragPos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        if self.cursor() == Qt.ClosedHandCursor:
            self.setCursor(Qt.ArrowCursor)

    def mouseMoveEvent(self, event):
        if event.button() == Qt.LeftButton:
            e = QtCore.QPointF(self.mapToScene(event.pos()))
        if event.buttons() == Qt.RightButton:
            newPos = event.pos()
            diff = newPos - self._dragPos
            self._dragPos = newPos
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - diff.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - diff.y())
