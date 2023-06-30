from ..ultraman_consts import ULTRAMAN_CONSTS
class DecodeHelper:
    @classmethod
    def positionsFromResult(cls, result):
        positions = []
        for i in range(len(result.data[ULTRAMAN_CONSTS.ADDR_POSX])):
            x = result.data[ULTRAMAN_CONSTS.ADDR_POSX][i] + (result.data[ULTRAMAN_CONSTS.ADDR_POSX2][i]<<8)
            y = result.data[ULTRAMAN_CONSTS.ADDR_POSY][i] + (result.data[ULTRAMAN_CONSTS.ADDR_POSY2][i]<<8)
            positions.append((x,y))
        return positions