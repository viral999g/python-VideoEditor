import json
from flask import Flask, request, Response, render_template, flash, redirect, url_for, session, logging, send_from_directory
from functools import wraps
from io import StringIO
from itsdangerous import URLSafeTimedSerializer
import datetime
import time
from bson.objectid import ObjectId
import os
import re
from flask import Flask
from werkzeug.utils import secure_filename
import moviepy.editor as mp
import imageio
import cv2
from flask import send_file
from PIL import Image
import imagehash
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

PROJECT_PATH = "/home/bharat/Downloads/videoEditor"

# UPLOAD_FOLDER = '/user_banners'
UPLOAD_FOLDER = PROJECT_PATH+'/user_banners/'
ALLOWED_EXTENSIONS = set(['.png', '.jpg', '.jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/upload_banner", methods = ["GET", "POST"])
def process_file():
    if request.method == 'POST':
        obj = {}
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            error_obj = {}
            error_obj["error"] = "Image not selected"
            resp = Response(json.dumps(error_obj, separators=(',',':')))
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        file = request.files['file']

        videos = []
        videos_links = []

        print(request.form)
        for i in request.form:
            videos.append(i)

        v = videos[0]
                
        # if file.filename == '':
        #     error_obj = {}
        #     error_obj["error"] = "Image not selected"
        #     resp = Response(json.dumps(error_obj, separators=(',',':')))
        #     resp.headers['Access-Control-Allow-Origin'] = '*'
        #     return resp

        # filename, file_extension = os.path.splitext(file.filename)
        # # print(file_extension)
        # if file and file_extension in ALLOWED_EXTENSIONS:
        #     filename = secure_filename(file.filename)
        #     filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        #     print(filepath)
        #     file.save(filepath)
        #     print(file, filename, filepath)

        # video_path = PROJECT_PATH+"/videos/" + v + ".mp4"
        
        # video = mp.VideoFileClip(video_path)
        # # print(duration)

        # width, height = video.size
        # # width = 1280
        # img_height = 180
        # # video.resize(height = 150)

        # # print(filename)

        # img = cv2.imread(UPLOAD_FOLDER + filename)
        # name, extention = os.path.splitext(filename)

        # img_height, img_width, channels = img.shape 

        # hash = str(imagehash.average_hash(Image.open(UPLOAD_FOLDER + filename)))
        # # print(hash)
        # new_filename = hash + "_" + v + extention
        # video_filename = new_filename.replace(extention, "") + ".mp4"
        # video_banner_fp = PROJECT_PATH + "/user_videos/" + video_filename

        # if os.path.isfile(video_banner_fp):
        #     obj[video_filename] = video_banner_fp
        #     resp = Response(json.dumps(obj, separators=(',',':')))
        #     resp.headers['Access-Control-Allow-Origin'] = '*'
        #     return resp

        # ratio = width / img_width

        # resized_img = cv2.resize(img,(width, int(img_height * ratio)))
        # cv2.imwrite(UPLOAD_FOLDER + new_filename ,resized_img)
        # # Make the text. Many more options are available.
        # logo = (mp.ImageClip(UPLOAD_FOLDER + new_filename)
        #         .set_duration(video.duration)
        #         .resize(height=180)
        #         #  .resize(width=400)
        #         #  .margin(right=4, top=8, opacity=0) # (optional) logo-border padding 
        #         .set_pos(("left","bottom"))) 
        # final = mp.clips_array([[video], [logo]])

        # final.write_videofile(video_banner_fp)

        # videos_links.append(video_banner_fp)

        # obj[video_filename] = video_banner_fp

        # resp = Response(json.dumps(obj, separators=(',',':')))
        # resp.headers['Access-Control-Allow-Origin'] = '*'

        # return resp

if __name__ == '__main__':
	app.secret_key = 'mysecret'
	app.run(host= '0.0.0.0', port=8100,debug=True)