import math
import random
from pygame.sprite import collide_rect
from System import Constant
from Entities import Skill,NormalAttack,Pet,CommonEntity,TextDamage

class Player(CommonEntity.CommonEntity):
    def __init__(self,id,x,y,width,height,charName):
        super().__init__(id,x,y,width,height,charName)

        self.max_hp = 2000
        self.hp = self.max_hp
        self.max_mp = 1000
        self.mp = self.max_mp 
        self.physical_damage = 200
        self.magic_damage = 200
        self.crit_rate = 100
        self.crit_damage = 150
        self.life_steal = 10
        self.physical_armor = 10
        self.magic_armor = 10
        self.physical_armor_penetration = 0
        self.magic_armor_penetration = 0
        self.attack_range = 2
        self.attack_speed = 100 
        self.speed_run = 5
        self.speed_jump = 9

        self.weapon = "sword"
        self.showWeapon = True

        self.hpPotion = 30
        self.mpPotion = 30
        self.hpCD = 10*Constant.FPS
        self.mpCD = 10*Constant.FPS
        self.hpCDCount = 0
        self.mpCDCount = 0

        self.isInGates = False
        self.textDamages = None
        
        self.enemy_target = None
        self.pets = None
        self.skills = []
        self.normalAttack = []
        self.exp = 0
        self.expNextLevel = Constant.level_up_step[self.level-1]

        self.message = None
        self.message_time_life = 0
        
        self.diamond = 0

        self.totalDamage = 0
        self.totalGetHit = 0
        self.totalHeal = 0

    def setProperties(self, properties):
        self.max_hp = properties["max_hp"]
        self.hp = self.max_hp
        self.max_mp = properties["max_mp"]
        self.mp = self.max_mp
        self.physical_damage = properties["physical_damage"]
        self.magic_damage = properties["magic_damage"]
        self.crit_rate = properties["crit_rate"]
        self.crit_damage = properties["crit_damage"]
        self.life_steal = properties["life_steal"]
        self.physical_armor = properties["physical_armor"]
        self.magic_armor = properties["magic_armor"]
        self.physical_armor_penetration = properties["physical_armor_penetration"]
        self.magic_armor_penetration= properties["magic_armor_penetration"]
        self.attack_speed = properties["attack_speed"]
        self.speed_run = properties["speed_run"]
        self.skills = []
        self.level = properties["level"]

    def loop(self,objects,mapLimit):
        if(self.message_time_life > 0): 
            self.message_time_life -= 1
            if(self.message_time_life == 0): self.message = None

        if self.hpCDCount > 0: self.hpCDCount -= 1
        if self.mpCDCount > 0: self.mpCDCount -= 1

        if self.isInGates: return
        self.y += min(1,(self.fall_count / Constant.FPS) * Constant.gravity)
        
        if self.checkMove(objects,mapLimit,self.x):
            self.move(self.x,self.y)
        if(self.fall_count == 0): self.jump_count = 0
        self.fall_count += 1
        self.checkFall(objects)
        self.update()
        if(self.hit_count): self.hit_count-=1
        if(self.attack_count > 0): self.attack_count -= 1
       
    def checkMove(self,objects,mapLimit,px):
        self.move(px,0)
        if self.rect.x < mapLimit[0] or self.rect.x + self.rect.width > mapLimit[1]:
            self.move(-px,0)
            return False
        for obj in objects:
            if collide_rect(obj,self):
                self.move(-px,0)
                return False
        self.move(-px,0)
        return True

    def move(self,dx,dy):
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        self.status = "idle"
        if self.isDead: self.status = "die"
        elif self.hit_count > 0:
            self.status = "hit"
        elif self.y < 0:
            if self.jump_count == 1:
                self.status = "jump"
            elif self.jump_count == 2:
                self.status = "double_jump"
        elif self.y > Constant.gravity * 2:
            self.status = "fall"
        elif self.x != 0:
            self.status = "run"
        self.animation_count += 1
        if(self.animation_count > 1000): self.animation_count = 0

    def checkFall(self, objects):
        for obj in objects:
            if collide_rect(self, obj):
                if self.y > 0:
                    if self.y > Constant.gravity * 30:
                        damage = int((self.y - Constant.gravity * 30)*self.max_hp*0.06)
                        if damage > 0:
                            self.getHit(damage,None,"physical",None)   
                            self.hit_count = Constant.FPS // 9

                    self.fall_count = 0
                    self.y = 0
                    self.jump_count = 0
                    self.rect.bottom = obj.rect.top
                elif self.y < 0:
                    self.y = 1
                    self.rect.top = obj.rect.bottom

    def handleNormalAttack(self):
        if(self.attack_count == 0):
            self.attack_count = int(self.attack_delay/(self.attack_speed/100))
            self.normalAttack.clear()
            self.normalAttack.append(NormalAttack.swordAttack(self))

    def handleSkillAttack(self,damage,typeDamage,target):
        if target.hp <= 0: return
        target.getHit(damage,self.getPenetration(typeDamage),typeDamage,self,False)
        if(target.hp <= 0):
            self.expUp(target.exp)
            if(id(self.enemy_target) == id(target)): self.enemy_target = None

    def handleWeaponAttack(self,damage,typeDamage,target):
        if target.hp <= 0: return
        finalDamage = self.damageCrit(damage)
        if(target.hp < finalDamage): self.health(target.hp * (self.life_steal/100))
        else: self.health(finalDamage * (self.life_steal/100))
        target.getHit(finalDamage,self.getPenetration(typeDamage),typeDamage,self,False)
        if(target.hp <= 0):
            self.expUp(target.exp)
            if(id(self.enemy_target) == id(target)): self.enemy_target = None
     
    def handleMove(self,objects,mapLimit,keys):
        if self.isDead: return
        self.x = 0
        if keys["left"]:
            if self.checkMove(objects,mapLimit,-self.speed_run):
                self.move_left(0)

        if keys["right"]:
            if self.checkMove(objects,mapLimit,self.speed_run):
                self.move_right(0)
     
        if keys["up"]:
            if(self.jump_count < 2):
                self.jump()

        if keys["health"]:
            if(self.hpPotion>0) and self.hpCDCount == 0:
                self.hpCDCount = self.hpCD
                self.hpPotion -= 1
                self.health(self.max_hp*0.05)

        if keys["mana"]:
            if(self.mpPotion>0) and self.mpCDCount == 0:
                self.mpCDCount = self.mpCD
                self.mpPotion -= 1
                self.recoverMana(self.max_mp*0.05)

    def damageCrit(self,damage):
        crit = random.randint(0,100)
        if(crit <= self.crit_rate):
            return int(damage * (1 + self.crit_damage/100))
        return int(damage)
    
    def expUp(self,exp):
        if self.exp != "max":
            self.exp += exp
            self.textDamages.append(TextDamage.textDamage(self.rect.x,self.rect.y,self.rect.width,self.rect.height,exp,"exp"))
            if(self.exp >= Constant.level_up_step[self.level-1]):
                if self.level < len(Constant.level_up_step):
                    self.levelUp()
                else:
                    self.exp = "max"

    def health(self,health,isOther = False):
        if self.hp == self.max_hp: return
        health = int(health)
        if(self.hp + health > self.max_hp): 
            self.textDamages.append(TextDamage.textDamage(self.rect.x,self.rect.y,self.rect.width,self.rect.height,self.max_hp - self.hp,"heal"))
            self.hp = self.max_hp
            if not isOther: 
                self.totalHeal += self.max_hp - self.hp
        else:
            self.textDamages.append(TextDamage.textDamage(self.rect.x,self.rect.y,self.rect.width,self.rect.height,health,"heal"))
            self.hp += health
            if not isOther:
                self.totalHeal += health

    def recoverMana(self,mana):
        if self.mp == self.max_mp: return
        mana = int(mana)
        if(self.mp + mana > self.max_mp): 
            self.mp = self.max_mp
        else:
            self.mp += mana

    def getHit(self,damage,penetration,typeDamage,enemy,isPet = False):
        if self.isDead or self.isInGates: return
        self.hit_count = self.hit_count_limit
        if penetration == None or typeDamage == "true": finalDamage = int(damage)
        else: finalDamage = int(self.damageDecrease(damage,penetration,typeDamage))

        if self.hp - finalDamage < 0: 
            self.hp = 0
            self.totalGetHit += finalDamage - self.hp
        else: 
            self.hp -= finalDamage
            self.totalGetHit += finalDamage

        self.textDamages.append(TextDamage.textDamage(self.rect.x,self.rect.y,self.rect.width,self.rect.height,finalDamage,typeDamage))
        if self.hp <= 0: 
            self.die()
            return

        if enemy != None:
            if self.enemy_target == None:
                self.enemy_target = enemy
            if(self.pets != None):
                self.pets.enemy_target = enemy

    def revival(self,hp,mp):
        self.isDead = False
        print(self.id,self.isDead)
        self.hp = int(hp)
        self.mp = int(mp)
    
    def nextMap(self,x,y,textDamages):
        self.rect.x = x
        self.rect.y = y
        self.textDamages = textDamages
        self.isInGates = False
        self.enemy_target = None
        if self.pets != None:
            self.pets.resetPos()
        if self.isDead:
            self.revival(self.max_hp,self.max_mp)
    def die(self):
        self.isDead = True
        self.x = 0
        self.pets = None


