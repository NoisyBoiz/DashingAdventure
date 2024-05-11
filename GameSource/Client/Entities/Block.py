from System import GlobalSprites
from Function.Func import checkInScreen

class Block():
    def __init__(self):
        pass

def drawTree(screen,offset_x,offset_y,tree):
    if(checkInScreen(offset_x,offset_y,tree)):
        image = GlobalSprites.tree[tree.blockName][tree.index]
        screen.blit(image,(tree.rect.x - offset_x,tree.rect.y - offset_y))

def drawPlant(screen,offset_x,offset_y,plant):
    if(checkInScreen(offset_x,offset_y,plant)):
        if plant.blockName == "plant120x120":
            image = GlobalSprites.plant120x120[plant.index]
        else:
            image = GlobalSprites.plant120x240[plant.index]
        screen.blit(image,(plant.rect.x - offset_x,plant.rect.y - offset_y))

def drawRock(screen,offset_x,offset_y,rock):
    if(checkInScreen(offset_x,offset_y,rock)):
        image = GlobalSprites.rock[rock.index]
        screen.blit(image,(rock.rect.x - offset_x,rock.rect.y - offset_y))

def drawObject(screen,offset_x,offset_y,obj):
    if(checkInScreen(offset_x,offset_y,obj)):
        image = GlobalSprites.allObject[obj.blockName][obj.index]
        screen.blit(image,(obj.rect.x - offset_x,obj.rect.y - offset_y))
