from pygame import Rect
from pygame.draw import rect
from System import Font, GlobalSprites
from Interact import Button 
class Achievement:
    def __init__(self,x,y,w,h,player):
        self.rect = Rect(x,y,w,h)
        wbox = min(int(w*0.8),700)
        hbox = min(int(h*0.8),550)
        self.boxRect = Rect(x+(w-wbox)//2,y+(h-hbox)//2,wbox,hbox)
        self.gapColumn = 10
        self.gapRow = 10
        self.getTextInit()
        self.getAchievementAllPlayer(player)
        self.closeButton = Button.CircleButton(None, self.boxRect.x + self.boxRect.width - 60,self.boxRect.y + 20, 20, 1 ,(255, 189, 139),(223, 67, 0), "X")
    def update(self,players):
        self.getAchievementAllPlayer(players)

    def getAchievementAllPlayer(self,players):
        self.achievementAllPlayer = []
        for player in players:
            self.achievementAllPlayer.append(self.getAchievement(player))
        self.getPosition()

    def getTextInit(self):
        self.textInit = []

        self.textInit.append(Font.Arial20.render("Player Name: ",True,(255,255,255)))
        self.textInit.append(Font.Arial20.render("Total Damage: ",True,(255,255,255)))
        self.textInit.append(Font.Arial20.render("Total Damage Get: ",True,(255,255,255)))
        self.textInit.append(Font.Arial20.render("Total Heal: ",True,(255,255,255)))

    def getAchievement(self,player):
        self.properties = []

        self.properties.append(Font.Arial20.render(str(player.name),True,(255,255,255)))
        self.properties.append(Font.Arial20.render(str(player.totalDamage),True,(255,255,255)))
        self.properties.append(Font.Arial20.render(str(player.totalGetHit),True,(255,255,255)))
        self.properties.append(Font.Arial20.render(str(player.totalHeal) ,True,(255,255,255)))
       
        self.textRect = self.properties[0].get_rect()
        return self.properties
   
    def getPosition(self):
        self.posX = self.boxRect.x + (self.boxRect.width - len(self.achievementAllPlayer) * (100 + self.gapColumn) - (150 + self.gapColumn)) // (len(self.achievementAllPlayer) + 2)
        self.posY = self.boxRect.y + self.boxRect.height//2 - (self.textRect.height + self.gapRow)*len(self.properties)//2
    
    def checkClick(self,pos):
        if self.closeButton.checkCollision(pos):
            return "Back"
        return ""
    
    def resize(self,w,h):
        self.rect.width = w
        self.rect.height = h
        self.boxRect.x = self.rect.x + (w - self.boxRect.width)//2
        self.boxRect.y = self.rect.y + (h - self.boxRect.height)//2
        self.closeButton.resize(self.boxRect.x + self.boxRect.width - 70,self.boxRect.y + 20, 20)
        self.getPosition()

    def draw(self,screen):
        rect(screen,(255, 187, 92),self.boxRect,self.boxRect.width,50)
        for i,key in enumerate(self.textInit):
            screen.blit(key,(self.posX,self.posY + i*(self.textRect.height + self.gapRow)))
        for i,key in enumerate(self.achievementAllPlayer):
            for j,txt in enumerate(key):
                screen.blit(txt,(self.posX +  (150 + self.gapColumn) + (100 + self.gapColumn)*i, self.posY + j*(self.textRect.height + self.gapRow)))
        self.closeButton.draw(screen)
