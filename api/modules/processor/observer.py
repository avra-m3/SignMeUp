import os
from threading import Thread

from modules.objects import PATHS


def watch():
    proc_list = []
    while True:
        for file in os.listdir(PATHS.QUEUED):
            path = os.path.join(PATHS.QUEUED, file)
            type = file.rsplit(".", 1)[-1].lower()
            ctime = os.path.getctime(path)
            def run():
                pass

            thread = Thread(run)
