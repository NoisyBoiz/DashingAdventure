from System import GlobalSprites
from Function.Func import checkInScreen

class Item:
    def __init__(self) -> None:
        pass
   
def drawItem(screen,offset_x,offset_y,item):
    if(checkInScreen(offset_x,offset_y,item)):
        image = GlobalSprites.allItems[item.itemName][0]
        screen.blit(image,(item.rect.x - offset_x,item.rect.y - offset_y))