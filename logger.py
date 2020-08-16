import os
import glob
import sys
import time
import threading
import logging
from google.cloud import logging as cloudlogging
#import google.cloud.logging
from sh import tail

#client = google.cloud.logging.Client()
log_client = cloudlogging.Client()
log_handler = log_client.get_default_handler()
cloud_logger = logging.getLogger("cloudLogger")
cloud_logger.setLevel(logging.INFO)
cloud_logger.addHandler(log_handler)

#client.setup_logging()
logsdir = os.environ['LOG_FOLDER']
lastlog = ""

def follow():
    global lastlog
    for line in tail("-f", lastlog, _iter=True):
        if ("INFO" in line):
            cloud_logger.info(line)
        else:
            cloud_logger.error(line)

def getLastLog():
    list_of_files = glob.glob(logsdir)
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

if __name__ == "__main__":
    while True:
        latest_file = getLastLog()
        if(lastlog != latest_file):
            thread_follow = threading.Thread(target=follow)
            print ("Run new Thread")
            lastlog = latest_file
            
            thread_follow.setDaemon(True)
            thread_follow.start()
        time.sleep(60)