from src.headless_gearboy import HeadlessGearboyWorker
from src.tas_generator import TasGenerator
from src.tas import TasInfo, Tas
from src.ultraman_ball import ultraman_generation_steps
from src.export.bk2exporter import BK2Exporter
import sys
import time
from src.tas_logger import global_logger
import hashlib

def sha1sum(filename):
    h  = hashlib.sha1()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest()

if __name__ == "__main__":
    if(len(sys.argv)<2):
        print("Usage: tatas.py rom")
        exit(-1)
    global_logger.info("Started with ROM " + sys.argv[1])
    worker = HeadlessGearboyWorker(sys.argv[1],silent=True)
    try:
        generator = TasGenerator([worker], ultraman_generation_steps)
        tas = generator.generate("/tmp/ultraman/")
        sha1 = sha1sum(sys.argv[1])
        tasInfo = TasInfo(name="Ultraman Ball TAS",gamename="Ultraman Ball",SHA1=sha1)
        tas.setInfo(tasInfo)
        exporter = BK2Exporter()
        exporter.export("movie.bk2", tas)
    finally:
        worker.terminate()
