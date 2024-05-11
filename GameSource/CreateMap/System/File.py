import System.Object as Object
import System.Setting as Setting
import json

listGrass = ["Grass", "GrassPink", "Desert", "Snow"]

def read(objectGroups):
    saveData = []
    try:
        dataInit = open("Assets\\Map\\map.json","r")
        saveData = json.loads(dataInit.read())
        dataInit.close()
    except: 
        pass
    if saveData == []:
        return
    for obj in saveData:
        pos = obj["pos"]
        type = obj["type"].split("-")[0]
        if type == "block":
            type2 = obj["type"].split("-")[1]
            if type2 in listGrass:
                index = int(obj["type"].split("-")[2])
                newObj = Object.Object(pos,type2)
                newObj.updateIndex(index)
            else:
                if Setting.imageSetting[type]["type"] == "category":
                    index = Setting.imageSetting[type]["index"][obj["type"].split("-")[1]]
                else:
                    index = int(obj["type"].split("-")[1])
                newObj = Object.Object(pos,type)
                newObj.updateIndex(index)
            
        else:
            if Setting.imageSetting[type]["type"] == "category":
                index = Setting.imageSetting[type]["index"][obj["type"].split("-")[1]]
            else:
                index = int(obj["type"].split("-")[1])
            newObj = Object.Object(pos,type)
            newObj.updateIndex(index)
        objectGroups.add(newObj)

def save(objectGroups):
    saveData = []
    for obj in objectGroups:
        if Setting.imageSetting[obj.type]["type"] == "category":
            if obj.type == "block":
                rs = {
                    "pos": obj.pos,
                    "type": obj.type+"-"+Setting.imageSetting[obj.type]["index"][obj.index] +"-0",
                }
            else:
                rs = {
                    "pos": obj.pos,
                    "type": obj.type+"-"+Setting.imageSetting[obj.type]["index"][obj.index],
                }
            saveData.append(rs)
        else:
            if obj.type in listGrass:
                rs = {
                    "pos": obj.pos,
                    "type": "block-" + obj.type+"-"+str(obj.index),
                }
            else:
                rs = {
                    "pos": obj.pos,
                    "type": obj.type+"-"+str(obj.index),
                }
            saveData.append(rs)
    fileSave = open("Assets\\Map\\map.json","w")
    json.dump(saveData, fileSave)
    fileSave.close()