import os
import sys
import traceback

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject

import fileutil
import qtutil

import progressui
from workerthreads import createWorkerThread


BRUSH_STATUS_ERROR = QtGui.QBrush(QtGui.QColor(128, 0, 0))
BRUSH_STATUS_SUCCESS = QtGui.QBrush(QtGui.QColor(0, 128, 0))
BRUSH_STATUS_PENDING = QtGui.QBrush(QtGui.QColor(0, 0, 128))
BRUSH_STATUS_UNKNOWN = QtGui.QBrush(QtGui.QColor(128, 128, 128))


def enqueueFiles(fns, parseProgressDialog, file_parser):
    files_cnt = len(fns)
    parseProgressDialog.setMaximum(files_cnt)
    parseProgressDialog.setMinimumDuration(0)
    parseProgressDialog.setValue(0)            
    for fn in fns:
        file_parser.enqueue(fn)


def updateItemStatus(item, columns):
    if item.data['status'] == 'processed':
        color = BRUSH_STATUS_SUCCESS
        status_text = 'Processed'
    elif item.data['status'] == 'error':
        color = BRUSH_STATUS_ERROR
        status_text = 'Error: %s' % item.data['exception']
    elif item.data['status'] == 'pending':
        color = BRUSH_STATUS_PENDING
        status_text = 'Pending'
    else:
        color = BRUSH_STATUS_UNKNOWN
        status_text = 'Unknown'
    
    status_pos = [column_var for column_var, column_label in columns].index('status_text')
    item.setForeground(status_pos, color)
    item.setText(status_pos, status_text)
    
    for pos, (column_var, column_label) in enumerate(columns):
        if column_var not in item.data:
            continue
        item_text = item.data.get(column_var, '')
        item_text = str(item_text) if item_text is not None else ''
        item.setText(pos, item_text)


def display_exception(textarea, fn, e):
    textarea.setTextColor(QtGui.QColor("red"))
    textarea.append('Error when processing %s:' % fn)
    textarea.setTextColor(QtGui.QColor("green"))
    textarea.append('%s' % e)
    textarea.setTextColor(QtGui.QColor("blue"))
    if hasattr(e, 'output'):
        textarea.append('%s' % e.output)
    formatted_exc = traceback.format_exc()
    if formatted_exc != 'None\n':
        textarea.append('%s' % formatted_exc)


def createUIItem(item, tree, columns):        
    ui_item = QtGui.QTreeWidgetItem(tree,
                                    [str(item.get(column_var, ''))
                                     for column_var, column_label
                                     in columns])
    ui_item.data = item
    updateItemStatus(ui_item, columns)
    return ui_item


def run(argv, *args, **kw):
    app = QtGui.QApplication(sys.argv)
    window = BatchWindow(*args, **kw)
    sys.exit(app.exec_())    


