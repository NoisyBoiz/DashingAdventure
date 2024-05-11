from pygame import Rect
from pygame.draw import rect,circle
from pygame.font import SysFont
from System import Font

class Button:
    def __init__(self,text,x,y,width,height,border,colorBackground,colorBorder,colorText):
        self.rect = Rect(x,y,width,height)
        self.border = border
        self.font = SysFont("Arial",int(self.rect.height*0.5))
        self.colorBackground = colorBackground
        self.colorBorder = colorBorder
        self.colorText = colorText
        self.updateText(text)
    def updateText(self,text):
        self.text = text
        self.txt_surface = self.font.render(self.text,True,self.colorText)
        self.textRect =  self.txt_surface.get_rect()

    def resize(self,x,y,width,height):
        self.rect = Rect(x,y,width,height)
    
    def draw(self,screen):
        rect(screen,self.colorBackground,self.rect, int(min(self.rect.height,self.rect.width)/2),min(self.rect.height,self.rect.width)//8)
        rect(screen,self.colorBorder,self.rect,self.border,min(self.rect.height,self.rect.width)//8)
        screen.blit(self.txt_surface,(self.rect.x + (self.rect.width - self.textRect.width)//2,self.rect.y + (self.rect.height - self.textRect.height)//2))

    
class CircleButton:
    def __init__(self,image,x,y,radius,border,colorBackground,colorBorder,text = ""):
        self.rect = Rect(x,y,radius*2,radius*2)
        self.circlePos = (x+radius,y+radius)
        self.circleRadius = radius
        self.border = border
        self.colorBackground = colorBackground
        self.colorBorder = colorBorder

        self.image = image
        if image != None:
            imgRect = self.image.get_rect()
            self.imageRect = (x + radius - imgRect.width//2,y + radius - imgRect.height//2)
        if text != "":
            self.text = Font.Arial20Bold.render(text,True,(0,0,0))
            self.textRect = self.text.get_rect()
    # def resize(self,x,y,radius):
    #     self.imageRect = self.image.get_rect()
    def resize(self,x,y,radius):
        self.rect = Rect(x,y,radius*2,radius*2)
        self.circlePos = (x+radius,y+radius)
        self.circleRadius = radius
        if self.image != None:
            self.imageRect = (x + radius - self.imageRect.width//2,y + radius - self.imageRect.height//2)

    def checkCollision(self,pos):
        return (pos[0] - self.circlePos[0])**2 + (pos[1] - self.circlePos[1])**2 <= self.circleRadius**2
    
    def draw(self,screen):
        circle(screen, (255, 175,0), self.circlePos,self.circleRadius)
        circle(screen, (255, 86, 0), self.circlePos,self.circleRadius,self.border*2)
        if self.image != None:
            screen.blit(self.image,self.imageRect)
        else:
            screen.blit(self.text,(self.rect.x + (self.rect.width - self.textRect.width)//2,self.rect.y + (self.rect.height - self.textRect.height)//2))