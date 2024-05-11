from pygame.font import SysFont
from System import Constant

class textDamage:
    def __init__(self) -> None:
        pass
        
def drawDamages(screen,offset_x,offset_y,textDamage):
    if(textDamage.x + len(textDamage.string)*textDamage.size > offset_x  and textDamage.x < offset_x + Constant.Screen_Width and textDamage.y > offset_y and textDamage.y < offset_y + Constant.Screen_Height):
        font = SysFont("comicsans", textDamage.size)
        text = font.render(textDamage.string, 1, textDamage.color)
        screen.blit(text, (textDamage.x -offset_x,textDamage.y - offset_y))