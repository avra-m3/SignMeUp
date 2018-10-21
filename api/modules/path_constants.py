import os


class PATHS:
    ROOT = os.getenv("root_proc_dir") or "./processing"
    TEMP = "{}/uploaded".format(ROOT)
    QUEUED = "{}/queue".format(ROOT)
    OUTPUT = "{}/out".format(ROOT)
    DONE = "{}/complete".format(ROOT)
    FAIL = "{}/failed".format(ROOT)

    IMAGE_FORMATS = ["png", "jpg", "jpeg", "gif"]

    @staticmethod
    def create_dirs():
        if not os.path.isdir(PATHS.ROOT):
            os.mkdir(PATHS.ROOT)
        if not os.path.isdir(PATHS.TEMP):
            os.mkdir(PATHS.TEMP)
        if not os.path.isdir(PATHS.QUEUED):
            os.mkdir(PATHS.QUEUED)
        if not os.path.isdir(PATHS.DONE):
            os.mkdir(PATHS.DONE)
        if not os.path.isdir(PATHS.OUTPUT):
            os.mkdir(PATHS.OUTPUT)
        if not os.path.isdir(PATHS.FAIL):
            os.mkdir(PATHS.FAIL)