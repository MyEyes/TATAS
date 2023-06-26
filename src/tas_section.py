class TasSection:
    def __init__(self, name, start_state, end_state, inputs):
        self.name = name
        self.inputs = inputs
        self.start_state = start_state
        self.end_state = end_state

    def __repr__(self):
        start = self.start_state
        if len(start) == 0:
            start = "<rom start>"
        return f"[Section | {self.name} | {start}->{self.end_state} | {len(self.inputs)} Frames]"