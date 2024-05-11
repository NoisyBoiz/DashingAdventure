from pygame.draw import rect
from System import GlobalSprites , Font
from Function.Func import checkInScreen

class Boss():
    def __init__(self) -> None:
        pass

def drawBoss(screen,offset_x,offset_y,boss):
    if(checkInScreen(offset_x,offset_y,boss)):
        borderHpBar = 1
        rect(screen, (110, 20, 0), (boss.rect.x - offset_x  - borderHpBar, boss.rect.y - offset_y -  10 - borderHpBar, boss.rect.width+borderHpBar*2, 8+borderHpBar*2),borderHpBar)
        rect(screen, (255, 0, 0), (boss.rect.x - offset_x, boss.rect.y - offset_y -10,boss.rect.width,8))
        rect(screen, (0, 255, 198), (boss.rect.x - offset_x, boss.rect.y - offset_y -10,(boss.rect.width/boss.max_hp)*boss.hp,8))
        sprites = GlobalSprites.allBoss[boss.characterName]
        index = boss.animation_count // boss.animation_delay % GlobalSprites.lengthAllBoss[boss.characterName][boss.status]
        screen.blit(sprites[boss.status+"_"+boss.direction][index],(boss.rect.x - offset_x ,boss.rect.y - offset_y))
        text = Font.Arial20.render("Boss - Lv "+ str(boss.level) + ". " + boss.characterName, True, (240, 0, 0))
        textRect = text.get_rect()
        screen.blit(text,(boss.rect.x - offset_x + (boss.rect.width - textRect.width)//2 ,boss.rect.y - offset_y - 20 - textRect.height))