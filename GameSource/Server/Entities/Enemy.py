import math
import random
from pygame.sprite import collide_rect
from System import Constant
from Entities import CommonEntity,TextDamage

class Enemy(CommonEntity.CommonEntity):
    def __init__(self,id,x,y,width,height,charName):
        super().__init__(id,x,y,width,height,charName)
        self.initPos = (x,y)
        self.animation_delay = 5
        
        self.max_hp = 500
        self.hp = self.max_hp
        self.physical_damage = 30
        self.magic_damage = 30
        self.physical_armor = 5
        self.magic_armor = 5
        self.physical_armor_penetration = 0
        self.magic_armor_penetration = 0
        self.crit_rate = 10
        self.crit_damage = 100
        self.attack_range = 2
        self.speed_run = 1
        self.speed_jump = 9

        self.attack_delay = Constant.FPS//2
        self.attack_speed = 90

        self.enemy_target = []
        self.not_hit_count = 0
        self.notRunCout = 0
        self.notRunLimit = 30
        self.is_heal = False
        self.heal_count = 0
        self.heal_delay = Constant.FPS//2
        self.heal_per_second = self.max_hp // 10
        self.stop_count = 0
        self.limit_stop = 5*Constant.FPS
        self.limit_run = 0
        self.pursue_range = 8
        self.exp = 10
    
    def setProperties(self,hightestLevel):
        self.level = max(int(hightestLevel * random.uniform(0.8,1.2)),1)
        self.max_hp = int(self.max_hp * (1 + (self.level) * 0.2))
        self.hp = self.max_hp
        self.physical_damage = int(self.physical_damage * (1 + (self.level) * 0.2))
        self.magic_damage = int(self.magic_damage * (1 + (self.level) * 0.2))
        self.physical_armor = int(self.physical_armor * (1 + (self.level) * 0.2))
        self.magic_armor = int(self.magic_armor * (1 + (self.level) * 0.2))
        self.physical_armor_penetration = int(self.physical_armor_penetration * (1 + (self.level) * 0.2))
        self.magic_armor_penetration = int(self.magic_armor_penetration * (1 + (self.level) * 0.2))
        self.crit_rate = int(self.crit_rate * (1 + (self.level) * 0.2))
        self.crit_damage = int(self.crit_damage * (1 + (self.level) * 0.2))
        self.exp = int(self.exp * (1 + (self.level) * 0.1))

    def loop(self,objects,mapLimit):
        if(self.checkMove(objects,mapLimit)): 
            self.notRunCout = 0
            self.move(self.x,self.y)
        else: 
            self.notRunCout += 1
            if(self.notRunCout > self.notRunLimit): 
                self.notRunCout = 0
                self.getLimitRun()
            self.move(0,self.y)
        self.checkFall(objects)
        self.y += min(1,(self.fall_count / Constant.FPS) * Constant.gravity)
        if(self.fall_count == 0): self.jump_count = 0
        self.fall_count += 1
        if(self.is_heal): self.heal()
        
        if(len(self.enemy_target) == 0): 
            self.run()
            if(self.hp < self.max_hp): self.not_hit_count += 1
            if(self.not_hit_count > Constant.FPS*5):
                self.is_heal = True
                self.not_hit_count = 0
                self.attack_count = int(self.attack_delay/(self.attack_speed/100))
        else: 
            if(self.attack_count > 0): self.attack_count -= 1
            self.pursue()
            self.attackEnemy()
            target = self.getTarget()
            if target[1] > 0: self.direction = "left"
            else: self.direction = "right"
            
        self.update()
        if(self.hit_count): self.hit_count-=1
      
    def checkMove(self,objects,mapLimit):
        self.move(self.x,0)
        if self.rect.x < mapLimit[0] or self.rect.x + self.rect.width > mapLimit[1]:
            self.move(-self.x,0)
            self.getLimitRun()
            return False
        for obj in objects:
            if collide_rect(obj,self):
                if(self.jump_count < 2): self.jump()
                self.move(-self.x,0)
                return False
        self.move(-self.x,0)
        return True
    
    def getHit(self,damage,penetration,typeDamage,target,isPet):
        if penetration == None or typeDamage == "true": finalDamage = int(damage)
        else: finalDamage = int(self.damageDecrease(damage,penetration,typeDamage))
        self.hp -= finalDamage
        self.textDamages.append(TextDamage.textDamage(self.rect.x ,self.rect.y,self.rect.width,self.rect.height,finalDamage,typeDamage))
        
        if target != None:
            if not isPet: 
                if self.hp < 0:
                    target.totalDamage += finalDamage + self.hp
                else:
                    target.totalDamage += finalDamage
            if target not in self.enemy_target:
                if(isPet): 
                    self.enemy_target.append(target.player)
                    if(target.player.enemy_target == None): target.player.enemy_target = self
                    if(target.enemy_target == None): target.enemy_target = self
                else:
                    if(target.enemy_target == None): target.enemy_target = self
                    if(target.pets != None):
                        if(target.pets.enemy_target == None): target.pets.enemy_target = self
                self.enemy_target.append(target)

        if self.hp <= 0: 
            self.die()
            return
        
        self.hit_count = self.hit_count_limit
        self.is_heal = False
        self.not_hit_count = 0

    def attackEnemy(self):
        if(self.attack_count == 0):
            target = self.getTarget()
            if(target[0] == None): return
            if(math.sqrt(target[1]*target[1] + target[2]*target[2]) <= Constant.block_size*self.attack_range):
                self.attack_count = int(self.attack_delay/(self.attack_speed/100))
                target[0].getHit(self.physical_damage,self.physical_armor_penetration,"physical",self)
                if(target[0].hp <= 0):
                    self.enemy_target.remove(target[0])
                    self.px = 0
   
    def heal(self):
        if(self.hp < self.max_hp):
            if(self.heal_count >= self.heal_delay):
                self.heal_count = 0
                if(self.hp + self.heal_per_second > self.max_hp):
                    self.textDamages.append(TextDamage.textDamage(self.rect.x,self.rect.y,self.rect.width,self.rect.height,self.max_hp-self.hp,"heal"))
                    self.hp = self.max_hp
                else: 
                    self.textDamages.append(TextDamage.textDamage(self.rect.x,self.rect.y,self.rect.width,self.rect.height,self.heal_per_second,"heal"))
                    self.hp += self.heal_per_second
        else: self.is_heal = False
        self.heal_count += 1
    def getTarget(self):
        for enemy in self.enemy_target:
            if enemy.isDead: self.enemy_target.remove(enemy)
        if(len(self.enemy_target) == 0): return (None,0,0)
        target = self.enemy_target[0]
        px = self.rect.x + self.rect.width//2 - self.enemy_target[0].rect.x - self.enemy_target[0].rect.width//2
        py = self.rect.y + self.rect.height//2  - self.enemy_target[0].rect.y - self.enemy_target[0].rect.height//2
        for enemy in self.enemy_target:
            pxx = self.rect.x + self.rect.width//2 - enemy.rect.x - enemy.rect.width//2
            pyy = self.rect.y + self.rect.height//2 - enemy.rect.y - enemy.rect.height//2
            if(math.sqrt(pxx*pxx+pyy*pyy) < math.sqrt(px*px+py*py)):
                px = pxx
                py = pyy
                target = enemy
        return (target,px,py)
    def pursue(self):
        target = self.getTarget()
        if(target[0] == None): return
        newPos = self.rect.x - self.initPos[0]
        if(abs(newPos) < self.pursue_range * Constant.block_size):
            if(math.sqrt(target[1]*target[1] + target[2]*target[2]) > Constant.block_size * self.attack_range*0.8 and abs(target[1]) > (target[0].speed_run*0.8)):
                if(target[1]<0): self.move_right(target[0].speed_run*0.8)
                elif(target[1]>0): self.move_left(target[0].speed_run*0.8)
            else: 
                self.x = 0
        else: 
            if(abs(target[0].rect.x - self.initPos[0]) > self.pursue_range * Constant.block_size):
                self.x = 0
                self.stop_count+=1
                if(self.stop_count >= self.limit_stop):
                    self.stop_count = 0
                    self.limit_run = 0
                    self.enemy_target.pop()
                    self.is_heal = True
            else:
                if(newPos > 0): self.x = -self.speed_run
                else: self.x = self.speed_run
                self.stop_count = 0
                
    def run(self):
        if(self.x == 0): self.getLimitRun()
        if(self.limit_run > 0): 
            if(self.rect.x - self.initPos[0]  > self.limit_run * Constant.block_size): self.getLimitRun()
        else: 
            if(self.rect.x - self.initPos[0]  < self.limit_run * Constant.block_size): self.getLimitRun()

    def getLimitRun(self):
        preLimitRun = self.limit_run
        self.limit_run = random.randint(-4,4)
        while(abs(self.limit_run - preLimitRun) < 1):
            self.limit_run = random.randint(-4,4)
        if(self.limit_run > 0): self.move_right(0)
        else: self.move_left(0)
   
    def die(self):
        self.isDead = True

    
