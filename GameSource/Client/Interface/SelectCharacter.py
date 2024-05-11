from pygame.draw import rect, polygon
from pygame import Rect, Surface
from System import Constant, GlobalSprites, Font
from Interact import Button
from Function import Func

class SelectCharacter:
    def __init__(self,textButtonPlay,properties):
        self.widthCard = 75
        self.heightCard = self.widthCard
        self.gapColumn = 10
        self.aniIdle_count = 0
        self.aniIdle_delay = 4
        self.aniRun_count = 0
        self.aniRun_delay = 4
        self.indexIdle = 0
        self.len = GlobalSprites.lengthMainCharacters[list(GlobalSprites.lengthMainCharacters.keys())[0]]
        self.cardRect = []
        self.cardImageRect = []
        self.imageRect = GlobalSprites.mainCharacters[list(GlobalSprites.mainCharacters.keys())[0]]["idle_left"][0].get_rect()
        self.colorMarginSelect = (255, 93, 16)
        self.colorMarginInSelect = (250, 240, 228)
        self.colorBackgroundSelect = (255, 93, 16)
        self.colorBackgroundInSelect = (255, 133, 81)
        self.idSelect = 0
        self.ButtonBack = Button.Button("Back",10,Constant.Screen_Height - 60,100,40,4,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.ButtonPlay = Button.Button(textButtonPlay,Constant.Screen_Width - 110,Constant.Screen_Height - 60,100,40,4,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.handleRectCard()
        self.switch = GlobalSprites.switchSelect
        self.characterName = "healer"
        self.showSelectRect = GlobalSprites.mainCharactersShowSelect[0]["idle"][0].get_rect()
        self.SkillDescription = SkillDescription(Constant.Screen_Width*3//4 + self.showSelectRect.width//4 - 260//2 ,Constant.Screen_Height//3, 260, 100)
        self.characterProperties = characterProperties(Constant.Screen_Width//4 - self.showSelectRect.width//4 - 230//2, 0 ,properties)
    def update(self,properties):
        self.characterProperties.update(properties)
    def reset(self):
        self.characterName = "healer"
        self.idSelect = 0
    def loop(self):
        self.aniIdle_count += 1
        self.indexIdle = self.aniIdle_count//self.aniIdle_delay%self.len["idle"]
        if self.aniIdle_count // self.aniIdle_delay >= self.len["idle"]:
            self.aniIdle_count = 0
    
    def resize(self,width,height):
        self.widthCard = int(width/Constant.Screen_Width_Origin * 75)
        self.heightCard = self.widthCard
        self.gapColumn = int(width/Constant.Screen_Width_Origin * 10)
        self.ButtonBack.resize(10,height - 60,100,40)
        self.ButtonPlay.resize(width - 110,height - 60,100,40)
        self.handleRectCard()
        self.SkillDescription.resize(width*3//4 + self.showSelectRect.width//4 - 260//2 ,height//3)
        self.characterProperties.resize(width//4 - self.showSelectRect.width//4 - self.characterProperties.width//2, 0)

    def handleRectCard(self):
        self.cardRect.clear()
        self.cardImageRect.clear()
        center = (Constant.Screen_Width - self.gapColumn*3 - self.widthCard*4)/2
        py = (Constant.Screen_Height-self.heightCard - 20)
        for i in range(4):
            self.cardRect.append((center + self.gapColumn*i +self.widthCard*i,py))

        py = py + (self.heightCard - self.imageRect.height)//2
        margin = (self.widthCard - self.imageRect.width)//2
        for i in range(4):
            self.cardImageRect.append((self.cardRect[i][0]+margin,py))

    def checkClick(self,pos):
        for i in range(4):
            if self.cardRect[i][0] <= pos[0] <= self.cardRect[i][0]+self.widthCard and self.cardRect[i][1] <= pos[1] <= self.cardRect[i][1]+self.heightCard:
                self.idSelect = i
                self.aniRun_count = 0
                self.indexRun = 0
                self.characterName = self.switch[i]
                self.SkillDescription.characterName = self.characterName
                self.characterProperties.characterName = self.characterName

        if self.ButtonPlay.rect.collidepoint(pos):
            if self.idSelect == None: return ""
            return "Select"
        if self.ButtonBack.rect.collidepoint(pos):
            return "Back"

        self.SkillDescription.handleEvent(pos)
        
        return ""
    
    def draw(self,screen):
        screen.blit(GlobalSprites.mainCharactersShowSelect[self.idSelect]["idle"][self.indexIdle],((Constant.Screen_Width - self.showSelectRect.width)//2,(Constant.Screen_Height - self.showSelectRect.height)//2))
        for i in range(4):
            if self.idSelect == i: 
                colorMargin = self.colorMarginSelect
                colorBackground = self.colorBackgroundSelect
            else: 
                colorMargin = self.colorMarginInSelect
                colorBackground = self.colorBackgroundInSelect
            rect(screen,colorBackground,(self.cardRect[i][0],self.cardRect[i][1],self.widthCard,self.heightCard))
            rect(screen,colorMargin,(self.cardRect[i][0],self.cardRect[i][1],self.widthCard,self.heightCard),4)
            screen.blit(GlobalSprites.mainCharactersSelectIcon[i]["idle"][self.indexIdle],self.cardImageRect[i])
        self.ButtonPlay.draw(screen)
        self.ButtonBack.draw(screen)
        self.SkillDescription.draw(screen)
        self.characterProperties.draw(screen)

class SkillDescription:
    def __init__(self,x,y,width,height):
        self.rect = Rect(x,y,width,height)
        self.border = 2
        self.gap = 10
        self.circleRadius = (width - self.gap*3)//8
        self.imageSize = int(self.circleRadius*2 - self.border*2)
        self.allImageSkills = Func.splitSprite(["IconSkills"],200,200,self.imageSize,self.imageSize, False, False)
        self.characterName = "healer"
        self.descriptionStep = ""
        self.index = 0
        self.surface = Surface((width,height)).convert_alpha()
        # self.surface.fill((255,255,255,0))
        self.descriptionText = {
            "heal": "Heal: Heal for all players by 200% your magic damage",
            "debuffEnemy": "Debuff Enemy: Reduce 50% of enemy damage",
            "buffPlayers": "Buff Players: Increase 50% of players damage",
            "revival": "Revival: Revive all dead players or heal all players alive by 200% your magic damage",
            "dragon": "Dragon: Summon a dragon to attack enemy",
            "meteorites": "Meteorites: Summon meteorites to attack enemy",
            "burn": "Burn: Burn enemy by 0.5% of enemy max health per second",
            "fireBall": "Fire Ball: Summon a fire ball to attack enemy in 5 seconds",
            "slash": "Slash: Slash enemy",
            "flash": "Flash: Flash to enemy",
            "assassinBuff": "Assassin Buff: Increase 50% of your damage",
            "teleport": "Teleport: Teleport to enemy",
            "buffArmor": "Buff Armor: Increase 50% of your armor",
            "explosion": "Explosion: Reduce your health by 50% and deal damage equal 50% your health to enemy",
            "autoHealth": "Auto Health: Heal 2% of your max health per second",
            "summonPet": "Summon Pet: Summon a pet to attack enemy, your pet will disappear when pet die or you die"
        }
        self.skills = {
            "healer" : ["heal","debuffEnemy","buffPlayers","revival"],
            "wizard" : ["dragon","meteorites","burn","fireBall"],
            "assassin" : ["slash","flash","assassinBuff","teleport"],
            "paladin" : ["buffArmor","explosion","autoHealth","summonPet"]
        }
        self.getCircleButton()

    def resize(self,x,y):
        self.rect.x = x
        self.rect.y = y
        self.getCircleButton()
        
    def getCircleButton(self):
        self.skillCircleButton = {}
        for charName in self.skills:
            self.skillCircleButton[charName] = []
            for i in range(4):
                self.skillCircleButton[charName].append(Button.CircleButton(self.allImageSkills[self.skills[charName][i]][0],self.rect.x + i*(self.circleRadius*2 + self.gap),self.rect.y,self.circleRadius,self.border,(255, 189, 139),(223, 67, 0)))

    def getDescriptionBox(self,screen,text):
        arrText = []
        ms = ""
        for i in text.split(" "):
            if Font.Arial20.render((ms + i + " "), True, (0,0,0)).get_rect().width > self.rect.width - 20:
                arrText.append(Font.Arial20.render(ms, True, (0,0,0))) 
                ms = i + " "
            else:
                ms += i + " "
        
        if ms != "":
            arrText.append(Font.Arial20.render(ms, True, (0,0,0)))
        textRect = arrText[0].get_rect()

        y = self.rect.y + self.circleRadius*2 + 20
        h = max(textRect.height*len(arrText) + 20,100)
        rect(screen, (255, 204, 112), (self.rect.x,y,self.rect.width,h),min(self.rect.width,h)//2, min(self.rect.width,h)//20)
        rect(screen, (198, 61, 47), (self.rect.x,y,self.rect.width,h),2, min(self.rect.width,h)//20)
        for i in range(len(arrText)):
            screen.blit(arrText[i],(self.rect.x + 10,y + 10 + i*textRect.height))

    def handleEvent(self,pos):
        onclick = False
        for i in range(4):
            if self.skillCircleButton[self.characterName][i].checkCollision(pos):
                self.descriptionStep = self.skills[self.characterName][i]
                self.index = i%4
                onclick = True
                break
        if not onclick:
            self.descriptionStep = ""
                
    def draw(self,screen):
        for i in range(4):
            self.skillCircleButton[self.characterName][i].draw(screen)

        if self.descriptionStep != "":
            width = self.circleRadius*2
            size = 30
            x = self.skillCircleButton[self.characterName][self.index].rect.x
            y = self.rect.y + self.circleRadius*2 + 20
            polygon(screen, (198, 61, 47), [(x + width//2 - size//2 , y),(x + width//2 + size//2, y),(x + width//2, y - size//2)])
            self.getDescriptionBox(screen,self.descriptionText[self.descriptionStep])


class characterProperties:
    def __init__(self,x,y,properties):
        self.x = x
        self.y = y
        self.width = 230
        self.gapColumn = 3
        self.characterName = "healer"
        self.properties = properties
        self.listChar = ["healer", "wizard", "assassin", "paladin"]
        self.update(properties)

    def update(self,properties):
        self.AllProperties = {}
        for charName in self.listChar:
            if charName in properties:
                pro = properties[charName]
            else: 
                pro = DefaulProperties[charName]
            self.AllProperties[charName] = []
            self.AllProperties[charName].append(Font.Arial20.render("Level: " + str(pro["level"]),True,(0,0,0)))
            self.AllProperties[charName].append(Font.Arial20.render("HP: " + str(pro["max_hp"]),True,(0,0,0)))
            self.AllProperties[charName].append(Font.Arial20.render("MP: " + str(pro["max_mp"]),True,(0,0,0)))
            self.AllProperties[charName].append(Font.Arial20.render("Physical Damage: " + str(pro["physical_damage"]),True,(0,0,0)))
            self.AllProperties[charName].append(Font.Arial20.render("Magic Damage: " + str(pro["magic_damage"]),True,(0,0,0)))
            self.AllProperties[charName].append(Font.Arial20.render("Crit Rate: " + str(pro["crit_rate"]) + "%",True,(0,0,0)))
            self.AllProperties[charName].append(Font.Arial20.render("Crit Damage: " + str(pro["crit_damage"]) + "%",True,(0,0,0)))
            self.AllProperties[charName].append(Font.Arial20.render("Life Steal: " + str(pro["life_steal"]) + "%",True,(0,0,0)))
            self.AllProperties[charName].append(Font.Arial20.render("Physical Armor: " + str(pro["physical_armor"]),True,(0,0,0)))
            self.AllProperties[charName].append(Font.Arial20.render("Magic Armor: " + str(pro["magic_armor"]),True,(0,0,0)))
            self.AllProperties[charName].append(Font.Arial20.render("Physical AP: " + str(pro["physical_armor_penetration"]),True,(0,0,0)))
            self.AllProperties[charName].append(Font.Arial20.render("Magic AP: " + str(pro["magic_armor_penetration"]),True,(0,0,0)))
            self.AllProperties[charName].append(Font.Arial20.render("Attack Speed: " + str(pro["attack_speed"])+ "%",True,(0,0,0)))
            self.AllProperties[charName].append(Font.Arial20.render("Speed Run: " + str(pro["speed_run"]),True,(0,0,0)))
               
        self.getPos()
    def getPos(self):
        self.height = (self.AllProperties["healer"][0].get_rect().height + self.gapColumn)*len(self.AllProperties["healer"])
        self.PosX = self.x
        self.PosY = self.y + Constant.Screen_Height//2 - 50 - self.height//2

    def resize(self,x,y):
        self.x = x
        self.y = y
        self.getPos()

    def draw(self,screen):
        rect(screen, (255, 204, 112), (self.PosX-20,self.PosY-15,self.width,self.height+30),self.width//2, self.width//20)
        for i,key in enumerate(self.AllProperties[self.characterName]):
            screen.blit(key,(self.PosX, self.PosY + i*(key.get_rect().height + self.gapColumn)))



DefaulProperties = {
    "healer":{
        "level": 1,
        "max_hp": 1500,
        "max_mp": 1500,
        "physical_damage": 0,
        "magic_damage": 200,
        "crit_rate": 10,
        "crit_damage": 100,
        "life_steal": 10,
        "physical_armor": 0,
        "magic_armor": 0,
        "physical_armor_penetration": 0,
        "magic_armor_penetration": 0,
        "attack_speed": 100,
        "speed_run": 5,
        "speed_jump": 9
    },
    "wizard":{
        "level": 1,
        "max_hp": 1000,
        "max_mp": 2000,
        "physical_damage": 0,
        "magic_damage": 200,
        "crit_rate": 10,
        "crit_damage": 100,
        "life_steal": 10,
        "physical_armor": 0,
        "magic_armor": 0,
        "physical_armor_penetration": 0,
        "magic_armor_penetration": 50,
        "attack_speed": 100,
        "speed_run": 5,
        "speed_jump": 9
    },
    "assassin":{
        "level": 1,
        "max_hp": 2000,
        "max_mp": 1000,
        "physical_damage": 50,
        "magic_damage": 0,
        "crit_rate": 40,
        "crit_damage": 100,
        "life_steal": 10,
        "physical_armor": 20,
        "magic_armor": 20,
        "physical_armor_penetration": 50,
        "magic_armor_penetration": 10,
        "attack_speed": 100,
        "speed_run": 5,
        "speed_jump": 9
    },
    "paladin":{
        "level": 1,
        "max_hp": 3000,
        "max_mp": 1000,
        "physical_damage": 10,
        "magic_damage": 10,
        "crit_rate": 10,
        "crit_damage": 100,
        "life_steal": 10,
        "physical_armor": 50,
        "magic_armor": 50,
        "physical_armor_penetration": 5,
        "magic_armor_penetration": 5,
        "attack_speed": 100,
        "speed_run": 5,
        "speed_jump": 9
    }
}
