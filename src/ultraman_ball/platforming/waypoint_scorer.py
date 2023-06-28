class WaypointScorer:
    def __init__(self, waypoints):
        self.waypoints = waypoints

    def score(self, positions):
        baseScore = 0x10000
        frameCost = 2
        minVal = 1<<31
        maxVal = 0
        maxFrame = -1
        currWaypoint = 0
        for i, p in enumerate(positions):
            x = p[0]
            y = p[1]
            tgt = self.waypoints[currWaypoint]
            dist = math.sqrt((tgt[0]-x)**2 + (tgt[1]-y)**2)
            score = baseScore - dist - i * frameCost
            if score > maxVal:
                maxVal = score
                maxFrame = i
        return maxVal, maxFrame