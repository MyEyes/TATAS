import logging
class TasGenerationStep:
    def __init__(self, name, short_name):
        self.name = name
        self.short_name = short_name
        self.logger = logging.getLogger('TATAS.Step.'+short_name)

    def logStart(self):
        self.logger.info(f"[{self.name}]")

    def logEnd(self):
        self.logger.info(f"[{self.name} END]")

    def generate(self, run, prevStep=None, prevSection=None):
        pass