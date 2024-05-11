from pygame import Rect,sprite
from math import sqrt,cos,sin,atan
from System import Constant

def checkCollision(skill,objects):
        for object in objects:
            if sprite.collide_rect(skill,object):
                skill.end()
    
def attackPlayer(skill,players):
    check = False
    for player in players:
        if player.isDead: continue
        if sprite.collide_rect(skill,player):
            player.getHit(skill.damage,0,skill.attack_type,skill.boss)
            check = True
        if player.pets != None:
            if sprite.collide_rect(skill,player.pets):
                player.pets.getHit(skill.damage,0,skill.attack_type,skill.boss)
                check = True
    return check

class DropBubbles():
    def __init__(self,boss):
        self.skillName = "DropBubbles"
        self.rect = Rect(boss.rect.x+(boss.rect.width-Constant.player_size*1.4)//2, boss.rect.y,Constant.player_size*1.4,Constant.player_size*1.4)
        self.damage = boss.magic_damage
        self.attack_type = "magic"
        self.boss = boss
        self.direction = boss.direction
        self.animation_count = 0
        self.animation_delay = 3
        self.getSpeech()

    def getSpeech(self):
        target = self.boss.getTarget()[0]
        if target == None: 
            self.end()
            return

        h1 = Constant.block_size * 3
        h2 = Constant.block_size * 3
        if self.rect.y < target.rect.y:
            h2 += (target.rect.y - self.rect.y)
        elif self.rect.y > target.rect.y:
            h1 += (self.rect.y - target.rect.y)

        self.speed_y = sqrt(2*h1/Constant.gravity) * Constant.gravity
        x = target.rect.x + target.rect.width // 2 - (self.rect.x + self.rect.width // 2)
       
        self.speed_x = x / (sqrt(2*h1/Constant.gravity) + sqrt(2*h2*Constant.gravity)) + target.x
    
    def loop(self,players,objects,limitMap):
        self.animation_count += 1
        self.rect.x += self.speed_x
        self.rect.y -= self.speed_y
        self.speed_y -= Constant.gravity

        if attackPlayer(self,players): 
            self.end()
            return
        checkCollision(self,objects)
        if self.rect.x < limitMap[0] or self.rect.x + self.rect.width > limitMap[1]: self.end()
    
    def end(self):
        if self in self.boss.skills:
            self.boss.skills.remove(self)
    
class ShootBubbles():
    def __init__(self,boss):
        self.skillName = "ShootBubbles"
        self.rect = Rect(boss.rect.x+(boss.rect.width-Constant.player_size*1.6)//2, boss.rect.y + boss.rect.height//3,Constant.player_size*1.6,Constant.player_size*1.6)
        self.damage = boss.magic_damage
        self.attack_type = "magic"
        self.attack_range = Constant.block_size * 10
        self.boss = boss
        self.direction = boss.direction
        self.animation_count = 0
        self.animation_delay = 3
        if self.direction == "left": self.speed_run = -12
        else: self.speed_run = 12

    def loop(self,players,objects,limitMap):
        self.animation_count += 1
        self.rect.x += self.speed_run
        self.attack_range -= abs(self.speed_run)
        if attackPlayer(self,players) or self.attack_range <= 0:
            self.end()
            return
        checkCollision(self,objects)
        if self.rect.x < limitMap[0] or self.rect.x + self.rect.width > limitMap[1]: self.end()

    def end(self):
        if self in self.boss.skills:
            self.boss.skills.remove(self)

class PersureBubbles:
    def __init__(self,boss):
        self.skillName = "PersureBubbles"
        self.rect = Rect(boss.rect.x+(boss.rect.width-Constant.player_size*1.6)//2, boss.rect.y + boss.rect.height//3,Constant.player_size*1.6,Constant.player_size*1.6)
        self.damage = boss.magic_damage*5
        self.attack_type = "magic"
        self.boss = boss
        self.direction = boss.direction
        self.animation_count = 0
        self.animation_delay = 3
        self.enemy_target = boss.getTarget()[0]
        self.speed_run = 4

    def loop(self,players,objects,limitMap):
        self.animation_count += 1

        if attackPlayer(self,players): self.end()
        if self.enemy_target.isDead: self.end()
        
        x = self.rect.x - (self.enemy_target.rect.x + self.enemy_target.rect.width // 2)
        y = self.rect.y - (self.enemy_target.rect.y + self.enemy_target.rect.height // 2)
        if x != 0:
            a = atan(y/x)
            speech_x = abs(cos(a) * self.speed_run)
            speech_y = abs(sin(a) * self.speed_run)
        else:
            speech_y = self.speed_run
            speech_x = 0
        if y > 0: speech_y = -speech_y
        if x > 0: speech_x = -speech_x

        if x > 0: self.direction = "left"
        else: self.direction = "right"

        self.rect.x += speech_x
        self.rect.y += speech_y

    def end(self):
        if self in self.boss.skills:
            self.boss.skills.remove(self)
