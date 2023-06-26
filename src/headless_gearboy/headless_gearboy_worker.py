import subprocess
import os
from ..worker import Worker
from .headless_gearboy_workfile import HeadlessGearboyWorkfile
class HeadlessGearboyWorker(Worker):
    def __init__(self, rom, headless_gearboy="../Gearboy/platforms/headless/gearboy-headless", headless_gearboy_worker="../Gearboy/platforms/headless/runner/worker_runner/worker_runner.so"):
        headless_gearboy_dir = os.path.dirname(headless_gearboy)
        self.proc = subprocess.Popen([headless_gearboy, rom, headless_gearboy_worker], env={'LD_LIBRARY_PATH': headless_gearboy_dir})
        
        self.in_pipe_path = f"/tmp/gb_worker_{self.proc.pid}_in"
        while not os.path.exists(self.in_pipe_path):
            pass
        self.in_pipe = open(self.in_pipe_path, "wb")

        self.out_pipe_path = f"/tmp/gb_worker_{self.proc.pid}_out"
        while not os.path.exists(self.out_pipe_path):
            pass
        self.out_pipe = open(self.out_pipe_path, "rb")

    def create_workfile(self, workitem, path):
        return HeadlessGearboyWorkfile(workitem, path)

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
        return self.out_pipe.read(4)

    def terminate(self):
        self.proc.kill()
        os.unlink(self.in_pipe_path)
        os.unlink(self.out_pipe_path)