from pygame import MOUSEBUTTONDOWN
from Interact import Button, InputBox, CheckBox
from System import Constant, Font
class AuthenticationPlayer:
    def __init__(self,x,y,w,h):
        self.nameGame = Font.Avara.render("DASHING ADVENTURE",True,(0,0,0))
        self.nameGameRect = self.nameGame.get_rect()
        self.interactInit(w,h)

    def interactInit(self,w,h):
        buttonWidth = 250
        buttonHeight = 50
        gap = 10
        top = (h - buttonHeight*3 - gap*2)*1/8
        self.textPos = ((w - self.nameGameRect.width)//2, top)
        y = top*3 + self.nameGameRect.height
        self.loginButton = Button.Button("Login",(w - buttonWidth)//2, y,buttonWidth,buttonHeight,3,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.signUpButton = Button.Button("Sign Up",(w - buttonWidth)//2, y + buttonHeight+gap,buttonWidth,buttonHeight,3,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.exitButton = Button.Button("Exit",(w - buttonWidth)//2, y +(buttonHeight+gap)*2 ,buttonWidth,buttonHeight,3,(255, 120, 90),(250, 240, 228),(255, 255, 255))

    def resize(self,w,h):
        buttonWidth = 250
        buttonHeight = 50
        gap = 10
        top = (h - buttonHeight*3 - gap*2)*1/8
        self.textPos = ((w - self.nameGameRect.width)//2, top)
        y = top*3 + self.nameGameRect.height
        self.loginButton.resize((w - buttonWidth)//2, y ,buttonWidth,buttonHeight)
        self.signUpButton.resize((w - buttonWidth)//2, y + buttonHeight+gap,buttonWidth,buttonHeight)
        self.exitButton.resize((w - buttonWidth)//2, y + (buttonHeight+gap)*2 ,buttonWidth,buttonHeight)

    def checkClick(self,mousePos):
        if self.loginButton.rect.collidepoint(mousePos):
            return "Login"
        if self.signUpButton.rect.collidepoint(mousePos):
            return "SignUp"
        if self.exitButton.rect.collidepoint(mousePos):
            return "Exit"
        return ""
    
    def draw(self,screen):
        screen.blit(self.nameGame,self.textPos)
        self.loginButton.draw(screen)
        self.signUpButton.draw(screen)
        self.exitButton.draw(screen)

class Login:
    def __init__(self,x,y,w,h):
        self.interactInit(w,h)
    def interactInit(self,w,h):
        buttonWidth = 250
        buttonHeight = 50
        gap = 10
        top = (h - buttonHeight*3 - gap*2)*2/5
        self.usernameBox = InputBox.Text("Username", (w - buttonWidth)//2, top ,buttonWidth,buttonHeight)
        self.passwordBox = InputBox.Password("Password", (w - buttonWidth)//2, top+(buttonHeight+gap),buttonWidth,buttonHeight,True)
        self.rememberCheckBox = CheckBox.CheckBox("Remember Me",(w - buttonWidth)//2 + 10,top+(buttonHeight+gap)*2,18,2,1,(255, 255, 255),(0, 0, 0),(0,0,0))
        self.loginButton = Button.Button("Login",(w - buttonWidth)//2,top+(buttonHeight+gap)*3,buttonWidth,buttonHeight,3,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.backButton = Button.Button("Back",10, h - 60,150,buttonHeight,3,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.signUpButton = Button.Button("Sign Up", w - 160, h - 60,150,buttonHeight,3,(255, 120, 90),(250, 240, 228),(255, 255, 255))

    def resize(self,w,h):
        buttonWidth = 250
        buttonHeight = 50
        gap = 10
        top = (h - buttonHeight*3 - gap*2)*2/5
        self.usernameBox.resize((w - buttonWidth)//2, top ,buttonWidth,50)
        self.passwordBox.resize((w - buttonWidth)//2, top+(buttonHeight+gap),buttonWidth,50)
        self.rememberCheckBox.resize((w - buttonWidth)//2 + 10,top+(buttonHeight+gap)*2,18)
        self.loginButton.resize((w - buttonWidth)//2,top+(buttonHeight+gap)*3,buttonWidth,50)
        self.backButton.resize(10, h - 60,150,50)
        self.signUpButton.resize(w - 160, h - 60,150,50)

    def checkClick(self,mousePos):
        if self.backButton.rect.collidepoint(mousePos):
            self.reset()
            return "Back"
        if self.signUpButton.rect.collidepoint(mousePos):
            return "SignUp"
        if self.loginButton.rect.collidepoint(mousePos):
            return "Login"
        if self.rememberCheckBox.rect.collidepoint(mousePos):
            self.rememberCheckBox.toggle()
    
    def handle_event(self,event):
        self.usernameBox.handle_event(event)
        self.passwordBox.handle_event(event)
    def getUserName(self):
        return self.usernameBox.text.strip()
    def getPassword(self):
        return self.passwordBox.text.strip()
    def getRemember(self):
        return self.rememberCheckBox.checked
    def reset(self):
        self.usernameBox.resetAll()
        self.passwordBox.resetAll()
        self.rememberCheckBox.reset()

    def draw(self,screen):
        self.usernameBox.draw(screen)
        self.passwordBox.draw(screen)
        self.loginButton.draw(screen)
        self.backButton.draw(screen)
        self.signUpButton.draw(screen)
        self.rememberCheckBox.draw(screen)

class SignUp:
    def __init__(self,x,y,w,h):
        self.interactInit(w,h)

    def interactInit(self,w,h):
        buttonWidth = 250
        buttonHeight = 50
        gap = 10
        top = (h - buttonHeight*8 - gap*7)//2

        self.nameBox = InputBox.Text("Name *", (w - buttonWidth)//2, top ,buttonWidth,buttonHeight)
        self.usernameBox = InputBox.Text("Username *", (w - buttonWidth)//2, top+(buttonHeight+gap),buttonWidth,buttonHeight)
        self.emailBox = InputBox.Text("Email *", (w - buttonWidth)//2, top+(buttonHeight+gap)*2,buttonWidth,buttonHeight)
        self.passwordBox = InputBox.Password("Password *", (w - buttonWidth)//2, top+(buttonHeight+gap)*3,buttonWidth,buttonHeight,True)
        self.comfirmPasswordBox = InputBox.Password("Comfirm Password *", (w - buttonWidth)//2, top+(buttonHeight+gap)*4,buttonWidth,buttonHeight,False)
        self.signUpButton = Button.Button("Sign Up",(w - buttonWidth)//2, top+(buttonHeight+gap)*5,buttonWidth, buttonHeight, 4,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.backButton = Button.Button("Back", 10, h - 60,150,buttonHeight,3,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.loginButton = Button.Button("Login", w - 160, h - 60,150,buttonHeight,3,(255, 120, 90),(250, 240, 228),(255, 255, 255))

    def resize(self,w,h):
        buttonWidth = 250
        buttonHeight = 50
        gap = 10
        top = (h - buttonHeight*8 - gap*7)//2
        self.nameBox.resize((w - buttonWidth)//2, top ,buttonWidth,buttonHeight)
        self.usernameBox.resize((w - buttonWidth)//2, top+(buttonHeight+gap),buttonWidth,buttonHeight)
        self.emailBox.resize((w - buttonWidth)//2, top+(buttonHeight+gap)*2,buttonWidth,buttonHeight)
        self.passwordBox.resize((w - buttonWidth)//2, top+(buttonHeight+gap)*3,buttonWidth,buttonHeight)
        self.comfirmPasswordBox.resize((w - buttonWidth)//2, top+(buttonHeight+gap)*4,buttonWidth,buttonHeight)
        self.signUpButton.resize((w - buttonWidth)//2,top+(buttonHeight+gap)*5,buttonWidth,buttonHeight)
        self.backButton.resize(10, h - 60,150,buttonHeight)
        self.loginButton.resize(w - 160, h - 60,150,buttonHeight)

    def checkClick(self,mousePos):
        if self.backButton.rect.collidepoint(mousePos):
            self.reset()
            return "Back"
        if self.loginButton.rect.collidepoint(mousePos):
            self.reset()
            return "Login"
        if self.signUpButton.rect.collidepoint(mousePos):
            return "SignUp"
        return ""
    def reset(self):
        self.emailBox.resetAll()
        self.nameBox.resetAll()
        self.usernameBox.resetAll()
        self.passwordBox.resetAll()
        self.comfirmPasswordBox.resetAll()
    def getUserName(self):
        return self.usernameBox.text.strip()
    def getEmail(self):
        return self.emailBox.text.strip()
    def getName(self):
        return self.nameBox.text.strip()
    def getPassword(self):
        return self.passwordBox.text.strip()
    def getComfirmPassword(self):
        return self.comfirmPasswordBox.text.strip()
    
    def handle_event(self,event):
        if event.type == MOUSEBUTTONDOWN:
            if self.passwordBox.showPassword.rect.collidepoint(event.pos):
                self.comfirmPasswordBox.showPassword.toggle()
                if self.comfirmPasswordBox.showPassword.checked:
                    self.comfirmPasswordBox.renderTextCut(self.comfirmPasswordBox.text)
                else:
                    self.comfirmPasswordBox.renderTextCut(self.comfirmPasswordBox.hiddenText)
        self.usernameBox.handle_event(event)
        self.emailBox.handle_event(event)
        self.nameBox.handle_event(event)
        self.passwordBox.handle_event(event)
        self.comfirmPasswordBox.handle_event(event)

    def draw(self,screen):
        self.nameBox.draw(screen)
        self.usernameBox.draw(screen)
        self.emailBox.draw(screen)
        self.passwordBox.draw(screen)
        self.comfirmPasswordBox.draw(screen)
        self.loginButton.draw(screen)
        self.signUpButton.draw(screen)
        self.backButton.draw(screen)
    
        
        
        