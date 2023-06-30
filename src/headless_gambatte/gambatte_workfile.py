import struct
from ..workfile import Workfile
from ..workitem_result import WorkItemResult
class GambatteWorkfile(Workfile):
    #define WORKITEM_SAVESTATE_FILE_MAX_LEN 128
    #define WORKITEM_OUTPUT_FILE_MAX_LEN 256
    #define WORKITEM_INPUT_FILE_MAX_LEN 256
    def __init__(self, workitem, path):
        super().__init__(workitem, path)

    def writeOut(self):
        self.written = True
        with open(self.path,"wb") as f:
            f.write(self.workitem.start_state.encode().ljust(128, b"\0"))
            f.write(self.workitem.output_savestate.encode().ljust(128, b"\0"))
            f.write(self.workitem.output_file.encode().ljust(256, b"\0"))
            f.write(struct.pack("@N", len(self.workitem.inputs)))
            f.write(bytes(self.workitem.inputs))
            f.write(struct.pack("@N", len(self.workitem.outdata)))
            for o in self.workitem.outdata:
                f.write(struct.pack("@I", o))


    def outputToResult(self):
        result = WorkItemResult(self.workitem)
        for d in self.workitem.outdata:
            result.data[d] = []
        bytes_per_frame = len(self.workitem.outdata)
        data = None
        with open(self.workitem.output_file, "rb") as f:
            data = f.read()
            #print(data)
        for i in range(len(data)):
            result.data[self.workitem.outdata[i%bytes_per_frame]].append(data[i])
        self.result = result
        #print(result.data)
        return result