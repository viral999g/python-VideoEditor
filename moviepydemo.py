import moviepy.editor as mp
import imageio
import cv2
# imageio.plugins.ffmpeg.download()

video = mp.VideoFileClip("sample.mp4").subclip(5, 10)
duration = video.duration
print(duration)
width, height = video.size
# width = 1280
img_height = 150
video.resize((width, height - 150)).margin(bottom=150, left=0, right=0,top=0)

img = cv2.imread('banner.jpeg')

resized_img = cv2.resize(img,(width,img_height))
cv2.imwrite("rebanner.jpg",resized_img)
# Make the text. Many more options are available.
logo = (mp.ImageClip("rebanner.jpg")
         .set_duration(video.duration)
         .resize(height=150)
        #  .resize(width=400)
        #  .margin(right=4, top=8, opacity=0) # (optional) logo-border padding 
         .set_pos(("left","bottom"))) 
final = mp.CompositeVideoClip([video, logo]) 
final.write_videofile("test.mp4")

# video.to_gif("samplegif.gif")