import os
import random
import string
from .worker import Worker
import logging

class TasGenerationRun:
    workers = list[Worker]
    def __init__(self, projPath, workers:Worker):
        self.projPath = projPath
        self.workers = workers
        self.existing = []
        self.tmpFiles = []
        self.logger = logging.getLogger('TATAS.Run')
        self.totalFrames = 0
        self.sections = []

    def getRndName(self, length=8):
        return ''.join(random.choices(string.ascii_letters,k=length))

    def ensureRunDir(self, step):
        os.makedirs(self.projPath, exist_ok=True) 

    def getRunFilePath(self, name):
        path = os.path.join(self.projPath,name)
        self.existing.append(path)
        return path

    def ensureStepDir(self, step):
        os.makedirs(os.path.join(self.projPath,step.short_name), exist_ok=True)

    def getStepFilePath(self, step, name):
        self.ensureStepDir(step)
        path = os.path.join(self.projPath,step.short_name,name)
        self.existing.append(path)
        return path

    def getStepRndPath(self, step, tmp=False):
        self.ensureStepDir(step)
        name = self.getRndName()
        path = os.path.join(self.projPath,step.short_name,name)
        while path in self.existing:
            name = self.getRndName()
            path = os.path.join(self.projPath,step.short_name,name)
        self.existing.append(path)
        if tmp:
            self.tmpFiles.append(path)
        return path

    def clearTmpFiles(self):
        self.logger.info(f"Clearing {len(self.tmpFiles)} tmp files")
        for p in self.tmpFiles:
            os.unlink(p)
            self.existing.remove(p)
        self.tmpFiles.clear()


    def getAbsoluteFrameNumber(self, inNextSectionFrame):
        return self.totalFrames + inNextSectionFrame

    def addSection(self, section):
        self.sections.append(section)
        self.totalFrames += len(section.inputs)
