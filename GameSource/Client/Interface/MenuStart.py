from pygame.draw import rect
from pygame import Rect
from Interact import Button
from System import Constant, Font

class MenuStart:
    def __init__(self,x,y,w,h):
        self.nameGame = Font.Avara.render("DASHING ADVENTURE",True,(255,255,255))
        self.nameGameRect = self.nameGame.get_rect()
        self.rect = Rect(x,y,w,h)
        self.playerName = ""
        self.interactInit(w,h)

    def interactInit(self,w,h):
        buttonWidth = 300
        buttonHeight = 50
        gap = 10
        top = (h - buttonHeight*4 - gap*3) // 2
        self.textPos = ((w - self.nameGameRect.width)//2, (h - buttonHeight*3 - gap*2)*1/6)
        self.accountControlButton = Button.Button("Welcome Back "+ self.playerName,(w-buttonWidth)//2,top,buttonWidth,buttonHeight,3,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.singlePlayerButton = Button.Button("Single Player",(w-buttonWidth)//2,top + buttonHeight + gap,buttonWidth,buttonHeight,3,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.multiPlayerButton = Button.Button("Multi Player",(w-buttonWidth)//2,top + (buttonHeight + gap)*2,buttonWidth,buttonHeight,3,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.settingButton = Button.Button("Setting",(w-buttonWidth)//2,top + (buttonHeight + gap)*3,buttonWidth,buttonHeight,3,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.buttonExit = Button.Button("Exit",(w-buttonWidth)//2,top + (buttonHeight + gap)*4,buttonWidth,buttonHeight,3,(255, 120, 90),(250, 240, 228),(255, 255, 255))

    def resize(self,w,h):
        self.interactInit(w,h)

    def updatePlayerName(self,playerName):
        self.playerName = playerName
        self.accountControlButton.updateText("Welcome Back "+ playerName)
   
    def loop(self):
        pass
    def checkClick(self,pos):
        if self.singlePlayerButton.rect.collidepoint(pos):
            return "SinglePlayer"
        if self.multiPlayerButton.rect.collidepoint(pos):
            return "MultiPlayer"
        if self.accountControlButton.rect.collidepoint(pos):
            return "AccountControl"
        if self.buttonExit.rect.collidepoint(pos):
            return "Exit"
        if self.settingButton.rect.collidepoint(pos):
            return "Setting"
        return ""

    def draw(self,screen):
        screen.blit(self.nameGame,self.textPos)
        self.accountControlButton.draw(screen)
        self.singlePlayerButton.draw(screen)
        self.multiPlayerButton.draw(screen)
        self.settingButton.draw(screen)
        self.buttonExit.draw(screen)
      