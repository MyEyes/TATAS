from ..tas_generation_step import TasGenerationStep
from ..tas_generation_run import TasGenerationRun
from ..tas_section import TasSection
from .ultraman_consts import ULTRAMAN_CONSTS, INPUT
from ..workitem import WorkItem
from .platforming.waypoint_scorer import WaypointScorer
from .platforming.exploration_scorer import ExplorationScorer
from .platforming.evo.generation import Generation
from ..export.ffmpeg_helper import FFMpegHelper
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
        if len(waypoints)>0:
            self.scorer = WaypointScorer(waypoints, frameCost=2)
        else:
            self.scorer = ExplorationScorer()
        self.openAttempts = []
        super().__init__("Ultraman Ball - Platforming Level "+level, level)

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

    def render_generation_stats(self, genRun, currG, numGen):
        textVid = genRun.getStepFilePath(self, f"gen_{numGen}_stats.mp4")
        title = f"Gen {numGen}"
        text = currG.getStats()
        textFile = genRun.getStepFilePath(self, f"gen_{numGen}_stats.txt")
        with open(textFile, "w") as f:
            f.write(text)
        FFMpegHelper.TextCardToVideo(title, textFile, textVid)
        genRun.addVideo(textVid)

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

        score = attempt.score
        textVid = genRun.getStepFilePath(self, f"gen_{numGen}_t.mp4")
        FFMpegHelper.AddBottomText(f"Gen {numGen} - {int(score)}", wi.output_movie, textVid)
        genRun.addVideo(textVid)

    def generate(self, genRun:TasGenerationRun, prevStep, prevSection):
        worker = genRun.workQueue
        start_state = prevSection.end_state
        level_state, inputs = self.find_first_gameplay_frame(genRun, start_state)

        currG = Generation.generateRandom(level_state, 300)
        currG.attemptsPerOrganism = 5
        generations = [currG]
        topScore = 0
        do_generations = 3

        titleCard = genRun.getStepFilePath(self, "title.mp4")
        FFMpegHelper.TextToVideo(f"Level {self.level}", titleCard)
        genRun.addVideo(titleCard)

        for i in range(do_generations):
            currG.run(genRun,self,genRun.workQueue)
            currG.scoreOrganisms(self.scorer)
            topScore = currG.sortedOrganismScores[0][1]
            self.logger.info(f"Generation {i} done. Top Score: {topScore}")
            self.render_generation_stats(genRun, currG, i)
            self.render_generation_best(genRun, currG, i)
            if i<do_generations-1:
                currG = currG.createOffspring(keepTop=25,newRandom=50,breed=250,mutate=300)
                generations.append(currG)
                genRun.clearTmpFiles()

        bestAttempt = currG.getBestAttempt()

        wi = WorkItem(start_state)
        wi.output_file = genRun.getStepRndPath(self)
        wi.output_savestate = genRun.getStepFilePath(self, f"end")
        wi.inputs = inputs + bestAttempt.inputs
        wi.outdata = []
        wf = worker.create_workfile(wi, genRun.getStepRndPath(self))
        result = worker.process_workfile_sync(wf)

        section = TasSection(self.name, start_state, wi.output_savestate, wi.inputs)
        return section