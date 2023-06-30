import struct
from .workitem_result import WorkItemResult
class Workfile:
    #define WORKITEM_SAVESTATE_FILE_MAX_LEN 128
    #define WORKITEM_OUTPUT_FILE_MAX_LEN 256
    #define WORKITEM_INPUT_FILE_MAX_LEN 256
    def __init__(self, workitem, path):
        self.workitem = workitem
        self.path = path
        self.written = False
        self.result = None

    def writeOut(self):
        pass

    def outputToResult(self) -> WorkItemResult:
        pass

    def waitForCompletion(self):
        while not self.result:
            pass
        return

    def isCompleted(self):
        return self.result != None