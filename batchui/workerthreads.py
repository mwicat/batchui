from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject

from Queue import Queue


class Worker(QtCore.QObject):

    item_processed = QtCore.pyqtSignal(object)
    item_failed = QtCore.pyqtSignal(object)    
    
    def __init__(self, process_fun=None, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.queue = Queue()
        self.flushing = False
        self.process = process_fun if process_fun is not None else lambda x: x

    def enqueue(self, fns):
        self.queue.put(fns)

    def flush(self):
        self.queue = Queue()
        self.flushing = True

    def run(self):
        while True:
            try:
                item = self.queue.get()
                item_new = self.process(item)
                self.item_processed.emit((item, item_new))
            except Exception as e:
                self.item_failed.emit((item, e))


class SimpleWorker(QtCore.QObject):

    item_processed = QtCore.pyqtSignal(object)
    item_failed = QtCore.pyqtSignal(object)    

    def __init__(self, process_fun, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.process = process_fun

    def run(self):
        while True:
            try:
                item_new = self.process()
                if not item_new:
                    break
                self.item_processed.emit(item_new)
            except Exception as e:
                self.item_failed.emit(e)

def createWorkerThread(process_fun=None, cb=None, start=True, worker_cls=Worker,
                       error_handler=None):
    worker_thread = QtCore.QThread()
    worker = worker_cls(process_fun)
    worker.moveToThread(worker_thread)
    worker_thread.started.connect(worker.run)
    if cb is not None:
        worker.item_processed.connect(cb)
    if error_handler is not None:
        worker.item_failed.connect(error_handler)
    if start:
        worker_thread.start()
    return worker, worker_thread
