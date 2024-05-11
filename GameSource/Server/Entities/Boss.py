import random
from Entities import Enemy,BossSkills

class Boss(Enemy.Enemy):
    def __init__(self,id,x,y,width,height,charName):
        super().__init__(id,x,y,width,height,charName)

        self.max_hp = 5000
        self.hp = self.max_hp
        self.physical_damage = 50
        self.magic_damage = 50
        self.physical_armor = 30
        self.magic_armor = 30
        self.physical_armor_penetration = 0
        self.magic_armor_penetration = 0
        self.crit_rate = 100
        self.crit_damage = 150
        self.life_steal = 10
        self.attack_range = 8
        self.speed_run = 2
        self.pursue_range = 30

        self.skills = []
        self.part = 1
        self.skillTimes = 5
        self.endSkill = True
        self.typeSkill = 0
        self.skillInit = False

        self.exp = 1000

    def attackEnemy(self):
        if self.part != 2 and self.hp <= self.max_hp * 0.5:
            self.part = 2
            self.attack_count = 0

        if(self.attack_count == 0):
            if self.endSkill == True:
                self.typeSkill = random.randint(0,2)
                self.endSkill = False
                self.skillInit = False
            if self.typeSkill == 0:
                self.handleSkill1()
            elif self.typeSkill == 1:
                self.handleSkill2()
            elif self.typeSkill == 2:
                self.handleSkill3()

    def handleSkill1(self):
        if self.skillInit == False:
            self.skillInit = True
            self.attack_delay = 5
            if self.part == 1:
                self.skillTimes = 5
            else:
                self.skillTimes = 10

        if self.skillTimes > 0:
            self.skills.append(BossSkills.DropBubbles(self))
            self.skillTimes -= 1
        else:
            self.endSkill = True
            self.attack_delay = 100
        self.attack_count = int(self.attack_delay/(self.attack_speed/100))
            
    def handleSkill2(self):
        if self.skillInit == False:
            self.skillInit = True
            self.attack_delay = 8
            if self.part == 1:
                self.skillTimes = 5
            else:
                self.skillTimes = 10

        if self.skillTimes > 0:
            self.skills.append(BossSkills.ShootBubbles(self))
            self.skillTimes -= 1
        else:
            self.endSkill = True
            self.attack_delay = 100
        self.attack_count = int(self.attack_delay/(self.attack_speed/100))

    def handleSkill3(self):
        self.skills.append(BossSkills.PersureBubbles(self))
        self.endSkill = True
        self.attack_count = 100

