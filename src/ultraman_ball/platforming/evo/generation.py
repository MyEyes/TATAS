import logging
from ..decodeHelper import DecodeHelper
from .frameOrganism import FrameOrganism
from .inputSequenceOrganism import InputSequenceOrganism
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
            self.attempts.extend(o.generateAttempts(self.numFramesPerAttempt, self.attemptsPerOrganism))
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

    def createOffspring(self, keepTop=50, newRandom=100, breed=250, mutate=600, organismClasses=[FrameOrganism, InputSequenceOrganism]):
        totalOrganisms = keepTop+newRandom+breed+mutate
        self.logger.debug(f"Creating next Generation with {totalOrganisms} organisms. Keeping top {keepTop}")
        self.logger.debug(f"Keeping {keepTop} best. Mutating {mutate}. Breeding {breed}. Random {newRandom}")
        organisms = []

        #Keep top organisms for every organism class
        top_organisms_by_class = {}
        for oc in organismClasses:
            top_organisms_by_class[oc] = []
        for t in self.sortedOrganismScores:
            c = t[0].__class__
            if len(top_organisms_by_class[c])<keepTop:
                top_organisms_by_class[c].append(t[0])
            done = True
            for oc in organismClasses:
                if(len(top_organisms_by_class[oc])<keepTop):
                    done = False
            if done:
                break
        top_organisms = []
        for oc in organismClasses:
            top_organisms.extend(top_organisms_by_class[oc])
        
        organisms.extend(top_organisms)
        for _ in range(newRandom):
            organismClass = random.choice(organismClasses)
            organisms.append(organismClass.generateRandom())
        for _ in range(mutate):
            baseO = random.choice(top_organisms)
            organisms.append(baseO.mutate(0.05, 0.1))
        for _ in range(breed):
            baseA = random.choice(top_organisms)
            baseB = random.choice(top_organisms)
            # We might want to retry, the idea with that is that we can let the breed function
            # of each organism class decide if they can crossbreed with another species
            retryCount = 5
            newOrg = None
            while retryCount > 0: 
                while baseA == baseB:
                    baseB = random.choice(self.organisms)
                newOrg = baseA.breed(baseB)
                if newOrg:
                    break
            if newOrg:
                organisms.append(newOrg)
        return Generation(self.start_state, organisms, self.attemptsPerOrganism, self.numFramesPerAttempt)

    def getStats(self):
        stats = ""
        stats += f"NumOrganisms = {len(self.organisms)}\n"
        stats += f"NumAttempts = {len(self.attempts)}\n"
        stats += f"Organism Counts:\n"
        organismKindCounters = {}
        for o in self.organisms:
            if o.__class__ not in organismKindCounters:
                organismKindCounters[o.__class__] = 0
            organismKindCounters[o.__class__] += 1
        for (k,v) in organismKindCounters.items():
            stats +=f"\t\t{k.__name__}: {v}\n"
        stats += "Top Scores\n"
        for i in range(10):
            stats += f"{i}\t{int(self.sortedOrganismScores[i][1])}\n"
        return stats

    @classmethod
    def generateRandom(cls, start_state, totalOrganisms, organismClasses=[FrameOrganism, InputSequenceOrganism]):
        organisms = []
        for _ in range(totalOrganisms):
            organismClass = random.choice(organismClasses)
            organisms.append(organismClass.generateRandom())
        return Generation(start_state, organisms)