from .organism import Organism
from .attempt import Attempt
from .inputTransitionGene import InputTransitionGene
import random

class InputSequenceOrganism(Organism):
    def __init__(self, inputs):
        self.inputs = inputs

    def generateAttempts(self, numFrames, maxNumAttempts):
        return [self.generateAttempt(numFrames)]

    def generateAttempt(self, numFrames):
        inputs = bytearray(numFrames)
        inputIndex = 0
        for i in range(numFrames):
            inputs[i] = self.inputs[inputIndex]
            inputIndex += 1
            if(inputIndex >= len(self.inputs)):
                inputIndex = 0
        attempt = Attempt(self, inputs)
        return attempt

    def breed(self, partner, changeChance = 0.05):
        partnerInputs = None
        if isinstance(partner, InputSequenceOrganism):
            partnerInputs = partner.inputs
        else:
            #If we want to breed with another species, we can breed with what their inputs
            #would have been on a different attempt
            partnerInputs = partner.generateAttempt(len(self.inputs)).inputs
        newInputLen = max(len(self.inputs),len(partnerInputs))
        newInputs = bytearray(newInputLen)
        selfIndex = random.randint(0, len(self.inputs))
        partnerIndex = random.randint(0, len(partnerInputs))
        dominant = random.getrandbits(1) == 1
        if dominant:
            currIndex = selfIndex
            currInputs = self.inputs
        else:
            currIndex = partnerIndex
            currInputs = partnerInputs
        for i in range(newInputLen):
            newInputs[i] = currInputs[currIndex]
            selfIndex += 1
            if(selfIndex >= len(self.inputs)):
                selfIndex = 0
            if(partnerIndex >= len(partnerInputs)):
                partnerIndex = 0
            if random.random() < changeChance:
                dominant = not dominant
                if dominant:
                    currIndex = selfIndex
                    currInputs = self.inputs
                else:
                    currIndex = partnerIndex
                    currInputs = partnerInputs
        return InputSequenceOrganism(newInputs)
        
    def mutate(self, mutationChance, mutationStrength):
        newInputs = bytearray(len(self.inputs)*2)
        i = 0
        o = 0
        while i<len(self.inputs) and o<len(newInputs):
            if random.random() < mutationChance:
                mutationKind = random.randint(0, 5)
                mutationLen = random.randint(0, (int)(len(self.inputs)*mutationStrength))
                if mutationKind == 0: #Skip inputs
                    i += mutationLen
                elif mutationKind == 1: #Repeat inputs
                    lenRepeat = random.randint(0, (int)(len(self.inputs)*mutationStrength))
                    i -= mutationLen
                    if(i<0):
                        i=0
                elif mutationKind == 2: #Mask inputs
                    mask = random.getrandbits(8)
                    mutationLen = min(mutationLen, len(self.inputs)-i, len(newInputs)-o)
                    for d in range(mutationLen):
                        newInputs[o+d] = self.inputs[i+d] & mask
                    i += mutationLen
                    o += mutationLen
                elif mutationKind == 3: #Set inputs
                    mask = random.getrandbits(8)
                    mutationLen = min(mutationLen, len(self.inputs)-i, len(newInputs)-o)
                    for d in range(mutationLen):
                        newInputs[o+d] = self.inputs[i+d] | mask
                    i += mutationLen
                    o += mutationLen
                elif mutationKind == 4: #Scramble
                    mutationLen = min(mutationLen, len(newInputs)-o)
                    for d in range(mutationLen):
                        newInputs[o+d] = random.getrandbits(8)
                    i += mutationLen
                    o += mutationLen

            else:
                newInputs[o] = self.inputs[i]
                i += 1
                o += 1
        return InputSequenceOrganism(newInputs[:o+1])

    @classmethod
    def generateRandom(cls, numFrames=500):
        newInputs = bytearray(numFrames)
        for i in range(numFrames):
            newInputs[i] = random.getrandbits(8)
        return InputSequenceOrganism(newInputs)
