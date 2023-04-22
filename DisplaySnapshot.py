import sys
from PIL import Image
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QAction
from PyQt5.QtWidgets import QMenuBar

from TakeSnapshot import TakeSnapshot

def pil2pixmap(im):

    if im.mode == "RGB":
        r, g, b = im.split()
        im = Image.merge("RGB", (b,g,r))
    elif im.mode == "RGBA":
        r, g, b, a = im.split()
        im = Image.merge("RGBA", (b,g,r,a))
    elif im.mode == "L":
        im = im.convert("RGBA")

    # Convert image to RGBA if not done yet
    im2 = im.convert("RGBA")
    data = im2.tobytes("raw", "RGBA")
    qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
    pixmap = QtGui.QPixmap.fromImage(qim)
    return pixmap


class DisplaySnapshotWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # General window data
        self.setWindowTitle("Snapshot Display")

        # Window parameters
        self.setWindowFlags(self.windowFlags() & Qt.WindowStaysOnTopHint)

        # Display Information
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel(self)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.label.setMinimumSize(1, 1)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.installEventFilter(self)

        self.image = QPixmap("default.png")
        self.set_image()
        self.layout.addWidget(self.label)

    def eventFilter(self, source, event):
        if source is self.label and event.type() == QtCore.QEvent.Resize:
            self.label.setPixmap(self.image.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio))
        return super(DisplaySnapshotWindow, self).eventFilter(source, event)

    def set_image(self, pil_img=None):
        if pil_img is not None:
            self.image = pil2pixmap(pil_img)
        self.label.setPixmap(self.image.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio))



