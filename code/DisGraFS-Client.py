import os
import sys
import time
import urllib.parse
import subprocess
import websockets
import asyncio
import time
import webbrowser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import PatternMatchingEventHandler
from collections import deque

def extractArgsFromUrl(url):
    args = urllib.parse.unquote(url)
    protocolIndex = args.find("://")
    if protocolIndex == -1:
        print("Error: Wrong url argument format \n")
        input("Press Enter to quit")
        sys.exit(-2)
    args = args[protocolIndex + 3:]
    args = args.split(' ')
    return args

if __name__ == "__main__":

    ########
    # init #
    ########

    print("DisGraFS Client")

    if len(sys.argv) < 2:
        print("Error: Wrong argument format \n")
        input("Press Enter to quit")
        sys.exit(-1)
    args = extractArgsFromUrl(sys.argv[1])
#    redisUrl = "redis://:123@47.113.222.89:6379/1"
    redisUrl = "redis://irisesd:DCchengding2003@disgrafs.redis.rds.aliyuncs.com:6379/1"
    mountPointNoSlash = "X:"
    mountPointSlash = "X:/"
    wsUrl = "ws://47.101.152.229:9090"
#    wsUrl = "ws://47.113.230.170:9090"
    wsAuth = "admin:123456"

    try:
        redisUrl = args[0]
        print(args[0])
        redisUrl = "redis://irisesd:DCchengding2003@disgrafs.redis.rds.aliyuncs.com:6379/1"
        print(redisUrl)
        mountPoint = args[1]
        wsUrl = args[2]
        wsAuth = args[3]
        # example: disgrafs://redis://:disgrafs@juicefs.disgrafs.tech Z: ws://localhost:9090 admin:123456
        if mountPoint[-1] != '/':
            mountPointNoSlash = mountPoint
            mountPointSlash = mountPoint + '/'
        else:
            mountPointNoSlash = mountPoint[:-1]
            mountPointSlash = mountPoint
        print(mountPointSlash)
        mountPointSlash = "X:/"
    except Exception:
        print("Error: Wrong url argument number \n")
        input("Press Enter to quit")
        sys.exit(-3)

    print("Starting juicefs...")
    print(["juicefs", "mount", redisUrl, mountPointNoSlash,"-v"]);
#    subprocess.Popen(["juicefs", "mount", redisUrl, mountPointNoSlash,"-v"], shell=True)
    subprocess.Popen("juicefs mount redis://irisesd:DCchengding2003@disgrafs.redis.rds.aliyuncs.com:6379/1 X: -v", shell=True)
    print("Juicefs started")

    ############
    # watchdog #
    ############

    def createDatapack(type, path1 : str, path2 = ""):
        timeStamp = int(round(time.time() * 1000))
        purePath1 = path1[len(mountPointSlash):]
        purePath1 = purePath1.replace('\\', '/')
        purePath2 = ""
        if path2 != "":
            purePath2 = path2[len(mountPointSlash):]
            purePath2 = purePath2.replace('\\', '/')
        dictObj = { "type": type, "path1": purePath1, "path2": purePath2, "time":timeStamp }
        return repr(dictObj)

    sendTasklist = deque()
    modifyCounter = dict()

    print("Establishing watchdog observer...")

    def on_created(event):
        print("Watchdog working 1")
        message = "Watchdog: "
        print(event.is_directory)
        if not event.is_directory:
            message = "file "
            message += f"{event.src_path} created"
            print(message)
            #sendTasklist.append(createDatapack("create", event.src_path))
            modifyCounter[event.src_path] = 0

    def on_deleted(event):
        message = "Watchdog: "
        print("Watchdog working 2")
        if not event.is_directory:
            message = "file "
            message += f"{event.src_path} deleted"
            print(message)
            sendTasklist.append({"time": time.time(), "message": createDatapack("delete", event.src_path)})

    def on_modified(event):
        message = "Watchdog: "
        print("Watchdog working 3")
        if not event.is_directory:
            message = "file "
            message += f"{event.src_path} modified"
            print(message)
            modifyCounter[event.src_path] = modifyCounter[event.src_path] + 1
            if modifyCounter[event.src_path] == 3:
                modifyCounter[event.src_path] = 0
                #sendTasklist.append(createDatapack("modify", event.src_path))
                sendTasklist.append({"time": time.time(), "message": createDatapack("create", event.src_path)})

    def on_moved(event):
        message = "Watchdog: "
        print("Watchdog working 4")
        if not event.is_directory:
            message = "file "
            message += f"{event.src_path} moved to {event.dest_path}"
            print(message)
            sendTasklist.append({"time": time.time(), "message": createDatapack("move", event.src_path, event.dest_path)})

    event_handler = FileSystemEventHandler()
    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_modified = on_modified
    event_handler.on_moved = on_moved
    my_observer = Observer()
    while not os.path.exists(mountPointSlash):
        time.sleep(0.1)
    my_observer.schedule(event_handler, mountPointSlash, recursive=True)
    my_observer.start()
    print("Watchdog observer established")

    async def login():
        print(wsUrl)
        wsClient = await websockets.connect(wsUrl)
        print(wsClient)
        await wsClient.send(wsAuth)
        return wsClient

    async def wsSender(wsClient):
        while True:
            print(1)
            while len(sendTasklist) == 0:
                await asyncio.sleep(0.1)
            print(2)
            toSend = sendTasklist.popleft()
            print(3)
            while time.time() < toSend["time"]:
                await asyncio.sleep(0.1)
            print("Message sent: ", toSend["message"])
            await wsClient.send(toSend["message"])

    async def wsReceiver(wsClient):
        while True:
            print(4)
            socketRecv = await wsClient.recv()
            try:
                print(5)
                command = eval(socketRecv)
                print(6)
                if command["command"] == "exit":
                    asyncio.get_event_loop().stop()
                    return
                elif command["command"] == "open":
                    webbrowser.open("file://" + mountPointSlash + command["parameter"][0])
                elif command["command"] == "delete":
                    #print("deleting: ", mountPointSlash + command["parameter"][0])
                    os.remove(mountPointSlash + command["parameter"][0])
                else:
                    print("Error: Failed to resolve command from server:", socketRecv)
            except Exception:
                print("Error: Failed to execute command from server:", socketRecv)

    try:
        loop = asyncio.get_event_loop()
        wsClient = loop.run_until_complete(login())
        loop.run_until_complete(asyncio.wait([wsSender(wsClient), wsReceiver(wsClient)]))

    except KeyboardInterrupt:
        pass

    finally:
        print("ready to stop!!!!!!!!!!!!!!!!!!!!")
        my_observer.stop()
        subprocess.Popen("juicefs umount X:", shell=True).wait()
#        subprocess.Popen(["juicefs", "umount", mountPointNoSlash], shell=True).wait()
        loop.call_soon(wsClient.close())
        input("Press Enter to quit")
        sys.exit(0)

