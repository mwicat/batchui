import os
import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject


def setupUi(window):
    pkg_path = os.path.dirname(__file__)
    mainwindow_file = os.path.join(pkg_path, 'mainwindow.ui')
    if os.path.exists(mainwindow_file):
        from PyQt4 import uic
        ui = uic.loadUi(mainwindow_file, window)
    else:
        from ui_mainwindow import Ui_MainWindow
        ui = Ui_MainWindow()
        ui.setupUi(window)
    return ui


def setupDnD(window):

    def dragEnterEvent(event):
        if getattr(window, 'blockDnD', False):
            return
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(event):
        if getattr(window, 'blockDnD', False):
            return
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(event):
        if getattr(window, 'blockDnD', False):
            return
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            window.emit(QtCore.SIGNAL("dropped"), links)
        else:
            event.ignore()

    window.dragEnterEvent = dragEnterEvent
    window.dragMoveEvent = dragMoveEvent
    window.dropEvent = dropEvent
    

class XStream(QObject):
    _stdout = None
    _stderr = None

    messageWritten = QtCore.pyqtSignal(str)

    def flush( self ):
        pass

    def fileno( self ):
        return -1

    def write( self, msg ):
        if ( not self.signalsBlocked() ):
            self.messageWritten.emit(unicode(msg))

    @staticmethod
    def stdout():
        if ( not XStream._stdout ):
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
        return XStream._stdout

    @staticmethod
    def stderr():
        if ( not XStream._stderr ):
            XStream._stderr = XStream()
            sys.stderr = XStream._stderr
        return XStream._stderr
