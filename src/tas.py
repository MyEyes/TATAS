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

    def setInfo(self, tasInfo):
        self.info = tasInfo