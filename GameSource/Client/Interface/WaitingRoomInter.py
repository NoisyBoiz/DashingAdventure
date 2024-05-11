from pygame.draw import rect
from System import Constant,Font,GlobalSprites
from Interact import Button

class WaitingRoom:
    def __init__(self,x,y,width,height):
        self.thisPlayerID = None 
        self.hostID = {}
        self.playerID =  {}
        self.playerCharacter = [None,None,None,None]
        self.textName = [None,None,None,None]
        self.textNameRect = [None,None,None,None]
        self.readyPlayer = [False,False,False,False]
        
        self.aniIdle_count = 0
        self.aniIdle_delay = 3
        self.aniRun_count = 0
        self.aniRun_delay = 4
        self.indexIdle = 0
        self.len = GlobalSprites.lengthMainCharacters[list(GlobalSprites.lengthMainCharacters.keys())[0]]
        self.cardRect = []
        self.cardImageRect = []
        self.readyBoxRect = []
        self.imageRect = GlobalSprites.mainCharactersSelect[0]["idle"][0].get_rect()
        self.colorBackground = (255, 93, 16)
        self.idSelect = 0
        
        self.ButtonBack = Button.Button("Back",10,Constant.Screen_Height - 60,100,40,5,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.ButtonPlay = Button.Button("Play",Constant.Screen_Width - 110,Constant.Screen_Height - 60,100,40,5,(255, 235, 200),(250, 240, 228),(255, 255, 255))
        self.ButtonPlayActive = Button.Button("Play",Constant.Screen_Width - 110,Constant.Screen_Height - 60,100,40,5,(225, 50, 10),(250, 240, 228),(255, 255, 255))
        self.ButtonReady = Button.Button("Ready",Constant.Screen_Width - 110,Constant.Screen_Height - 60,100,40,5,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.ButtonUnReady = Button.Button("UnReady",Constant.Screen_Width - 110,Constant.Screen_Height - 60,100,40,5,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.ButtonChangeCharacter = Button.Button("Change Character",(Constant.Screen_Width - 150)//2,Constant.Screen_Height - 60,150,40,5,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.switch = GlobalSprites.switchSelectIndex
        self.roomID = ""
        self.textRoomID = Font.Arial20Bold.render("Room ID: " + self.roomID,True,(0,0,0))
        self.textRoomIDRect = self.textRoomID.get_rect()
        self.textAddPlayer = Font.Arial80Bold.render("+",True,(255, 150, 100))
        self.textAddPlayerRect = self.textAddPlayer.get_rect()
        self.textReady = Font.Arial20Bold.render("Ready",True,(0,0,0))
        self.textUnReady = Font.Arial20Bold.render("UnReady",True,(0,0,0))
        self.textReadyRect = []
        self.textUnReadyRect = []
        self.allPlayerReady = False
        self.handleRectCard(width,height)
    def updateRoom(self,waitingRoom):
        receivePlayers = waitingRoom.players
        copyPlayer = self.playerID.copy()
        copyReceivePlayers = receivePlayers.copy()

        for key in copyPlayer:
            if key not in copyReceivePlayers:
                self.removePlayer(self.playerID[key])
                self.playerID.pop(key)
            else:
                if receivePlayers[key].characterName != self.playerCharacter[self.playerID[key]]:
                    self.updatePlayerCharacter(self.playerID[key],receivePlayers[key].characterName)
                receivePlayers.pop(key)
                
        for plID in receivePlayers:
            self.updateNewPlayer(receivePlayers[plID])
        
        if waitingRoom.host not in self.hostID:
            self.hostID.clear()
            self.hostID[waitingRoom.host] = self.playerID[waitingRoom.host]

        self.readyPlayer = [False,False,False,False]
        for plID in waitingRoom.readyPlayer:
            self.readyPlayer[self.playerID[plID]] = True
        if len(waitingRoom.readyPlayer) == len(self.playerID) - 1:
            self.allPlayerReady = True
        else:
            self.allPlayerReady = False

    def removePlayer(self,ite):
        self.playerCharacter[ite] = None
        self.textName[ite] = None
        self.textNameRect[ite] = None
       
    def updatePlayerCharacter(self,ite,charName):
        self.playerCharacter[ite] = charName
    def updateNewPlayer(self,player):
        firstNone = self.playerCharacter.index(None)
        self.playerID[player.id] = firstNone
        self.playerCharacter[firstNone] = player.characterName
        self.textName[firstNone] = Font.Arial20.render(player.name,True,(0,0,0))
        self.textNameRect[firstNone] = self.textName[firstNone].get_rect()

    def updateRoomID(self,roomID):
        self.roomID = roomID
        self.textRoomID = Font.Arial20.render("Room ID: " + self.roomID,True,(0,0,0))
        self.textRoomIDRect = self.textRoomID.get_rect()
        
    def loop(self):
        self.aniIdle_count += 1
        self.indexIdle = self.aniIdle_count//self.aniIdle_delay%self.len["idle"]
        if self.aniIdle_count // self.aniIdle_delay >= self.len["idle"]:
            self.aniIdle_count = 0
    
    def resize(self,width,height):
        self.ButtonBack.resize(10,height - 60,100,40)
        self.ButtonPlay.resize(width - 110,height - 60,100,40)
        self.ButtonPlayActive.resize(width - 110,height - 60,100,40)
        self.ButtonReady.resize(width - 110,height - 60,100,40)
        self.ButtonUnReady.resize(width - 110,height - 60,100,40)
        self.ButtonChangeCharacter.resize((width - 150)//2,height - 60,150,40)
        self.handleRectCard(width,height)

    def handleRectCard(self,width,height):
        self.widthCard = width//6

        if width > 1000: 
            self.widthCard = width//8

        self.heightCard = self.widthCard//2*3
        self.gap = (width - self.widthCard*4)//5

        self.cardRect.clear()
        self.cardImageRect.clear()

        py = (height-self.heightCard)//2
        for i in range(4):
            self.cardRect.append((self.gap*(i+1)+self.widthCard*i,py))
    
        py = (height-self.imageRect.height)//2
        margin = (self.widthCard - self.imageRect.width)//2
        for i in range(4):
            self.cardImageRect.append((self.cardRect[i][0]+margin,py))

        readyTextRect = self.textReady.get_rect()
        unreadyTextRect = self.textUnReady.get_rect()

        widthReadyBox = self.widthCard*0.8
        heightReadyBox = readyTextRect.height * 1.3
       
        self.readyBoxRect.clear()
        self.textReadyRect.clear()
        self.textUnReadyRect.clear()

        for i in range(4):
            self.readyBoxRect.append((self.cardRect[i][0]+(self.widthCard-widthReadyBox)//2,self.cardRect[i][1] - heightReadyBox - 10,widthReadyBox,heightReadyBox))
            self.textReadyRect.append((self.readyBoxRect[i][0]+(self.readyBoxRect[i][2]-readyTextRect.width)//2,self.readyBoxRect[i][1]+(self.readyBoxRect[i][3]-readyTextRect.height)//2))
            self.textUnReadyRect.append((self.readyBoxRect[i][0]+(self.readyBoxRect[i][2]-unreadyTextRect.width)//2,self.readyBoxRect[i][1]+(self.readyBoxRect[i][3]-unreadyTextRect.height)//2))

    def checkClick(self,pos):
        if self.ButtonChangeCharacter.rect.collidepoint(pos):
            return "ChangeCharacter"
        if self.ButtonPlay.rect.collidepoint(pos) and self.idSelect != None:
            return "Start"
        if self.ButtonBack.rect.collidepoint(pos):
            return "Back"
        return ""
    
    def draw(self,screen):
        for i in range(4):
            if self.playerCharacter[i] != None:

                rect(screen,self.colorBackground,(self.cardRect[i][0],self.cardRect[i][1],self.widthCard,self.heightCard))
       
                screen.blit(GlobalSprites.mainCharactersSelect[self.switch[self.playerCharacter[i]]]["idle"][self.indexIdle],self.cardImageRect[i])
                screen.blit(self.textName[i],(self.cardRect[i][0]+(self.widthCard-self.textNameRect[i].width)//2,self.cardRect[i][1]+10))
                if i != list(self.hostID.values())[0]:
                    if self.readyPlayer[i]:
                        rect(screen,(255, 60, 10),self.readyBoxRect[i])
                        screen.blit(self.textReady,self.textReadyRect[i])
                    else:
                        rect(screen,(240, 150, 100),self.readyBoxRect[i])
                        screen.blit(self.textUnReady,self.textUnReadyRect[i])
            else:
                rect(screen,self.colorBackground,(self.cardRect[i][0],self.cardRect[i][1],self.widthCard,self.heightCard))
                screen.blit(self.textAddPlayer,(self.cardRect[i][0]+(self.widthCard-self.textAddPlayerRect.width)//2,self.cardRect[i][1]+(self.heightCard-self.textAddPlayerRect.height)//2))

        if self.thisPlayerID in self.hostID:
            if self.allPlayerReady:
                self.ButtonPlayActive.draw(screen)
            else:
                self.ButtonPlay.draw(screen)
        else:
            if self.readyPlayer[self.playerID[self.thisPlayerID]]:
                self.ButtonUnReady.draw(screen)
            else:
                self.ButtonReady.draw(screen)
        self.ButtonBack.draw(screen)
        self.ButtonChangeCharacter.draw(screen)
        screen.blit(self.textRoomID,(10,10))