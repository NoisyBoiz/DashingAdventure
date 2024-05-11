from System import GlobalSprites
from Function.Func import checkInScreen

class DropBubbles():
    def __init__(self) -> None:
        pass

class ShootBubbles():
    def __init__(self) -> None:
        pass

class PersureBubbles():
    def __init__(self) -> None:
        pass

def drawBossSkill(screen,offset_x,offset_y,skill,bossName):   
    if bossName == "slimeRed" or bossName == "buffalo":
        name = "Pyro" 
    elif bossName == "eye":
        name = "Electro"
    elif bossName == "slimeGreen" or bossName == "thornYellow":
        name = "Dendro"
    else:
        name = "Hydro"
    index = skill.animation_count // skill.animation_delay % GlobalSprites.lengthAllBossSkill[name]
    screen.blit(GlobalSprites.allBossSkill[name+"_"+skill.direction][index],(skill.rect.x - offset_x,skill.rect.y - offset_y))