class Healer(Player):
    def __init__(self,id,x,y,width,height,charName):
        super().__init__(id,x,y,width,height,charName)

        self.max_hp = 1500
        self.hp = self.max_hp
        self.max_mp = 1500
        self.mp = self.max_mp 
        self.physical_damage = 0
        self.magic_damage = 200
        self.crit_rate = 10
        self.crit_damage = 100
        self.life_steal = 10
        self.physical_armor = 0
        self.magic_armor = 0
        self.physical_armor_penetration = 0
        self.magic_armor_penetration = 0
        self.attack_range = 7
        self.attack_speed = 100 
        self.speed_run = 5
        self.speed_jump = 9

        self.weapon = "magicRod"
        self.conditionSkill = Skill.HealerConditionSkill()
        self.listSkills = ["heal","debuffEnemy","buffPlayers","revival"]

    def handleNormalAttack(self):
        if(self.enemy_target != None and self.attack_count == 0):
            px = self.rect.x + self.rect.width//2 - self.enemy_target.rect.x - self.enemy_target.rect.width//2
            py = self.rect.y + self.rect.height//2 - self.enemy_target.rect.y - self.enemy_target.rect.height//2
            if(math.sqrt(px*px+py*py) <= Constant.block_size*self.attack_range):
                if px > 0: self.direction = "left"
                else: self.direction = "right"
                self.attack_count = int(self.attack_delay/(self.attack_speed/100))
                self.normalAttack.append(NormalAttack.Dendro(self))

    def handleUseSkill(self,players,keys):
        if self.isDead: return
        if keys["skill1"]:
            if(self.conditionSkill.heal(self)):
                skill = Skill.Heal(self,players)
                # self.skills.append(skill)
           
        if keys["skill2"]:
            if(self.conditionSkill.debuffEnemy(self)):
                skill = Skill.DebuffEnemy(self)
                self.skills.append(skill)

        if keys["skill3"]:
            if(self.conditionSkill.buffPlayers(self)):
                skill = Skill.BuffPlayers(self,players)
                self.skills.append(skill)

        if keys["skill4"]:
            if(self.conditionSkill.revival(self)):
                skill = Skill.Revival(self,players)
                # self.skills.append(skill)

    def levelUp(self):
        self.exp -= Constant.level_up_step[self.level-1]
        self.expNextLevel = Constant.level_up_step[self.level]
        self.level += 1
        self.max_hp += int(self.max_hp*0.03)
        self.max_mp += int(self.max_mp*0.03)
        self.magic_damage += int(self.magic_damage*0.02)
        self.crit_rate += 1
        self.crit_damage += 1
        self.life_steal += 1
        self.attack_speed += 5
        self.magic_armor_penetration += 5

