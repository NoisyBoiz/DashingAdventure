import random
class textDamage:
    def __init__(self,x,y,objWidth,objHeight,damage,type):
        self.x = x + objWidth // 2 + random.randint(-objWidth//4,objWidth//4)
        self.y = y + objHeight // 2
        self.damage = damage
        self.animation_count = 0
        self.animation_delay = 2
        self.size = 5
        if type=="true":
            self.color = (255,255,255)
            self.string = "-" + str(damage)
        elif(type=="physical"): 
            self.color = (255,0,0)
            self.string = "-" + str(damage)
        elif(type=="magic"): 
            self.color = (255,0,255)
            self.string = "-" + str(damage)
        elif(type=="heal"): 
            self.color = (0,255,0)
            self.string = "+" + str(damage)
        elif(type=="exp"):
            self.color = (255,255,0)
            self.string = "+ " + str(damage) + " exp"
    def loop(self,textDamages):
        self.update(textDamages)
    def update(self,textDamages):
        if(self.animation_count >= self.animation_delay):
            self.size += 1
            if(self.size == 28):
                textDamages.remove(self)
                return
            self.y -= 5
            self.x -= 1
            self.animation_count = 0
        self.animation_count += 1
   
        