class BatchWindow(QtGui.QMainWindow):
    def __init__(self, app_name, parse_file=None, process_item=None,
                 columns=None, preferences=None,
                 actions=None, is_valid_file=None, parameters_cls=None,
                 guidata=None):
        super(BatchWindow, self).__init__()

        self.app_name = app_name
        self.treeColumns = columns
        
        self.guidata = guidata
        
        self.ui = qtutil.setupUi(self)
        self.showStatus("Hint: Drag and drop files and directories" 
                        " for processing to the list")

        self.setWindowTitle(app_name)

        self.setupFilesTreeWidget()
        
        self.ui.showWithoutGuessAction.toggled.connect(self.handleShowWithoutGuess)
        self.ui.exitAction.triggered.connect(QtGui.qApp.quit)

        self.setupContextMenu()
        self.installActions(actions)

        self.setupSplitters()

        self.parameters = self.installParameters(parameters_cls)
        self.preferences = self.installPreferences(preferences)     
        
        self.ui.processButton.clicked.connect(self.processItems)

        self.installFileVisitor(is_valid_file)
        self.installParser(parse_file)
        self.installProcessor(process_item)

        self.show()
       
    def setupFilesTreeWidget(self):
        qtutil.setupDnD(self.ui.filesTreeWidget)
        QObject.connect(self.ui.filesTreeWidget,
                        QtCore.SIGNAL("dropped"),
                        self.filesDropped)
        self.ui.filesTreeWidget.keyPressEvent = self.removeItem
        self.ui.filesTreeWidget.setHeaderLabels([column_label
                                                 for column_var, column_label
                                                 in self.treeColumns])        
        self.ui.filesTreeWidget.header().resizeSection(0, 300)
     
    def installActions(self, actions):
        if actions is None:
            return

        for action_name, action_handler in actions:
            def action_cb():
                items = self.getSelectedItems()
                action_handler(items)
                for item in items:
                    print 'updating item'
                    updateItemStatus(item, self.treeColumns)
            self.actionEdit = self.ui.menuActions.addAction(action_name,
                                                            action_cb)
            self.popMenu.addAction( self.actionEdit )
    
    def installParameters(self, parameters_cls):    
        if self.guidata is not None and parameters_cls is not None:
            GroupBox = self.guidata.dataset.qtwidgets.DataSetEditGroupBox
            groupbox1 = GroupBox("Output parameters",
                                            parameters_cls, comment='',
                                            show_button=True)
            groupbox1.layout.setAlignment(QtCore.Qt.AlignTop)
            layout = QtGui.QHBoxLayout()
            layout.addWidget(groupbox1)
            self.ui.sideWidget.setLayout(layout)
            parameters = groupbox1.dataset
            return parameters
        else:
            self.ui.sideWidget.hide()
    
    def installPreferences(self, preferences):
        if self.guidata is not None and preferences is not None:        
            uc = self.guidata.userconfig.UserConfig({})
            uc.set_application(self.app_name, '1.0.0')
                    
            preferences.read_config(uc, 'preferences', '')
            
            def preferences_requested():
                preferences.edit(self)
                preferences.write_config(uc,'preferences','')            
            
            self.ui.preferencesAction.triggered.connect(preferences_requested)
            
            return preferences
        else:
            self.ui.preferencesAction.setVisible(False)

    def installParser(self, parse_file):
        def incrementParseDialog(fn):
            progressui.incrementProgressDialog(self.parseProgressDialog,
                                               'Parsed', fn)
        def parse_file2(fn):
            short_fn = fileutil.shorten_fn(fn)
            item = parse_file(fn, self.preferences, self.parameters) \
                if parse_file is not None else {}
            item['status'] = 'pending'
            item['fn'] = fn
            item['short_fn'] = short_fn
            return item            
        
        def file_parsed((fn, item_data)):
            item = self.createTreeItem(item_data)
            incrementParseDialog(fn)
        
        parse_error_handler = self.create_item_failed_cb(incrementParseDialog)
        
        self.file_parser, self.t1 = \
            createWorkerThread(parse_file2,
                               file_parsed,
                               error_handler=parse_error_handler)
        self.parseProgressDialog = \
            progressui.createProgressDialog(self.file_parser.flush,
                                           'Parsing')

    def installFileVisitor(self, is_valid_file):
        def files_visited((dirfn, fns)):
            enqueueFiles(fns, self.parseProgressDialog, self.file_parser)
            
        def walk_dir(dirfn):
            return fileutil.walk_dir(dirfn, is_valid_file)

        self.fs_walker, self.t2 = createWorkerThread(walk_dir, files_visited)

    def installProcessor(self, process_item):
        def incrementProcessDialog(fn):
            progressui.incrementProgressDialog(self.processProgressDialog,
                                               'Processed', fn)
        def process_item2(item):
            if process_item is not None:
                process_item(item, self.shouldBackup(),
                             self.preferences,
                             self.parameters)
            item.data['status'] = 'processed'
            return item

        def item_processed((item, item2)):
            updateItemStatus(item, self.treeColumns)
            fn = item.data['fn']
            incrementProcessDialog(fn)
                
        process_error_handler = self.create_item_failed_cb(incrementProcessDialog)
        self.item_processor,self.t3 = \
            createWorkerThread(process_item2,
                              item_processed,
                              error_handler=process_error_handler)
        self.processProgressDialog = \
            progressui.createProgressDialog(self.item_processor.flush,
                                             'Processing')

    def handleShowWithoutGuess(self, checked):
        for item in self.getItems():
            hide = not self.shouldShowItem(item, checked)
            self.filesTreeWidget.setItemHidden(item, hide)

    def setupContextMenu(self):
        self.popMenu = QtGui.QMenu(self)
        def on_context_menu(point):
            self.popMenu.exec_( self.ui.filesTreeWidget.mapToGlobal(point) )
                
        self.ui.filesTreeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.ui.filesTreeWidget,
                     QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'),
                     on_context_menu)

    def setupSplitters(self):
        self.ui.verticalSplitter.setStretchFactor(0, 1)
        self.ui.verticalSplitter.setStretchFactor(1, 0)
        self.ui.horizontalSplitter.setStretchFactor(0, 1)
        self.ui.horizontalSplitter.setStretchFactor(1, 0)

    def shouldShowItem(self, item, checked=None):
        if checked is None:
            checked = self.ui.showWithoutGuessAction.isChecked()
        shouldShow = item.data is not None and item.data['status'] != 'error' or checked
        return shouldShow

    def shouldBackup(self):
        return self.ui.backupAction.isChecked()

    def showStatus(self, msg):
        self.ui.statusbar.showMessage(msg)

    def getItems(self):
        root = self.ui.filesTreeWidget.invisibleRootItem()
        child_count = root.childCount()
        return [root.child(i) for i in range(child_count)]

    def getSelectedItems(self):
        root = self.ui.filesTreeWidget.invisibleRootItem()
        rows = set(index.row() for index in self.ui.filesTreeWidget.selectedIndexes())
        return [root.child(row) for row in rows] 

    def processItems(self):
        items = [item for item in self.getItems() 
                 if item.data is not None and item.data['status'] != 'error']
        enqueueFiles(items, self.processProgressDialog, self.item_processor)

    def processItem(self, item):
        return 

    def createTreeItem(self, item_data): 
        item = createUIItem(item_data,
                            self.ui.filesTreeWidget,
                            self.treeColumns)
        if not self.shouldShowItem(item): 
            self.filesTreeWidget.setItemHidden(item, True)
        return item
    
    def filesDropped(self, l):
        for url in l:
            if os.path.isdir(url):
                self.addFilesFrom(url)
            else:
                self.addFile(url)

    def removeItem(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            root = self.ui.filesTreeWidget.invisibleRootItem()
            for item in self.ui.filesTreeWidget.selectedItems():
                root.removeChild(item)
        return QtGui.QTreeWidget.keyPressEvent(self.ui.filesTreeWidget, event)

    def addFile(self, fn):
        enqueueFiles([fn], self.parseProgressDialog, self.file_parser)

    def addFilesFrom(self, dirfn):
        self.fs_walker.enqueue(dirfn)

    def create_item_failed_cb(self, progress_cb):
        def item_failed((item, e)):
            fn = item.data['fn'] if hasattr(item, 'data') else item
            item_data = {}
            item_data['status'] = 'error'
            item_data['exception'] = e
            item_data['status_text'] = 'Error: %s' % e
            item_data['fn'] = fn
            item_data['short_fn'] = fileutil.shorten_fn(fn)
            item = self.createTreeItem(item_data)
            display_exception(self.ui.console, fn, e)
            progress_cb(fn)
        return item_failed
