import os
import json

def readFile(path):
    string = ""
    f = open(os.path.join(os.getcwd(),'Assets',"Setting", path),'r',encoding = 'utf-8')
    for i in f.readlines():
        string += i
    f.close()
    result = json.loads(string)
    return result

def saveFile(path,data):
    save = open(os.path.join(os.getcwd(),'Assets',"Setting", path),'w',encoding = 'utf-8')
    save.write(json.dumps(data))
    save.close()