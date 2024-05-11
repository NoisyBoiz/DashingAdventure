from pygame.draw import rect
from pygame import Rect,MOUSEBUTTONDOWN
from System import Constant, Font
from Interact import Button, InputBox

class AccountControl:
    def __init__(self,x,y,width,height):
        self.playerName = ""
        self.wellcome = Font.Arial20.render("Wellcome Back: ",True,(12, 19, 69))
        self.wellcomeRect = self.wellcome.get_rect()
        self.textName = Font.Arial20.render(self.playerName,True,(0,0,0))
        self.textNameRect = self.textName.get_rect()
        self.updateBackgroudWellcomeRect()
        self.interactInit(width,height)

    def interactInit(self,w,h):
        buttonWidth = 250
        buttonHeight = 50
        gap = 10
        top = (h - buttonHeight*4 - gap*2) // 2
        self.changeNameButton = Button.Button("Change Name",(w-buttonWidth)//2,top,buttonWidth,buttonHeight,4,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.changePasswordButton = Button.Button("Change Password",(w-buttonWidth)//2,top + buttonHeight + gap,buttonWidth,buttonHeight,4,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.logoutButton = Button.Button("Log Out",(w-buttonWidth)//2,top + buttonHeight*3 + gap,buttonWidth,buttonHeight,4,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.backButton = Button.Button("Back",10, h - 60,150,buttonHeight,4,(255, 120, 90),(250, 240, 228),(255, 255, 255))

    def resize(self,w,h):
        self.interactInit(w,h)

    def updatePlayerName(self,playerName):
        self.playerName = playerName
        self.textName = Font.Arial20.render(self.playerName,True,(0,0,0))
        self.textNameRect = self.textName.get_rect()
        self.updateBackgroudWellcomeRect()

    def updateBackgroudWellcomeRect(self):
        textWidth = self.wellcomeRect.width + self.textNameRect.width
        backgroudWellcomeRectWidth = textWidth + 10
        backgroudWellcomeRectHeight = self.wellcomeRect.height * 1.3
        self.backgroudWellcomeRect = Rect(10 - (backgroudWellcomeRectWidth - textWidth)//2, 10 - (backgroudWellcomeRectHeight - self.wellcomeRect.height)//2, backgroudWellcomeRectWidth,backgroudWellcomeRectHeight)

    def checkClick(self,pos):
        if self.changeNameButton.rect.collidepoint(pos):
            return "ChangeName"
        if self.changePasswordButton.rect.collidepoint(pos):
            return "ChangePassword"
        if self.logoutButton.rect.collidepoint(pos):
            return "LogOut"
        if self.backButton.rect.collidepoint(pos):
            return "Back"
        return ""

    def draw(self,screen):
        self.changeNameButton.draw(screen)
        self.changePasswordButton.draw(screen)
        self.logoutButton.draw(screen)
        self.backButton.draw(screen)
        rect(screen,(242, 238, 157),self.backgroudWellcomeRect)
        screen.blit(self.wellcome,(10,10))
        screen.blit(self.textName,(self.wellcomeRect.width + 10,10))



class ChangeName:
    def __init__(self,x,y,width,height):
        self.interactInit(width,height)
    def interactInit(self,w,h):
        buttonWidth = 250
        buttonHeight = 50
        gap = 10
        top = (h - buttonHeight*3 - gap*2) // 2
        self.inputBox = InputBox.Text("New Name", (w-buttonWidth)//2,top,buttonWidth,buttonHeight)
        self.passwordBox = InputBox.Password("Password", (w-buttonWidth)//2,top + buttonHeight + gap,buttonWidth,buttonHeight,True)
        self.changeButton = Button.Button("Change",(w-buttonWidth)//2,top + (buttonHeight + gap)*2,buttonWidth,buttonHeight,4,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.backButton = Button.Button("Back",10, h - 60,150,buttonHeight,4,(255, 120, 90),(250, 240, 228),(255, 255, 255))

    def resize(self,w,h):
        self.interactInit(w,h)
   
    def checkClick(self,mousePos):
        if self.backButton.rect.collidepoint(mousePos):
            self.reset()
            return "Back"
        if self.changeButton.rect.collidepoint(mousePos):
            return "Change"
        return ""
    def reset(self):
        self.inputBox.resetAll()
        self.passwordBox.resetAll()
    def getName(self):
        return self.inputBox.text.strip()
    def getPassword(self):
        return self.passwordBox.text.strip()
    
    def handle_event(self,event):
        self.inputBox.handle_event(event)
        self.passwordBox.handle_event(event)

    def draw(self,screen):
        self.inputBox.draw(screen)
        self.passwordBox.draw(screen)
        self.changeButton.draw(screen)
        self.backButton.draw(screen)
    
        

class ChangePassword:
    def __init__(self,x,y,w,h):
        self.interactInit(w,h)
    def interactInit(self,w,h):
        buttonWidth = 250
        buttonHeight = 50
        gap = 10
        top = (h - buttonHeight*3 - gap*2) // 2
        self.inputWidth = 200
        self.passwordBox = InputBox.Password("Password", (w - self.inputWidth)//2, top ,self.inputWidth,buttonHeight,True)
        self.newPasswordBox = InputBox.Password("New Password", (w - self.inputWidth)//2, top + buttonHeight + gap,self.inputWidth,buttonHeight,True)
        self.comfirmPasswordBox = InputBox.Password("Comfirm Password", (w - self.inputWidth)//2, top + (buttonHeight + gap)*2,self.inputWidth,buttonHeight,False)
        self.changeButton = Button.Button("Change",(w - self.inputWidth)//2, top + (buttonHeight + gap)*3,self.inputWidth,buttonHeight,4,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.backButton = Button.Button("Back",10, h - 60,150,buttonHeight,4,(255, 120, 90),(250, 240, 228),(255, 255, 255))
   
    def resize(self,w,h):
        self.interactInit(w,h)

    def checkClick(self,mousePos):
        if self.backButton.rect.collidepoint(mousePos):
            self.reset()
            return "Back"
        if self.changeButton.rect.collidepoint(mousePos):
            return "Change"
        return ""
    def reset(self):
        self.passwordBox.resetAll()
        self.newPasswordBox.resetAll()
        self.comfirmPasswordBox.resetAll()
    def getPassword(self):
        return self.passwordBox.text.strip()
    def getNewPassword(self):
        return self.newPasswordBox.text.strip()
    def getComfirmPassword(self):
        return self.comfirmPasswordBox.text.strip()
    
    def handle_event(self,event):
        if event.type == MOUSEBUTTONDOWN:
            if self.newPasswordBox.showPassword.rect.collidepoint(event.pos):
                self.comfirmPasswordBox.showPassword.toggle()
                if self.comfirmPasswordBox.showPassword.checked:
                    self.comfirmPasswordBox.renderTextCut(self.comfirmPasswordBox.text)
                else:
                    self.comfirmPasswordBox.renderTextCut(self.comfirmPasswordBox.hiddenText)
        self.passwordBox.handle_event(event)
        self.newPasswordBox.handle_event(event)
        self.comfirmPasswordBox.handle_event(event)

    def draw(self,screen):
        self.passwordBox.draw(screen)
        self.newPasswordBox.draw(screen)
        self.comfirmPasswordBox.draw(screen)
        self.changeButton.draw(screen)
        self.backButton.draw(screen)
    
        
        