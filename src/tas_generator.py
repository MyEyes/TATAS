from .tas_generation_run import TasGenerationRun
from .tas import Tas
import logging
class TasGenerator:
    def __init__(self, workQueue, steps):
        self.workQueue = workQueue
        self.steps = steps
        self.logger = logging.getLogger('TATAS.Generator')

    def generate(self, proj_path):
        self.logger.info("Starting to generate")
        run = TasGenerationRun(proj_path, self.workQueue)
        lastStep = None
        lastSection = None
        for s in self.steps:
            try:
                s.logStart()
                newSection = s.generate(run, lastStep, lastSection)
                if newSection is None:
                    s.logEnd()
                    self.logger.critical(f"Generation of section failed, aborting")
                    return None
                s.logEnd()
            finally:
                run.clearTmpFiles()
            self.logger.info(f"Generated section: {newSection}")
            run.addSection(newSection)
            lastStep = s
            lastSection = newSection
        return Tas(run.sections)

