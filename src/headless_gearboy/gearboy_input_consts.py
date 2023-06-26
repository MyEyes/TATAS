class INPUT:
    A_Key = 1<<4
    B_Key = 1<<5
    Start_Key = 1<<7
    Select_Key = 1<<6
    Right_Key = 1<<0
    Left_Key = 1<<1
    Up_Key = 1<<2
    Down_Key = 1<<3
    No_Input = 0

    @classmethod
    def asBytes(cls, pressed):
        return b""+bytes([pressed])