class Wizard(Player):
    def __init__(self,id,x,y,width,height,charName):
        super().__init__(id,x,y,width,height,charName)

        self.max_hp = 1000
        self.hp = self.max_hp
        self.max_mp = 2000
        self.mp = self.max_mp 
        self.physical_damage = 0
        self.magic_damage = 200
        self.crit_rate = 10
        self.crit_damage = 100
        self.life_steal = 10
        self.physical_armor = 0
        self.magic_armor = 0
        self.physical_armor_penetration = 0
        self.magic_armor_penetration = 50
        self.attack_range = 7
        self.attack_speed = 100 
        self.speed_run = 5
        self.speed_jump = 9

        self.weapon = "magicRod"
        self.conditionSkill = Skill.WizardConditionSkill()
        self.listSkills = ["dragon","meteorites","burn","fireBall"]
    def handleNormalAttack(self):
        if(self.enemy_target != None and self.attack_count == 0):
            px = self.rect.x + self.rect.width//2 - self.enemy_target.rect.x - self.enemy_target.rect.width//2
            py = self.rect.y + self.rect.height//2 - self.enemy_target.rect.y - self.enemy_target.rect.height//2
            if(math.sqrt(px*px+py*py) <= Constant.block_size*self.attack_range):
                if px > 0: self.direction = "left"
                else: self.direction = "right"
                self.attack_count = int(self.attack_delay/(self.attack_speed/100))
                self.normalAttack.append(NormalAttack.Pyro(self))
    
    def handleUseSkill(self,players,keys):
        if self.isDead: return
        if keys["skill1"]:
            if(self.conditionSkill.dragon(self)):
                skill = Skill.Dragon(self)
                self.skills.append(skill)
           
        if keys["skill2"]:
            if(self.conditionSkill.meteorites(self)):
                skill = Skill.Meteorites(self)
                self.skills.append(skill)

        if keys["skill3"]:
            if(self.conditionSkill.burn(self)):
                skill = Skill.Burn(self)
                self.skills.append(skill)

        if keys["skill4"]:
            if(self.conditionSkill.fireBall(self)):
                skill = Skill.FireBall(self)
                self.skills.append(skill)
    def levelUp(self):
        self.exp -= Constant.level_up_step[self.level-1]
        self.expNextLevel = Constant.level_up_step[self.level]
        self.level += 1
        self.max_hp += int(self.max_hp*0.01)
        self.max_mp += int(self.max_mp*0.05)
        self.magic_damage += int(self.magic_damage*0.03)
        self.crit_rate += 3
        self.crit_damage += 5
        self.life_steal += 5
        self.attack_speed += 8
        self.magic_armor_penetration += 10

