from pygame.draw import circle
from pygame import Surface,Rect,transform,key
from System import Font, Constant
from Function import Func
from Interact import Button

class InteracInGame:
    def __init__(self,x,y,w,h):
        self.rect = Rect(x,y,w,h)

        self.margin = 10
        self.border = 1
        self.gap = 7

        self.circleRadius = int(Constant.block_size*0.8/2)
        self.imageSize = int(self.circleRadius*2 - self.border*2)
        self.getImageInit()
        self.getCircleButton()
    
    def getImageInit(self):
        self.allImage = Func.splitSprite(["IconMenu"],200,200,self.imageSize,self.imageSize,False,False)
    
    def getCircleButton(self):
        x = self.rect.width - (self.gap + self.circleRadius*2) * 3
        y = 10
        self.circleButton = []
        self.circleButton.append(Button.CircleButton(self.allImage["achievement"][0],x,y,self.circleRadius,self.border,(255, 189, 139),(223, 67, 0)))
        self.circleButton.append(Button.CircleButton(self.allImage["characterProperties"][0],x + (self.circleRadius*2 + self.gap),y,self.circleRadius,self.border,(255, 189, 139),(223, 67, 0)))
        self.circleButton.append(Button.CircleButton(self.allImage["menu"][0],x + (self.circleRadius*2 + self.gap)*2,y,self.circleRadius,self.border,(255, 189, 139),(223, 67, 0)))

    def resize(self,width,height):
        self.rect.width = width
        self.rect.height = height
        self.getCircleButton()

    def checkClick(self,pos):
        if self.circleButton[0].checkCollision(pos):
            return "Achievement"
        if self.circleButton[1].checkCollision(pos):
            return "CharacterProperties"
        if self.circleButton[2].checkCollision(pos):
            return "Menu"
        return ""
    
    def draw(self,screen):
        for i in self.circleButton:
            i.draw(screen)
