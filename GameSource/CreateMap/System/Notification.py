import pygame
import System.Setting as Setting
import System.File as File
class Button():
    def __init__(self,text,x,y,width,height,padding,border,colorBackground,colorBorder,colorText):
        self.rect = pygame.Rect(x,y,width,height)
        self.padding = padding
        self.border = border
        self.text = text
        self.font = pygame.font.SysFont("Arial",int(self.rect.height*0.5))
        self.colorBackground = colorBackground
        self.colorBorder = colorBorder
        self.colorText = colorText
    def draw(self,screen):
        pygame.draw.rect(screen,self.colorBackground,self.rect)
        pygame.draw.rect(screen,self.colorBorder,self.rect,self.border)
        text = self.font.render(self.text,True,self.colorText)
        textRect = text.get_rect()
        textRect.center = (self.rect.x+self.rect.width//2,self.rect.y+self.rect.height//2)
        screen.blit(text,textRect)

# thông báo xác nhận lưu dữ liệu
class Notification:
    def __init__(self):
        self.width = Setting.screen_width//2
        self.height = Setting.screen_height//2.5
        self.rect = pygame.Rect(Setting.screen_width//2-self.width//2,Setting.screen_height//2-self.height//2,self.width,self.height)
        self.buttonWidth = 80
        self.buttonHeight = 40
        self.buttonCancel = Button("Cancel",self.rect.x+((self.width-self.buttonWidth*2)//3),self.rect.y+self.rect.height-Setting.block_size,self.buttonWidth,self.buttonHeight,5,2,(255, 250, 215),(35,35,35),(40,40,40))
        self.buttonAccept = Button("Accept",self.rect.x+((self.width-self.buttonWidth*2)//3)*2+self.buttonWidth,self.rect.y+self.rect.height-Setting.block_size,self.buttonWidth,self.buttonHeight,5,2,(255, 250, 215),(35,35,35),(40,40,40))
        self.buttonClose = Button("Close",self.rect.x+((self.width-self.buttonWidth)//2),self.rect.y+self.rect.height-Setting.block_size,self.buttonWidth,self.buttonHeight,5,2,(255, 250, 215),(35,35,35),(40,40,40))
        self.status = 0

        self.font = pygame.font.SysFont('Arial', 30)
        self.textComfirm = self.font.render("Do you want to save?", True, (0, 0, 0))
        self.textComfirmRect = self.textComfirm.get_rect()
        self.textSucces = self.font.render("Save success!", True, (0, 0, 0))
        self.textSuccesRect = self.textSucces.get_rect()
       
    def drawComfirm(self,screen):
        pygame.draw.rect(screen,(233, 119, 119),(self.rect))
        screen.blit(self.textComfirm,(self.rect.x+(self.width-self.textComfirmRect.width)//2,self.rect.y+self.textComfirmRect.height))
        self.buttonAccept.draw(screen)
        self.buttonCancel.draw(screen)

    def drawSaveSucces(self,screen):
        pygame.draw.rect(screen,(233, 119, 119),(self.rect))
        screen.blit(self.textSucces,(self.rect.x+(self.width-self.textSuccesRect.width)//2,self.rect.y+self.textSuccesRect.height))
        self.buttonClose.draw(screen)

    def checkClick(self,mousePos,status,objectGroups):
        if self.status == 0:
            if self.buttonAccept.rect.x <= mousePos[0] <= self.buttonAccept.rect.x+self.buttonAccept.rect.width and self.buttonAccept.rect.y <= mousePos[1] <= self.buttonAccept.rect.y+self.buttonAccept.rect.height:
                File.save(objectGroups)
                status.haveChange = False
                if status.isQuit: return True
                self.status = 1
            if self.buttonCancel.rect.x <= mousePos[0] <= self.buttonCancel.rect.x+self.buttonCancel.rect.width and self.buttonCancel.rect.y <= mousePos[1] <= self.buttonCancel.rect.y+self.buttonCancel.rect.height:
                status.actionType = "move"
                return True
        elif self.status == 1:
            if self.buttonClose.rect.x <= mousePos[0] <= self.buttonClose.rect.x+self.buttonClose.rect.width and self.buttonClose.rect.y <= mousePos[1] <= self.buttonClose.rect.y+self.buttonClose.rect.height:
                self.status = 0
                status.actionType = "move"
                return True
            
    def draw(self,screen):
        if self.status == 0:
            self.drawComfirm(screen)
        elif self.status == 1:
            self.drawSaveSucces(screen)