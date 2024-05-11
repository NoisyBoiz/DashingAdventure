from pygame import Rect
from System import Constant
from pygame.sprite import collide_rect

class CommonEntity():
    def __init__(self,id,x,y,width,height,charName):
        self.rect = Rect(x,y,width,height)
        self.id = id
        self.name = None
        self.x = 0
        self.y = 0

        self.direction = "left"
        self.status = "idle"
        self.characterName = charName

        self.animation_count = 0
        self.animation_delay = 3
        self.attack_count = 0
        self.attack_delay = 20
        self.fall_count = 0
        self.jump_count = 0
        
        self.hit_count = 0
        self.hit_count_limit = Constant.FPS // 2
        
        self.isDead = False

        self.level = 1

    def update(self):
        self.status = "idle"
        if self.hit_count > 0:
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
   
    def checkFall (self, objects):
        for obj in objects:
            if collide_rect(self, obj):
                if self.y > 0:
                    self.fall_count = 0
                    self.y = 0
                    self.jump_count = 0
                    self.rect.bottom = obj.rect.top
                elif self.y < 0:
                    self.y = 1
                    self.rect.top = obj.rect.bottom

    def jump(self): 
        if(self.jump_count < 1): self.y = -Constant.gravity * self.speed_jump
        else : self.y = -Constant.gravity * (self.speed_jump+2)
        self.animation_count = 0
        self.jump_count += 1

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

    def move_left(self,x):
        self.x = -(self.speed_run + x)
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self,x):
        self.x = (self.speed_run + x)
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def damageDecrease(self,damage,penetration,typeDamage):
        if typeDamage == "physical":
            return damage * (1 - (self.physical_armor - penetration)/(self.physical_armor + 100))
        elif typeDamage == "magic":
            return damage * (1 - (self.magic_armor - penetration)/(self.magic_armor + 100))

    def getPenetration(self,typeDamage):
        if typeDamage == "physical":
            return self.physical_armor_penetration
        elif typeDamage == "magic":
            return self.magic_armor_penetration
        return 0
    
    def die(self):
        self.isDead = True