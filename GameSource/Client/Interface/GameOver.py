from pygame import Surface
from System import Constant,Font
from Interact import Button
class GameOver:
    def __init__(self,x,y,width,height):
        self.surface = Surface((Constant.Screen_Width,Constant.Screen_Height)).convert_alpha()
        self.surface.fill((205, 250, 213, 150))
        self.text = Font.Arial60.render("You Are Dead!", True, (0,0,0))
        self.text2 = Font.Arial40.render("You can exit game or revial with at least 5 diamond", True, (0,0,0))
        self.interactInit(width,height)
        self.isObserve = False
    def interactInit(self,width,height):
        buttonWidth = 120
        buttonHeight = 50
        gap = 100
        top = height*2//3
        self.exitButton = Button.Button("Exit",(width - buttonWidth*2 - gap)//2,top,buttonWidth,buttonHeight,2,(255,255,255),(255,0,0),(255,0,0))
        self.revivalButton = Button.Button("Revival",(width + gap)//2, top, buttonWidth, buttonHeight,2,(255,255,255),(255,0,0),(255,0,0))
        self.observeButton = Button.Button("Observe other player",(width - 300)//2, top + 70, 300, 50,2,(255,255,255),(255,0,0),(255,0,0))
        self.backButton = Button.Button("Back",10, height - 50, 200, 40, 2, (255,255,255), (255,0,0), (255,0,0))
    def checkClick(self,pos,canObserveOtherPlayer):
        if self.isObserve:
            if self.backButton.rect.collidepoint(pos):
                return "Back"
        else:
            if self.exitButton.rect.collidepoint(pos):
                return "Exit"
            if self.revivalButton.rect.collidepoint(pos):
                return "Revival"
            if self.observeButton.rect.collidepoint(pos) and canObserveOtherPlayer:
                return "Observe"
        return ""
    def resize(self,width,height):
        self.surface = Surface((width,height)).convert_alpha()
        self.surface.fill((150,20,40,150))
        self.interactInit(width,height)
        
    def draw(self,screen,canObserveOtherPlayer,diamond):
        if self.isObserve:
            self.backButton.draw(screen)
        else:
            screen.blit(self.surface,(0,0))
            screen.blit(self.text,(Constant.Screen_Width//2 - self.text.get_rect().width//2,Constant.Screen_Height//3 - 50 - self.text.get_rect().height//2))
            screen.blit(self.text2,(Constant.Screen_Width//2 - self.text2.get_rect().width//2,Constant.Screen_Height//3 + 50 - self.text2.get_rect().height//2))
            text = Font.Arial30.render("Your diamond: " + str(diamond), True, (0,0,0))
            screen.blit(text,(Constant.Screen_Width//2 - text.get_rect().width//2,Constant.Screen_Height//3 + 100 - text.get_rect().height//2))

            self.exitButton.draw(screen)
            self.revivalButton.draw(screen)
            if canObserveOtherPlayer: self.observeButton.draw(screen)