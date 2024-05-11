from pygame import Rect
import math
from System import Constant, GlobalSprites
from Function.Func import checkInScreen

class NormalAttackFar():
    def __init__(self):
        pass
    
class Cryo(NormalAttackFar):
    def __init__(self):
        pass
class Dendro(NormalAttackFar):
    def __init__(self):
        pass
class Electro(NormalAttackFar):
    def __init__(self):
        pass
class Hydro(NormalAttackFar):
    def __init__(self):
        pass
class Pyro(NormalAttackFar):
    def __init__(self):
        pass

class swordAttack():
    def __init__(self):
        pass


def DrawNormalAttack(screen,offset_x,offset_y,normalAttack,otherPlayer):
    # if(otherPlayer and not checkInScreen(offset_x,offset_y,normalAttack)): return
    if(normalAttack.skillName == "swordAttack"):
        index = normalAttack.animation_count // normalAttack.animation_delay % GlobalSprites.lengthNormalAttackNear["swordAttack"]
        screen.blit(GlobalSprites.normalAttackNear["swordAttack_"+normalAttack.direction][index],(normalAttack.rect.x - offset_x,normalAttack.rect.y - offset_y))
    else:
        index = normalAttack.animation_count // normalAttack.animation_delay % GlobalSprites.lengthNormalAttackFar[normalAttack.skillName]
        screen.blit(GlobalSprites.normalAttackFar[normalAttack.skillName + "_" + normalAttack.direction][index],(normalAttack.rect.x - offset_x,normalAttack.rect.y - offset_y))