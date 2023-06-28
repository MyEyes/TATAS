import logging
class TasInfo:
    def __init__(self, name="TATAS Generated TAS", author="firzen", version="1.0", rerecordCount=0, cycleCount=0, platform="GB", gamename="Unknown", SHA1="", Core="Gambatte"):
        self.name = name
        self.author = author
        self.version = version
        self.rerecordCount = rerecordCount
        self.cycleCount = cycleCount
        self.platform = platform
        self.gamename = gamename
        self.SHA1 = SHA1,
        self.Core = Core

class Tas:
    def __init__(self, sections):
        self.sections = sections
        self.genSectionSubtitles = False
        self.info = TasInfo()
        self.logger = logging.getLogger('TATAS.Tas')

    def setInfo(self, tasInfo):
        self.info = tasInfo

    def logInfo(self):
        self.logger.info("====TAS INFO====")
        self.logger.info("Sections:")
        totalFrames = 0
        for i,s in enumerate(self.sections):
            self.logger.info(f"\t{i}: {s}")
            totalFrames += len(s.inputs)
        self.logger.info(f"Total Length: {totalFrames} frames")
