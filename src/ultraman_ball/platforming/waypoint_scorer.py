import math
from .decodeHelper import DecodeHelper
from ..ultraman_consts import ULTRAMAN_CONSTS
class WaypointScorer:
    def __init__(self, waypoints, frameCost=2):
        self.waypoints = waypoints
        self.frameCost = frameCost

    def scoreResult(self, result):
        positions = DecodeHelper.positionsFromResult(result)
        factor = 1
        for d in result.data[ULTRAMAN_CONSTS.ADDR_GAME_STATE]:
            if d == 9: #State of beating level
                factor = 2
        score, frame = self.score(positions)
        return score*factor, frame

    def score(self, positions):
        baseScore = 0x10000
        minVal = 1<<31
        maxVal = 0
        maxFrame = -1
        currWaypoint = 0
        for i, p in enumerate(positions):
            x = p[0]
            y = p[1]
            tgt = self.waypoints[currWaypoint]
            dist = math.sqrt((tgt[0]-x)**2 + (tgt[1]-y)**2)
            score = baseScore - dist - i * self.frameCost
            if score > maxVal:
                maxVal = score
                maxFrame = i
        return maxVal, maxFrame