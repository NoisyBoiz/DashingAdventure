from System import Font,Constant
from pygame import Rect, key, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from pygame.draw import rect
from Interact import InputBox,Button
from Function import HandleFile

class Setting:
    def __init__(self,x,y,w,h):
        self.rect = Rect(x,y,w,h)
        self.interactInit(w,h)
    def interactInit(self,w,h):
        buttonWidth = 250
        buttonHeight = 50
        gap = 10
        top = (h - buttonHeight*3 - gap*2)//2
        self.settingControl = Button.Button("Control",(w-buttonWidth)//2,top,buttonWidth,buttonHeight,4,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.settingSound = Button.Button("Music",(w-buttonWidth)//2,top + buttonHeight + gap,buttonWidth,buttonHeight,4,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.backButton = Button.Button("Back",10, h - 60,150,buttonHeight,4,(255, 120, 90),(250, 240, 228),(255, 255, 255))
    def resize(self,w,h):
        self.rect.width = w
        self.rect.height = h
        self.interactInit(w,h)

    def checkClick(self,pos):
        if self.settingControl.rect.collidepoint(pos):
            return "Control"
        if self.settingSound.rect.collidepoint(pos):
            return "Sound"
        if self.backButton.rect.collidepoint(pos):
            return "Back"
        return ""
    def draw(self,screen):
        rect(screen,(196, 223, 223),self.rect)
        self.settingControl.draw(screen)
        self.settingSound.draw(screen)
        self.backButton.draw(screen)

class SettingControl:
    def __init__(self,x,y,w,h,settingKeys):
        self.rect = Rect(x,y,w,h)
        self.content = ["Left","Right","Up","Skill 1","Skill 2","Skill 3","Skill 4","Skill 5","Health","Recove Mana","Escape Gate"]
        self.control = ["left","right","up","skill1","skill2","skill3","skill4","skill5","health","mana","escapeGate"]
        self.gapColumn = 10
        self.gapRow = 100
        self.settingKeys = settingKeys
        self.textInit(x,y,w,h)
        self.edit = False
        self.isDuplicate = False
    def textInit(self,x,y,w,h):
        self.contentText = []
        self.posText = []
        self.input = []

        for content in self.content:
            self.contentText.append(Font.Arial20.render(content + ": ", True, (0,0,0)))

        x = (Constant.Screen_Width - 300)//2
        y = 50
        inputWidth = 100
        inputHeight = 30
        for i in range(len(self.content)):
            self.posText.append((x, y + i*(inputHeight + self.gapColumn)))
            self.input.append(InputBox.Key(key.name(self.settingKeys[self.control[i]]),x + 200, y + i*(inputHeight + self.gapColumn), inputWidth, inputHeight, key.name(self.settingKeys[self.control[i]])))
        
        buttonWidth = 100
        gap = 10
        self.editButton = Button.Button("Edit", (w - buttonWidth*3 - gap*2)//2, h - 50, buttonWidth, 40,2,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.resetButton = Button.Button("Reset", (w - buttonWidth)//2, h - 50, buttonWidth, 40,2,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.saveButton = Button.Button("Save", (w + buttonWidth + gap*2)//2, h - 50, buttonWidth, 40,2,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.backButton = Button.Button("Back", 10, h-50, buttonWidth,40,2,(255, 120, 90),(250, 240, 228),(255, 255, 255))

    def resize(self,w,h):
        x = self.rect.x
        y = self.rect.y
        self.rect = Rect(x,y,w,h)
        self.textInit(x,y,w,h)

    def handle_event(self,event):
        if not self.edit: return

        for i in self.input:
            i.handle_event(event)

        dup = []
        for i in self.input:
            for j in self.input:
                if i!=j and i.text == j.text:
                    i.duplicate(True)
                    j.duplicate(True)
                    if i not in dup: dup.append(i)
                    if j not in dup: dup.append(j)
                else:
                    if i not in dup: i.duplicate(False)
                    if j not in dup: j.duplicate(False)

        self.isDuplicate = len(dup) > 0
                
    def checkClick(self,pos):
        if self.editButton.rect.collidepoint(pos):
            self.editSwitch()
            return ""
        if self.resetButton.rect.collidepoint(pos):
            data = HandleFile.readFile("Keys.json")
            data["keys"] = data["keysDefault"]
            self.settingKeys = data["keysDefault"]
            HandleFile.saveFile("Keys.json",data)
            for i,k in enumerate(self.input):
                k.reset(key.name(self.settingKeys[self.control[i]]))
            return ""
        if self.edit and self.saveButton.rect.collidepoint(pos) and not self.isDuplicate:
            data = HandleFile.readFile("Keys.json")
            for i,k in enumerate(self.input):
                data["keys"][self.control[i]] = key.key_code(k.text)
            HandleFile.saveFile("Keys.json",data)
            self.editSwitch()
            return "Save"
        if self.backButton.rect.collidepoint(pos):
            return "Back"
        
    def editSwitch(self):
        self.edit = not self.edit
        self.editButton.updateText("UnEdit" if self.edit else "Edit")
        for button in self.input:
            button.changeColor(self.edit)

    def draw(self,screen):
        rect(screen,(196, 223, 223),self.rect)
        for i,k in enumerate(self.contentText):
            screen.blit(k,self.posText[i])
        for i in self.input:
            i.draw(screen)
        self.editButton.draw(screen)
        self.resetButton.draw(screen)
        self.saveButton.draw(screen)
        self.backButton.draw(screen)


class SettingSound:
    def __init__(self,x,y,w,h,soundSetting):
        self.rect = Rect(x,y,w,h)
        self.content = ["Background Music","Sound Effect"]
        self.keys = ["BackgroundMusic","SoundEffect"]
        self.soundSetting = soundSetting
        self.interactInit(w,h)

    def interactInit(self,w,h):
        self.contentText = []
        self.posText = []
        self.range = []
    
        for txt in self.content:
            self.contentText.append(Font.Arial20.render(txt, True, (0,0,0)))
            
        rangeWidth = 200
        rangeHeight = 10
        gapColumn = 200
        gapRow = 20
        textRect = self.contentText[0].get_rect()
        x = (Constant.Screen_Width - rangeWidth - gapColumn)//2
        top = (Constant.Screen_Height - (textRect.height + gapRow)*len(self.content))//2

        for i in range(len(self.content)):
            self.posText.append((x,top + i*(textRect.height + gapRow)))
            self.range.append(InputBox.Range(x + gapColumn, top + i*(textRect.height + gapRow),rangeWidth,rangeHeight,0,0,100))

        self.backButton = Button.Button("Back",10, h-50, 100,40,2,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.updateValue()

    def handle_event(self,event):
        for i in self.range:
            if i.handle_event(event):
                self.soundSetting[self.keys[self.range.index(i)]] = i.value
                HandleFile.saveFile("Sound.json",self.soundSetting)
                return True
        return False
    
    def checkClick(self,pos):
        if self.backButton.rect.collidepoint(pos):
            return "Back"
        return ""
    
    def updateSoundSetting(self,soundSetting):
        self.soundSetting = soundSetting
        self.updateValue()

    def updateValue(self):
        for i,k in enumerate(self.range):
            k.setValue(self.soundSetting[self.keys[i]])

    def resize(self,w,h):
        self.interactInit(w,h)

    def draw(self,screen):
        rect(screen,(196, 223, 223),self.rect)
        for i,k in enumerate(self.contentText):
            screen.blit(k,self.posText[i])
        for i in self.range:
            i.draw(screen)
        self.backButton.draw(screen)
        