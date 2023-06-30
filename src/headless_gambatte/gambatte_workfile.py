import struct
from ..workfile import Workfile
from ..workitem_result import WorkItemResult
class GambatteWorkfile(Workfile):
    WORKITEM_MAGIC = 0x4B524F57
    WORKITEM_VERSION = 0x00000100

    #define WORKITEM_SAVESTATE_FILE_MAX_LEN 128
    #define WORKITEM_OUTPUT_FILE_MAX_LEN 256
    #define WORKITEM_INPUT_FILE_MAX_LEN 256
    def __init__(self, workitem, path):
        super().__init__(workitem, path)

    def writeOut(self):
        self.written = True
        with open(self.path,"wb") as f:
            f.write(struct.pack("@I", self.WORKITEM_MAGIC))
            f.write(struct.pack("@I", self.WORKITEM_VERSION))
            f.write(struct.pack("@N", len(self.workitem.start_state)))
            f.write(self.workitem.start_state.encode())
            f.write(struct.pack("@N", len(self.workitem.output_savestate)))
            f.write(self.workitem.output_savestate.encode())
            f.write(struct.pack("@N", len(self.workitem.output_movie)))
            f.write(self.workitem.output_movie.encode())
            f.write(struct.pack("@N", len(self.workitem.output_file)))
            f.write(self.workitem.output_file.encode())
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