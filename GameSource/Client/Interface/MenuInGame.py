from pygame import Rect
from pygame.draw import rect
from Interact import Button
from System import Constant, Font

class MenuInGame:
    def __init__(self,x,y,width,height):        
        self.rect = Rect(x,y,width,height)
        wbox = min(int(width*0.8),700)
        hbox = min(int(height*0.8),550)
        self.boxRect = Rect(x+(width-wbox)//2,y+(height-hbox)//2,wbox,hbox)
        self.playerName = ""
        self.interactInit(width,height)
        self.closeButton = Button.CircleButton(None, self.boxRect.x + self.boxRect.width - 60,self.boxRect.y + 20, 20, 1 ,(255, 189, 139),(223, 67, 0), "X")

    def interactInit(self,w,h):
        buttonWidth = 200
        buttonHeight = 50
        gap = 10
        top = (h - buttonHeight*3 - gap) // 2
        self.settingButton = Button.Button("Setting",(w-buttonWidth)//2,top,buttonWidth,buttonHeight,4,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.buttonExit = Button.Button("Exit Game",(w-buttonWidth)//2,top + buttonHeight*2 + gap,buttonWidth,buttonHeight,4,(255, 120, 90),(250, 240, 228),(255, 255, 255))

    def resize(self,w,h):
        self.rect.width = w
        self.rect.height = h
        self.boxRect.x = self.rect.x + (w - self.boxRect.width)//2
        self.boxRect.y = self.rect.y + (h - self.boxRect.height)//2
        self.interactInit(w,h)
        self.closeButton.resize(self.boxRect.x + self.boxRect.width - 70,self.boxRect.y + 20, 20)
        
    def checkClick(self,pos):
        if self.buttonExit.rect.collidepoint(pos):
            return "Exit"
        if self.settingButton.rect.collidepoint(pos):
            return "Setting"
        if self.closeButton.checkCollision(pos):
            return "Back"
        return ""

    def draw(self,screen):
        rect(screen,(255, 186, 134),self.boxRect, self.rect.height//2, self.rect.height//20)
        self.settingButton.draw(screen)
        self.buttonExit.draw(screen)
        self.closeButton.draw(screen)
      