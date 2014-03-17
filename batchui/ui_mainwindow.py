# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'batchui\mainwindow.ui'
#
# Created: Sun Mar 16 23:28:53 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(917, 636)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalSplitter = QtGui.QSplitter(self.centralwidget)
        self.horizontalSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSplitter.setObjectName(_fromUtf8("horizontalSplitter"))
        self.verticalSplitter = QtGui.QSplitter(self.horizontalSplitter)
        self.verticalSplitter.setOrientation(QtCore.Qt.Vertical)
        self.verticalSplitter.setObjectName(_fromUtf8("verticalSplitter"))
        self.verticalLayoutWidget = QtGui.QWidget(self.verticalSplitter)
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.filesTreeWidget = QtGui.QTreeWidget(self.verticalLayoutWidget)
        self.filesTreeWidget.setAcceptDrops(True)
        self.filesTreeWidget.setAutoFillBackground(False)
        self.filesTreeWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.filesTreeWidget.setObjectName(_fromUtf8("filesTreeWidget"))
        self.filesTreeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.verticalLayout_2.addWidget(self.filesTreeWidget)
        self.processButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.processButton.setMinimumSize(QtCore.QSize(0, 0))
        self.processButton.setObjectName(_fromUtf8("processButton"))
        self.verticalLayout_2.addWidget(self.processButton)
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.verticalSplitter)
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_3.addWidget(self.label)
        self.console = QtGui.QTextEdit(self.verticalLayoutWidget_2)
        self.console.setReadOnly(True)
        self.console.setObjectName(_fromUtf8("console"))
        self.verticalLayout_3.addWidget(self.console)
        self.sideWidget = QtGui.QWidget(self.horizontalSplitter)
        self.sideWidget.setObjectName(_fromUtf8("sideWidget"))
        self.verticalLayout_4.addWidget(self.horizontalSplitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 917, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuView = QtGui.QMenu(self.menuBar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        self.menuEdit = QtGui.QMenu(self.menuBar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuActions = QtGui.QMenu(self.menuBar)
        self.menuActions.setObjectName(_fromUtf8("menuActions"))
        MainWindow.setMenuBar(self.menuBar)
        self.actionOptions = QtGui.QAction(MainWindow)
        self.actionOptions.setObjectName(_fromUtf8("actionOptions"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.showWithoutGuessAction = QtGui.QAction(MainWindow)
        self.showWithoutGuessAction.setCheckable(True)
        self.showWithoutGuessAction.setObjectName(_fromUtf8("showWithoutGuessAction"))
        self.backupAction = QtGui.QAction(MainWindow)
        self.backupAction.setCheckable(True)
        self.backupAction.setObjectName(_fromUtf8("backupAction"))
        self.exitAction = QtGui.QAction(MainWindow)
        self.exitAction.setObjectName(_fromUtf8("exitAction"))
        self.preferencesAction = QtGui.QAction(MainWindow)
        self.preferencesAction.setObjectName(_fromUtf8("preferencesAction"))
        self.menuFile.addAction(self.exitAction)
        self.menuView.addAction(self.showWithoutGuessAction)
        self.menuEdit.addAction(self.backupAction)
        self.menuEdit.addAction(self.preferencesAction)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())
        self.menuBar.addAction(self.menuView.menuAction())
        self.menuBar.addAction(self.menuActions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "BatchUI", None))
        self.processButton.setText(_translate("MainWindow", "Process", None))
        self.label.setText(_translate("MainWindow", "Errors:", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuView.setTitle(_translate("MainWindow", "View", None))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit", None))
        self.menuActions.setTitle(_translate("MainWindow", "Actions", None))
        self.actionOptions.setText(_translate("MainWindow", "Options...", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.showWithoutGuessAction.setText(_translate("MainWindow", "Show unidentified files", None))
        self.backupAction.setText(_translate("MainWindow", "Backup files before modification", None))
        self.exitAction.setText(_translate("MainWindow", "&Exit", None))
        self.exitAction.setShortcut(_translate("MainWindow", "Ctrl+Q", None))
        self.preferencesAction.setText(_translate("MainWindow", "Preferences...", None))

