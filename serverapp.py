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
import glob
from pytube import YouTube


app = Flask(__name__, static_folder='static')
CORS(app)

PROJECT_PATH = "/volume2/www/html/videoEditor"

# UPLOAD_FOLDER = '/user_banners'
UPLOAD_FOLDER = PROJECT_PATH+'/user_banners/'
ALLOWED_EXTENSIONS = set(['.png', '.jpg', '.jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/upload_banner", methods = ["GET", "POST"])
def process_file():
    if request.method == 'POST':
        image_name = None
        local_filepath = None
        local_filepaths = []
        obj = {}
        error_obj = {}
        # check if the post request has the file part
        image_inserver = False

        print(request.form)
        for i in request.form:
            if "video" in i:
                v = i.split("_")[1]
            elif "img" in i:
                image_hash = i.split("_")[1]         

        videos = []
        videos_links = []

       

        # if 'file' not in request.files or image_name == None:
        #     print('No file part')
        #     error_obj = {}
        #     error_obj["error"] = "Image not selected"
        #     resp = Response(json.dumps(error_obj, separators=(',',':')))
        #     resp.headers['Access-Control-Allow-Origin'] = '*'
        #     return resp

        #     # print "Found"

        # filename, file_extension = os.path.splitext(file.filename)
        # # print(file_extension)
        # if file and file_extension in ALLOWED_EXTENSIONS:
        #     filename = secure_filename(file.filename)
        #     filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        #     print(filepath)
        #     file.save(filepath)
        #     print(file, filename, filepath)

        try:
            file = request.files['file']
            print(file)
            name, extention = os.path.splitext(file.filename)

            # filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'],image_hash + extention)
            print(filepath)
            file.save(filepath)
            # print(file, filename, filepath)
            local_filepath = filepath

        except:
            # local_filename = glob.glob(UPLOAD_FOLDER + image_hash + ".*")
            local_filepaths = glob.glob(UPLOAD_FOLDER + image_hash + ".*")

        # print(local_filename)
            if len(local_filepaths) == 0 :
                error_obj["error"] = "Image not selected"
                resp = Response(json.dumps(error_obj, separators=(',',':')))
                resp.headers['Access-Control-Allow-Origin'] = '*'
                return resp
            else:
                local_filepath = local_filepaths[0]
        
        video_path = PROJECT_PATH+"/videos/" + v + ".mp4"

        try:  
            video = mp.VideoFileClip(video_path)
        except:
            print("Downloading video " + v)
            youtube_url = "https://www.youtube.com/embed/" + v
            YouTube(youtube_url).streams.first().download(filename=v, output_path= PROJECT_PATH + "/videos/")
            video = mp.VideoFileClip(video_path)

        # print(duration)

        width, height = video.size
        # width = 1280
        img_height = 180
        # video.resize(height = 150)

        # print(filename)

        img = cv2.imread(local_filepath)
        img_height, img_width, channels = img.shape 


        # hash = str(imagehash.average_hash(Image.open(UPLOAD_FOLDER + filename)))
        # print(hash)
        # new_filename = image_name + extention
        video_filename = image_hash + "_" + v + ".mp4"
        video_banner_fp = PROJECT_PATH + "/user_videos/" + video_filename

        if os.path.isfile(video_banner_fp):
            obj[video_filename] = video_banner_fp
            resp = Response(str("http://52.14.227.128/videoEditor/user_videos/" + video_filename))
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp

        
        ratio = width / img_width 
        resized_img = cv2.resize(img,(width,int(img_height * ratio)))
        # print(Image ori widt)
        print(img_height)
        print(img_width)

        print(height)
        print(width)

        print(ratio)
        print(img_height * ratio)

        cv2.imwrite(local_filepath ,resized_img)
        # Make the text. Many more options are available.
        logo = (mp.ImageClip(local_filepath)
                .set_duration(video.duration)
                #  .resize(width=400)
                #  .margin(right=4, top=8, opacity=0) # (optional) logo-border padding 
                .set_pos(("left","bottom"))) 
        final = mp.clips_array([[video], [logo]])

        final.write_videofile(video_banner_fp, write_logfile=True)

        obj[video_filename] = "http://52.14.227.128/videoEditor/user_videos/" + video_filename

        resp = Response(str("http://52.14.227.128/videoEditor/user_videos/" + video_filename))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        # print(resp)

        return resp

@app.route("/get_log", methods = ["GET", "POST"])
def get_log():
    if request.method == 'POST':
        current_status = 0
        try:
            video_id = request.json["video_id"]
            video_path = PROJECT_PATH + "/user_videos/" + video_id + ".mp4.log"

            original_video_id = video_id.split("_")[1]

            video = mp.VideoFileClip(PROJECT_PATH + "/videos/" + original_video_id + ".mp4")
            frames = int(video.duration * video.fps)
        
            log_file = open(video_path, "r")
            logs = []

            for f in log_file:
                if "frame= " in f:
                    logs.append(f.replace("\n", ""))

            log = logs[-1]
            start_point = log.find("=")
            end_point = log.find("fps")
            current_frames = int(log[start_point + 1: end_point].strip())

            current_status = (current_frames / frames) * 100
            print(current_frames)
            print(frames)

            print(current_status)
        except:
            resp = Response(str(0))
            resp.headers['Access-Control-Allow-Origin'] = '*'

            return resp


    resp = Response(str(current_status))
    resp.headers['Access-Control-Allow-Origin'] = '*'

    time.sleep(2)

    return resp

    

if __name__ == '__main__':
	app.secret_key = 'mysecret'
	app.run(host= '0.0.0.0', port=8100,debug=True,threaded=True)