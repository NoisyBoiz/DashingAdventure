from pygame.rect import Rect
from pygame.font import SysFont
from pygame import draw

class CheckBox:
    def __init__(self,text,x,y,size,markSize,border,colorBackground,colorBorder,colorText):
        self.rect = Rect(x,y,size,size)
        self.markSize = markSize
        self.border = border
        self.text = text
        self.font = SysFont("Arial",int(self.rect.height))
        self.colorBackground = colorBackground
        self.colorBorder = colorBorder
        self.colorText = colorText
        self.checked = False
    def draw(self,screen):
        draw.rect(screen,self.colorBackground,self.rect)
        draw.rect(screen,self.colorBorder,self.rect,self.border)
        text = self.font.render(self.text,True,self.colorText)
        textRect = text.get_rect()
        screen.blit(text,(self.rect.x + self.rect.width*1.5,self.rect.y + (self.rect.height - textRect.height)//2))
        if self.checked:
           draw.line(screen,self.colorText,(self.rect.x + self.rect.width - self.markSize *1.5,self.rect.y + self.markSize *1.5),(self.rect.x + self.rect.width//3,self.rect.y + self.rect.height  - self.markSize *1.5),self.markSize)
           draw.line(screen,self.colorText,(self.rect.x + self.markSize *1.5,self.rect.y + self.markSize *1.5 + self.rect.height//3),(self.rect.x + self.rect.width//3,self.rect.y + self.rect.height - self.markSize *1.5),self.markSize)
    def checkClick(self,mousePos):
        if self.rect.collidepoint(mousePos):
            self.checked = not self.checked
    def reset(self):
        self.checked = False
    def resize(self,x,y,size):
        self.rect = Rect(x,y,size,size)
        
    def toggle(self):
        self.checked = not self.checked
       