import pygame
from os import listdir
from os.path import isfile, join
import System.Setting as Setting

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]
def splitSprite(direc, width, height,s_width, s_height, getLength, direction=False):
    path = join("Assets\\Image", direc)
    files = [f for f in listdir(path) if isfile(join(path, f))]
    all_sprites = {}
    all_length = {}
    for file in files:
        sprite_sheet = pygame.image.load(join(path, file))
        # sprite_sheet = pygame.image.load(join(path, file)).convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale(surface,(s_width,s_height)))
        if direction:
            all_sprites[file.replace(".png", "") + "_right"] = sprites
            all_sprites[file.replace(".png", "") + "_left"] = flip(sprites)
            if getLength:
                all_length[file.replace(".png", "") + "_right"] = len(sprites)
                all_length[file.replace(".png", "") + "_left"] = len(sprites)
        else:
            all_sprites[file.replace(".png", "")] = sprites
            if getLength:
                all_length[file.replace(".png", "")] = len(sprites)
    if getLength:
        return all_sprites, all_length
    return all_sprites


def getPoint(pos,offset_x,offset_y):
    x = pos[0]-offset_x
    y = pos[1]-offset_y
    x = x//Setting.block_size*Setting.block_size
    y = y//Setting.block_size*Setting.block_size
    return [x,y]

def getRealPosition(pos,offset_x,offset_y):
    x = pos[0]-offset_x
    y = pos[1]-offset_y
    return [x,y]




def splitSpriteImgPath(direc,imgName ,width, height,s_width, s_height, getLength, direction=False):
    path = join("Assets\\Image", direc)
    all_sprites = {}
    all_length = {}
    sprite_sheet = pygame.image.load(join(path, imgName+".png"))
    #sprite_sheet = pygame.image.load(join(path, imgName)).convert_alpha()
    sprites = []
    for i in range(sprite_sheet.get_width() // width):
        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        rect = pygame.Rect(i * width, 0, width, height)
        surface.blit(sprite_sheet, (0, 0), rect)
        sprites.append(pygame.transform.scale(surface,(s_width,s_height)))
    if direction:
        all_sprites[imgName + "_right"] = sprites
        all_sprites[imgName + "_left"] = flip(sprites)
        if getLength:
            all_length[imgName + "_right"] = len(sprites)
            all_length[imgName + "_left"] = len(sprites)
    else:
        all_sprites[imgName] = sprites
        if getLength:
            all_length[imgName] = len(sprites)
    if getLength:
        return all_sprites, all_length
    return all_sprites
 