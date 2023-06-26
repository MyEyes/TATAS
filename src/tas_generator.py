from .tas_generation_run import TasGenerationRun
import logging
class TasGenerator:
    def __init__(self, workers, steps):
        self.workers = workers
        self.steps = steps
        self.logger = logging.getLogger('TATAS.Generator')

    def generate(self, proj_path):
        sections = []
        self.logger.info("Starting to generate")
        run = TasGenerationRun(proj_path, self.workers)
        lastStep = None
        lastSection = None
        for s in self.steps:
            s.logStart()
            newSection = s.generate(run, lastStep, lastSection)
            s.logEnd()
            self.logger.info(f"Generated section: {newSection}")
            sections.append(newSection)
            lastStep = s
            lastSection = newSection
        return sections

