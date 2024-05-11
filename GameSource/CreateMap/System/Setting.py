import pygame
import System.Func as Func

screen_width = 1200
screen_height = 600
block_size = 60
blockIcon_size = 40

imageCursor = {
    "normal": pygame.cursors.Cursor((0,0), pygame.transform.scale(pygame.image.load("Assets\\Image\\MapAction\\cursorNormal.png"),(block_size//2,block_size//2))),
    "vertical" : pygame.cursors.Cursor((0,0), pygame.transform.scale(pygame.image.load("Assets\\Image\\MapAction\\cursorLR.png"),(block_size//2,block_size//2))),
    "horizontal" : pygame.cursors.Cursor((0,0), pygame.transform.scale(pygame.image.load("Assets\\Image\\MapAction\\cursorUD.png"),(block_size//2,block_size//2))),
    "all" : pygame.cursors.Cursor((0,0), pygame.transform.scale(pygame.image.load("Assets\\Image\\MapAction\\cursorAll.png"),(block_size//2,block_size//2))),
}

imageAction = {
    # "instruction": pygame.transform.scale(pygame.image.load("Assets\\Image\\MapAction\\instruction.png"),(blockIcon_size,blockIcon_size)),
    "save": pygame.transform.scale(pygame.image.load("Assets\\Image\\MapAction\\save.png"),(blockIcon_size,blockIcon_size)),
    "move": pygame.transform.scale(pygame.image.load("Assets\\Image\\MapAction\\move.png"),(blockIcon_size,blockIcon_size)),
    "shift": pygame.transform.scale(pygame.image.load("Assets\\Image\\MapAction\\shift.png"),(blockIcon_size,blockIcon_size)),
    "add": pygame.transform.scale(pygame.image.load("Assets\\Image\\MapAction\\add.png"),(blockIcon_size,blockIcon_size)),
    "edit": pygame.transform.scale(pygame.image.load("Assets\\Image\\MapAction\\edit.png"),(blockIcon_size,blockIcon_size)),
    "delete": pygame.transform.scale(pygame.image.load("Assets\\Image\\MapAction\\delete.png"),(blockIcon_size,blockIcon_size)), 
}

imageSetting = {
    "character": {"type":"folder","imgPath":"MainCharacters\\MaskDude","endPath":"idle", "oriWidth":32, "oriHeight":32, "newWidth":block_size,"newHeight":block_size},
    "enemy":{
        "type":"category",
        "category":{
            "slime":{"type":"folder","imgPath":"Enemy\\Slime","endPath":"idle","oriWidth":100, "oriHeight":100, "newWidth":block_size, "newHeight":block_size},
            "slimeRed":{"type":"folder","imgPath":"Enemy\\SlimeRed","endPath":"idle","oriWidth":100, "oriHeight":100, "newWidth":block_size, "newHeight":block_size},
            "slimeGreen":{"type":"folder","imgPath":"Enemy\\SlimeGreen","endPath":"idle","oriWidth":100, "oriHeight":100, "newWidth":block_size, "newHeight":block_size},
            "buffalo":{"type":"folder","imgPath":"Enemy\\Buffalo","endPath":"idle","oriWidth":100, "oriHeight":100, "newWidth":block_size, "newHeight":block_size},
            "eye": {"type":"folder","imgPath":"Enemy\\Eye","endPath":"idle","oriWidth":100, "oriHeight":100, "newWidth":block_size, "newHeight":block_size},
            "thorn": {"type":"folder","imgPath":"Enemy\\Thorn","endPath":"idle","oriWidth":100, "oriHeight":100, "newWidth":block_size, "newHeight":block_size},
            "worm": {"type":"folder","imgPath":"Enemy\\Worm","endPath":"idle","oriWidth":100, "oriHeight":100, "newWidth":block_size, "newHeight":block_size},
            "thornYellow":{ "type":"folder","imgPath":"Enemy\\ThornYellow","endPath":"idle","oriWidth":100, "oriHeight":100, "newWidth":block_size, "newHeight":block_size}
        },
        "index":{}
        },
    "boss":{
        "type":"category",
        "category":{
            "slime":{"type":"folder","imgPath":"Enemy\\Slime","endPath":"idle","oriWidth":100, "oriHeight":100, "newWidth":block_size*3, "newHeight":block_size*3},
            "slimeRed":{"type":"folder","imgPath":"Enemy\\SlimeRed","endPath":"idle","oriWidth":100, "oriHeight":100, "newWidth":block_size*3, "newHeight":block_size*3},
            "slimeGreen":{"type":"folder","imgPath":"Enemy\\SlimeGreen","endPath":"idle","oriWidth":100, "oriHeight":100, "newWidth":block_size*3, "newHeight":block_size*3},
            "buffalo":{"type":"folder","imgPath":"Enemy\\Buffalo","endPath":"idle","oriWidth":100, "oriHeight":100, "newWidth":block_size*3, "newHeight":block_size*3},
            "eye": {"type":"folder","imgPath":"Enemy\\Eye","endPath":"idle","oriWidth":100, "oriHeight":100, "newWidth":block_size*3, "newHeight":block_size*3},
            "thorn": {"type":"folder","imgPath":"Enemy\\Thorn","endPath":"idle","oriWidth":100, "oriHeight":100, "newWidth":block_size*3, "newHeight":block_size*3},
            "worm": {"type":"folder","imgPath":"Enemy\\Worm","endPath":"idle","oriWidth":100, "oriHeight":100, "newWidth":block_size*3, "newHeight":block_size*3},
            "thornYellow":{ "type":"folder","imgPath":"Enemy\\ThornYellow","endPath":"idle","oriWidth":100, "oriHeight":100, "newWidth":block_size*3, "newHeight":block_size*3}
        },
        "index":{}
        },
    "Grass": {"type":"folder", "imgPath":"Terrain" ,"endPath":"Grass", "oriWidth":50, "oriHeight":50, "newWidth":block_size,"newHeight":block_size},
    "GrassPink": {"type":"folder", "imgPath":"Terrain" ,"endPath":"GrassPink", "oriWidth":50, "oriHeight":50, "newWidth":block_size,"newHeight":block_size},
    "Snow": {"type":"folder", "imgPath":"Terrain" ,"endPath":"Snow", "oriWidth":50, "oriHeight":50, "newWidth":block_size,"newHeight":block_size},
    "Desert":{ "type":"folder", "imgPath":"Terrain" ,"endPath":"Desert", "oriWidth":50, "oriHeight":50, "newWidth":block_size,"newHeight":block_size},
    "block":{
        "type":"category",
        "category":{
            "Rock":{ "type":"folder", "imgPath":"Terrain" ,"endPath":"Rock", "oriWidth":50, "oriHeight":50, "newWidth":block_size,"newHeight":block_size},
            "RockBlue":{ "type":"folder", "imgPath":"Terrain" ,"endPath":"RockBlue", "oriWidth":50, "oriHeight":50, "newWidth":block_size,"newHeight":block_size},
            "RockRed":{ "type":"folder", "imgPath":"Terrain" ,"endPath":"RockRed", "oriWidth":50, "oriHeight":50, "newWidth":block_size,"newHeight":block_size},
            "RockGreen":{ "type":"folder", "imgPath":"Terrain" ,"endPath":"RockGreen", "oriWidth":50, "oriHeight":50, "newWidth":block_size,"newHeight":block_size},
            "Wood":{ "type":"folder", "imgPath":"Terrain" ,"endPath":"Wood", "oriWidth":50, "oriHeight":50, "newWidth":block_size,"newHeight":block_size},
        },
        "index":{}
    },
    "traps":{
        "type":"category",
        "category":{
            "BlueFire":{ "type":"folder", "imgPath":"Traps\\BlueFire" ,"endPath":"BlueFire", "oriWidth":200, "oriHeight":300, "newWidth":block_size//2,"newHeight":block_size},
            "Fire":{ "type":"folder", "imgPath":"Traps\\Fire" ,"endPath":"Fire", "oriWidth":200, "oriHeight":300, "newWidth":block_size//2,"newHeight":block_size},
            "Flower":{ "type":"folder", "imgPath":"Traps\\Flower" ,"endPath":"Flower", "oriWidth":200, "oriHeight":200, "newWidth":block_size,"newHeight":block_size},
            "Thorn":{ "type":"folder", "imgPath":"Traps\\Thorn" ,"endPath":"Thorn", "oriWidth":200, "oriHeight":50, "newWidth":block_size,"newHeight":block_size//4},
        },
        "index":{}
    },
    "tree":{"type":"folder", "imgPath":"Tree", "endPath":"tree",  "oriWidth":300, "oriHeight":300, "newWidth":block_size*4, "newHeight":block_size*4},
    "plant120x120":{"type":"file", "imgPath":"Plant" , "endPath":"plant120x120", "oriWidth":120, "oriHeight":120, "newWidth":block_size, "newHeight":block_size},
    "plant120x240":{"type":"file", "imgPath":"Plant" , "endPath":"plant120x240", "oriWidth":120, "oriHeight":240, "newWidth":block_size, "newHeight":block_size*2},
    "rock":{"type":"folder", "imgPath":"Rock","endPath":"rock","oriWidth":120,"oriHeight":120,"newWidth":block_size,"newHeight":block_size},
    "gates":{"type":"folder", "imgPath":"Gates","endPath":"gates","oriWidth":240,"oriHeight":240,"newWidth":block_size*2,"newHeight":block_size*2},
}


blockSetting = {
    "character": {"defaultIndex":0,"shift": True,"indexChange": False, "overload": False},
    "enemy": {"defaultIndex":0,"shift": True,"indexChange": True, "overload": False},
    "boss":{ "defaultIndex":0,"shift": True,"indexChange": True, "overload": False},
    "Grass": {"defaultIndex":1,"shift": False,"indexChange": False, "overload": False},
    "GrassPink": {"defaultIndex":0,"shift": False,"indexChange": False, "overload": False},
    "Snow": {"defaultIndex":0,"shift": False,"indexChange": False, "overload": False},
    "Desert": {"defaultIndex":0,"shift": False,"indexChange": False, "overload": False},
    "block": {"defaultIndex":0,"shift": False,"indexChange": True, "overload": False},

    "traps": {"defaultIndex":0,"shift": True,"indexChange": True, "overload": False},
    "tree": {"defaultIndex":0,"shift": True,"indexChange": True, "overload": False},
    "plant120x120": {"defaultIndex":0,"shift": True,"indexChange": True, "overload": False},
    "plant120x240": {"defaultIndex":0,"shift": True,"indexChange": True, "overload": False},
    "rock": {"defaultIndex":0,"shift": True,"indexChange": True, "overload": False},
    "gates": {"defaultIndex":0,"shift": True,"indexChange": True, "overload": False},
}

imageBlock = {}
imageBlockIcon = {}
limitIndexBlock = {}

def getImgCategory(name):
    imageS = imageSetting[name]["category"]
    imageBlock[name] = []
    imageBlockIcon[name] = []
    limitIndexBlock[name] = 0
    for i,key in enumerate(imageS):
        imageSetting[name]["index"][i] = key
        imageSetting[name]["index"][key] = i
        setting = imageS[key]
        limitIndexBlock[name] += 1
        if setting["type"] == "folder":
            imageBlock[name].append(Func.splitSprite(setting["imgPath"],setting["oriWidth"],setting["oriHeight"],setting["newWidth"],setting["newHeight"],False,False)[setting["endPath"]][0])
        elif setting["type"] == "file":
            imageBlock[name].append(Func.splitSprite(setting["imgPath"],setting["endPath"],setting["oriWidth"],setting["oriHeight"],setting["newWidth"],setting["newHeight"],False,False)[0])
        imageBlockIcon[name].append(Func.splitSprite(setting["imgPath"],setting["oriWidth"],setting["oriHeight"],(setting["oriWidth"]/setting["oriHeight"])*blockIcon_size,blockIcon_size,False,False)[setting["endPath"]][0])

for key in imageSetting:
    setting = imageSetting[key]
    if blockSetting[key]["indexChange"] and setting["type"] != "category":
        if setting["type"] == "folder":
            sprite, length = (Func.splitSprite(setting["imgPath"],setting["oriWidth"],setting["oriHeight"],setting["newWidth"],setting["newHeight"],True,False))
            imageBlock[key] = sprite[setting["endPath"]]
            limitIndexBlock[key] = length[setting["endPath"]]
            imageBlockIcon[key] = (Func.splitSprite(setting["imgPath"],setting["oriWidth"],setting["oriHeight"],(setting["oriWidth"]/setting["oriHeight"])*blockIcon_size,blockIcon_size,False,False))[setting["endPath"]]
        elif setting["type"] == "file":
            sprite, length = (Func.splitSpriteImgPath(setting["imgPath"],setting["endPath"],setting["oriWidth"],setting["oriHeight"],setting["newWidth"],setting["newHeight"],True,False))
            imageBlock[key] = sprite[setting["endPath"]]
            limitIndexBlock[key] = length[setting["endPath"]]
            imageBlockIcon[key] = (Func.splitSpriteImgPath(setting["imgPath"],setting["endPath"],setting["oriWidth"],setting["oriHeight"],(setting["oriWidth"]/setting["oriHeight"])*blockIcon_size,blockIcon_size,False,False))[setting["endPath"]]
    else:
        if setting["type"] == "folder":
            imageBlock[key] = (Func.splitSprite(setting["imgPath"],setting["oriWidth"],setting["oriHeight"],setting["newWidth"],setting["newHeight"],False,False))[setting["endPath"]]
            imageBlockIcon[key] = (Func.splitSprite(setting["imgPath"],setting["oriWidth"],setting["oriHeight"],(setting["oriWidth"]/setting["oriHeight"])*blockIcon_size,blockIcon_size,False,False))[setting["endPath"]]
            limitIndexBlock[key] = 1
        elif setting["type"] == "file":
            imageBlock[key] = (Func.splitSprite(setting["imgPath"],setting["endPath"],setting["oriWidth"],setting["oriHeight"],setting["newWidth"],setting["newHeight"],False,False))
            imageBlockIcon[key] = (Func.splitSprite(setting["imgPath"],setting["endPath"],setting["oriWidth"],setting["oriHeight"],(setting["oriWidth"]/setting["oriHeight"])*blockIcon_size,blockIcon_size,False,False)[setting["endPath"]])
            limitIndexBlock[key] = 1
        elif setting["type"] == "category":
            getImgCategory(key)
        
    
