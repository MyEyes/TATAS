from .organism import Organism
from .attempt import Attempt
from .inputTransitionGene import InputTransitionGene
import random
class FrameGeneTuple:
    def __init__(self, frames, gene):
        self.frames = frames
        self.gene = gene

class FrameOrganism(Organism):
    def __init__(self, frameGeneTuples):
        self.frameGeneTuples = frameGeneTuples

    def generateAttempts(self, numFrames, maxNumAttempts):
        return [self.generateAttempt(numFrames) for _ in range(maxNumAttempts)]

    def generateAttempt(self, numFrames):
        inputs = bytearray(numFrames)
        tupleIndex = 0
        geneFrames = 0
        currGeneTuple = self.frameGeneTuples[tupleIndex]
        for i in range(numFrames):
            if geneFrames >= currGeneTuple.frames:
                tupleIndex = (tupleIndex+1)%len(self.frameGeneTuples)
                currGeneTuple = self.frameGeneTuples[tupleIndex]
                currGeneTuple.gene.reset()
                geneFrames = 0
            inputs[i] = currGeneTuple.gene.generateInput()
        attempt = Attempt(self, inputs)
        return attempt

    # Go through and assign every potential frame to either genes from self or partner
    def breed(self, partner, changeChance = 0.05):
        if not isinstance(partner, FrameOrganism):
            return partner.breed(self, changeChance)
        newTuples = []

        selfIndex = 0
        partnerIndex = 0

        selfTotalFrames = sum([ft.frames for ft in self.frameGeneTuples])
        partnerTotalFrames = sum([ft.frames for ft in partner.frameGeneTuples])
        if selfTotalFrames < partnerTotalFrames:
            totalFrames = random.randint(selfTotalFrames, partnerTotalFrames)
        else:
            totalFrames = random.randint(partnerTotalFrames, selfTotalFrames)
        selfCurr = self.frameGeneTuples[selfIndex]
        selfRemaining = selfCurr.frames

        partnerCurr = partner.frameGeneTuples[partnerIndex]
        partnerRemaining = partnerCurr.frames

        curr = random.choice([selfCurr, partnerCurr]).gene
        lastCurr = curr
        length = 0

        for _ in range(totalFrames):
            change = False
            selfRemaining -= 1
            if random.random() < changeChance:
                change = True
            if selfRemaining == 0:
                selfIndex += 1
                if selfIndex >= len(self.frameGeneTuples):
                    selfIndex = 0
                selfCurr = self.frameGeneTuples[selfIndex]
                selfRemaining = selfCurr.frames
                change = True

            partnerRemaining -= 1
            if partnerRemaining == 0:
                partnerIndex += 1
                if partnerIndex >= len(partner.frameGeneTuples):
                    partnerIndex = 0
                partnerCurr = partner.frameGeneTuples[partnerIndex]
                partnerRemaining = partnerCurr.frames
                change = True
            lastCurr = curr
            length += 1
            if change:
                curr = random.choice([selfCurr, partnerCurr]).gene
                if curr != lastCurr:
                    newTuples.append(FrameGeneTuple(length, lastCurr))
                    length = 0
        if length > 0:
            newTuples.append(FrameGeneTuple(length, lastCurr))

        return FrameOrganism(newTuples)

    def breed2(self, partner):
        dominant = 1
        skipSelf = 2
        skipPartner = 4
        mix = 8

        selfI = 0
        partnerI = 0
        totalTuples = max(len(self.frameGeneTuples),len(partner.frameGeneTuples))+random.getrandbits(2)-1
        #Just to avoid some case where we might reduce number of genes to nothing
        if totalTuples < 2:
            totalTuples = 2
        newTuples = []
        for _ in range(totalTuples):

            kind = random.getrandbits(4)

            dominantOne = partner
            dominantI = partnerI
            recessiveOne = self
            recessiveI = selfI

            if kind & dominant == 1:
                dominantOne = self
                dominantI = selfI
                recessiveOne = partner
                recessiveI = partnerI

            if kind & mix == 1:
                newTuples.append(FrameGeneTuple(dominantOne.frameGeneTuples[dominantI].frames, recessiveOne.frameGeneTuples[recessiveI].gene))
            else:
                newTuples.append(dominantOne.frameGeneTuples[dominantI])
            
            if kind & skipSelf == 1:
                selfI += 1
                if selfI >= len(self.frameGeneTuples):
                    selfI = 0
            if kind & skipPartner == 1:
                partnerI += 1
                if partnerI >= len(partner.frameGeneTuples):
                    partnerI = 0
        return FrameOrganism(newTuples)
        
    def mutate(self, mutationChance, mutationStrength):
        newTuples = []
        for fg in self.frameGeneTuples:
            newFrames = fg.frames
            newGene = fg.gene
            newTuple = FrameGeneTuple(newFrames, newGene)
            newTuples.append(newTuple)
        return FrameOrganism(newTuples)

    @classmethod
    def generateRandom(cls, numGenes=4, minFrames=10, maxFrames=100, geneClass=InputTransitionGene):
        newTuples = []
        for _ in range(numGenes):
            frames = random.randint(minFrames, maxFrames)
            gene = geneClass.generateRandom()
            newTuples.append(FrameGeneTuple(frames, gene))
        return FrameOrganism(newTuples)
