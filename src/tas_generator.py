from .tas_generation_run import TasGenerationRun
class TasGenerator:
    def __init__(self, workers, steps):
        self.workers = workers
        self.steps = steps

    def generate(self, proj_path):
        sections = []
        run = TasGenerationRun(proj_path, self.workers)
        lastStep = None
        lastSection = None
        for s in self.steps:
            newSection = s.generate(run, lastStep, lastSection)
            sections.append(newSection)
            lastStep = s
            lastSection = newSection
        return sections

