from pygame import Rect

class Gates:
    def __init__(self,x,y,width,height,index):
        self.rect = Rect(x,y,width,height)
        self.index = index
    def checkPlayerCollision(self,player):
        if self.rect.colliderect(player.rect):
            return True
        return False
    def checkMouseCollision(self,mousePos,offset):
        if self.rect.collidepoint(mousePos[0]+offset[0],mousePos[1]+offset[1]):
            return True
        return False
    def checkEnter(self,player,mousePos,offset):
        if self.checkPlayerCollision(player) and self.checkMouseCollision(mousePos,offset):
            return True
        return False