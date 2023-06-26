from .gambatte_input_writer import GambatteInputWriter
core_writers = {
    'Gambatte': GambatteInputWriter()
}

def getInputWriterForCore(core):
    global core_writers
    if core in core_writers:
        return core_writers[core]
    raise Exception(f"No Input Writer for Core {core}")