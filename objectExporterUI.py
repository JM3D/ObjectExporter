from maya import cmds

from objExporter.objectExporterController import ObjectExporterController
from objectExporterController import ObjectExporterController
from PySide2 import QtWidgets, QtCore, QtGui
import os

USERAPPDIR = cmds.internalVar(userAppDir=True)
DIRECTORY = os.path.join(USERAPPDIR, 'objectExporterController')


class ObjectExporterUI(QtWidgets.QDialog):

    objectExporter = None  # type: ObjectExporterController

    def __init__(self):

        super(ObjectExporterUI, self).__init__()

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) # set window to stay on top
        self.setWindowTitle('Object Exporter')
        self.objectExporter = ObjectExporterController()
        self.buildUI()
        self.currentPath = USERAPPDIR

    def buildUI(self):

        layout = QtWidgets.QVBoxLayout(self) # make main vertical layout

        # make save path layout and add it to main layout
        savePathWidget = QtWidgets.QWidget()
        savePathLayout = QtWidgets.QHBoxLayout(savePathWidget)
        layout.addWidget(savePathWidget)

        # save path button
        self.pathBtn = QtWidgets.QPushButton('Choose Directory')
        savePathLayout.addWidget(self.pathBtn)
        self.pathBtn.clicked.connect(self.choosePath)

        # make save name layout and add it to main layout
        saveNameWidget = QtWidgets.QWidget()
        saveNameLayout = QtWidgets.QHBoxLayout(saveNameWidget)
        layout.addWidget(saveNameWidget)

        # save name field
        self.saveNameField = QtWidgets.QLineEdit()
        saveNameLayout.addWidget(self.saveNameField)

        # save filetype combobox
        self.fileTypeCombo = QtWidgets.QComboBox()
        self.fileTypeCombo.addItems(self.objectExporter.fileTypes)
        saveNameLayout.addWidget(self.fileTypeCombo)
        self.fileTypeCombo.activated.connect(self.passFileType)

        # save button
        exportBtn = QtWidgets.QPushButton('Export')
        saveNameLayout.addWidget(exportBtn)
        exportBtn.clicked.connect(self.export)

        # adjust pivot button
        adjustPivotBtn = QtWidgets.QPushButton('Adjust Pivot')
        layout.addWidget(adjustPivotBtn)
        adjustPivotBtn.clicked.connect(self.objectExporter.adjustPivot) # send signal

        # delete history button
        deleteHistoryBtn = QtWidgets.QPushButton('Delete History')
        layout.addWidget(deleteHistoryBtn)
        deleteHistoryBtn.clicked.connect(self.objectExporter.deleteHistory) # send signal

        # close button
        closeBtn = QtWidgets.QPushButton('Close')
        layout.addWidget(closeBtn)
        closeBtn.clicked.connect(self.close)

    def choosePath(self):
        self.objectExporter.savePath = cmds.fileDialog2(cap='Choose Save Path', fm=3)
        print ('Path chosen is', self.objectExporter.savePath)
        self.pathBtn.setText(self.objectExporter.savePath[0])



    def export(self):
        name = self.saveNameField.text()
        if not name.strip():
            displayWarning('You must give a name.')
            return

        self.objectExporter.exportAtOrigin(name)
        #self.saveNameField.setText(self.objectExporter.savePath[0])

    def passFileType(self):
        self.objectExporter.currentFileType = str(self.fileTypeCombo.currentText())

def showUI():

    ui = ObjectExporterUI()
    ui.show()

    return ui
