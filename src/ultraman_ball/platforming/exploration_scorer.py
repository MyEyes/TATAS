import math
from .decodeHelper import DecodeHelper
from ..ultraman_consts import ULTRAMAN_CONSTS
class ExplorationScorer:
    def __init__(self, frameCost=2, exploreBonus = 10, granularity=64):
        self.frameCost = frameCost
        self.exploreBonus = exploreBonus
        self.levelBeatScore = 65536*2
        self.granularity = granularity

    def scoreResult(self, result):
        positions = DecodeHelper.positionsFromResult(result)
        for frame, d in enumerate(result.data[ULTRAMAN_CONSTS.ADDR_GAME_STATE]):
            if d == 9: #State of beating level
                return self.levelBeatScore - frame*self.frameCost, frame
        return self.score(positions)

    def scorePosition(self, position, state, delta):
        bonus = 0
        for dx in range(-delta, delta+1, delta):
            for dy in range(-delta, delta+1, delta):
                pos = (position[0]+dx, position[1]+dy)
                posSlot = (int(pos[0]/self.granularity), int(pos[1]/self.granularity))
                if posSlot not in state:
                    state[posSlot] = True
                    bonus += self.exploreBonus
        return bonus


    def score(self, positions):
        score = 0
        minVal = 1<<31
        maxVal = 0
        maxFrame = -1
        state = {}
        for i, p in enumerate(positions):
            x = p[0]
            y = p[1]
            pos = (x,y)
            score += self.scorePosition(pos, state, self.granularity)
            score -= self.frameCost
            if score > maxVal:
                maxVal = score
                maxFrame = i
        return maxVal, maxFrame