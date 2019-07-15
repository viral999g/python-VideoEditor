import moviepy.editor as mp
import imageio
import cv2
# imageio.plugins.ffmpeg.download()

video = mp.VideoFileClip("sample.mp4").subclip(0, 15).margin(bottom=150, left=0, right=0,top=0)
duration = video.duration
print(duration)
width, height = video.size
height = 150
img = cv2.imread('banner.jpg',cv2.IMREAD_COLOR )

resized_img = cv2.resize(img,(width,height))
cv2.imwrite("rebanner.jpg",resized_img)

# Make the text. Many more options are available.
logo = (mp.ImageClip("rebanner.jpg")
         .set_duration(video.duration)
         .resize(width=2000)
         .resize(height=150) # if you need to resize... 
         .margin(right=4, top=8, opacity=0) # (optional) logo-border padding 
         .set_pos(("center","bottom"))) 
final = mp.CompositeVideoClip([video, logo]) 
final.subclip(0, int(duration)).write_videofile("test.mp4")

# video.to_gif("samplegif.gif")