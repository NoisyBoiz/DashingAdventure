from pygame import Rect
from pygame.sprite import collide_rect
from System import Constant

class Item:
    def __init__(self,x,y,width,height,name,animation = False):
        self.rect = Rect(x,y,width,height)
        self.y = 0
        self.fall_count = 0
        self.animation_count = 0
        self.animation_delay = 2
        self.itemName = name
        self.animation = animation
    def loop(self,objects):
        if self.animation:
            self.update()
        self.y += min(1,(self.fall_count / Constant.FPS) * Constant.gravity)
        self.checkFall(objects)
        self.rect.y += self.y
        self.fall_count += 1
    def update(self):
        self.animation_count += 1
        if(self.animation_count > 1000): self.animation_count = 0
    def checkFall (self, objects):
        for obj in objects:
            if collide_rect(self, obj):
                self.fall_count = 0
                self.y = 0
                self.rect.bottom = obj.rect.top + 1
              
