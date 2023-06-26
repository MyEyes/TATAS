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
        self.logger = logging.getLogger('TATAS.Run')

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

    def getStepRndPath(self, step):
        self.ensureStepDir(step)
        name = self.getRndName()
        path = os.path.join(self.projPath,step.short_name,name)
        while path in self.existing:
            name = self.getRndName()
            path = os.path.join(self.projPath,step.short_name,name)
        self.existing.append(path)
        return path
