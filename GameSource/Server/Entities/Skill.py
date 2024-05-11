from pygame import Rect,sprite
from math import sqrt,cos,sin,atan
from System import Constant

class Dragon:
    def __init__(self,player):
        self.skillName = "dragon"
        self.rect = Rect(player.rect.x,player.rect.y,Constant.player_size,Constant.player_size)
        self.damage = player.magic_damage
        self.attack_delay = 8
        self.attack_type = "magic"
        self.attack_range = 10 * Constant.block_size
        self.direction = player.direction
        if self.direction == "left": self.speed_run = -10
        else: self.speed_run = 10
        self.attacked = []
        self.end = False
        self.animation_count = 0
        self.animation_delay = 2
    def loop(self,player,enemys,boss,objects,mapLimit):
        self.animation_count += 1
        self.rect.x += self.speed_run
        self.attack_range -= self.speed_run
        if(self.attack_range <= 0):
            self.end = True
            return
        self.attackMonster(player,enemys)
        self.attackMonster(player,boss)
        self.checkCollision(player,objects)

    def attackMonster(self,player,enemys):
        for enemy in enemys:
            if enemy.isDead: continue
            if enemy in self.attacked: continue
            if self.rect.colliderect(enemy.rect):
                player.handleSkillAttack(self.damage,self.attack_type,enemy)
                self.attacked.append(enemy)

    def checkCollision(self,player,objects):
        for object in objects:
            if self.rect.colliderect(object.rect):
                self.end = True

class Meteorites:
    def __init__(self,player):
        self.skillName = "meteorites"
        if player.enemy_target == None: 
            x = player.rect.x
            y = player.rect.y - Constant.block_size * 3
            if player.direction == "left": self.speed_x = -10
            else: self.speed_x = 10
        else: 
            y = player.enemy_target.rect.y - Constant.block_size * 3
            if player.rect.x < player.enemy_target.rect.x: 
                x = player.enemy_target.rect.x - Constant.block_size * 3
                self.speed_x = 10
            else: 
                x = player.enemy_target.rect.x + Constant.block_size * 3
                self.speed_x = -10

        self.rect = Rect(x, y ,Constant.player_size,Constant.player_size)
        self.damage = player.magic_damage
        self.attack_type = "magic"
        self.speed_y = 10
        self.animation_count = 0
        self.animation_delay = 2
        self.attack_range = Constant.block_size * 6
        self.end = False

    def loop(self,player,enemys,boss,objects,mapLimit):
        self.animation_count += 1
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.attack_range -= int(self.speed_x*sqrt(2))
        if self.attack_range <= 0: self.end = True
        elif self.attackMonster(player,boss): self.end = True
        elif self.attackMonster(player,enemys): self.end = True
        elif self.checkCollision(objects): self.end = True

    def attackMonster(self,player,enemys):
        for enemy in enemys:
            if enemy.isDead: continue
            if sprite.collide_rect(self,enemy):
                player.handleSkillAttack(self.damage,self.attack_type,enemy)
                return True
        return False
    def checkCollision(self,objects):
        for object in objects:
            if self.rect.colliderect(object.rect):
                return True
        return False
    
