from PyQt4 import QtGui

def createProgressDialog(on_canceled, label):
    progressDialog = QtGui.QProgressDialog('%s...' % label, 'Cancel', 0, 100)
    progressDialog.setWindowTitle('%s progress' % label)        
    progressDialog.canceled.connect(on_canceled)
    return progressDialog


def incrementProgressDialog(progressDialog, label, item):
    if progressDialog.wasCanceled():
        return
    newval = progressDialog.value() + 1
    progressDialog.setValue(newval)
    progressDialog.setLabelText('%s\n%s' % (label, item))
