from pygame import Rect,key,MOUSEBUTTONDOWN,MOUSEBUTTONUP,MOUSEMOTION,KEYDOWN,K_BACKSPACE
from pygame.draw import rect,circle

from System import Font
from Interact import CheckBox

COLOR_INACTIVE = (255, 229, 202)
COLOR_ACTIVE = (199, 0, 57)

class Text:
    def __init__(self,placeholder, x, y, w, h, text=''):
        self.rect = Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.textColor = (0,0,0)
        self.active = False
        self.txt_surface = Font.Arial20.render(text, True, self.textColor)
        self.textRect = self.txt_surface.get_rect()
        self.placeholder = Font.Arial20.render(placeholder,True,(255, 255, 255))
        self.placeholderRect = self.placeholder.get_rect()
        self.blink = 0
        self.blinkDelay = 20
    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == KEYDOWN:
            if self.active:
                if event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface =Font.Arial20.render(self.text, True, self.textColor)
                self.textRect = self.txt_surface.get_rect()
                if self.textRect.width > (self.rect.width - 20):
                    renderText = self.text[len(self.text) - int((self.rect.width-20)/self.textRect.width*len(self.text))::]
                    self.txt_surface =Font.Arial20.render(renderText, True, self.textColor)
   
    def resize(self,x,y,width,height):
        self.rect = Rect(x,y,width,height)

    def resetText(self):
        self.text = ""
        self.txt_surface = Font.Arial20.render(self.text, True, self.textColor)
        self.textRect = self.txt_surface.get_rect()
    def resetColor(self):
        self.color = COLOR_INACTIVE
    def resetAll(self):
        self.resetText()
        self.resetColor()
        self.active = False

    def draw(self, screen):
        rect(screen, (250, 152, 132), self.rect)
        rect(screen, self.color, self.rect, 2)
        if(self.text == ""): screen.blit(self.placeholder,(self.rect.x+10,self.rect.y + (self.rect.height - self.placeholderRect.height)/2))
        screen.blit(self.txt_surface, (self.rect.x+10,self.rect.y + (self.rect.height - self.textRect.height)/2))
        if self.active:
            self.blink += 1
            if self.blink > self.blinkDelay:
                rect(screen, (0,0,0), (self.rect.x + self.textRect.width + 10 ,self.rect.y + (self.rect.height - self.textRect.height)/2,2,self.textRect.height))
            if self.blink > self.blinkDelay*2:
                self.blink = 0


