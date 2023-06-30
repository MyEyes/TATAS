class Attempt:
    def __init__(self, organism, inputs):
        self.organism = organism
        self.inputs = inputs
        self.score = -1
        self.workfile = None