class Assassin(Player):
    def __init__(self,id,x,y,width,height,charName):
        super().__init__(id,x,y,width,height,charName)
   
        self.max_hp = 2000
        self.hp = self.max_hp
        self.max_mp = 1000
        self.mp = self.max_mp 
        self.physical_damage = 50
        self.magic_damage = 0
        self.crit_rate = 40
        self.crit_damage = 100
        self.life_steal = 10
        self.physical_armor = 20
        self.magic_armor = 20
        self.physical_armor_penetration = 50
        self.magic_armor_penetration = 10
        self.attack_range = 7
        self.attack_speed = 100 
        self.speed_run = 5
        self.speed_jump = 9

        self.weapon = "sword"
        self.conditionSkill = Skill.AssassinConditionSkill()
        self.listSkills =  ["slash","flash","assassinBuff","teleport"]
    def handleNormalAttack(self):
        if(self.attack_count == 0):
            self.attack_count = int(self.attack_delay/(self.attack_speed/100))
            self.normalAttack.clear()
            self.normalAttack.append(NormalAttack.swordAttack(self))

    def handleUseSkill(self,players,keys):
        if self.isDead: return
        if keys["skill1"]:
            if(self.conditionSkill.slash(self)):
                skill = Skill.Slash(self)
                self.skills.append(skill)
           
        if keys["skill2"]:
            if(self.conditionSkill.flash(self)):
                skill = Skill.Flash(self)
                self.skills.append(skill)

        if keys["skill3"]:
            if(self.conditionSkill.assassinBuff(self)):
                skill = Skill.AssassinBuff(self)
                self.skills.append(skill)

        if keys["skill4"]:
            if(self.conditionSkill.teleport(self)):
                skill = Skill.Teleport(self)
                self.skills.append(skill)

    def levelUp(self):
        self.exp -= Constant.level_up_step[self.level-1]
        self.expNextLevel = Constant.level_up_step[self.level]
        self.level += 1
        self.max_hp += int(self.max_hp*0.04)
        self.max_mp += int(self.max_mp*0.02)
        self.physical_damage += int(self.magic_damage*0.03)
        self.crit_rate += 5
        self.crit_damage += 8
        self.life_steal += 8
        self.attack_speed += 8
        self.physical_armor += 5
        self.magic_armor += 5
        self.physical_armor_penetration += 10