class Password:
    def __init__(self,placeholder, x, y, w, h, buttonShowPassword, text = '' ):
        self.rect = Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.hiddenText = text
        self.textColor = (0,0,0)
        self.active = False
        self.txt_surface = Font.Arial20.render(text, True, self.textColor)
        self.textRect = self.txt_surface.get_rect()
        self.placeholder = Font.Arial20.render(placeholder,True,(255, 255, 255))
        self.placeholderRect = self.placeholder.get_rect()
        self.blink = 0
        self.blinkDelay = 20
        self.showPassword = CheckBox.CheckBox("",x + w - 18 - 10,y + (h - 18)//2,18,2,1,(255,90,90),(255,90,30),(0,0,0))
        self.buttonShowPassword = buttonShowPassword
    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.buttonShowPassword and self.showPassword.rect.collidepoint(event.pos):
                self.showPassword.toggle()
                if self.showPassword.checked:
                    self.renderTextCut(self.text)
                else:
                    self.renderTextCut(self.hiddenText)
            elif self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == KEYDOWN:
            if self.active:
                if event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.hiddenText = self.hiddenText[:-1]
                else:
                    self.text += event.unicode
                    self.hiddenText += "*"

                if self.showPassword.checked:
                    self.renderTextCut(self.text)
                else:
                    self.renderTextCut(self.hiddenText)

    def renderTextCut(self,text):
        self.txt_surface =Font.Arial20.render(text, True, self.textColor)
        self.textRect = self.txt_surface.get_rect()
        if self.textRect.width > (self.rect.width - 48):
            renderText = text[len(self.text) - int((self.rect.width - 40)/self.textRect.width*len(self.text))::]
            self.txt_surface =Font.Arial20.render(renderText, True, self.textColor)

    def resize(self,x,y,width,height):
        self.rect = Rect(x,y,width,height)
        self.showPassword.resize(x + width - 18 - 10,y + (height - 18)//2,18)

    def resetText(self):
        self.text = ""
        self.hiddenText = ""
        self.txt_surface =Font.Arial20.render(self.text, True, self.textColor)
        self.textRect = self.txt_surface.get_rect()
    def resetColor(self):
        self.color = COLOR_INACTIVE
    def resetAll(self):
        self.resetText()
        self.resetColor()
        self.active = False
    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        rect(screen, (250, 152, 132), self.rect)
        rect(screen, self.color, self.rect, 2)
        if(self.text == ""): screen.blit(self.placeholder,(self.rect.x+10,self.rect.y + (self.rect.height - self.placeholderRect.height)/2))
        screen.blit(self.txt_surface, (self.rect.x+10,self.rect.y + (self.rect.height - self.textRect.height)/2))
        if self.buttonShowPassword: self.showPassword.draw(screen)
        if self.active:
            self.blink += 1
            if self.blink > self.blinkDelay:
                rect(screen, (0,0,0), (self.rect.x + self.textRect.width+10,self.rect.y + (self.rect.height - self.textRect.height)/2,2, self.textRect.height))
            if self.blink > self.blinkDelay*2:
                self.blink = 0

COLOR_INEDIT = (241, 222, 201)
COLOR_EDIT = (255, 211, 132)
COLOR_DUPLICATE = (255,0,0)
class Key:
    def __init__(self,placeholder, x, y, w, h, text=''):
        self.rect = Rect(x, y, w, h)
        self.color = COLOR_INEDIT
        self.colorBorder = COLOR_INACTIVE
        self.text = text
        self.textColor = (0,0,0)
        self.active = False
        self.txt_surface = Font.Arial20.render(text, True, self.textColor)
        self.textRect = self.txt_surface.get_rect()
        self.placeholder = Font.Arial20.render(placeholder,True,(255, 255, 255))
        self.placeholderRect = self.placeholder.get_rect()
        self.blink = 0
        self.blinkDelay = 20
        self.isDuplicate = False
    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.colorBorder = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == KEYDOWN:
            if self.active:
                self.text = key.name(event.key)
                self.txt_surface =Font.Arial20.render(self.text, True, self.textColor)
                self.textRect = self.txt_surface.get_rect()
                return True
            
    def resize(self,x,y,width,height):
        self.rect = Rect(x,y,width,height)

    def reset(self,text):
        self.text = text
        self.txt_surface =Font.Arial20.render(self.text, True, self.textColor)
        self.textRect = self.txt_surface.get_rect()
        self.color = COLOR_INEDIT
        self.active = False

    def changeColor(self,edit):
        self.color = COLOR_EDIT if edit else COLOR_INEDIT
    def duplicate(self,status):
        self.color = COLOR_DUPLICATE if status else COLOR_EDIT
        self.isDuplicate = status
    def draw(self, screen):
        rect(screen, self.color, self.rect)
        rect(screen, self.colorBorder, self.rect, 2)
        if(self.text == ""): screen.blit(self.placeholder,(self.rect.x + (self.rect.width - self.placeholderRect.width)//2 ,self.rect.y + (self.rect.height - self.placeholderRect.height)//2))
        screen.blit(self.txt_surface, (self.rect.x + (self.rect.width - self.textRect.width)//2, self.rect.y + (self.rect.height - self.textRect.height)//2))
        if self.active:
            self.blink += 1
            if self.blink > self.blinkDelay:
                rect(screen, (0,0,0), (self.rect.x + (self.rect.width + self.textRect.width)//2 + 2,self.rect.y + (self.rect.height - self.textRect.height)//2, 2, self.textRect.height))
            if self.blink > self.blinkDelay*2:
                self.blink = 0

class Range:
    def __init__(self,x,y,width,height,value,minValue,maxValue,barColor=(0,0,0),knotColor=(255,255,255)):
        self.rect = Rect(x,y,width,height)
        self.value = value
        self.minValue = minValue
        self.maxValue = maxValue
        self.isClick = False
        self.barColor = barColor
        self.knotColor = knotColor
        self.knotRadius = int(height//2*1.5)
        self.updateKnotPos()

    def setValue(self,value):
        self.value = value
        self.updateKnotPos()

    def getValue(self):
        return self.value
    
    def handle_event(self,event):
        if event.type == MOUSEBUTTONDOWN:
            if self.checkClick(event.pos):
                self.isClick = True
        if event.type == MOUSEBUTTONUP:
            self.isClick = False
        if event.type == MOUSEMOTION:
            if self.checkMove(event.pos):
                return True
        return False
    
    def checkClick(self,pos):
        px = self.knotPos[0] - pos[0]
        py = self.knotPos[1] - pos[1]
        if px*px + py*py < self.knotRadius*self.knotRadius:
            self.isClick = True
            return True
        return False
    
    def checkRelease(self):
        self.isClick = False

    def checkMove(self,pos):
        if self.isClick:
            if pos[0] < self.rect.x:
                self.value = self.minValue
            elif pos[0] > self.rect.x + self.rect.width:
                self.value = self.maxValue
            else:
                self.value = int((pos[0] - self.rect.x)*100/self.rect.width)
            self.updateKnotPos()
            return True
        return False
    
    def updateKnotPos(self):
        self.knotPos = (self.rect.x + int(self.value/self.maxValue*self.rect.width),self.rect.y + self.rect.height//2)

    def draw(self,screen):
        rect(screen,self.barColor,self.rect, self.rect.height//2, self.rect.height//2)
        circle(screen,self.knotColor,self.knotPos,self.knotRadius)