class Burn:
    def __init__(self,player):
        self.skillName = "burn"
        self.target = player.enemy_target
        self.rect = Rect(self.target.rect.x,self.target.rect.y,Constant.block_size,Constant.block_size)
        self.updatePos()
        self.time = 5*Constant.FPS
        self.attack_type = "magic"
        self.end = False
        self.animation_count = 0
        self.animation_delay = 2
    def updatePos(self):
        self.rect.x = self.target.rect.x + (self.target.rect.width - self.rect.width)//2
        self.rect.y = self.target.rect.y + (self.target.rect.height - self.rect.height)//2
    def loop(self,player,enemys,boss,objects,mapLimit):
        self.time -= 1
        if(self.time <= 0):
            self.end = True
            return
        if(self.time%(5*Constant.FPS//20)==0):
            damage = self.target.max_hp * 0.001
            player.handleSkillAttack(damage,self.attack_type,self.target)
        self.animation_count += 1
        self.updatePos()

class FireBall:
    def __init__(self,player):
        self.rect = Rect(player.rect.x,player.rect.y - Constant.block_size, player.rect.width,player.rect.height)
        self.skillName = "fireBall"
        self.damage = player.magic_damage
        self.time = Constant.FPS * 5
        self.animation_count = 0
        self.animation_delay = 2
        self.end = False
    def updatePos(self,player):
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y - Constant.block_size
    def loop(self,player,enemys,boss,objects,mapLimit):
        self.time -= 1
        if(self.time <= 0):
            self.end = True
            return
        if(self.time%(Constant.FPS*5//10)==0):
            if player.enemy_target != None:
                player.skills.append(FireBallSmall(player.enemy_target,self.damage,self.rect.x+self.rect.width//2,self.rect.y+self.rect.height//2))
        self.updatePos(player)
        self.animation_count += 1

class FireBallSmall():
    def __init__(self,target,damage,x,y):
        self.rect = Rect(x,y,30,30)
        self.skillName = "fireBallSmall"
        self.damage = damage
        self.attack_type = "magic"
        self.animation_count = 0
        self.animation_delay = 2
        self.enemy_target = target
        self.speed_run = 9
        self.limit_run = 10 * Constant.block_size
        self.end = False

    def loop(self,player,enemys,boss,objects,mapLimit):
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

        self.rect.x += speech_x
        self.rect.y += speech_y
        if self.rect.colliderect(self.enemy_target.rect):
            player.handleSkillAttack(self.damage,self.attack_type,self.enemy_target)
            self.end = True
            return
        
        self.limit_run -= self.speed_run
        if self.limit_run < 0:
            self.end = True
            return

class Slash:
    def __init__(self,player):
        self.skillName = "slash"
        self.rect = Rect(player.rect.x,player.rect.y,Constant.player_size,Constant.player_size)
        self.updatePos(player)
        self.damage = player.physical_damage*2
        self.attack_type = "physical"
        self.direction = player.direction
        self.animation_count = 0
        self.animation_delay = 1
        self.end = False

        player.showWeapon = False
    def updatePos(self,player):
        self.direction = player.direction
        if player.direction == "left": 
            self.rect.x = player.rect.x - self.rect.width + 10
            self.rect.y = player.rect.y
        else:
            self.rect.x = player.rect.x + player.rect.width - 10
            self.rect.y = player.rect.y

    def loop(self,player,enemys,boss,objects,mapLimit):
        self.animation_count += 1
        self.updatePos(player)
        if self.animation_count > 10: 
            self.end = True
            player.showWeapon = True
            return
        if(self.animation_count%(10//2) == 0):
            self.attackMonster(player,enemys)
            self.attackMonster(player,boss)

    def attackMonster(self,player,enemys):
        for enemy in enemys:
            if enemy.isDead: continue
            if self.rect.colliderect(enemy.rect):
                player.handleWeaponAttack(self.damage,self.attack_type,enemy)

class AssassinBuff:
    def __init__(self,player):
        self.rect = Rect(player.rect.x,player.rect.y,Constant.player_size*1.3,Constant.player_size*1.5)
        self.updatePos(player)
        self.skillName = "assassinBuff"
        self.physical_damage = 20
        self.speed_run = 1
        self.attack_speed = 50
        self.animation_count = 0
        self.animation_delay = 3
        self.time = Constant.FPS * 10
        self.buff(player)
        self.end = False
    def updatePos(self,player):
        self.rect.x = player.rect.x + (player.rect.width - self.rect.width)//2
        self.rect.y = player.rect.y + (player.rect.height - self.rect.height)//2
    def loop(self,player,enemys,boss,objects,mapLimit):
        self.time -=1
        if(self.time <= 0):
            self.debuff(player)
            self.end = True
            return
        self.updatePos(player)
        self.animation_count += 1

    def buff(self,player):
        player.physical_damage += int(player.physical_damage*self.physical_damage/100)
        player.speed_run += self.speed_run
        player.attack_speed += self.attack_speed
    def debuff(self,player):
        player.physical_damage -= int(player.physical_damage*self.physical_damage/100)
        player.speed_run -= self.speed_run
        player.attack_speed -= self.attack_speed
    

class Flash:
    def __init__(self,player):
        self.rect = Rect(player.rect.x,player.rect.y,Constant.player_size,Constant.player_size)
        self.direction = player.direction
        self.updatePos(player)
        self.limitRange = 4 * Constant.block_size
        self.skillName = "flash"
        if player.direction == "left": self.speed = -25
        else: self.speed = 25
        self.damage = player.physical_damage
        self.attack_type = "physical"
        self.attacked = []
        self.end = False
        self.animation_count = 0
        self.animation_delay = 2

    def updatePos(self,player):
        if self.direction == "left": self.rect.x = player.rect.x 
        else: self.rect.x = player.rect.x - Constant.player_size*4
        self.rect.y = player.rect.y

    def loop(self,player,enemys,boss,objects,mapLimit):
        self.animation_count += 1
        self.updatePos(player)
        player.x = 0
        player.y = 0
        if self.checkCollision(player,objects,mapLimit): 
            self.end = True
            return
        player.move(self.speed,0)
        self.attackMonster(player,boss)
        self.attackMonster(player,enemys)
        self.limitRange -= abs(self.speed)
        if self.limitRange <= 0: self.end = True
    def attackMonster(self,player,enemys):
        for enemy in enemys:
            if enemy.isDead: continue
            if enemy in self.attacked: continue
            if player.rect.colliderect(enemy.rect):
                player.handleSkillAttack(self.damage,self.attack_type,enemy)
                self.attacked.append(enemy)

    def checkCollision(self,player,objects,mapLimit):
        player.move(self.speed,0)
        if player.rect.x < mapLimit[0] or player.rect.x + player.rect.width > mapLimit[1]:
            player.move(-self.speed,0)
            return True
        for object in objects:
            if player.rect.colliderect(object.rect):
                if self.speed > 0: x = - player.rect.right + object.rect.left
                else: x = - player.rect.left + object.rect.right
                player.move(x,0)
                return True
        player.move(-self.speed,0)
            

class Teleport:
    def __init__(self,player):
        self.rect = Rect(player.rect.x,player.rect.y,Constant.player_size*2,Constant.player_size*2)
        self.skillName = "teleport"
        self.attack_range = 0
        self.damage = player.physical_damage * 3
        self.attack_type = "physical"
        self.enemy_target = player.enemy_target
        self.animation_count = 0
        self.animation_delay = 2
        self.use(player)
        self.end = False
    def updatePos(self,player):
        self.rect.x = player.rect.x + (player.rect.width - self.rect.width)//2
        self.rect.y = player.rect.y + player.rect.height - self.rect.height

    def use(self,player):
        if player.rect.x < self.enemy_target.rect.x: player.direction = "right"
        else: player.direction = "left"
        player.rect.x = self.enemy_target.rect.x
        player.rect.y = self.enemy_target.rect.y
        player.handleSkillAttack(self.damage,self.attack_type,self.enemy_target)
        self.updatePos(player)
    def loop(self,player,enemys,boss,objects,mapLimit):
        self.animation_count += 1
        if(self.animation_count//self.animation_delay >= 4):
            self.end = True
            return
        
    
class Heal:
    def __init__(self,player,players):
        self.rect = Rect(player.rect.x,player.rect.y,Constant.player_size,Constant.player_size)
        self.skillName = "heal"
        self.healHp = player.magic_damage
        self.use(player,players)
        
    def use(self,player,allPlayer):
        for pl in allPlayer:
            if pl.isDead: continue
            pl.health(self.healHp,True)
            player.totalHeal += self.healHp 
            
        # self.end = True
    def loop(self,player,enemys,boss,objects,mapLimit):
        pass

class DebuffEnemy:
    def __init__(self,player):
        self.skillName = "debuffEnemy"
        self.time = Constant.FPS * 10
        self.target = player.enemy_target
        self.debuff_physical_damage = 50
        self.debuff_magic_damage = 50
        self.debuff_physical_armor = 50
        self.debuff_magic_armor = 50
        self.debuff()
        self.end = False

    def loop(self,player,enemys,boss,objects,mapLimit):
        self.time -= 1
        if(self.time <= 0):
            self.end = True

    def debuff(self):
        self.target.physical_damage = self.target.physical_damage*(1-self.debuff_physical_damage/100)
        self.target.magic_damage = self.target.magic_damage*(1-self.debuff_magic_damage/100)
        self.target.physical_armor = self.target.physical_armor*(1-self.debuff_physical_armor/100)
        self.target.magic_armor = self.target.magic_armor*(1-self.debuff_magic_armor/100)

    def buff(self):
        self.target.physical_damage = self.target.physical_damage/(1-self.debuff_physical_damage/100)
        self.target.magic_damage = self.target.magic_damage/(1-self.debuff_magic_damage/100)
        self.target.physical_armor = self.target.physical_armor/(1-self.debuff_physical_armor/100)
        self.target.magic_armor = self.target.magic_armor/(1-self.debuff_magic_armor/100)

class BuffPlayers:
    def __init__(self,player,players):
        self.skillName = "buffPlayers"
        self.time = Constant.FPS * 10
        self.buffSpeed_run = int(player.speed_run*0.1)
        self.buffSpeed_attack = int(player.magic_damage*0.1)
        self.buffPhysicalDamage = int(player.magic_damage*0.5)
        self.buffMagicDamage = int(player.magic_damage*0.5)
        self.end = False
        self.players = players
        self.buff()

    def loop(self,player,enemys,boss,objects,mapLimit):
        self.time -= 1
        if(self.time <= 0):
            self.end = True
            self.debuff()

    def debuff(self):
        for player in self.players:
            player.speed_run -= self.buffSpeed_run
            player.attack_speed -= self.buffSpeed_attack
            player.physical_damage -= self.buffPhysicalDamage
            player.magic_damage -= self.buffMagicDamage

    def buff(self):
        for player in self.players:
            player.speed_run += self.buffSpeed_run
            player.attack_speed += self.buffSpeed_attack
            player.physical_damage += self.buffPhysicalDamage
            player.magic_damage += self.buffMagicDamage

class Revival:
    def __init__(self,player,players):
        self.skillName = "revival"
        self.use(player,players)
        # self.end = False
        
    def use(self,player,players):
        for pl in players:
            if pl.isDead == True:
                pl.revival(player.magic_damage*2,player.magic_damage*2)
            else:
                pl.health(player.magic_damage*2,True)
            player.totalHeal += player.magic_damage*2

        # self.end = True
    def loop(self,player,enemys,boss,objects,mapLimit):
        pass
    
class BuffArmor:
    def __init__(self,player):
        self.skillName = "buffArmor"
        self.armorBuff = int(player.hp * 0.1)
        self.time = Constant.FPS * 10
        self.buff(player)
        self.end = False
    def loop(self,player,enemys,boss,objects,mapLimit):
        self.time -= 1
        if(self.time <= 0):
            self.end = True
            self.debuff(player)
    def buff(self,player):
        player.physical_armor += self.armorBuff
        player.magic_armor += self.armorBuff
    def debuff(self,player):
        player.physical_armor -= self.armorBuff
        player.magic_armor -= self.armorBuff

class Explosion:
    def __init__(self,player):
        self.rect = Rect(player.rect.x,player.rect.y,Constant.player_size*3.7,Constant.player_size*3.7)
        self.updatePos(player)
        self.skillName = "explosion"
        self.attack_range = self.rect.width // 2
        self.damage = player.hp - 1
        self.attack_type = "magic"
        self.animation_count = 0
        self.animation_delay = 2
        self.attack_times = 1
        self.use(player)
        self.end = False
    def updatePos(self,player):
        self.rect.x = player.rect.x - (self.rect.width - player.rect.width)//2
        self.rect.y = player.rect.y - (self.rect.height - player.rect.height)//2
    def use(self,player):
        player.getHit(player.hp * 0.5, None , "true", None, False)
    def loop(self,player,enemys,boss,objects,mapLimit):
        self.updatePos(player)
        if(self.attack_times == 1):
            self.attackMonster(player,enemys)
            self.attackMonster(player,boss)
            self.attack_times -= 1
        self.animation_count += 1
        if(self.animation_count // self.animation_delay >= 5):
            self.end = True
            return
    def attackMonster(self,player,enemy):
        for enemy in enemy:
            if enemy.isDead: continue
            px = player.rect.x + player.rect.width // 2 - enemy.rect.x - enemy.rect.width // 2
            py = player.rect.y + player.rect.height // 2 - enemy.rect.y - enemy.rect.height // 2
            if(sqrt(px * px + py * py) <= self.attack_range + enemy.rect.width // 2):
                player.handleSkillAttack(self.damage,self.attack_type,enemy)

class AutoHealth:
    def __init__(self,player):
        self.skillName = "autoHealth"
        self.time = Constant.FPS * 5
        self.heal_delay = self.time // 5
        self.healHp = player.max_hp*0.05
        self.end = False
    def loop(self,player,enemys,boss,objects,mapLimit):
        self.time -= 1
        if(self.time <= 0):
            self.end = True
        
        if(self.time%self.heal_delay==0): player.health(self.healHp)
  
class conditionSkill:
    def __init__(self):
        self.CD = {}
        self.Count = {}
        self.Mp = {}   
     
    def loop(self):
        for skill in self.Count:
            if self.Count[skill] > 0: self.Count[skill] -= 1

    def commonCheck(self,player,skillName):
        if self.Count[skillName] > 0: return False
        if player.mp < self.Mp[skillName]: return False
        return True
    
    def commonUse(self,player,skillName):
        player.mp -= self.Mp[skillName]
        self.Count[skillName] = self.CD[skillName]
    
class HealerConditionSkill(conditionSkill):
    def __init__(self):
        super().__init__()
        self.CD = {
            "heal":10 * Constant.FPS,
            "debuffEnemy": 10 * Constant.FPS,
            "buffPlayers": 10 * Constant.FPS,
            "revival": 10 * Constant.FPS,
        }
        self.Count = {
            "heal": 0,
            "debuffEnemy": 0,
            "buffPlayers": 0,
            "revival": 0,
        }
        self.Mp = {
            "heal": 10,
            "debuffEnemy": 10,
            "buffPlayers": 10,
            "revival": 100,
        }
    def heal(self,player):
        skillName = "heal"
        if not self.commonCheck(player,skillName): return False
        self.commonUse(player,skillName)
        return True
    
    def debuffEnemy(self,player):
        skillName = "debuffEnemy"
        if not self.commonCheck(player,skillName): return False
        if player.enemy_target == None: return False
        self.commonUse(player,skillName)
        return True

    def buffPlayers(self,player):
        skillName = "buffPlayers"
        if not self.commonCheck(player,skillName): return False
        self.commonUse(player,skillName)
        return True
    
    def revival(self,player):
        skillName = "revival"
        if not self.commonCheck(player,skillName): return False
        self.commonUse(player,skillName)
        return True
    
class AssassinConditionSkill(conditionSkill):
    def __init__(self):
        super().__init__()
        self.CD = {
            "slash":4 * Constant.FPS,
            "flash":6 * Constant.FPS,
            "assassinBuff": 10 * Constant.FPS,
            "teleport": 3 * Constant.FPS,
        }
        self.Count = {
            "slash": 0,
            "flash": 0,
            "assassinBuff": 0,
            "teleport": 0,
        }
        self.Mp = {
            "slash": 10,
            "flash": 10,
            "assassinBuff": 10,
            "teleport": 10,
        }
    def slash(self,player):
        skillName = "slash"
        if not self.commonCheck(player,skillName): return False
        self.commonUse(player,skillName)
        return True
    
    def flash(self,player):
        skillName = "flash"
        if not self.commonCheck(player,skillName): return False
        self.commonUse(player,skillName)
        return True
    
    def assassinBuff(self,player):
        skillName = "assassinBuff"
        if not self.commonCheck(player,skillName): return False
        self.commonUse(player,skillName)
        return True
    
    def teleport(self,player):
        skillName = "teleport"
        if not self.commonCheck(player,skillName): return False
        if(player.enemy_target == None): return False
        px = player.rect.x + player.rect.width // 2 - player.enemy_target.rect.x - player.enemy_target.rect.width // 2
        py = player.rect.y + player.rect.height // 2 - player.enemy_target.rect.y - player.enemy_target.rect.height // 2 
        if(sqrt(px * px + py * py) > Constant.block_size * 20): return False
        self.commonUse(player,skillName)
        return True
    
class WizardConditionSkill(conditionSkill):
    def __init__(self):
        super().__init__()
        self.CD = {
            "dragon": 2 * Constant.FPS,
            "meteorites": 10 * Constant.FPS,
            "burn": 10 * Constant.FPS,
            "fireBall": 10 * Constant.FPS,
        }
        self.Count = {
            "dragon": 0,
            "meteorites": 0,
            "burn": 0,
            "fireBall": 0,
        }
        self.Mp = {
            "dragon": 10,
            "meteorites": 10,
            "burn": 10,
            "fireBall": 10,
        }
    def dragon(self,player):
        skillName = "dragon"
        if not self.commonCheck(player,skillName): return False
        self.commonUse(player,skillName)
        return True
    def meteorites(self,player):
        skillName = "meteorites"
        if not self.commonCheck(player,skillName): return False
        self.commonUse(player,skillName)
        return True
    def burn(self,player):
        skillName = "burn"
        if not self.commonCheck(player,skillName): return False
        if player.enemy_target == None: return False
        self.commonUse(player,skillName)
        return True
    def fireBall(self,player):
        skillName = "fireBall"
        if not self.commonCheck(player,skillName): return False
        self.commonUse(player,skillName)
        return True
    
class PaladinConditionSkill(conditionSkill):
    def __init__(self):
        super().__init__()
        self.CD = {
            "buffArmor": 10 * Constant.FPS,
            "autoHealth": 10 * Constant.FPS,
            "explosion": 10 * Constant.FPS,
            "summonPet": 3 * Constant.FPS,
        }
        self.Count = {
            "buffArmor": 0,
            "autoHealth": 0,
            "explosion": 0,
            "summonPet": 0,
        }
        self.Mp = {
            "buffArmor": 10,
            "autoHealth": 10,
            "explosion": 10,
            "summonPet": 10,
        }
    def buffArmor(self,player):
        skillName = "buffArmor"
        if not self.commonCheck(player,skillName): return False
        self.commonUse(player,skillName)
        return True
    def autoHealth(self,player):
        skillName = "autoHealth"
        if not self.commonCheck(player,skillName): return False
        self.commonUse(player,skillName)
        return True
    def explosion(self,player):
        skillName = "explosion"
        if not self.commonCheck(player,skillName): return False
        if player.hp <= 1: return False
        self.commonUse(player,skillName)
        return True
    def summonPet(self,player):
        skillName = "summonPet"
        if not self.commonCheck(player,skillName): return False
        self.commonUse(player,skillName)
        return True
    