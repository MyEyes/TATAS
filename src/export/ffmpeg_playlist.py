import os
class FFMpegPlaylist:
    def __init__(self, path, buildpath):
        self.playlistPath = path
        self.buildPath = buildpath
        self.videos = []

    def addVideo(self, videoPath):
        self.videos.append(videoPath)

    def genBuildfile(self):
        with open(self.buildPath,"w") as f:
            f.write("ffconcat version 1.0\n")
            for v in self.videos:
                f.write(f"file {v}\n")

    def commit(self):
        self.genBuildfile()
        os.replace(self.buildPath, self.playlistPath)