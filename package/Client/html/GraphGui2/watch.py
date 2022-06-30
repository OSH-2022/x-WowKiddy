from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import subprocess
import ffmpy


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print("文件被修改了 %s" % event.src_path)
        

    def on_created(self, event):
        print("文件被创建了 %s" % event.src_path)
        if event.src_path[-3:] == "MP4":    #由于打标程序只支持mp4格式视频
            print("1")
            print(event.src_path[2:]+".JPG")
            if os.path.exists("X:\\.Spirit\\"+ event.src_path[2:]+".JPG"):
                print("Exist.")
                os.remove("X:\\.Spirit\\"+ event.src_path[2:]+".JPG")
            print("2")
            command_2 = "ffmpeg -i "+ event.src_path+ ' -vf "fps=1/3:round=zero:start_time=-9,scale=640x360,tile=10x5" '+ "X:\\.Spirit\\" + event.src_path[2:]+".jpg"
            print(command_2)
            subprocess.Popen(command_2, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
            

    
if __name__ == "__main__":
    time.sleep(5)
    path = "X:"
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print("Watchdog is watching you.")
    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()
    observer.join()