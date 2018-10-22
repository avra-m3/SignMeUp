import os
import time
from threading import Thread

from modules.path_constants import PATHS
from modules.observer.controller import process


def watch():
    """
    Watch the queue directory for newly created files.
    :return: Shouldn't
    """
    # Dictionary of files currently processing; key is file name
    proc_list = {}
    while True:
        files = os.listdir(PATHS.QUEUED)
        # Process files not in proc_list
        for file in [l for l in files if l not in proc_list.keys()]:
            path = os.path.join(PATHS.QUEUED, file)
            extension = file.rsplit(".", 1)[-1].lower()
            ctime = os.path.getctime(path)

            print("Picked up {} for processing".format(file))

            # We thread this to ensure unexpected exceptions don't flow back to us
            thread = Thread(target=process, args=[path, file])

            proc_list[file] = (path, extension, ctime, thread)
            thread.start()

        # Remove all items in proc_list where k is no longer in the directory OR the thread is marked as dead.
        [proc_list.pop(k) for k in list(proc_list.keys()) if k not in files]

        # Lets avoid taking up too much cpu time
        time.sleep(1)
