from System import GlobalSprites
from Function.Func import checkInScreen

class Gates:
    def __init__(self) -> None:
        pass

def drawGates(screen,offset_x,offset_y,gates):
    if(checkInScreen(offset_x,offset_y,gates)):
        image = GlobalSprites.gates[gates.index]
        screen.blit(image,(gates.rect.x - offset_x,gates.rect.y - offset_y))