# -*- coding: utf-8 -*-

import os
import subprocess
from datetime import datetime
from logging import getLogger, FileHandler, StreamHandler, DEBUG
logger = getLogger(__name__)
if not logger.handlers:
    fileHandler = FileHandler(r'./log/capture.log')
    fileHandler.setLevel(DEBUG)
    streamHander = StreamHandler()
    streamHander.setLevel(DEBUG)
    logger.setLevel(DEBUG)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHander)

movie_host = {
    'ip': os.getenv('SSS_WEBCAM_HOST'),
    'user': os.getenv('SSS_WEBCAM_USER'),
    'password': os.getenv('SSS_WEBCAM_PASS')
}

data_path = {
    'ts': './data/ts',
    'jpg': './data/jpg',
    'mp4': './data/mp4'
}

##############
## added by k.k

cloud_path = {
    'port': os.getenv('SSS_CLOUD_PORT'),
    'user': os.getenv('SSS_CLOUD_USER'),
    'dir': os.getenv('SSS_CLOUD_DIR')
}
#############

def get_segment_video(seg_size):
    """
    rtsp経由でseg_size秒のts動画を取得
    """

    process = subprocess.Popen([
        'ffmpeg',
        '-f', 'mjpeg',
        '-i',"http://{0}:{1}@{2}/cgi-bin/mjpeg".format(movie_host['user'], movie_host['password'], movie_host['ip']),
        '-loglevel', 'warning',
        '-vcodec', 'copy',
        "{0}/{1}.avi".format(data_path['ts'], datetime.now().isoformat())
    ])
    try:
        process.wait(timeout=seg_size)
    except subprocess.TimeoutExpired:
        process.kill()

    #command = "ffmpeg -f mjpeg -i http://{0}:{1}@{2}/cgi-bin/mjpeg \
    #-loglevel info \
    #-vcodec copy \
    #{4}/{6}.avi".format(
    #    movie_host['user'],
    #    movie_host['password'],
    #    movie_host['ip'],
    #    seg_size,
    #    data_path['ts'],
    #    seg_size,
    #    datetime.now().isoformat()
    #)
    #print(command)
    #os.system(command)


def get_image():
    """
    rtsp経由で画像を一枚取得
    """
    ###################
    ## modified by k.k
    curTime = datetime.now().isoformat()

    command = "ffmpeg -i http://{0}:{1}@{2}/cgi-bin/mjpeg \
    -vframes 1 -loglevel warning \
    {3}/{4}.jpg".format(
        movie_host['user'],
        movie_host['password'],
        movie_host['ip'],
        data_path['jpg'],
	curTime
    )

    ####
    #command = "ffmpeg -i http://{0}:{1}@{2}/cgi-bin/mjpeg \
    #-vframes 1 -loglevel warning \
    #{3}/{4}.jpg".format(
    #    movie_host['user'],
    #    movie_host['password'],
    #    movie_host['ip'],
    #    data_path['jpg'],
    #    datetime.now().isoformat()
    #)
    ####

    logger.info(command)
    os.system(command)

    # after capturing image, upload to server
    upload_img(curTime)


def encode(file_path):
    codec = 'libx264'
    bitrate = ['3000k', '3000k', '3000k']
    framerate = 30

    command = "ffmpeg -i {0} \
    -loglevel warning \
    -vcodec {1} \
    -b:v {2} \
    -map 0:0 \
    {3}/{4}".format(
        file_path,
        codec,
        bitrate[0],
        data_path['mp4'],
        os.path.splitext(os.path.basename(file_path))[0] + '.mp4'
    )
    logger.info(command)
    os.system(command)


###################
## added by k.k

def upload_img(file_path):
    key = '~/.ssh/kattolab_controll_pc_id_rsa'
    dst = '10.0.0.11'

    command = "scp -i {0} {1}/{2}.jpg kattolab@10.0.0.11:~/ && ssh kattolab@10.0.0.11 -i {0} './ftput.sh ./{2}.jpg && rm -f ./{2}.jpg'".format(
        		key,
        		data_path['jpg'],
        		file_path
    )
    logger.info(command)
    os.system(command)
	

			
			
