from pygame.draw import rect
from System import GlobalSprites
from Function.Func import checkInScreen

class Pet():
    def __init__(self) -> None:
        pass
    
def drawPet(screen,offset_x,offset_y,pet):
    if(checkInScreen(offset_x,offset_y,pet)):
        borderHpBar = 1
        sprites = GlobalSprites.mainCharacters[pet.characterName]
        index = pet.animation_count // pet.animation_delay % GlobalSprites.lengthMainCharacters[pet.characterName][pet.status]
        screen.blit(sprites[pet.status+"_"+pet.direction][index],(pet.rect.x - offset_x,pet.rect.y - offset_y))
        rect(screen, (110, 20, 0), (pet.rect.x - offset_x - borderHpBar,pet.rect.y - offset_y -10-borderHpBar,pet.rect.width+borderHpBar*2,5+borderHpBar*2),borderHpBar)
        rect(screen, (255, 0, 0), (pet.rect.x - offset_x ,pet.rect.y - offset_y -10,pet.rect.width,5))
        rect(screen, (0, 255, 0), (pet.rect.x - offset_x ,pet.rect.y - offset_y -10,(pet.rect.width/pet.max_hp)*pet.hp,5))