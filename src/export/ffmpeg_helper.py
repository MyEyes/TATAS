import os

class FFMpegHelper:
    @classmethod
    def AddBottomText(cls, text, inVid, outVid, font="monospace", fontsize=16):
        cmd = f"ffmpeg -y -i {inVid} -vf \"drawtext=font={font}:fontsize={fontsize}:fontcolor=white:x=0:y=(h-text_h):box=1:boxcolor=black@0.8:boxborderw=5:text='{text}'\" {outVid} 2>/dev/null"
        os.system(cmd)

    @classmethod
    def TextToVideo(cls, text, outVid, duration=3, font="monospace", fontsize=30):
        cmd = f"ffmpeg -y -f lavfi -i color=size=166x140:duration={duration}:rate=25:color=black -vf \"drawtext=font={font}:fontsize={fontsize}:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:text='{text}'\" {outVid} 2>/dev/null"
        os.system(cmd)

