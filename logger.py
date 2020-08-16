import os
import glob
import sys
import time
import threading
import logging
import google.cloud.logging
from sh import tail

logsdir = os.environ['LOG_FOLDER']
lastlog = ""

def follow():
    global lastlog
    print("MONITORING THIS LOG FILE: " + lastlog)
    for line in tail("-f", lastlog, _iter=True):
        if "|INFO|" in line:
            logging.info(line)
        else:
            logging.error(line)

def getLastLog():
    list_of_files = glob.glob(logsdir)
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

if __name__ == "__main__":
    client = google.cloud.logging.Client()
    client.setup_logging()
    while True:
        latest_file = getLastLog()
        
        if(lastlog != latest_file):
            thread_follow = threading.Thread(target=follow)
            print ("Run new Thread")
            lastlog = latest_file
            
            thread_follow.setDaemon(True)
            thread_follow.start()
        time.sleep(60)