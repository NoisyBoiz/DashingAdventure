from pygame import Rect
from math import cos,sin,atan
from System import Constant

class NormalAttackFar():
    def __init__(self,player):
        self.id = 6
        self.rect = Rect(player.rect.x,player.rect.y + player.rect.height//2,30,30)
        self.skillName = ""
        self.damage = player.magic_damage
        self.attack_type = "magic"
        self.player = player
        self.animation_count = 0
        self.animation_delay = 2
        self.enemy_target = player.enemy_target
        self.speed_run = 9
        self.limit_run = 10 * Constant.block_size
        self.direction = player.direction
        self.player.showWeapon = False
    def loop(self,enemys,boss,objects):
        self.animation_count += 1
        
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
        if self.rect.colliderect(self.enemy_target.rect):
            self.player.handleWeaponAttack(self.damage,self.attack_type,self.enemy_target)
            self.end()
        
        self.limit_run -= self.speed_run
        if self.limit_run < 0:
            self.end()

    def end(self):
        self.player.showWeapon = True
        self.player.normalAttack.remove(self)
    
class Cryo(NormalAttackFar):
    def __init__(self,player):
        super().__init__(player)
        self.skillName = "Cryo"
class Dendro(NormalAttackFar):
    def __init__(self,player):
        super().__init__(player)
        self.skillName = "Dendro"
class Electro(NormalAttackFar):
    def __init__(self,player):
        super().__init__(player)
        self.skillName = "Electro"
class Hydro(NormalAttackFar):
    def __init__(self,player):
        super().__init__(player)
        self.skillName = "Hydro"
class Pyro(NormalAttackFar):
    def __init__(self,player):
        super().__init__(player)
        self.skillName = "Pyro"

class swordAttack():
    def __init__(self,player):
        self.id = 6
        self.rect = Rect(player.rect.x,player.rect.y,50,50)
        self.skillName = "swordAttack"
        self.damage = player.physical_damage
        self.attack_type = "physical"
        self.player = player
        self.animation_count = 0
        self.animation_delay = max(1,int(self.player.attack_delay/(self.player.attack_speed/100)/8))
        self.updatePosition()
        self.player.showWeapon = False
    def loop(self,enemys,boss,objects):
        self.updatePosition()  
        if self.animation_count == 0:
            self.attackMonster(enemys)
            self.attackMonster(boss)
        self.animation_count += 1
        if self.animation_count // self.animation_delay >= 8:
            self.end()

    def updatePosition(self):
        self.direction = self.player.direction
        if self.direction == "left":
            self.rect.x = self.player.rect.x - 40
            self.rect.y = self.player.rect.y - 6
        else:
            self.rect.x = self.player.rect.x + 48
            self.rect.y = self.player.rect.y - 6
    
    def attackMonster(self,enemys):
        for enemy in enemys:
            if enemy.isDead: continue
            if self.rect.colliderect(enemy.rect):
                self.player.handleWeaponAttack(self.damage,self.attack_type,enemy)

    def end(self):
        self.player.showWeapon = True
        self.player.normalAttack.remove(self)