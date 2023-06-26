from .tas_exporter import TasExporter
from .inputHelper import getInputWriterForCore
import zipfile
import os

class BK2Exporter(TasExporter):
    def __init__(self):
        self.tmpdir = "/tmp/bk2_export/"
        self.padding = 489

    def addHeader(self, zip, tas):
        self.headerPath = os.path.join(self.tmpdir, "Header.txt")
        with open(self.headerPath, "w") as f:
            f.write(f"MovieVersion BizHawk v2.0\n")
            f.write(f"Author {tas.info.author}\n")
            f.write(f"emuVersion 2.7.0\n")
            f.write(f"OriginalEmuVersion Version 2.7.0\n")
            f.write(f"Platform {tas.info.platform}\n")
            f.write(f"GameName {tas.info.gamename}\n")
            f.write(f"SHA1 {tas.info.SHA1}\n")
            f.write(f"BoardName MBC1 ROM\n")
            f.write(f"Core {tas.info.Core}\n")
            f.write(f"rerecordCount {tas.info.rerecordCount}\n")
            f.write(f"CycleCount {tas.info.cycleCount}\n")
            # MovieVersion BizHawk v2.0
            # Author default user
            # emuVersion Version 2.7.0
            # OriginalEmuVersion Version 2.7.0
            # Platform SGB
            # GameName Ultraman Ball (Japan)
            # SHA1 3CDFCFB1A88D0CBFEB1C7B12751409FAF69BBA02
            # BoardName MBC1 ROM
            # GB_Firmware_SGB2 93407EA10D2F30AB96A314D8ECA44FE160AEA734
            # Core Gambatte
            # rerecordCount 9246
            # CycleCount 773937224
        zip.write(self.headerPath,"Header.txt")

    def addSubtitles(self, zip, tas):
        self.subtitlePath = os.path.join(self.tmpdir, "Subtitles.txt")
        with open(self.subtitlePath, "w") as f:
            if tas.genSectionSubtitles:
                pass
            f.write("\n")            
        zip.write(self.subtitlePath,"Subtitles.txt")

    def addComments(self, zip, tas):
        self.commentPath = os.path.join(self.tmpdir, "Comments.txt")
        with open(self.commentPath, "w") as f:
            f.write("\n")            
        zip.write(self.commentPath,"Comments.txt")    

    def writeInputPadding(self, inputFile, core):
        inputWriter = getInputWriterForCore(core)
        for i in range(self.padding):
            inputWriter.writeByteAsInputLine(inputFile, 0)

    def writeSectionInput(self, inputFile, section, core):
        inputWriter = getInputWriterForCore(core)
        for i in section.inputs:
            inputWriter.writeByteAsInputLine(inputFile, i)

    def addInputs(self, zip, tas):
        self.inputPath = os.path.join(self.tmpdir, "Inputs.txt")
        with open(self.inputPath, "w") as f:
            self.writeInputPadding(f, tas.info.Core)
            for section in tas.sections:
                self.writeSectionInput(f, section, tas.info.Core)
        zip.write(self.inputPath, "Input Log.txt")

    def addSyncSettings(self, zip, tas):
        self.syncSettingsPath = os.path.join(os.path.dirname(__file__),"gambatte_sync.txt")
        zip.write(self.syncSettingsPath, "SyncSettings.json")

    def export(self, path, tas):
        os.makedirs(self.tmpdir, exist_ok=True)
        with zipfile.ZipFile(path, "w") as z:
            self.addHeader(z, tas)
            self.addSubtitles(z, tas)
            self.addComments(z, tas)
            self.addInputs(z, tas)
            self.addSyncSettings(z, tas)