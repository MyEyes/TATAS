class TasGenerationStep:
    def __init__(self, name, short_name):
        self.name = name
        self.short_name = short_name

    def generate(self, run, prevStep=None, prevSection=None):
        pass