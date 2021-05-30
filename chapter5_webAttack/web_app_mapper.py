import queue
import threading
import requests
import os

"""
A web app mapper,discovers something important that are exposed in a website using open-source CMS
using CMS joomla for test here 
"""

threads = 10
target = "http://192.168.29.128/Joomla_3.9.27-Stable-Full_Package"
directory = "./Joomla_3.9.27-Stable-Full_Package"
filters = [".jpg",".png",".gif",".css"]

os.chdir(directory)
web_path = queue.Queue()

for r,d,f in os.walk("."):
    for file in f:
        remote_path = "%s/%s"%(r,file)
        # if run in windows,replace backslash with slash
        if os.name == "nt":
            remote_path = remote_path.replace("\\", "/")
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        if os.path.splitext(file)[1] not in filters:
            web_path.put(remote_path)


def test_remote():
    while not web_path.empty():
        path = web_path.get()
        url = target+path
        try:
            res = requests.get(url)
            print("%d => %s"%(res.status_code,path))
        except Exception as e:
            pass


for i in range(threads):
    print("spawning thread:%s"%i)
    t = threading.Thread(target=test_remote)
    t.start()



