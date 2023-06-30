from ..tas_generation_step import TasGenerationStep
from ..tas_generation_run import TasGenerationRun
from ..tas_section import TasSection
from .ultraman_consts import ULTRAMAN_CONSTS, INPUT
from ..workitem import WorkItem

class UB_EnterFirstLevelStep(TasGenerationStep):
    def __init__(self):
        super().__init__("Ultraman Ball - Enter First Level Step", "efl")

    def find_next_start_press(self, genRun, start_state):
        worker = genRun.workQueue
        first_start = -1
        no_input = INPUT.asBytes(INPUT.No_Input)
        start_press = INPUT.asBytes(INPUT.Start_Key)
        for i in range(100):
            wi = WorkItem(start_state)
            wi.output_file = genRun.getStepRndPath(self, tmp=True)
            wi.inputs = no_input*i + start_press + no_input*10
            wi.outdata = [ULTRAMAN_CONSTS.ADDR_GAME_STATE]
            wf = worker.create_workfile(wi, genRun.getStepRndPath(self, tmp=True))
            result = worker.process_workfile_sync(wf)

            for f, s in enumerate(result.data[ULTRAMAN_CONSTS.ADDR_GAME_STATE]):
                if s == 16: #State of showing level preview
                    first_start = i
                    end_frame = f
                    break
            if first_start >= 0:
                break
        self.logger.info(f"Pressing start at frame {first_start}, entering level preview at frame {end_frame}")
        wi = WorkItem(start_state)
        wi.output_file = genRun.getStepRndPath(self, tmp=True)
        wi.output_savestate = genRun.getStepFilePath(self, "efl_end")
        wi.inputs = bytearray(no_input*end_frame)
        wi.inputs[first_start] = INPUT.Start_Key
        wi.outdata = []
        wf = worker.create_workfile(wi, genRun.getStepRndPath(self, tmp=True))
        result = worker.process_workfile_sync(wf)
        return wi.output_savestate, wi.inputs

    def generate(self, genRun:TasGenerationRun, prevStep, prevSection):
        start_state = prevSection.end_state
        preview_state, inputs = self.find_next_start_press(genRun, start_state)

        section = TasSection(self.name, start_state, preview_state, inputs)
        return section