import moviepy.editor as mp
import sys
from multiprocessing import Process
import time

video_path = "/home/bharat/Downloads/videoEditor/videos/ZW3Rf6L0nA0.mp4"
video = mp.VideoFileClip(video_path)
frames = int(video.duration * video.fps)


# sys.stdout = open('/home/bharat/Downloads/videoEditor/videos/text.txt', 'a')
def write_video():
    global frames
    video.margin(bottom=150)

    video.write_videofile("/home/bharat/Downloads/videoEditor/videos/demo.mp4", write_logfile=True, verbose=False, progress_bar=False)

# write_video()

# print(frames)
proc = Process(target=write_video)
proc.start()
print("-------------------------------------")
time.sleep(2)

current_frames = 0

while frames > current_frames :
    time.sleep(1)
    file = open("/home/bharat/Downloads/videoEditor/videos/demo.mp4.log", "r")
    logs = []

    for f in file:
        if "frame= " in f:
            logs.append(f.replace("\n", ""))

    log = logs[-1]
    start_point = log.find("=")
    end_point = log.find("fps")
    current_frames = int(log[start_point + 1: end_point].strip())
    print(current_frames)

proc.join()