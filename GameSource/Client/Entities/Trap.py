from System import GlobalSprites
from Function.Func import checkInScreen
from System import GlobalSprites
from Function.Func import checkInScreen

class Trap():
    def __init__(self) -> None:
        pass

def drawTrap(screen,offset_x,offset_y,trap):
    if(checkInScreen(offset_x,offset_y,trap)):
        index = trap.animation_count // trap.animation_delay % GlobalSprites.AllLengthTraps[trap.name][trap.name]
        image = GlobalSprites.AllTraps[trap.name][trap.name][index]
        screen.blit(image,(trap.rect.x - offset_x,trap.rect.y - offset_y))