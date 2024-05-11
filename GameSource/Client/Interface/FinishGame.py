from pygame import Rect, Surface
from Interact import Button
from System import Constant, Font
class FinishGame:
    def __init__(self,x,y,width,height):
        self.rect = Rect(x,y,width,height)
        self.surface = Surface((Constant.Screen_Width,Constant.Screen_Height)).convert_alpha()
        self.surface.fill((168, 223, 142,150))
        self.text = Font.Avara40.render("Congratulation!", True, (255,255,255))
        self.text2 = Font.Avara40.render("You have completed the game!", True, (255,255,255))
        self.isObserve = False
        self.isClose = False
        self.interactInit(width,height)

    def interactInit(self,width,height):
        self.exitButton = Button.Button("Exit",10,height - 50,200,40,2,(31, 65, 114),(19, 32, 67),(255, 255, 255))
        self.closeButton = Button.Button("Close",(width - 200)//2, height//2 + 100, 200, 40,2,(31, 65, 114),(19, 32, 67),(255, 255, 255))

    def resize(self,width,height):
        self.surface = Surface((width,height)).convert_alpha()
        self.surface.fill((168, 223, 142,150))
        self.interactInit(width,height)

    def checkClick(self,pos):
        if self.isClose:
            if self.exitButton.rect.collidepoint(pos):
                return "Exit"
        else:
            if self.closeButton.rect.collidepoint(pos):
                self.isClose = True
        return ""

    def draw(self,screen):
        if self.isClose:
            self.exitButton.draw(screen)
        else:
            screen.blit(self.surface,(0,0))
            screen.blit(self.text,(Constant.Screen_Width//2 - self.text.get_rect().width//2,Constant.Screen_Height//3 - self.text.get_rect().height//2))
            screen.blit(self.text2,(Constant.Screen_Width//2 - self.text2.get_rect().width//2,Constant.Screen_Height//2 - self.text2.get_rect().height//2))
            self.closeButton.draw(screen)
            