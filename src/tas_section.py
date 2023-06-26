class TasSection:
    def __init__(self, name, start_state, end_state, inputs):
        self.name = name
        self.inputs = inputs
        self.start_state = start_state
        self.end_state = end_state