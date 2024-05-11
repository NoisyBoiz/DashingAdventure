from pygame.draw import rect,polygon
from System import GlobalSprites, Font
from Function.Func import checkInScreen

class Player():
    def __init__(self) -> None:
        pass
    
class Wizard():
    def __init__(self) -> None:
        pass

class Healer():
    def __init__(self) -> None:
        pass

class Assassin():
    def __init__(self) -> None:
        pass

class Paladin():
    def __init__(self) -> None:
        pass


def drawPlayer(screen,offset_x,offset_y,player):
    if(player.isInGates): return
    sprites = GlobalSprites.mainCharacters[player.characterName]
    index = player.animation_count // player.animation_delay % GlobalSprites.lengthMainCharacters[player.characterName][player.status]
    screen.blit(sprites[player.status+"_"+player.direction][index],(player.rect.x - offset_x,player.rect.y - offset_y))
    if player.showWeapon:
        if player.weapon == "magicRod":
            drawMagicRod(screen,offset_x,offset_y,player)
        else:
            drawSword(screen,offset_x,offset_y,player)

def drawOtherPlayer(screen,offset_x,offset_y,player):
    if(player.isInGates): return
    if(checkInScreen(offset_x,offset_y,player)):
        borderHpBar = 1
        textName =Font.Arial20.render(player.name, True, (0, 0, 0))
        textNameRect = textName.get_rect()
        screen.blit(textName,(player.rect.x - offset_x + (player.rect.width - textNameRect.width)//2 ,player.rect.y - offset_y - 20 - textNameRect.height))
        rect(screen, (0, 32, 74), (player.rect.x - offset_x  - borderHpBar,player.rect.y - offset_y -10-borderHpBar,player.rect.width+borderHpBar*2,5+borderHpBar*2),borderHpBar)
        rect(screen, (82, 93, 102), (player.rect.x - offset_x  ,player.rect.y - offset_y -10,player.rect.width,5))
        rect(screen, (255, 23, 34), (player.rect.x - offset_x  ,player.rect.y - offset_y -10,(player.rect.width/player.max_hp)*player.hp,5))
        sprites = GlobalSprites.mainCharacters[player.characterName]
        index = player.animation_count // player.animation_delay % GlobalSprites.lengthMainCharacters[player.characterName][player.status]
        screen.blit(sprites[player.status+"_"+player.direction][index],(player.rect.x - offset_x ,player.rect.y - offset_y))
    if player.showWeapon:
        if player.weapon == "magicRod":
            drawMagicRod(screen,offset_x,offset_y,player)
        else:
            drawSword(screen,offset_x,offset_y,player)

def drawSword(screen,offset_x,offset_y,player):
    direction = player.direction
    if direction == "left":
        rect_x = player.rect.x - 10
        rect_y = player.rect.y - 2
    else:
        rect_x = player.rect.x + 10
        rect_y = player.rect.y - 2
    image = GlobalSprites.sword["sword_"+direction][0]
    screen.blit(image,(rect_x - offset_x,rect_y - offset_y))

def drawMagicRod(screen,offset_x,offset_y,player):
    direction = player.direction
    if direction == "left":
        rect_x = player.rect.x - 3
        rect_y = player.rect.y
    else:
        rect_x = player.rect.x + 3
        rect_y = player.rect.y 
    image = GlobalSprites.magicRod["magicRod_"+direction][0]
    screen.blit(image,(rect_x - offset_x,rect_y - offset_y))

def drawEnemyTarget(screen,offset_x,offset_y,player):
    if(player.enemy_target != None):
        size = 20
        x = player.enemy_target.rect.x
        y = player.enemy_target.rect.y
        width = player.enemy_target.rect.width
        height = player.enemy_target.rect.height
        polygon(screen, (255, 0, 0), [(x + width//2 - size//2 - offset_x, y - height//1.5 - offset_y),(x + width//2 + size//2 - offset_x, y - height//1.5 - offset_y),(x + width//2 - offset_x, y + size//2 - height//1.5- offset_y)])
