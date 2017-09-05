# -*- coding: utf-8 -*-

import os
from datetime import datetime


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


def get_segment_video(seg_size):
    """
    rtsp経由でseg_size秒のts動画を取得
    """
    command = "ffmpeg -i http://{0}:{1}@{2}/cgi-bin/mjpeg \
    -loglevel quiet \
    -vcodec copy \
    -map 0 \
    -f segment \
    -segment_format mpegts \
    -segment_time {3} \
    -segment_list  {4}/live.m3u8 \
    {4}/%d.ts".format(
        movie_host['user'],
        movie_host['password'],
        movie_host['ip'],
        seg_size,
        data_path['ts'],
    )
    print(command)
    os.system(command)


def get_image():
    """
    rtsp経由で画像を一枚取得
    """

    command = "ffmpeg -i http://{0}:{1}@{2}/cgi-bin/mjpeg \
    -vframes 1 \
    {3}/{4}.jpg".format(
        movie_host['user'],
        movie_host['password'],
        movie_host['ip'],
        data_path['jpg'],
        str(datetime.now())
    )
    print(command)
    os.system(command)


def encode(file_path):
    codec = 'libx264'
    bitrate = ['3000k', '3000k', '3000k']
    framerate = 30

    command = "ffmpeg -i {0} \
    -loglevel quiet \
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
    print(command)
    os.system(command)
