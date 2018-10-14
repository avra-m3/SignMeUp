import sys
from threading import Thread

from modules.processor.observer import watch

count = 0
observer = Thread(target=watch)
while True:
    observer.run()
    count += 1
    print("Observer Failed!!! count={}".format(count), file=sys.stderr)
