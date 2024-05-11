from pygame.sprite import collide_rect
import math
from System import Constant
from Entities import CommonEntity, TextDamage

class Pet(CommonEntity.CommonEntity):
    def __init__(self,x,y,width,height,player):
        super().__init__(0,x,y,width,height,"paladinGreen")
        self.max_hp = player.max_hp
        self.hp = self.max_hp
        self.attack_range = 2
        self.physical_damage = player.physical_armor
        self.magic_damage = player.magic_armor
        self.crit_rate = player.crit_rate
        self.crit_damage = player.crit_damage
        self.life_steal = 10
        self.physical_armor = player.physical_armor * 0.5
        self.magic_armor = player.magic_armor * 0.5
        self.physical_armor_penetration = 0
        self.magic_armor_penetration = 0
        self.speed_run = 5
        self.speed_jump = 9

        self.player = player
        self.speed_run = self.player.speed_run - 1
        self.speed_jump = self.player.speed_jump

        self.is_heal = False
        self.heal_count = 0
        self.heal_delay = Constant.FPS // 2
        self.heal_per_second = self.max_hp // 10
        self.not_hit_count = 0

        self.stop_count = 0
        self.limit_stop = 2*Constant.FPS
        self.limit_run = 0
        self.pursue_range = 10
        self.attack_delay = Constant.FPS
        self.attack_range = 1.5
       
        self.enemy_target = None

    def loop(self,objects):
        self.y += min(1,(self.fall_count / Constant.FPS) * Constant.gravity)
        if(self.y > Constant.gravity * 50) : self.y = Constant.gravity * 50
        if(self.fall_count == 0): self.jump_count = 0
        self.fall_count += 1
        if(self.checkMove(objects)): self.move(self.x,self.y)
        else: self.move(0,self.y)
        self.checkFall(objects)
        if(self.is_heal): self.heal()
        if(self.enemy_target == None): 
            self.follow()
            if(self.hp < self.max_hp): self.not_hit_count += 1
            if(self.not_hit_count > Constant.FPS*3):
                self.is_heal = True
                self.not_hit_count = 0
        else: 
            self.pursue()
            self.attackEnemy()
        self.update()
      
        if(self.hit_count > 0): self.hit_count-=1
        if(self.attack_count > 0): self.attack_count -= 1

    def checkMove(self,objects):
        self.move(self.x,0)
        for obj in objects:
            if collide_rect(obj,self):
                if(self.jump_count < 2): self.jump()
                self.move(-self.x,0)
                return False
        self.move(-self.x,0)
        return True
        
    def getHit(self,damage,penetration,typeDamage,enemy,isPet = False):
        if penetration == None or typeDamage == "true": finalDamage = int(damage)
        else: finalDamage = int(self.damageDecrease(damage,penetration,typeDamage))
        self.player.textDamages.append(TextDamage.textDamage(self.rect.x,self.rect.y,self.rect.width,self.rect.height,finalDamage,typeDamage))
        self.hp -= finalDamage
        if self.hp <= 0:
            self.die()
            return 

        if enemy != None:
            self.enemy_target = enemy
        self.hit_count = self.hit_count_limit
        self.is_heal = False
        self.not_hit_count = 0

    def attackEnemy(self):
        if(self.enemy_target != None and self.attack_count == 0):
            if(self.enemy_target.hp <= 0):
                self.player.enemy_target = None
                self.enemy_target = None
            else:
                px = abs(self.rect.x + self.rect.width//2 - self.enemy_target.rect.x - self.enemy_target.rect.width//2)
                py = abs(self.rect.y + self.rect.height//2 - self.enemy_target.rect.y - self.enemy_target.rect.height//2)
                if(math.sqrt(px*px+py*py) <= Constant.block_size*self.attack_range):
                    self.attack_count = self.attack_delay
                    self.enemy_target.getHit(self.physical_damage,self.physical_armor_penetration,"physical",self,isPet = True)
                    if(self.enemy_target.hp <= 0):
                        if hasattr(self.enemy_target,"exp"):
                            self.player.expUp(self.enemy_target.exp)
                        self.player.enemy_target = None
                        self.enemy_target = None

    def heal(self):
        if(self.hp < self.max_hp):
            if(self.heal_count >= self.heal_delay):
                self.heal_count = 0
                if(self.hp + self.heal_per_second  > self.max_hp):
                    self.hp = self.max_hp
                    self.player.textDamages.append(TextDamage.textDamage(self.rect.x,self.rect.y,self.rect.width,self.rect.height,self.max_hp-self.hp,"heal"))
                else: 
                    self.hp += self.heal_per_second 
                    self.player.textDamages.append(TextDamage.textDamage(self.rect.x,self.rect.y,self.rect.width,self.rect.height,self.heal_per_second,"heal"))
        else: self.is_heal = False
        self.heal_count += 1
    def pursue(self):
        newPos = self.rect.x - self.player.rect.x
        if(abs(newPos) < self.pursue_range * Constant.block_size):
            px = self.rect.x + self.rect.width//2 - self.enemy_target.rect.x - self.enemy_target.rect.width//2
            py = self.rect.y + self.rect.height//2 - self.enemy_target.rect.y - self.enemy_target.rect.height//2
            if(px<0): self.direction = "right"
            else: self.direction = "left"
            if(math.sqrt(px*px+py*py) > self.attack_range * Constant.block_size and abs(px) > (self.player.speed_run-1)):
                if(px < 0): self.move_right(0)
                elif(px > 0): self.move_left(0)
            else: 
                self.x = 0
        else: 
            if(abs(self.enemy_target.rect.x - self.player.rect.x) > self.pursue_range * Constant.block_size):
                self.x = 0
                self.stop_count+=1
                if(self.stop_count >= self.limit_stop):
                    self.stop_count = 0
                    self.limit_run = 0
                    self.enemy_target = None
                    self.is_heal = True
            else:
                if(newPos > 0): self.rect.x -= (self.player.speed_run - 1)
                else: self.rect.x += (self.player.speed_run - 1)
                self.stop_count = 0
    def follow(self):
        px = self.rect.x + self.rect.width//2 - self.player.rect.x - self.player.rect.width//2
        py = self.rect.y + self.rect.height//2  - self.player.rect.y - self.player.rect.height//2
        if(math.sqrt(px*px + py*py) > self.rect.width // 2 + self.player.rect.width // 2 and abs(px) > (self.player.speed_run - 1)):
            if(px < 0): self.move_right(round(abs(px)//Constant.block_size/(self.pursue_range//3),1))
            elif(px > 0): self.move_left(round(px//Constant.block_size/(self.pursue_range//3),1))
        else: self.x = 0
        if(math.sqrt(px*px + py*py) > (self.pursue_range + 1) * Constant.block_size):
            self.resetPos()
    def resetPos(self):
        self.enemy_target = None
        self.rect.x = self.player.rect.x
        self.rect.y = self.player.rect.y
        self.y = 0
        self.x = 0
       
    def die(self):
        self.isDead = True
        self.player.pets = None