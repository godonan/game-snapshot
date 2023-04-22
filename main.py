import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PyQt5.QtGui import QScreen
from DisplaySnapshot import DisplaySnapshotWindow
from TakeSnapshot import TakeSnapshot
from pynput.keyboard import Key, Listener, KeyCode
from KeyMonitor import KeyMonitor
import configparser


class GameSnapshot:
    def __init__(self, keybind, monitor):
        # Keybind to use
        self.keybind = keybind

        # monitor to take snapshot of
        self.snapshot_monitor = monitor


        self.key_monitor = KeyMonitor()
        self.key_monitor.keyPressed.connect(self.order_snapshot)
        self.key_monitor.start_monitoring()

        self.display_window = DisplaySnapshotWindow()
        self.display_window.show()

    def order_snapshot(self):
        if self.display_window is None:
            return
        #self.display_window.setWindowState(Qt.WindowMinimized)
        pil_img = TakeSnapshot.take_screenshot()
        #self.display_window.setWindowState(Qt.WindowNoState)
        self.display_window.set_image(pil_img)


def read_config():
    try:
        config = configparser.RawConfigParser()
        config.read('config.cfg')
        details_dict = dict(config.items('DETAILS'))
        return details_dict["keybind"], details_dict["monitor"]
    except:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText('Error reading config file. Using defaults (keybind=M, snapshotting monitor 1).')
        msg.setWindowTitle("Error")
        msg.exec_()
        return None, None


if __name__ == "__main__":

    app = QApplication(sys.argv)
    _keybind, _monitor = read_config()
    if _keybind is None:
        _keybind = "M"
    if _monitor is None:
        _monitor = 1

    snapshot_program = GameSnapshot(_keybind, _monitor)
    sys.exit(app.exec())