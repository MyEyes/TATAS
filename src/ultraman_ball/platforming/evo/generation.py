import logging
from ..decodeHelper import DecodeHelper
from .frameOrganism import FrameOrganism
from ....workitem import WorkItem
from ...ultraman_consts import ULTRAMAN_CONSTS
import random
class Generation:
    def __init__(self, start_state, organisms, attemptsPerOrganism=10, numFramesPerAttempt=400):
        self.organisms = organisms
        self.attemptsPerOrganism = attemptsPerOrganism
        self.numFramesPerAttempt = numFramesPerAttempt
        self.start_state = start_state
        self.bestAttempt = None
        self.attempts = []
        self.organismScores = {}
        self.sortedOrganismScores = []
        self.logger = logging.getLogger('TATAS.evo.generation')

    def generateAttempts(self):
        self.logger.debug("Generating attempts")
        for o in self.organisms:
            for _ in range(self.attemptsPerOrganism):
                self.attempts.append(o.generateAttempt(self.numFramesPerAttempt))
        self.logger.debug(f"Generated {len(self.attempts)} attempts")

    def run(self, genRun, step, workQueue):
        if len(self.attempts) == 0:
            self.generateAttempts()
        self.logger.debug("Submitting work")
        for a in self.attempts:
            wi = WorkItem(self.start_state)
            wi.output_file = genRun.getStepRndPath(step, tmp=True)
            wi.inputs = a.inputs
            wi.outdata = [ULTRAMAN_CONSTS.ADDR_POSX,ULTRAMAN_CONSTS.ADDR_POSX2,ULTRAMAN_CONSTS.ADDR_POSY,ULTRAMAN_CONSTS.ADDR_POSY2]
            wf = workQueue.create_workfile(wi, genRun.getStepRndPath(step, tmp=True))
            a.workfile = wf
            workQueue.submitWork(wf)
        # Wait until all attempts are done
        done = False
        while not done:
            done = True
            for a in self.attempts:
                if not a.workfile.isCompleted():
                    done = False
        self.logger.debug("Work done")

    def scoreOrganisms(self, scorer):
        self.logger.debug("Scoring organisms")
        self.organismScores = {}
        for o in self.organisms:
            self.organismScores[o] = 0
        for a in self.attempts:
            o = a.organism
            score, frame = scorer.scoreResult(a.workfile.result)
            a.score = score
            if score > self.organismScores[o]:
                self.organismScores[o] = score
            if self.bestAttempt is None or score > self.bestAttempt.score:
                self.bestAttempt = a
        self.sortedOrganismScores = sorted(self.organismScores.items(), key=lambda x:x[1], reverse=True)

    def getBestAttempt(self):
        return self.bestAttempt

    def createOffspring(self, keepTop=50, newRandom=100, breed=250, mutate=600, organismClass=FrameOrganism):
        totalOrganisms = keepTop+newRandom+breed+mutate
        self.logger.debug(f"Creating next Generation with {totalOrganisms} organisms. Keeping top {keepTop}")
        self.logger.debug(f"Keeping {keepTop} best. Mutating {mutate}. Breeding {breed}. Random {newRandom}")
        organisms = []
        top_organisms = [t[0] for t in self.sortedOrganismScores[:keepTop]]
        organisms.extend(top_organisms)
        for _ in range(newRandom):
            organisms.append(organismClass.generateRandom())
        for _ in range(mutate):
            baseO = random.choice(top_organisms)
            organisms.append(baseO.mutate(0.05, 0.1))
        for _ in range(breed):
            baseA = random.choice(top_organisms)
            baseB = random.choice(top_organisms)
            while baseA == baseB:
                baseB = random.choice(top_organisms)
            organisms.append(baseA.breed(baseB))
        return Generation(self.start_state, organisms, self.attemptsPerOrganism, self.numFramesPerAttempt)

    @classmethod
    def generateRandom(cls, start_state, totalOrganisms, organismClass=FrameOrganism):
        organisms = []
        for _ in range(totalOrganisms):
            organisms.append(organismClass.generateRandom())
        return Generation(start_state, organisms)