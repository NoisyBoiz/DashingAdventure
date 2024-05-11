from pygame.draw import rect
from System import GlobalSprites, Font
from Function.Func import checkInScreen

class Enemy():
    def __init__(self) -> None:
        pass
    
def drawEnemy(screen,offset_x,offset_y,enemy):
    if(checkInScreen(offset_x,offset_y,enemy)):
        borderHpBar = 1
        rect(screen, (110, 20, 0), (enemy.rect.x - offset_x  - borderHpBar,enemy.rect.y - offset_y -10-borderHpBar,enemy.rect.width+borderHpBar*2,5+borderHpBar*2),borderHpBar)
        rect(screen, (255, 0, 0), (enemy.rect.x - offset_x  ,enemy.rect.y - offset_y -10,enemy.rect.width,5))
        rect(screen, (0, 255, 198), (enemy.rect.x - offset_x  ,enemy.rect.y - offset_y -10,(enemy.rect.width/enemy.max_hp)*enemy.hp,5))
        sprites = GlobalSprites.enemys[enemy.characterName]
        index = enemy.animation_count // enemy.animation_delay % GlobalSprites.lengthEnemys[enemy.characterName][enemy.status]
        screen.blit(sprites[enemy.status+"_"+enemy.direction][index],(enemy.rect.x - offset_x ,enemy.rect.y - offset_y))
        text = Font.Arial18.render("Lv "+ str(enemy.level) + ". " + enemy.characterName, True, (0, 0, 0))
        textRect = text.get_rect()
        screen.blit(text,(enemy.rect.x - offset_x + (enemy.rect.width - textRect.width)//2 ,enemy.rect.y - offset_y - 20 - textRect.height))