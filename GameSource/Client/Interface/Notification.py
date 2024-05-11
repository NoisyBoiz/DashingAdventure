from typing import Any
from pygame import Rect
from pygame.draw import rect
from System import Font, Constant
from Interact import Button

class Notification:
    def __init__(self,width,height,status,message,backgroundColor = (142, 205, 221),borderColor = (34, 102, 141)):
        x = (Constant.Screen_Width - width)//2
        y = (Constant.Screen_Height - height)//2
        self.rect = Rect(x,y,width,height)
        self.status = Font.Arial30Bold.render(status,True,(0,0,0))
        self.statusRect = self.status.get_rect()
        self.message = Font.Arial25.render(message,True,(0,0,0))
        self.messageRect = self.message.get_rect()  
        self.border = 4
        self.closeButton = Button.Button("Close",x + (width - 100)//2,y + height - 50,100,40,2,(255, 250, 221),(255, 204, 112),(0, 0, 0))
        self.backgroundColor = backgroundColor
        self.borderColor = borderColor

    def resize(self,width,height):
        x = (width - self.rect.width)//2
        y = (height - self.rect.height)//2
        self.rect.x = x
        self.rect.y = y
        self.closeButton.resize(x + (self.rect.width - 100)//2,y + self.rect.height - 50,100,40)

    def checkClose(self,mousePos):
        if self.closeButton.rect.collidepoint(mousePos):
            return True
        return False
    
    def draw(self,screen):
        rect(screen,self.backgroundColor,self.rect,int(self.rect.height//2),int(self.rect.width//20))
        rect(screen,self.borderColor,self.rect,self.border,int(self.rect.width//20))
        screen.blit(self.status,(self.rect.x + (self.rect.width - self.statusRect.width)//2,self.rect.y + 10))
        screen.blit(self.message,(self.rect.x + (self.rect.width - self.messageRect.width)//2,self.rect.y + (self.rect.height - self.messageRect.height - 45 - 10)//2))
        self.closeButton.draw(screen)
        
class Comfirm:
    def __init__(self,width,height,status,message,backgroundColor = (142, 205, 221),borderColor = (34, 102, 141)):
        x = (Constant.Screen_Width - width)//2
        y = (Constant.Screen_Height - height)//2
        self.rect = Rect(x,y,width,height)
        self.status = Font.Arial30Bold.render(status,True,(0,0,0))
        self.statusRect = self.status.get_rect()
        self.message = Font.Arial25.render(message,True,(0,0,0))
        self.messageRect = self.message.get_rect()  
        self.border = 4
        self.backgroundColor = backgroundColor
        self.borderColor = borderColor
        self.interactInit(x,y,width,height)

    def interactInit(self,x,y,width,height):
        gap = (width - 200)//3
        self.acceptButton = Button.Button("Yes",x + gap,y + height - 50,100,40,2,(255, 250, 221),(255, 204, 112),(0, 0, 0))
        self.closeButton = Button.Button("No",x + gap*2 + 100,y + height - 50,100,40,2,(255, 250, 221),(255, 204, 112),(0, 0, 0))

    def resize(self,width,height):
        x = (width - self.rect.width)//2
        y = (height - self.rect.height)//2
        self.rect.x = x
        self.rect.y = y
        self.interactInit(x,y,width,height)

    def checkClick(self,mousePos):
        if self.closeButton.rect.collidepoint(mousePos):
            return False
        if self.acceptButton.rect.collidepoint(mousePos):
            return True
        return None
    
    def draw(self,screen):
        rect(screen,self.backgroundColor,self.rect,int(self.rect.height//2),int(self.rect.width//20))
        rect(screen,self.borderColor,self.rect,self.border,int(self.rect.width//20))
        screen.blit(self.status,(self.rect.x + (self.rect.width - self.statusRect.width)//2,self.rect.y + 10))
        screen.blit(self.message,(self.rect.x + (self.rect.width - self.messageRect.width)//2,self.rect.y + (self.rect.height - self.messageRect.height - 45 - 10)//2))
        self.closeButton.draw(screen)
        self.acceptButton.draw(screen)