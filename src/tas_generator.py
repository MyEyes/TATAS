from .tas_generation_run import TasGenerationRun
from .tas import Tas
import logging
class TasGenerator:
    def __init__(self, workers, steps):
        self.workers = workers
        self.steps = steps
        self.logger = logging.getLogger('TATAS.Generator')

    def generate(self, proj_path):
        self.logger.info("Starting to generate")
        run = TasGenerationRun(proj_path, self.workers)
        lastStep = None
        lastSection = None
        for s in self.steps:
            s.logStart()
            newSection = s.generate(run, lastStep, lastSection)
            if newSection is None:
                s.logEnd()
                self.logger.critical(f"Generation of section failed, aborting")
                return None
            s.logEnd()
            run.clearTmpFiles()
            self.logger.info(f"Generated section: {newSection}")
            run.addSection(newSection)
            lastStep = s
            lastSection = newSection
        return Tas(run.sections)

