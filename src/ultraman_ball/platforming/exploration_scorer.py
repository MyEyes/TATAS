import math
from .decodeHelper import DecodeHelper
from ..ultraman_consts import ULTRAMAN_CONSTS
class ExplorationScorer:
    def __init__(self, frameCost=2, exploreBonus = 10, granularity=64):
        self.frameCost = frameCost
        self.exploreBonus = exploreBonus
        self.levelBeatScore = 65536*2
        self.granularity = granularity
        self.dimX = 128
        self.dimY = 128
        self.state = bytearray(self.dimX*self.dimY)

    def scoreResult(self, result):
        positions = DecodeHelper.positionsFromResult(result)
        for frame, d in enumerate(result.data[ULTRAMAN_CONSTS.ADDR_GAME_STATE]):
            if d == 9: #State of beating level
                return self.levelBeatScore - frame*self.frameCost, frame
        return self.score(positions)

    def copyState(self, oldState, oldDimX):
        #Column length only changes when we change x dimension
        if oldDimX != self.dimX:
            for y in range(oldDimX):
                self.state[y*self.dimX:y*self.dimX+oldDimX] = oldState[y*oldDimX:(y+1)*oldDimX]
        else:
            self.state[:len(oldState)] = oldState

    def grow(self, growX=False, growY=False):
        if growX:
            oldstate = self.state
            self.dimX *= 2
            self.state = bytearray(self.dimX*self.dimY)
            self.copyState(oldstate, self.dimX//2)
        if growY:
            oldstate = self.state
            self.dimY *= 2
            self.state = bytearray(self.dimX*self.dimY)
            self.copyState(oldstate, self.dimX)

    def clean(self):
        for i in range(len(self.state)):
            self.state[i] = 0

    def scorePositionDirect(self, x, y):
        while x >= self.dimX:
            self.grow(growX=True, growY=False)
        while y >= self.dimY:
            self.grow(growX=False, growY=True)
        oldVal = self.state[y*self.dimX+x]
        self.state[y*self.dimX+x] = 1
        return self.exploreBonus if oldVal == 0 else 0

    def scorePosition(self, position, delta):
        bonus = 0
        for dx in range(-delta, delta+1, delta):
            for dy in range(-delta, delta+1, delta):
                bonus += self.scorePositionDirect(int((position[0]+dx)/self.granularity), int((position[1]+dy)/self.granularity))
        return bonus


    def score(self, positions):
        self.clean()
        score = 0
        minVal = 1<<31
        maxVal = 0
        maxFrame = -1
        for i, p in enumerate(positions):
            x = p[0]
            y = p[1]
            score += self.scorePosition(p, self.granularity)
            score -= self.frameCost
            if score > maxVal:
                maxVal = score
                maxFrame = i
        return maxVal, maxFrame