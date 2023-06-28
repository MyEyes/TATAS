from ..tas_generation_step import TasGenerationStep
from ..tas_generation_run import TasGenerationRun
from ..tas_section import TasSection
from .ultraman_consts import ULTRAMAN_CONSTS, INPUT
from ..workitem import WorkItem
from .platforming.waypoint_scorer import WaypointScorer
import random
import math

class Attempt:
    def __init__(self):
        self.inputs = []
        pass

class UB_PlatformingLevelStep(TasGenerationStep):
    def __init__(self, level="", waypoints=[]):
        self.level = level
        self.waypoints = waypoints
        self.scorer = WaypointScorer(waypoints)
        super().__init__("Ultraman Ball - Platforming Level "+level, level)

    def scoreAttempt(self, genRun, result):
        positions = []
        for i in range(len(result.data[ULTRAMAN_CONSTS.ADDR_POSX])):
            x = result.data[ULTRAMAN_CONSTS.ADDR_POSX][i] + (result.data[ULTRAMAN_CONSTS.ADDR_POSX2][i]<<8)
            y = result.data[ULTRAMAN_CONSTS.ADDR_POSY][i] + (result.data[ULTRAMAN_CONSTS.ADDR_POSY2][i]<<8)
            positions.append((x,y))
        
        return self.scorer.score(positions)

    def performAttempt(self, genRun, start_state, attempt):
        worker = genRun.workers[0]
        no_input = INPUT.asBytes(INPUT.No_Input)

        wi = WorkItem(start_state)
        wi.output_file = genRun.getStepRndPath(self)
        wi.inputs = attempt.inputs
        wi.outdata = [ULTRAMAN_CONSTS.ADDR_POSX,ULTRAMAN_CONSTS.ADDR_POSX2,ULTRAMAN_CONSTS.ADDR_POSY,ULTRAMAN_CONSTS.ADDR_POSY2]
        wf = worker.create_workfile(wi, genRun.getStepRndPath(self))
        result = worker.process_workfile_sync(wf)

        return self.scoreAttempt(genRun, result)

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
        worker = genRun.workers[0]
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
        wi.output_file = genRun.getStepRndPath(self)
        wi.output_savestate = genRun.getStepFilePath(self, f"start")
        wi.inputs = bytearray(no_input*end_frame)
        wi.outdata = []
        wf = worker.create_workfile(wi, genRun.getStepRndPath(self))
        result = worker.process_workfile_sync(wf)
        return wi.output_savestate, wi.inputs

    def generate(self, genRun:TasGenerationRun, prevStep, prevSection):
        worker = genRun.workers[0]
        start_state = prevSection.end_state
        level_state, inputs = self.find_first_gameplay_frame(genRun, start_state)

        bestAttempt = None
        bestScore = 0
        endFrame = 0
        i = 0
        while bestScore < 55000:
            attempt = self.genRandomAttempt(400)
            score, frame = self.performAttempt(genRun, level_state, attempt)
            #self.logger.info(f"Finished attempt {i}. Score: {score}")
            if score > bestScore:
                self.logger.info(f"Finished attempt {i}. New Best Score: {score}")
                bestAttempt = attempt
                bestScore = score
                endFrame = frame
            i+=1
        #self.logger.info(f"Best attempt score: {bestScore}, endFrame: {endFrame}")

        wi = WorkItem(start_state)
        wi.output_file = genRun.getStepRndPath(self)
        wi.output_savestate = genRun.getStepFilePath(self, f"end")
        wi.inputs = inputs + bestAttempt.inputs[:endFrame]
        wi.outdata = []
        wf = worker.create_workfile(wi, genRun.getStepRndPath(self))
        result = worker.process_workfile_sync(wf)

        section = TasSection(self.name, start_state, wi.output_savestate, wi.inputs)
        return section