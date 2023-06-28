class INPUT:
    # enum Button { A     = 0x01, B    = 0x02, SELECT = 0x04, START = 0x08,
	#               RIGHT = 0x10, LEFT = 0x20, UP     = 0x40, DOWN  = 0x80 };
    A_Key = 0x01
    B_Key = 0x02
    Start_Key = 0x08
    Select_Key = 0x04
    Right_Key = 0x10
    Left_Key = 0x20
    Up_Key = 0x40
    Down_Key = 0x80
    No_Input = 0

    @classmethod
    def asBytes(cls, pressed):
        return b""+bytes([pressed])