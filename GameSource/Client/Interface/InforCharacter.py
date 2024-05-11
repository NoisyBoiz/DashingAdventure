from pygame import Rect
from pygame.draw import rect, circle
from pygame.font import SysFont
from pygame.transform import scale
from System import GlobalSprites

class DrawInfor():
    def __init__(self,player,x,y,width,height,borderBar):
        self.rect = Rect(x,y,width,height)
        self.borderBar = borderBar
        self.characterName = player.characterName
        self.getPos()

    def getPos(self):
        avataImageSize = int(self.rect.height*0.8)
        self.avata = scale(GlobalSprites.mainCharacters[self.characterName]["idle_right"][0],(avataImageSize,avataImageSize))
        self.avataCircleRadius = int(self.rect.height//2)
        self.avataCirclePos = (self.rect.x+self.avataCircleRadius,self.rect.y+self.avataCircleRadius)
        self.avataImageRect = (self.rect.x + self.avataCircleRadius - avataImageSize//2, self.rect.y + self.avataCircleRadius - avataImageSize//2 - 5)

        gapColumn = 10
        hpHeight = self.rect.height*0.25
        hpWidth = self.rect.width - self.rect.height - gapColumn
       
        mpHeight = hpHeight*0.8
        mpWidth = hpWidth*0.8

        gapHpMp = 2
        gapRow = (self.rect.height - hpHeight*0.8 - hpHeight - mpHeight - gapHpMp - self.borderBar*2)//3

        self.textLevelFont = SysFont("Arial", int(hpHeight*0.8))
        self.textLevelRect = self.textLevelFont.render("Init", True, (0, 0, 0)).get_rect()
        self.textLevelRect.x = self.rect.x + self.rect.height + gapColumn
        self.textLevelRect.y = self.rect.y + gapRow

        self.hpBorderRect = Rect(self.rect.x + self.rect.height + gapColumn, self.textLevelRect.y + self.textLevelRect.height + gapRow,hpWidth,hpHeight)
        self.hpRect = Rect(self.hpBorderRect.x + self.borderBar, self.hpBorderRect.y + self.borderBar,hpWidth - self.borderBar*2,hpHeight - self.borderBar*2)
        self.hpFont = SysFont("Arial", int(self.hpRect.height*0.9))
        self.hpTextRect = self.hpFont.render("Init", True, (0, 0, 0)).get_rect()
        self.hpTextRect.x = self.hpRect.x + self.borderBar*2
        self.hpTextRect.y = self.hpRect.y + (self.hpRect.height - self.hpTextRect.height)//2
        self.mpBorderRect = Rect(self.rect.x + self.rect.height + gapColumn,self.hpBorderRect.y + self.hpBorderRect.height + gapHpMp,mpWidth,mpHeight)
        self.mpRect = Rect(self.mpBorderRect.x + self.borderBar,self.mpBorderRect.y + self.borderBar,mpWidth - self.borderBar*2,mpHeight- self.borderBar*2)
        self.mpFont = SysFont("Arial", int(self.mpRect.height*0.9))
        self.mpTextRect = self.mpFont.render("Init", True, (0, 0, 0)).get_rect()
        self.mpTextRect.x = self.mpRect.x + self.borderBar*2
        self.mpTextRect.y = self.mpRect.y + (self.mpRect.height - self.mpTextRect.height)//2
        
        
    def draw(self,screen,player):
        self.drawHpBar(screen,player)
        self.drawMpBar(screen,player)
        self.drawLevel(screen,player)
        self.drawAvata(screen)  

    # vẽ avatar của nhân vật
    def drawAvata(self,screen):
        circle(screen, (255, 175,0), self.avataCirclePos,self.avataCircleRadius)
        circle(screen, (255, 86, 0), self.avataCirclePos,self.avataCircleRadius,self.borderBar*2)
        screen.blit(self.avata,self.avataImageRect)

    # vẽ ra cấp độ của nhân vật
    def drawLevel(self,screen,player):
        if(player.exp != "max"):
            textLevel = self.textLevelFont.render(player.name +"   Lv."+str(player.level)+"   exp: "+str(player.exp)+"/"+str(player.expNextLevel), True, (0, 0, 0))
        else:
            textLevel = self.textLevelFont.render(player.name +"   Lv."+str(player.level)+" MAX", True, (0, 0, 0))
        screen.blit(textLevel,(self.textLevelRect.x,self.textLevelRect.y))

    def drawHpBar(self,screen,player):
        rect(screen, (82, 93, 102), self.hpRect)
        rect(screen, (255, 63, 49), (self.hpRect.x,self.hpRect.y,(self.hpRect.width/player.max_hp)*player.hp,self.hpRect.height))
        text = self.hpFont.render(str(player.hp)+"/"+str(player.max_hp), True, (0, 0, 0))
        screen.blit(text,(self.hpTextRect.x,self.hpTextRect.y))
        rect(screen, (50, 50, 50), self.hpBorderRect,self.borderBar)

    def drawMpBar(self,screen,player):
        rect(screen, (82, 93, 102), self.mpRect)
        rect(screen, (36, 206, 255), (self.mpRect.x,self.mpRect.y,(self.mpRect.width/player.max_mp)*player.mp,self.mpRect.height))
        text = self.mpFont.render(str(player.mp)+"/"+str(player.max_mp), True, (0, 0, 0))
        screen.blit(text,(self.mpTextRect.x,self.mpTextRect.y))
        rect(screen, (50, 50, 50), self.mpBorderRect,self.borderBar)