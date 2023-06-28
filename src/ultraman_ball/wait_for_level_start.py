from ..tas_generation_step import TasGenerationStep
from ..tas_generation_run import TasGenerationRun
from ..tas_section import TasSection
from .ultraman_consts import ULTRAMAN_CONSTS, INPUT
from ..workitem import WorkItem

class UB_WaitForLevelStartStep(TasGenerationStep):
    def __init__(self, suffix=""):
        self.level = suffix
        super().__init__("Ultraman Ball - WaitForLevelStart "+suffix, "wls_"+suffix)

    def find_first_level_frame(self, genRun, start_state):
        worker = genRun.workers[0]
        no_input = INPUT.asBytes(INPUT.No_Input)

        wi = WorkItem(start_state)
        wi.output_file = genRun.getStepRndPath(self, tmp=True)
        wi.inputs = bytearray(no_input*(300))
        wi.outdata = [ULTRAMAN_CONSTS.ADDR_GAME_STATE]
        wf = worker.create_workfile(wi, genRun.getStepRndPath(self, tmp=True))
        result = worker.process_workfile_sync(wf)

        for f, s in enumerate(result.data[ULTRAMAN_CONSTS.ADDR_GAME_STATE]):
            if s == 5: #State of playing level
                end_frame = f
                break
        
        self.logger.info(f"First frame in level is {end_frame}, tas_frame: {genRun.getAbsoluteFrameNumber(end_frame)}")
        wi = WorkItem(start_state)
        wi.output_file = genRun.getStepRndPath(self, tmp=True)
        wi.output_savestate = genRun.getRunFilePath(f"{self.level}_start")
        wi.inputs = bytearray(no_input*end_frame)
        wi.outdata = []
        wf = worker.create_workfile(wi, genRun.getStepRndPath(self, tmp=True))
        result = worker.process_workfile_sync(wf)
        return wi.output_savestate, wi.inputs

    def generate(self, genRun:TasGenerationRun, prevStep, prevSection):
        start_state = prevSection.end_state
        level_state, inputs = self.find_first_level_frame(genRun, start_state)

        section = TasSection(self.name, start_state, level_state, inputs)
        return section