class WorkItem:
    def __init__(self, start_state):
        self.start_state = start_state
        self.output_file = ""
        self.output_savestate = ""
        self.output_movie = ""
        self.outdata = []
        self.inputs = []