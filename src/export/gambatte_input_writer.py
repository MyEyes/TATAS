from .inputWriter import InputWriter
from ..headless_gearboy.gearboy_input_consts import INPUT
class GambatteInputWriter(InputWriter):
    def __init__(self):
        pass

    #[Input]
    #LogKey:#Up|Down|Left|Right|Start|Select|B|A|Power|
    def writeByteAsInputLine(self, inputFile, inputByte):
        inputFile.write("|") #Input line start marker
        inputFile.write("U" if inputByte & INPUT.Up_Key != 0 else ".")
        inputFile.write("D" if inputByte & INPUT.Down_Key != 0 else ".")
        inputFile.write("L" if inputByte & INPUT.Left_Key != 0 else ".")
        inputFile.write("R" if inputByte & INPUT.Right_Key != 0 else ".")
        inputFile.write("S" if inputByte & INPUT.Start_Key != 0 else ".")
        inputFile.write("s" if inputByte & INPUT.Select_Key != 0 else ".")
        inputFile.write("B" if inputByte & INPUT.B_Key != 0 else ".")
        inputFile.write("A" if inputByte & INPUT.A_Key != 0 else ".")
        inputFile.write(".|\n") #No Power press, input end, new line
