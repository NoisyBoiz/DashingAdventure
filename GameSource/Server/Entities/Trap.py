from pygame import Rect
from pygame.sprite import collide_rect, Sprite

class Trap(Sprite):
    def __init__(self,x,y,width,height,name):
        super().__init__()
        self.rect = Rect(x,y,width,height)
        self.animation_count = 0
        self.animation_delay = 6
        self.damage_delay = 10
        self.damage_count = 0
        self.makeHit = False
        self.name = name
    def loop(self,players,isFinish):
        self.update()

        if not isFinish:
            if(self.checkDamage()):
                if not self.attackPlayer(players):
                    self.damage_count = 0

    def update(self):
        self.animation_count += 1
        if self.animation_count > 1000: self.animation_count = 0
    def checkDamage(self):
        if(self.damage_count <= 0):
            self.damage_count = self.damage_delay
            return True
        else:
            self.damage_count -= 1
            return False
    def attackPlayer(self,players):
        check = False
        for player in players:
            if not player.isDead:
                if collide_rect(self,player):
                    player.getHit(int(player.max_hp*0.005),None,"physical",None)
                    check = True
            if player.pets != None:
                if collide_rect(self,player.pets):
                    player.pets.getHit(int(player.pets.max_hp*0.005),None,"physical",None)
                    check = True
        return check

