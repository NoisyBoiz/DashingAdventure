from pygame.draw import circle
from pygame import Surface,Rect,transform,key
from System import Font, Constant
from Function import Func
from Interact import Button

class Menu:
    def __init__(self,x,y,width,height,player,settingKeys):
        self.rect = Rect(x,y,width,height)
        self.margin = 10
        self.border = 1
        self.gap = 7
        self.circleRadius = int(Constant.block_size/2)
        self.imageSize = int(self.circleRadius*2 - self.border*2)
       
        self.settingKeys = settingKeys
        self.skills = player.listSkills

        self.getImageInit()
        self.getCircleButton()
        self.getKeyInit()

        self.surface = Surface((self.circleRadius*2,self.circleRadius*2)).convert_alpha()
        self.surface.fill((0,0,0,0))
        circle(self.surface, (0,0,0,150), (self.circleRadius,self.circleRadius), self.circleRadius)
         
        self.textAdd = Font.Arial40Bold.render("+", True, (255,255,255))
        self.textAddRect = self.textAdd.get_rect()

    def updateSettingKeys(self,settingKeys):
        self.settingKeys = settingKeys
        self.getKeyInit()

    def getImageInit(self):
        self.allImagePotion = Func.splitSprite(["Items","Potions"],150,150,self.imageSize,self.imageSize,False,False)
        self.allImageSkills = Func.splitSprite(["IconSkills"],200,200,self.imageSize,self.imageSize, False, False)

    def getCircleButton(self):
        self.skillCircleButton = []
        self.potionCircleButton = []

        x = self.rect.width - (self.gap + self.circleRadius*2) * 2
        y = self.rect.height - self.circleRadius*2*2 - self.margin - self.gap

        self.potionCircleButton.append(Button.CircleButton(self.allImagePotion["HpPotion"][4],x,y,self.circleRadius,self.border,(255, 189, 139),(223, 67, 0)))
        self.potionCircleButton.append(Button.CircleButton(self.allImagePotion["MpPotion"][4],x + (self.circleRadius*2 + self.gap),y,self.circleRadius,self.border,(255, 189, 139),(223, 67, 0)))

        x = self.rect.width - (self.gap + self.circleRadius*2) * 4
        y = self.rect.height - self.circleRadius*2 - self.margin
        for i in range(4):
            self.skillCircleButton.append(Button.CircleButton(self.allImageSkills[self.skills[i]][0],x + i*(self.circleRadius*2 + self.gap),y,self.circleRadius,self.border,(255, 189, 139),(223, 67, 0)))

    def getKeyInit(self):
        self.SkillKeyText = []
        self.PotionKeyText = []
        self.SkillKeyText.append(Font.Arial20Bold.render(key.name(self.settingKeys["skill1"]).upper(), True, (0,0,0)))
        self.SkillKeyText.append(Font.Arial20Bold.render(key.name(self.settingKeys["skill2"]).upper(), True, (0,0,0)))
        self.SkillKeyText.append(Font.Arial20Bold.render(key.name(self.settingKeys["skill3"]).upper(), True, (0,0,0)))
        self.SkillKeyText.append(Font.Arial20Bold.render(key.name(self.settingKeys["skill4"]).upper(), True, (0,0,0)))
        self.PotionKeyText.append(Font.Arial20Bold.render(key.name(self.settingKeys["health"]).upper(), True, (0,0,0)))
        self.PotionKeyText.append(Font.Arial20Bold.render(key.name(self.settingKeys["mana"]).upper(), True, (0,0,0)))

    def resize(self,width,height):
        self.rect.width = width
        self.rect.height = height
        self.getCircleButton()

    def draw(self,screen,player):
        potion = [player.hpPotion,player.mpPotion]
        CDPotion = [player.hpCDCount,player.mpCDCount]
        CDSkills = []
        for skill in self.skills:
            CDSkills.append(player.conditionSkill.Count[skill])

        for i in range(2):
            self.potionCircleButton[i].draw(screen)
            screen.blit(self.PotionKeyText[i],(self.potionCircleButton[i].rect.x - 5,self.potionCircleButton[i].rect.y - 5))
            text = Font.Arial20Bold.render(str(potion[i]), True, (0,0,0))
            screen.blit(text,(self.potionCircleButton[i].rect.x + self.potionCircleButton[i].rect.width - 15,self.potionCircleButton[i].rect.y + self.potionCircleButton[i].rect.height - 15))
            if(potion[i] == 0): 
                screen.blit(self.surface,(self.potionCircleButton[i].rect.x,self.potionCircleButton[i].rect.y))
                screen.blit(self.textAdd,(self.potionCircleButton[i].rect.x + (self.circleRadius*2 - self.textAddRect.width)//2,self.potionCircleButton[i].rect.y + (self.circleRadius*2 - self.textAddRect.height)//2))
            if(CDPotion[i]>0):
                text = Font.Arial20Bold.render(str(round(CDPotion[i]/Constant.FPS,1)), True, (255,255,255))
                textRect = text.get_rect()
                screen.blit(self.surface,(self.potionCircleButton[i].rect.x,self.potionCircleButton[i].rect.y))
                screen.blit(text,(self.potionCircleButton[i].rect.x + (self.circleRadius*2 - textRect.width)//2,self.potionCircleButton[i].rect.y + (self.circleRadius*2 - textRect.height)//2))
                
        for i in range(4):
            self.skillCircleButton[i].draw(screen)
            screen.blit(self.SkillKeyText[i],(self.skillCircleButton[i].rect.x - 5,self.skillCircleButton[i].rect.y - 5))
            if(CDSkills[i]>0):
                text = Font.Arial20Bold.render(str(round(CDSkills[i]/Constant.FPS,1)), True, (255,255,255))
                textRect = text.get_rect()
                screen.blit(self.surface,(self.skillCircleButton[i].rect.x,self.skillCircleButton[i].rect.y))
                screen.blit(text,(self.skillCircleButton[i].rect.x + (self.circleRadius*2 - textRect.width)//2,self.skillCircleButton[i].rect.y + (self.circleRadius*2 - textRect.height)//2))

