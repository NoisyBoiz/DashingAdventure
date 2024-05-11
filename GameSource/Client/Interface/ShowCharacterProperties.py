from pygame import Rect
from pygame.draw import rect
from System import Font, GlobalSprites
from Interact import Button
class ShowCharacterProperties:
    def __init__(self,x,y,w,h,player):
        self.rect = Rect(x,y,w,h)
        wbox = min(int(w*0.8),700)
        hbox = min(int(h*0.8),550)
        self.boxRect = Rect(x+(w-wbox)//2,y+(h-hbox)//2,wbox,hbox)
        self.gapColumn = 3
        self.imageCharacter = GlobalSprites.mainCharactersShowSelect[GlobalSprites.switchSelectIndex[player.characterName]]["idle"][0]
        self.update(player)
        self.imageDiamond = GlobalSprites.diamond[0]

        self.closeButton = Button.CircleButton(None, self.boxRect.x + self.boxRect.width - 60,self.boxRect.y + 20, 20, 1 ,(255, 189, 139),(223, 67, 0), "X")
    def update(self,player):
        self.properties = []
        self.diamondQuantity = Font.Arial20.render(str(player.diamond),True,(255,255,255))
        self.properties.append(Font.Arial20.render("Level: " + str(player.level),True,(255,255,255)))
        self.properties.append(Font.Arial20.render("HP: " + str(player.hp) + "/" + str(player.max_hp),True,(255,255,255)))
        self.properties.append(Font.Arial20.render("MP: " + str(player.mp) + "/" + str(player.max_mp),True,(255,255,255)))
        self.properties.append(Font.Arial20.render("Physical Damage: " + str(player.physical_damage),True,(255,255,255)))
        self.properties.append(Font.Arial20.render("Magic Damage: " + str(player.magic_damage),True,(255,255,255)))
        self.properties.append(Font.Arial20.render("Crit Rate: " + str(player.crit_rate) + "%",True,(255,255,255)))
        self.properties.append(Font.Arial20.render("Crit Damage: " + str(player.crit_damage) + "%",True,(255,255,255)))
        self.properties.append(Font.Arial20.render("Life Steal: " + str(player.life_steal) + "%",True,(255,255,255)))
        self.properties.append(Font.Arial20.render("Physical Armor: " + str(player.physical_armor),True,(255,255,255)))
        self.properties.append(Font.Arial20.render("Magic Armor: " + str(player.magic_armor),True,(255,255,255)))
        self.properties.append(Font.Arial20.render("Physical AP: " + str(player.physical_armor_penetration),True,(255,255,255)))
        self.properties.append(Font.Arial20.render("Magic AP: " + str(player.magic_armor_penetration),True,(255,255,255)))
        self.properties.append(Font.Arial20.render("Attack Speed: " + str(player.attack_speed)+ "%",True,(255,255,255)))
        self.properties.append(Font.Arial20.render("Speed Run: " + str(player.speed_run),True,(255,255,255)))

        self.textRect = self.properties[0].get_rect()
        self.getPosition()
    
    def getPosition(self):
        imgRect = self.imageCharacter.get_rect()
        self.imageCharacterRect = (self.boxRect.x + self.boxRect.width//4 - imgRect.width//2,self.boxRect.y + self.boxRect.height//2 - imgRect.height//2)
        self.posX = self.boxRect.x + self.boxRect.width//2 
        self.posY = self.boxRect.y + self.boxRect.height//2 - (self.textRect.height + self.gapColumn)*len(self.properties)//2

    def checkClick(self,pos):
        if self.closeButton.checkCollision(pos):
            return "Back"
        return ""
    
    def resize(self,w,h):
        self.rect.width = w
        self.rect.height = h
        self.boxRect.x = self.rect.x + (w - self.boxRect.width)//2
        self.boxRect.y = self.rect.y + (h - self.boxRect.height)//2
        self.getPosition()
        self.closeButton.resize(self.boxRect.x + self.boxRect.width - 70,self.boxRect.y + 20, 20)

    def draw(self,screen):
        rect(screen,(255, 187, 92),self.boxRect,self.boxRect.width,50)
        screen.blit(self.imageDiamond,(self.imageCharacterRect[0],self.posY))
        screen.blit(self.diamondQuantity,(self.imageCharacterRect[0] + 40,self.posY))
        screen.blit(self.imageCharacter,self.imageCharacterRect)
        for i,key in enumerate(self.properties):
            screen.blit(key,(self.posX,self.posY + i*(self.textRect.height + self.gapColumn)))
        self.closeButton.draw(screen)
       
