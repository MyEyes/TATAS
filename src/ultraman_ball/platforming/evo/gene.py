class Gene:
    def __init__(self):
        self.name = "Gene"

    def generateInput(self):
        return b"\0"

    def reset(self):
        pass

    def mutate(self, mutationChance, mutationStrength):
        pass

    @classmethod
    def generateRandom(cls):
        pass