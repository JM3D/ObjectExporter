from maya import cmds
from pymel.core import *
from pymel.core.general import makeIdentity
import os

USERAPPDIR = cmds.internalVar(userAppDir=True)
DIRECTORY = os.path.join(USERAPPDIR, 'objectExporterController')

class ObjectExporterController():

    def __init__(self):
        self.fileTypes = ['OBJ', 'FBX export','mayaAscii']
        self.fileTypeExts = {'OBJexport':'obj', 'FBX export':'fbx', 'mayaAscii':'ma'}
        self.currentFileType = 'OBJexport'
        self.savePath = ''
        pass

    def deleteHistory(self):
        DeleteAllHistory()

    def adjustPivot(self):
        selection = ls(selection=True)
        bbox = exactWorldBoundingBox(selection)
        bottom = [(bbox[0] + bbox[3]) / 2, bbox[1], (bbox[2] + bbox[5]) / 2]
        xform(selection, piv=bottom, ws=True)

    def getCurrentPosition(self):
        selection = ls(selection=True)

        if selection:
            for item in selection:
                translate_x_value = cmds.getAttr("%s.translateX" % item)
                translate_y_value = cmds.getAttr("%s.translateY" % item)
                translate_z_value = cmds.getAttr("%s.translateZ" % item)

        self.objectLocation = [translate_x_value, translate_y_value, translate_z_value]


    def moveToOrigin(self):
        selection = ls(selection=True)
        move(0, 0, 0, selection, rpr=True)
        self.getCurrentPosition()

    def moveToPreviousLocation(self):
        selection = ls(selection=True)
        move(self.objectLocation[0] * -1,
             self.objectLocation[1] * -1,
             self.objectLocation[2] * -1, selection, rpr=True)


    def deleteHistory(self):
        delete(ch=True)

    def exportAtOrigin(self, name):
        selection = ls(selection=True)
        self.moveToOrigin()
        print ' SAVE PATH: ', self.savePath
        path = os.path.join(self.savePath[0], '{0}.{1}'.format(name, self.fileTypeExts[self.currentFileType]))
        print 'current file type is: ', self.currentFileType

        if cmds.ls(selection=True):
            try:
                cmds.file(path, force=True, type=str(self.currentFileType), exportSelected=True, pr=True)
                self.moveToPreviousLocation()
            except:
                displayWarning('File was not exported')

        else:
            cmds.file(save=True, type=self.currentFileType, force=True)
