from src.headless_gambatte import GambatteWorker
from src.tas_generator import TasGenerator
from src.tas import TasInfo, Tas
from src.ultraman_ball import ultraman_generation_steps
from src.export.bk2exporter import BK2Exporter
from src.workQueue import WorkQueue
from src.workfile import Workfile
import sys
import time
from src.tas_logger import global_logger
import hashlib

if __name__ == "__main__":
    if(len(sys.argv)<3):
        print("Usage: tatas.py rom workfile")
        exit(-1)
    global_logger.info("Started with ROM " + sys.argv[1])
    
    worker = GambatteWorker(sys.argv[1], silent=False)
    try:
        workfile = Workfile(None, sys.argv[2])
        workfile.written = True
        worker.process_workfile_sync(workfile)
    finally:
        worker.terminate()