class Paladin(Player):
    def __init__(self,id,x,y,width,height,charName):
        super().__init__(id,x,y,width,height,charName)
   
        self.max_hp = 3000
        self.hp = self.max_hp
        self.max_mp = 1000
        self.mp = self.max_mp 
        self.physical_damage = 10
        self.magic_damage = 10
        self.crit_rate = 10
        self.crit_damage = 100
        self.life_steal = 10
        self.physical_armor = 50
        self.magic_armor = 50
        self.physical_armor_penetration = 5
        self.magic_armor_penetration = 5
        self.attack_range = 7
        self.attack_speed = 100 
        self.speed_run = 5
        self.speed_jump = 9

        self.weapon = "sword"
        self.conditionSkill = Skill.PaladinConditionSkill()
        self.listSkills = ["buffArmor","explosion","autoHealth","summonPet"]
    def handleNormalAttack(self):
        if(self.attack_count == 0):
            self.attack_count = int(self.attack_delay/(self.attack_speed/100))
            self.normalAttack.clear()
            self.normalAttack.append(NormalAttack.swordAttack(self))

    def handleUseSkill(self,players,keys):
        if self.isDead: return
        if keys["skill1"]:
            if(self.conditionSkill.buffArmor(self)):
                skill = Skill.BuffArmor(self)
                self.skills.append(skill)

        if keys["skill2"]:
            if(self.conditionSkill.explosion(self)):
                skill = Skill.Explosion(self)
                self.skills.append(skill)

        if keys["skill3"]:
            if(self.conditionSkill.autoHealth(self)):
                skill = Skill.AutoHealth(self)
                self.skills.append(skill)
        
        if keys["skill4"]:
            if(self.conditionSkill.summonPet(self)):
                if(self.pets == None): 
                    pet = Pet.Pet(self.rect.x,self.rect.y,Constant.block_size,Constant.block_size,self)
                    pet.enemy_target = self.enemy_target
                    self.pets = pet
                else:
                    self.pets.rect.x = self.rect.x
                    self.pets.rect.y = self.rect.y
                    self.pets.hp = self.pets.max_hp
                    self.pets.enemy_target = self.enemy_target
    def levelUp(self):
        self.exp -= Constant.level_up_step[self.level-1]
        self.expNextLevel = Constant.level_up_step[self.level]
        self.level += 1
        self.max_hp += int(self.max_hp*0.05)
        self.max_mp += int(self.max_mp*0.01)
        self.physical_damage += int(self.magic_damage*0.02)
        self.crit_rate += 3
        self.crit_damage += 5
        self.life_steal += 5
        self.attack_speed += 5
        self.magic_armor += 10
        self.physical_armor += 10
        self.physical_armor_penetration += 5