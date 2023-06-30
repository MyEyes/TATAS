from .gene import Gene
import random

class InputTransitionGene(Gene):
    numButtons = 8
    weightBits = 8
    def __init__(self, weights):
        self.name = "InputTransitionGene"
        self.weights = weights
        self.turnOnWeights = self.weights[:self.numButtons]
        self.turnOffWeights = self.weights[self.numButtons:]
        self.state = 0

    def reset(self):
        self.state = 0

    def generateInput(self):
        newState = self.state
        for i in range(self.numButtons):
            press = 1<<i
            if (press & self.state) != 0: #Check if button pressed
                if random.getrandbits(self.weightBits) < self.turnOffWeights[i]: #If we roll less than weight
                    newState &= ~press
            else:
                if random.getrandbits(self.weightBits) < self.turnOnWeights[i]: #If we roll less than weight
                    newState |= press
        self.state = newState
        return self.state

    def mutate(self, mutationChance, mutationStrength):
        newWeights = []
        for i in range(len(weights)):
            newWeight = weights[i]
            if random.random() < mutationChance:
                newWeight += int((random.getrandbits(self.weightBits+1)-(1<<self.weightBits))*mutationStrength)
            newWeights.append(newWeight)
        return InputTransitionGene(newWeights)

    @classmethod
    def generateRandom(cls):
        return InputTransitionGene([random.getrandbits(cls.weightBits) for _ in range(2*cls.numButtons)])