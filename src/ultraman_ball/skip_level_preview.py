from ..tas_generation_step import TasGenerationStep
from ..tas_generation_run import TasGenerationRun
from ..tas_section import TasSection
from .ultraman_consts import ULTRAMAN_CONSTS, INPUT
from ..workitem import WorkItem

class UB_SkipLevelPreviewStep(TasGenerationStep):
    def __init__(self, suffix=""):
        super().__init__("Ultraman Ball - Skip Level Preview "+suffix, "slp"+suffix)

    def find_a_b_press(self, genRun, start_state):
        worker = genRun.workers[0]
        first_a = -1
        first_b = -1
        no_input = INPUT.asBytes(INPUT.No_Input)
        a_press = INPUT.asBytes(INPUT.A_Key)
        b_press = INPUT.asBytes(INPUT.B_Key)
        for b in range(100):
            for a in range(b):
                wi = WorkItem(start_state)
                wi.output_file = genRun.getStepRndPath(self)
                wi.inputs = bytearray(no_input*(b+70))
                wi.inputs[a] = INPUT.A_Key
                wi.inputs[b] = INPUT.B_Key
                wi.outdata = [ULTRAMAN_CONSTS.ADDR_GAME_STATE]
                wf = worker.create_workfile(wi, genRun.getStepRndPath(self))
                result = worker.process_workfile_sync(wf)

                for f, s in enumerate(result.data[ULTRAMAN_CONSTS.ADDR_GAME_STATE]):
                    if s == 4: #State of playing level
                        first_a = a
                        first_b = b
                        end_frame = f
                        break
                if first_a >= 0:
                    break
        self.logger.info(f"Pressing a at frame {first_a}, pressing b at frame {first_b}, entering level at frame {end_frame}")
        wi = WorkItem(start_state)
        wi.output_file = genRun.getStepRndPath(self)
        wi.output_savestate = genRun.getStepFilePath(self, "slp_end")
        wi.inputs = bytearray(no_input*end_frame)
        wi.inputs[first_a] = INPUT.A_Key
        wi.inputs[first_b] = INPUT.B_Key
        wi.outdata = []
        wf = worker.create_workfile(wi, genRun.getStepRndPath(self))
        result = worker.process_workfile_sync(wf)
        return wi.output_savestate, wi.inputs

    def generate(self, genRun:TasGenerationRun, prevStep, prevSection):
        start_state = prevSection.end_state
        level_state, inputs = self.find_a_b_press(genRun, start_state)

        section = TasSection(self.name, start_state, level_state, inputs)
        return section