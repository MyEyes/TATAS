import os

class FFMpegHelper:
    @classmethod
    def AddBottomText(cls, text, inVid, outVid, font="monospace", fontsize=16):
        cmd = f"ffmpeg -y -i {inVid} -vf \"drawtext=font={font}:fontsize={fontsize}:fontcolor=white:x=0:y=(h-text_h):box=1:boxcolor=black@0.8:boxborderw=5:text='{text}'\" {outVid} 2>/dev/null"
        os.system(cmd)

    @classmethod
    def TextToVideo(cls, text, outVid, duration=3, font="monospace", fontsize=30):
        cmd = f"ffmpeg -y -f lavfi -i color=size=342x280:duration={duration}:rate=60:color=black -vf \"drawtext=font={font}:fontsize={fontsize}:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:text='{text}'\" {outVid} 2>/dev/null"
        os.system(cmd)

    @classmethod
    def TextCardToVideo(cls, title, textFile, outVid, duration=6, font="monospace", fontsize_title=30, fontsize=12):
        cmd = f"ffmpeg -y -f lavfi -i color=size=342x280:duration={duration}:rate=60:color=black -vf \"drawtext=font={font}:fontsize={fontsize_title}:fontcolor=white:x=(w-text_w)/2:y=20:text='{title}', drawtext=font={font}:fontsize={fontsize}:fontcolor=white:x=40:y=65:textfile='{textFile}'\" {outVid} 2>/dev/null"
        os.system(cmd)