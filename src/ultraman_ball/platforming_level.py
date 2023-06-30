from ..tas_generation_step import TasGenerationStep
from ..tas_generation_run import TasGenerationRun
from ..tas_section import TasSection
from .ultraman_consts import ULTRAMAN_CONSTS, INPUT
from ..workitem import WorkItem
from .platforming.waypoint_scorer import WaypointScorer
from .platforming.evo.generation import Generation
import random
import math

class Attempt:
    def __init__(self):
        self.inputs = []
        self.workfile = None
        pass

class UB_PlatformingLevelStep(TasGenerationStep):
    def __init__(self, level="", waypoints=[]):
        self.level = level
        self.waypoints = waypoints
        self.scorer = WaypointScorer(waypoints, frameCost=2)
        self.openAttempts = []
        super().__init__("Ultraman Ball - Platforming Level "+level, level)

    def scoreAttempt(self, genRun, result):
        positions = []
        for i in range(len(result.data[ULTRAMAN_CONSTS.ADDR_POSX])):
            x = result.data[ULTRAMAN_CONSTS.ADDR_POSX][i] + (result.data[ULTRAMAN_CONSTS.ADDR_POSX2][i]<<8)
            y = result.data[ULTRAMAN_CONSTS.ADDR_POSY][i] + (result.data[ULTRAMAN_CONSTS.ADDR_POSY2][i]<<8)
            positions.append((x,y))
        
        return self.scorer.score(positions)

    def submitAttempt(self, genRun, start_state, attempt):
        worker = genRun.workQueue
        no_input = INPUT.asBytes(INPUT.No_Input)

        wi = WorkItem(start_state)
        wi.output_file = genRun.getStepRndPath(self, tmp=True)
        wi.inputs = attempt.inputs
        wi.outdata = [ULTRAMAN_CONSTS.ADDR_POSX,ULTRAMAN_CONSTS.ADDR_POSX2,ULTRAMAN_CONSTS.ADDR_POSY,ULTRAMAN_CONSTS.ADDR_POSY2]
        wf = worker.create_workfile(wi, genRun.getStepRndPath(self, tmp=True))
        attempt.workfile = wf
        worker.submitWork(wf)
        self.openAttempts.append(attempt)

    def retrieveAttempt(self, genRun):
        for attempt in self.openAttempts:
            if attempt.workfile.isCompleted():
                self.openAttempts.remove(attempt)
                return self.scoreAttempt(genRun, attempt.workfile.result)

        return None, None

    def genRandomAttempt(self, length):
        mask = ~INPUT.Select_Key #Never press select
        unpause = 0
        attempt = Attempt()
        attempt.inputs = bytearray(length)
        for i in range(length):
            if unpause == 0:
                attempt.inputs[i] = random.getrandbits(8) & mask
                if attempt.inputs[i] & INPUT.Start_Key:
                    unpause = 2
            elif unpause == 2: #Frame we let go of start so we can repress
                unpause -= 1
                attempt.inputs[i] = 0
            elif unpause == 1:
                attempt.inputs[i] = random.getrandbits(8) & mask
                attempt.inputs[i] |= INPUT.Start_Key #Make sure we unpause
                unpause -= 1
        return attempt

    def find_first_gameplay_frame(self, genRun, start_state):
        worker = genRun.workQueue
        no_input = INPUT.asBytes(INPUT.No_Input)

        wi = WorkItem(start_state)
        wi.output_file = genRun.getStepRndPath(self)
        wi.inputs = bytearray(no_input*(300))
        wi.outdata = [ULTRAMAN_CONSTS.ADDR_BLOCK_INPUT]
        wf = worker.create_workfile(wi, genRun.getStepRndPath(self))
        result = worker.process_workfile_sync(wf)

        for f, s in enumerate(result.data[ULTRAMAN_CONSTS.ADDR_BLOCK_INPUT]):
            if s == 0: #Input not blocked
                end_frame = f-1
                break
        
        self.logger.info(f"First gameplay frame in level is {end_frame}, tas_frame: {genRun.getAbsoluteFrameNumber(end_frame)}")
        wi = WorkItem(start_state)
        wi.output_file = genRun.getStepRndPath(self, tmp=True)
        wi.output_savestate = genRun.getStepFilePath(self, f"start")
        wi.inputs = bytearray(no_input*end_frame)
        wi.outdata = []
        wf = worker.create_workfile(wi, genRun.getStepRndPath(self))
        result = worker.process_workfile_sync(wf)
        return wi.output_savestate, wi.inputs

    def render_generation_best(self, genRun, currG, numGen):
        worker = genRun.workQueue
        attempt = currG.getBestAttempt()
        wi = WorkItem(attempt.workfile.workitem.start_state)
        wi.output_file = genRun.getStepRndPath(self, tmp=True)
        wi.output_movie = genRun.getStepFilePath(self, f"gen_{numGen}.mp4")
        wi.inputs = bytearray(attempt.inputs)
        wi.outdata = []
        wf = worker.create_workfile(wi, genRun.getStepFilePath(self, f"gen_{numGen}"))
        result = worker.process_workfile_sync(wf)

    def generate(self, genRun:TasGenerationRun, prevStep, prevSection):
        worker = genRun.workQueue
        start_state = prevSection.end_state
        level_state, inputs = self.find_first_gameplay_frame(genRun, start_state)

        currG = Generation.generateRandom(level_state, 300)
        currG.attemptsPerOrganism = 5
        generations = [currG]
        topScore = 0
        do_generations = 3

        for i in range(do_generations):
            currG.run(genRun,self,genRun.workQueue)
            currG.scoreOrganisms(self.scorer)
            topScore = currG.sortedOrganismScores[0][1]
            self.logger.info(f"Generation {i} done. Top Score: {topScore}")
            self.render_generation_best(genRun, currG, i)
            if i<do_generations-1:
                currG = currG.createOffspring(keepTop=25,newRandom=50,breed=250,mutate=300)
                generations.append(currG)
                genRun.clearTmpFiles()

        bestAttempt = currG.getBestAttempt()

        # bestAttempt = None
        # bestScore = 0
        # endFrame = 0
        # i = 0
        # while bestScore < 55000 and i < 20000:
        #     if len(self.openAttempts)<8:
        #         attempt = self.genRandomAttempt(400)
        #         self.submitAttempt(genRun, level_state, attempt)
        #     score, frame = self.retrieveAttempt(genRun)
        #     if score is not None:
        #         #self.logger.info(f"Finished attempt {i}. Score: {score}")
        #         if score > bestScore:
        #             self.logger.info(f"Finished attempt {i}. New Best Score: {score}")
        #             bestAttempt = attempt
        #             bestScore = score
        #             endFrame = frame
        #         i+=1
        # #self.logger.info(f"Best attempt score: {bestScore}, endFrame: {endFrame}")

        wi = WorkItem(start_state)
        wi.output_file = genRun.getStepRndPath(self)
        wi.output_savestate = genRun.getStepFilePath(self, f"end")
        wi.inputs = inputs + bestAttempt.inputs
        wi.outdata = []
        wf = worker.create_workfile(wi, genRun.getStepRndPath(self))
        result = worker.process_workfile_sync(wf)

        section = TasSection(self.name, start_state, wi.output_savestate, wi.inputs)
        return section