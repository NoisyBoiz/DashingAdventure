import pygame
import System.Setting as Setting
import System.Func as Func

class Object(pygame.sprite.Sprite):
    def __init__(self,pos,type):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.type = type
        self.index = Setting.blockSetting[type]["defaultIndex"]
 
        self.image = Setting.imageBlock[type][self.index]
        self.rect = self.image.get_rect()

        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect.x = pos[0]
        self.rect.y = pos[1]
    
    def updatePos(self, mousePos, status):
        if status.sticky:
            newPos = Func.getPoint(mousePos, status.offset_x, status.offset_y)
            if status.actionShift_direction == "vertical":
                self.pos[0] = newPos[0]
                self.rect.x = self.pos[0]
            elif status.actionShift_direction == "horizontal":
                self.pos[1] = newPos[1]
                self.rect.y = self.pos[1]
            else:
                self.pos[0] = newPos[0]
                self.pos[1] = newPos[1]
                self.rect.x = self.pos[0]
                self.rect.y = self.pos[1]
        else:
            newPos = Func.getRealPosition(mousePos, status.offset_x, status.offset_y)
            if status.actionShift_direction == "vertical":
                self.pos[0] = newPos[0] + status.shift_x_cursor
                self.rect.x = self.pos[0]
            elif status.actionShift_direction == "horizontal":
                self.pos[1] = newPos[1] + status.shift_y_cursor
                self.rect.y = self.pos[1]
            else:
                self.pos[0] = newPos[0] + status.shift_x_cursor
                self.pos[1] = newPos[1] + status.shift_y_cursor
                self.rect.x = self.pos[0]
                self.rect.y = self.pos[1]

    def updateIndex(self,index):
        self.index = index
        self.image = Setting.imageBlock[self.type][self.index]
        rect = self.image.get_rect()
        self.rect.width = rect.width
        self.rect.height = rect.height

    def updateType(self,type,index):
        if Setting.blockSetting[type]["indexChange"] == True:
            self.index = index
        else:
            self.index = Setting.blockSetting[type]["defaultIndex"]
        self.type = type
        self.image = Setting.imageBlock[type][self.index]
        rect = self.image.get_rect()
        self.rect.width = rect.width
        self.rect.height = rect.height

    def draw(self,screen,offset_x,offset_y):
        screen.blit(self.image,(self.pos[0]+offset_x,self.pos[1]+offset_y))