from pygame import Rect,Surface,SRCALPHA,Color
from pygame.transform import scale,flip
from pygame.image import load
from os import listdir, getcwd
from os.path import isfile, join
from System import Constant

def Flip(sprites):
    return [flip(sprite, True, False) for sprite in sprites]
def splitSprite(path, original_width, original_height, new_width, new_height, getLength, direction=False):
    fullPath = join(getcwd(),"assets","Image")
    for p in path:
        fullPath = join(fullPath,p)

    files = [f for f in listdir(fullPath) if isfile(join(fullPath, f))]
    all_sprites = {}
    all_length = {}
    for file in files:
        sprite_sheet = load(join(fullPath, file))
        #sprite_sheet = load(join(path, file)).convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // original_width):
            surface = Surface((original_width, original_height), SRCALPHA, 32)
            rect = Rect(i * original_width, 0, original_width, original_height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(scale(surface,(new_width,new_height)))
        if direction:
            all_sprites[file.replace(".png", "") + "_right"] = sprites
            all_sprites[file.replace(".png", "") + "_left"] = Flip(sprites)
            if getLength:
                all_length[file.replace(".png", "")] = len(sprites)
        else:
            all_sprites[file.replace(".png", "")] = sprites
            if getLength:
                all_length[file.replace(".png", "")] = len(sprites)
    if getLength:
        return all_sprites, all_length
    return all_sprites

def splitSpriteImgPath(path, original_width, original_height, new_width, new_height, getLength, direction=False):
    fullPath = join(getcwd(),"assets","Image")
    imgName = path[-1]
    path[-1] = path[-1] + ".png"
    for p in path:
        fullPath = join(fullPath,p)
        
    all_sprites = {}
    all_length = {}
    sprite_sheet = load(fullPath)
    #sprite_sheet = load(join(path, imgName)).convert_alpha()
    sprites = []
    for i in range(sprite_sheet.get_width() // original_width):
        surface = Surface((original_width, original_height), SRCALPHA, 32)
        rect = Rect(i * original_width, 0, original_width, original_height)
        surface.blit(sprite_sheet, (0, 0), rect)
        sprites.append(scale(surface,(new_width, new_height)))
    if direction:
        all_sprites[imgName + "_right"] = sprites
        all_sprites[imgName + "_left"] = Flip(sprites)
        if getLength:
            all_length[imgName] = len(sprites)
    else:
        all_sprites[imgName] = sprites
        if getLength:
            all_length[imgName] = len(sprites)
    if getLength:
        return all_sprites, all_length
    return all_sprites
 
def checkOverScreen(player,offset_x,offset_y,mapLimit):
    if(player.rect.x < Constant.screen_padding_lr + offset_x):
        if offset_x > mapLimit[0]:
            offset_x -= (Constant.screen_padding_lr + offset_x - player.rect.x)
    if (player.rect.x > Constant.Screen_Width - Constant.screen_padding_lr + offset_x - player.rect.width):
        if offset_x  + Constant.Screen_Width < mapLimit[1]:
            offset_x += (player.rect.x - (Constant.Screen_Width - Constant.screen_padding_lr + offset_x - player.rect.width))
    if(player.rect.y < Constant.screen_padding_tb + offset_y):
        offset_y -= (Constant.screen_padding_tb + offset_y - player.rect.y)
    if (player.rect.y > Constant.Screen_Height - Constant.screen_padding_tb + offset_y - player.rect.height):
        offset_y += (player.rect.y - (Constant.Screen_Height - Constant.screen_padding_tb + offset_y - player.rect.height))
    return offset_x,offset_y

def resetRectScreen(player,mapLimit):
    offset_x = player.rect.x + player.rect.width // 2 - Constant.Screen_Width // 2
    if offset_x < mapLimit[0]:
        offset_x = mapLimit[0]
    if offset_x > mapLimit[1] - Constant.Screen_Width:
        offset_x = mapLimit[1] - Constant.Screen_Width
    offset_y = player.rect.y + player.rect.height // 2 - Constant.Screen_Height // 2
    return offset_x,offset_y

def screenFollowX(player,offset_x,offset_y,mapLimit):
    offset_x = player.rect.x + player.rect.width // 2 - Constant.Screen_Width // 2
    if offset_x < mapLimit[0]:
        offset_x = mapLimit[0]
    if offset_x > mapLimit[1] - Constant.Screen_Width:
        offset_x = mapLimit[1] - Constant.Screen_Width

    if(player.rect.y < Constant.screen_padding_tb + offset_y):
        offset_y -= (Constant.screen_padding_tb + offset_y - player.rect.y)
    if (player.rect.y > Constant.Screen_Height - Constant.screen_padding_tb + offset_y - player.rect.height):
        offset_y += (player.rect.y - (Constant.Screen_Height - Constant.screen_padding_tb + offset_y - player.rect.height))
    return offset_x,offset_y

def screenFollowY(player,offset_x,offset_y,mapLimit):
    if(player.rect.x < Constant.screen_padding_lr + offset_x):
        if offset_x > mapLimit[0]:
            offset_x -= (Constant.screen_padding_lr + offset_x - player.rect.x)
    if (player.rect.x > Constant.Screen_Width - Constant.screen_padding_lr + offset_x - player.rect.width):
        if offset_x  + Constant.Screen_Width < mapLimit[1]:
            offset_x += (player.rect.x - (Constant.Screen_Width - Constant.screen_padding_lr + offset_x - player.rect.width))
    offset_y = player.rect.y + player.rect.height // 2 - Constant.Screen_Height // 2
    return offset_x,offset_y

# kiểm tra xem đối tượng có nằm trong màn hình không
def checkInScreen(offset_x,offset_y,obj):
    if((obj.rect.x + obj.rect.width > offset_x and obj.rect.x < offset_x + Constant.Screen_Width) and (obj.rect.y + obj.rect.height > offset_y and obj.rect.y < offset_y + Constant.Screen_Height)):
        return True
    return False