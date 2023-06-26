from src.headless_gearboy import HeadlessGearboyWorker
from src.tas_generator import TasGenerator
from src.ultraman_ball import ultraman_generation_steps
import sys
import time
from src.tas_logger import global_logger

if __name__ == "__main__":
    if(len(sys.argv)<2):
        print("Usage: tatas.py rom")
        exit(-1)
    global_logger.info("Started with ROM " + sys.argv[1])
    worker = HeadlessGearboyWorker(sys.argv[1],silent=True)
    try:
        generator = TasGenerator([worker], ultraman_generation_steps)

        generator.generate("/tmp/ultraman/")
    finally:
        worker.terminate()
