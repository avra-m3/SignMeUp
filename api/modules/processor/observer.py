import os
import time
from threading import Thread

from modules.objects import PATHS
from modules.processor.tools import begin_processing, process


def watch():
    proc_list = {}
    seen = []
    while True:
        for file in os.listdir(PATHS.QUEUED):
            if file in proc_list:
                seen.append(file)
                continue
            path = os.path.join(PATHS.QUEUED, file)
            type = file.rsplit(".", 1)[-1].lower()
            ctime = os.path.getctime(path)

            def run():
                process(path, file)

            thread = Thread(target=run)
            proc_list[file] = (path, type, ctime, thread)

            thread.start()
        [proc_list.pop(k) for k in proc_list if k not in seen]
        time.sleep(1)
