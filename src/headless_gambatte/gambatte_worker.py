import subprocess
import os
from ..worker import Worker
from .gambatte_workfile import GambatteWorkfile
class GambatteWorker(Worker):
    def __init__(self, rom, gambatte="../gambatte-runner/gambatte_runner", silent=True):
        gambatte_dir = os.path.dirname(gambatte)
        if silent:
            self.proc = subprocess.Popen([gambatte, rom], stdout=subprocess.DEVNULL, env={'LD_LIBRARY_PATH': gambatte_dir})
        else:
            self.proc = subprocess.Popen([gambatte, rom], env={'LD_LIBRARY_PATH': gambatte_dir})
        
        self.in_pipe_path = f"/tmp/gb_worker_{self.proc.pid}_in"
        while not os.path.exists(self.in_pipe_path):
            pass
        self.in_pipe = open(self.in_pipe_path, "wb")

        self.out_pipe_path = f"/tmp/gb_worker_{self.proc.pid}_out"
        while not os.path.exists(self.out_pipe_path):
            pass
        self.out_pipe = open(self.out_pipe_path, "rb")

    def create_workfile(self, workitem, path):
        return GambatteWorkfile(workitem, path)

    def process_workfile_sync(self, workfile):
        self.submit_workfile(workfile)
        self.read_response()
        return workfile.outputToResult()

    def submit_workfile(self, workfile):
        if not workfile.written:
            workfile.writeOut()
        self.in_pipe.write(workfile.path.encode()+b"\0")
        self.in_pipe.flush()

    def read_response(self):
        val = self.out_pipe.read(8)
        return val

    def terminate(self):
        self.proc.kill()
        os.unlink(self.in_pipe_path)
        os.unlink(self.out_pipe_path)