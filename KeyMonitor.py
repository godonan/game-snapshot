import sys

from PyQt5 import QtCore, QtWidgets

from pynput.keyboard import Key, Listener, KeyCode


class KeyMonitor(QtCore.QObject):
    keyPressed = QtCore.pyqtSignal()

    def __init__(self, keypress="M"):
        super().__init__()
        self.keypress = keypress.upper()
        self.listener = Listener(on_press=self.on_press)

    def on_press(self, key):
        if str(key).upper().replace('\'', '') == self.keypress:
            self.keyPressed.emit()

    def stop_monitoring(self):
        self.listener.stop()

    def start_monitoring(self):
        self.listener.start()
