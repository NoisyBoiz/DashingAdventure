from System import Constant, GlobalSprites, Font
from Function.Func import checkInScreen
from math import sqrt

class Dragon():
    def __init__(self):
        pass

class Meteorites():
    def __init__(self):
        pass

class FireBall():
    def __init__(self):
       pass

class FireBallSmall():
    def __init__(self):
       pass

class Burn():
    def __init__(self):
       pass

class Slash():
    def __init__(self):
        pass

class AssassinBuff():
    def __init__(self):
       pass
    
class Flash():
    def __init__(self):
       pass

class Teleport():
    def __init__(self):
       pass
    
class Heal():
    def __init__(self):
        pass

class DebuffEnemy():
    def __init__(self):
       pass

class BuffPlayers():
    def __init__(self):
       pass

class Revival():
    def __init__(self):
        pass

class BuffArmor():
    def __init__(self):
        pass

class AutoHealth():
    def __init__(self):
        pass

class Explosion():
    def __init__(self):
       pass

class SummonPet():
    def __init__(self):
       pass



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


def DrawSkill(screen,offset_x,offset_y,skill,otherPlayer):
    # if(otherPlayer and not checkInScreen(offset_x,offset_y,skill)): return
    if(skill.skillName == "dragon"):
        status = "init"
        index = skill.animation_count // skill.animation_delay
        if index >= GlobalSprites.lengthSkills["dragon"]["init"]:
            status = "initUp"
            index -= GlobalSprites.lengthSkills["dragon"]["init"]
        index = index%GlobalSprites.lengthSkills["dragon"][status]

        screen.blit(GlobalSprites.skills["dragon"][status+"_"+skill.direction][index],(skill.rect.x - offset_x,skill.rect.y - offset_y))
    elif(skill.skillName == "assassinBuff"):
        if not otherPlayer:
            text = Font.Arial20.render(str((skill.time) // Constant.FPS), True, (0,0,0))
            screen.blit(text,(30,100))
        index = skill.animation_count // skill.animation_delay %  GlobalSprites.lengthSkills["buff"]["buff"]
        screen.blit(GlobalSprites.skills["buff"]["buff"][index],(skill.rect.x - offset_x,skill.rect.y - offset_y))
    elif(skill.skillName == "explosion"):
        index = skill.animation_count // skill.animation_delay
        screen.blit(GlobalSprites.skills["explosion"]["explosion"][index],(skill.rect.x - offset_x,skill.rect.y - offset_y))
    elif(skill.skillName == "teleport"):
        index = skill.animation_count // skill.animation_delay
        screen.blit(GlobalSprites.skills["teleport"]["teleport"][index],(skill.rect.x - offset_x,skill.rect.y - offset_y))
    elif(skill.skillName == "slash"):
        index = skill.animation_count // skill.animation_delay % GlobalSprites.lengthSkills["slash"]["slash"]
        screen.blit(GlobalSprites.skills["slash"]["slash_"+skill.direction][index],(skill.rect.x - offset_x,skill.rect.y - offset_y))
    elif(skill.skillName == "meteorites"):
        index = skill.animation_count // skill.animation_delay % GlobalSprites.lengthSkills["meteorites"]["meteorites"]
        screen.blit(GlobalSprites.skills["meteorites"]["meteorites"][index],(skill.rect.x - offset_x,skill.rect.y - offset_y))
    elif(skill.skillName == "fireBall"):
        index = skill.animation_count // skill.animation_delay % GlobalSprites.lengthSkills["fireBall"]["fireBall"]
        screen.blit(GlobalSprites.skills["fireBall"]["fireBall"][index],(skill.rect.x - offset_x,skill.rect.y - offset_y))
    elif(skill.skillName == "fireBallSmall"):
        index = skill.animation_count // skill.animation_delay % GlobalSprites.lengthSkills["fireBallSmall"]["fireBall"]
        screen.blit(GlobalSprites.skills["fireBallSmall"]["fireBall"][index],(skill.rect.x - offset_x,skill.rect.y - offset_y))
    elif(skill.skillName == "flash"):
        index = skill.animation_count // skill.animation_delay % GlobalSprites.lengthSkills["flash"]["flash"]
        screen.blit(GlobalSprites.skills["flash"]["flash_"+skill.direction][index],(skill.rect.x - offset_x,skill.rect.y - offset_y))
    elif(skill.skillName == "burn"):
        index = skill.animation_count // skill.animation_delay % GlobalSprites.lengthSkills["burn"]["burn"]
        screen.blit(GlobalSprites.skills["burn"]["burn"][index],(skill.rect.x - offset_x,skill.rect.y - offset_y))