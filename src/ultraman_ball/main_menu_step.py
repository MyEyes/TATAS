from ..tas_generation_step import TasGenerationStep
from ..tas_generation_run import TasGenerationRun
from ..tas_section import TasSection
from .ultraman_consts import ULTRAMAN_CONSTS, INPUT
from ..workitem import WorkItem

class UB_MainMenuStep(TasGenerationStep):
    def __init__(self):
        super().__init__("Ultraman Ball - Main Menu", "mm")

    def find_menu_start(self, genRun):
        worker = genRun.workQueue

        wi = WorkItem("")
        wi.output_savestate = genRun.getRunFilePath("initial_state")
        wi.output_file = genRun.getStepFilePath(self, "init")
        wi.inputs = b"\0"*1024
        wi.outdata = [ULTRAMAN_CONSTS.ADDR_GAME_STATE]
        wf = worker.create_workfile(wi, genRun.getStepFilePath(self, "initwork"))
        result = worker.process_workfile_sync(wf)

        menu_starts = 0
        for i, s in enumerate(result.data[ULTRAMAN_CONSTS.ADDR_GAME_STATE]):
            if s == 1:
                menu_starts = i
                break
        if menu_starts>0:
            self.logger.info(f"State becomes 1 at frame {menu_starts}")
        return menu_starts

    def create_menu_start_state(self, genRun, menu_starts):
        worker = genRun.workQueue
        wi = WorkItem("")
        wi.output_file = genRun.getStepFilePath(self, "menugen")
        wi.inputs = b"\0"*(menu_starts-1)
        wi.output_savestate = genRun.getStepFilePath(self, "menu_start")
        wi.outdata = []
        wf = worker.create_workfile(wi, genRun.getStepFilePath(self, "create_menu_state"))
        result = worker.process_workfile_sync(wf)

        self.logger.info("Created menu start state")
        return wi.output_savestate, wi.inputs

    def find_first_start_press(self, genRun, start_state):
        worker = genRun.workQueue
        first_start = -1
        no_input = INPUT.asBytes(INPUT.No_Input)
        start_press = INPUT.asBytes(INPUT.Start_Key)
        for i in range(400):
            wi = WorkItem(start_state)
            wi.output_file = genRun.getStepRndPath(self, tmp=True)
            wi.inputs = no_input*i + start_press + no_input*10
            wi.outdata = [ULTRAMAN_CONSTS.ADDR_GAME_STATE]
            wf = worker.create_workfile(wi, genRun.getStepRndPath(self, tmp=True))
            result = worker.process_workfile_sync(wf)

            for f, s in enumerate(result.data[ULTRAMAN_CONSTS.ADDR_GAME_STATE]):
                if s == 2:
                    first_start = i
                    end_frame = f
                    break
            if first_start >= 0:
                break

        self.logger.info(f"Pressing start at frame {first_start}, entering main menu at frame {end_frame}")
        wi = WorkItem(start_state)
        wi.output_file = genRun.getStepRndPath(self, tmp=True)
        wi.output_savestate = genRun.getStepFilePath(self, "mm_end")
        wi.inputs = bytearray(no_input*end_frame)
        wi.inputs[first_start] = INPUT.Start_Key
        wi.outdata = []
        wf = worker.create_workfile(wi, genRun.getStepRndPath(self, tmp=True))
        result = worker.process_workfile_sync(wf)
        return wi.output_savestate, wi.inputs

    def generate(self, genRun:TasGenerationRun, prevStep, prevSection):
        menu_starts = self.find_menu_start(genRun)
        if menu_starts == 0:
            self.logger.error(f"Couldn't find first frame where menu is open")
            return None
        menu_start_state, inputs1 = self.create_menu_start_state(genRun, menu_starts)
        menu_end_state, inputs2 = self.find_first_start_press(genRun, menu_start_state)
        section = TasSection(self.name, "", menu_end_state, inputs1+inputs2)
        return section