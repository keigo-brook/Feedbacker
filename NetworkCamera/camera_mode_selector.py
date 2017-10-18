# -*- coding: utf-8 -*-

import capture
import threading
import time
from logging import getLogger, FileHandler, StreamHandler, DEBUG

logger = getLogger(__name__)
if not logger.handlers:
    fileHandler = FileHandler(r'./log/mode_selector.log')
    fileHandler.setLevel(DEBUG)
    streamHander = StreamHandler()
    streamHander.setLevel(DEBUG)
    logger.setLevel(DEBUG)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHander)

t = None

def change_mode(event):
    """
    input: { "event": 0L }
    0: 定常状態→1時間に1回jpgを取得
    1: 注意報→5分に1回jpgを取得
    2: 警報→60秒の動画を取得
    """

    # 前のイベントのスレッドをキャンセル
    global t
    if t is not None:
        t.stop()
        t = None

    # 新しいイベントのスレッドを開始
    t = CameraMode(event)


class CameraMode():
    def __init__(self, mode_num):
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.get_mode(mode_num))
        self.thread.daemon = True
        self.thread.start()


    def stop(self):
        self.stop_event.set()
        self.thread.join()


    def get_mode(self, mode_num):
        if mode_num == 0:
            logger.info("Node: {0}".format(mode_num))
            return self.normal_mode
        elif mode_num == 1:
            logger.info("Node: {0}".format(mode_num))
            return self.caution_mode
        elif mode_num == 2:
            logger.info("Node: {0}".format(mode_num))
            return self.alert_mode
        else:
            logger.info("Unknown mode: {0}".format(mode_num))
            return self.normal_mode


    def normal_mode(self):
        count = 0
        while not self.stop_event.is_set():
            if count == 0:
                capture.get_image()

            time.sleep(1)
            count += 1
            if count == 60*60:
                count = 0


    def caution_mode(self):
        count = 0
        while not self.stop_event.is_set():
            if count == 0:
                capture.get_image()

            time.sleep(1)
            count += 1
            if count == 60*5:
                count = 0


    def alert_mode(self):
        count = 0
        while not self.stop_event.is_set():
            capture.get_segment_video(60)
