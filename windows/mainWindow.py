# 3rd party imports
from PyQt5.QtWidgets import QWidget, QGraphicsScene
from PyQt5.QtCore import QPropertyAnimation, QRectF, QPointF, QPoint
from PyQt5 import uic

# python imports
import math
import os

# local imports
from widgets.contextMenu import ContextMenu
from widgets.serviceSticker import ServiceSticker
from windows.addWindow import AddWindow
import resources
import glob

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi(os.getcwd() + "\\ui\\mainWindow.ui", self)

        PREFIX = '   ' # 3 SPACES

        self.searchBar.setText(PREFIX)

        # creating animations
        self.crownToolButtonAnim = QPropertyAnimation(self.crownToolButton, b'geometry')
        self.plusToolButtonAnim = QPropertyAnimation(self.plusToolButton, b'geometry')

        self.scene = QGraphicsScene()

        for i in range(6):
            item = ServiceSticker('Google', 'tim@mail.com', index = i)
            self.scene.addItem(item)

        self.graphicsView.setScene(self.scene)
        self.graphicsView.centerOn(0, 0)

        self.contextMenu = ContextMenu()

        # assigning events handlers
        self.searchBar.textChanged.connect(lambda: self.searchBarTextChanged(PREFIX))
        self.crownToolButton.clicked.connect(self.crownToolButtonClicked)
        self.plusToolButton.clicked.connect(self.plusToolButtonClicked)
        self.crownToolButtonAnim.finished.connect(
            lambda: self.crownToolButton.clicked.connect(self.crownToolButtonClicked)
        )
        self.plusToolButtonAnim.finished.connect(
            lambda: self.plusToolButton.clicked.connect(self.plusToolButtonClicked)
        )

    def paintEvent(self, ev):
        self.writeToGlobal(QRectF(self.graphicsView.geometry()))

        viewWidth = self.graphicsView.viewport().width()
        viewHeight = self.graphicsView.viewport().height()
        self.graphicsView.setSceneRect(
                              QRectF(
                                  QPoint(0, 0),
                                  QPoint(viewWidth, viewHeight)
                              )
                          )

    @staticmethod
    def writeToGlobal(data):
        glob.tempList[0] = data

    def searchBarTextChanged(self, prefix):
        self.leavePrefix(prefix)

    def crownToolButtonClicked(self):
        glob.doAnimation(self.crownToolButtonAnim, self.crownToolButton, 3)
        self.contextMenu.exec_(self.calculateCoordinates())

    def plusToolButtonClicked(self):
        glob.doAnimation(self.plusToolButtonAnim, self.plusToolButton, 3)

        addWindow = AddWindow(parent = self)
        addWindow.show()

    ''' This method leaves prefix in self.searchBar QLineEdit '''
    def leavePrefix(self, prefix):
        if len(self.searchBar.text()) < 3:
            self.searchBar.setText(prefix)

    def calculateCoordinates(self):
        coordinates = [
            self.mapToGlobal(self.crownToolButton.pos()).x(),
            self.mapToGlobal(self.crownToolButton.pos()).y()
        ]
        final_coordinates = []
        for coordinate in coordinates:
            final_coordinates.append(coordinate + 25)
        return QPoint(final_coordinates[0], final_coordinates[1])

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication([])
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())