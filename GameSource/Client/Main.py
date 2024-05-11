import pygame
import System.Constant as Constant

pygame.init()
screen = pygame.display.set_mode((Constant.Screen_Width,Constant.Screen_Height),pygame.RESIZABLE)

from Entities import Block, Boss, BossSkills, Enemy, Gates, Item, NormalAttack, Pet, Player, Skill, Trap, TextDamage
from Class import DataWorld
from System import ConnectServer, SoundEffect
from Function import Func, HandleControl, HandleFile
from SendReceive import Account, Control, MainData, DataInit, WaitingRoom
from Interface import MenuSkill, MessageBox, AuthenticationPlayer, Notification, MultiPlayer, MenuStart, SelectCharacter, AccountControl, ShowCharacterProperties, Setting, GameOver, MenuInGame, InforCharacter, FinishGame, InteractInGame, Achievement, WaitingRoomInter
from Interact import Button
from os import getcwd
from os.path import join    

programIcon = pygame.image.load(join(getcwd(),"Assets","game.png"))
pygame.display.set_icon(programIcon)
pygame.display.set_caption("Dashing Adventure")

authenticationPlayer = AuthenticationPlayer.AuthenticationPlayer(0,0,Constant.Screen_Width,Constant.Screen_Height)
login = AuthenticationPlayer.Login(0,0,Constant.Screen_Width,Constant.Screen_Height)
signUp = AuthenticationPlayer.SignUp(0,0,Constant.Screen_Width,Constant.Screen_Height)

accountControl = AccountControl.AccountControl(0,0,Constant.Screen_Width,Constant.Screen_Height)
changePassword = AccountControl.ChangePassword(0,0,Constant.Screen_Width,Constant.Screen_Height)
changeName = AccountControl.ChangeName(0,0,Constant.Screen_Width,Constant.Screen_Height)

menuStart = MenuStart.MenuStart(0,0,Constant.Screen_Width,Constant.Screen_Height)

multiPlayer = MultiPlayer.JoinRoom(0,0,Constant.Screen_Width,Constant.Screen_Height)
waitingRoom = WaitingRoomInter.WaitingRoom(0,0,Constant.Screen_Width,Constant.Screen_Height)

control = Control.Control()

setting = Setting.Setting(0,0,Constant.Screen_Width,Constant.Screen_Height)

settingControlData = HandleFile.readFile("Keys.json")["keys"]
settingSoundData = HandleFile.readFile("Sound.json")

settingControl = Setting.SettingControl(0,0,Constant.Screen_Width,Constant.Screen_Height,settingControlData)
settingSound = Setting.SettingSound(0,0,Constant.Screen_Width,Constant.Screen_Height,settingSoundData)

InterfaceStep = "AuthenticationPlayer"
InterfaceInGameStep = ""

playerID = None
characterProperties = None
isMultiPlayGame = False

ButtonBackObserve = Button.Button("Back",10,Constant.Screen_Height - 60,100,50,2,(255,255,255),(255,0,0),(255,0,0))

notifications = []

followPlayer = None
followPlayerID = None
canObserveOtherPlayer = False
isFinishGame = False

Poster = pygame.image.load(join(getcwd(),"assets","Image","Background","Poster.png")).convert_alpha()
Poster = pygame.transform.scale(Poster,(Constant.Screen_Width,Constant.Screen_Height))

SoundEffect.InitBackgroundMusic()
SoundEffect.backgroundMusic.play(-1)
SoundEffect.backgroundMusic.set_volume(settingSoundData["BackgroundMusic"]/100)

running = True

try:
    network = ConnectServer.Network()
except Exception as e:
    print(e)
    pass

def checkToken():
    global InterfaceStep,playerID,playerName
    try: 
        account = HandleFile.readFile("User.json")
        if account["token"] == None:
            return
        login = Account.Login(step="CheckToken",token=account["token"])
        receive = network.send(login)
        if receive.status == "Success":
            playerID = receive.playerID
            playerName = receive.name
            menuStart.updatePlayerName(receive.name)
            accountControl.updatePlayerName(receive.name)
            InterfaceStep = "MenuStart"
        else:
            HandleFile.saveFile("User.json",{"token":None})
    except Exception as e:
        print(e)
        pass

checkToken()

def handleEventAuthenticationPlayer(event):
    global running,InterfaceStep
    if InterfaceStep == "AuthenticationPlayer":
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            rsClick = authenticationPlayer.checkClick(pos)
            if rsClick == "Login":
                InterfaceStep = "Login"
            elif rsClick == "SignUp":
                InterfaceStep = "SignUp"
            elif rsClick == "Exit":
                running = False

def handleEventLogin(event):
    global InterfaceStep,running,playerID,playerName
    login.handle_event(event)
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        rsClick = login.checkClick(pos)
        if rsClick == "Login":
            if login.getUserName() == "" or login.getPassword() == "":
                notifications.append(Notification.Notification(min(Constant.Screen_Width*0.7,700),Constant.Screen_Height*0.5,"Error","Please fill out all the information"))
                return
            loginData = Account.Login(step="Login",username=login.getUserName(),password=login.getPassword(),token="",remember=login.getRemember())
            receive = network.send(loginData)
            if receive == None:
                notifications.append(Notification.Notification(min(Constant.Screen_Width*0.7,700),Constant.Screen_Height*0.5,"Error","Can't connect to server!"))
                return
            if receive.status == "Success":
                login.reset()
                playerID = receive.playerID
                playerName = receive.name
                menuStart.updatePlayerName(receive.name)
                accountControl.updatePlayerName(receive.name)
                if receive.token != None and loginData.remember == True: HandleFile.saveFile("User.json",{"token":receive.token})
                InterfaceStep = "MenuStart"
            else:
                notifications.append(Notification.Notification(min(Constant.Screen_Width*0.7,700),Constant.Screen_Height*0.5,receive.status,receive.message))

        elif rsClick == "SignUp": InterfaceStep = "SignUp"
        elif rsClick == "Back": InterfaceStep = "AuthenticationPlayer"

def handleEventSignUp(event):  
    global InterfaceStep,running
    signUp.handle_event(event)
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        rsClick = signUp.checkClick(pos)
        if rsClick == "SignUp":
            if signUp.getPassword() != signUp.getComfirmPassword():
                notifications.append(Notification.Notification(min(Constant.Screen_Width*0.7,700),Constant.Screen_Height*0.5,"Error","Comfirm password is not correct"))
                return
            if signUp.getName() == "" or signUp.getUserName() == "" or signUp.getEmail() == "" or signUp.getPassword() == "" or signUp.getComfirmPassword() == "":
                notifications.append(Notification.Notification(min(Constant.Screen_Width*0.7,700),Constant.Screen_Height*0.5,"Error","Please fill out all the information"))
                return
            signUpData = Account.SignUp(step="SignUp",email=signUp.getEmail(),name=signUp.getName(),username=signUp.getUserName(),password=signUp.getPassword())
            receive = network.send(signUpData)
            if receive == None:
                notifications.append(Notification.Notification(min(Constant.Screen_Width*0.7,700),Constant.Screen_Height*0.5,"Error","Can't connect to server!"))
                return
            if receive.status == "Success":
                signUp.reset()
            notifications.append(Notification.Notification(min(Constant.Screen_Width*0.7,700),Constant.Screen_Height*0.5,receive.status,receive.message))
        elif rsClick == "Login": InterfaceStep = "Login"
        elif rsClick == "Back": InterfaceStep = "AuthenticationPlayer"

def handleEventAccountControl(event):
    global InterfaceStep,playerName,playerID,characterProperties
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        rsClick = accountControl.checkClick(pos)
        if rsClick == "ChangeName":
            InterfaceStep = "ChangeName"
        elif rsClick == "ChangePassword":
            InterfaceStep = "ChangePassword"
        elif rsClick == "LogOut":
            InterfaceStep = "AuthenticationPlayer"
            playerName = None
            playerID = None
            characterProperties = None
            control.step = "LogOut"
            network.send(control)
        elif rsClick == "Back":
            InterfaceStep = "MenuStart"

def handleEventChangePassword(event): 
    global InterfaceStep,running       
    changePassword.handle_event(event)
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        rsClick = changePassword.checkClick(pos)
        if rsClick == "Change":
            oldPass = changePassword.getPassword()
            newPass = changePassword.getNewPassword()
            comfirmPass = changePassword.getComfirmPassword()
            if newPass != comfirmPass:
                notifications.append(Notification.Notification(min(Constant.Screen_Width*0.7,700),Constant.Screen_Height*0.5,"Error","Comfirm password is not correct"))
                return
            if oldPass == "" or newPass == "" or comfirmPass == "":
                notifications.append(Notification.Notification(min(Constant.Screen_Width*0.7,700),Constant.Screen_Height*0.5,"Error","Please fill out all the information"))
                return
            if oldPass == newPass:
                notifications.append(Notification.Notification(500,200,"Error","New password must be different from old password"))
                return
            changePass = Account.ChangePassword(step="ChangePassword",oldPassword=oldPass,newPassword=newPass)
            receive = network.send(changePass)
            if receive.status == "Success":
                changePassword.reset()
            notifications.append(Notification.Notification(min(Constant.Screen_Width*0.7,700),Constant.Screen_Height*0.5,receive.status,receive.message))

        elif rsClick == "Back": InterfaceStep = "AccountControl"

def handleEventChangeName(event):
    global InterfaceStep,running
    changeName.handle_event(event)
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        rsClick = changeName.checkClick(pos)
        if rsClick == "Change":
            name = changeName.getName()
            password = changeName.getPassword()
            if name == playerName:
                notifications.append(Notification.Notification(500,200,"Error","New Name must be different from old Name"))
                return
            if name == "" or password == "":
                notifications.append(Notification.Notification(min(Constant.Screen_Width*0.7,700),Constant.Screen_Height*0.5,"Error","Please fill out all the information"))
                return
            change = Account.ChangeName(step="ChangeName",name=name,password=password)
            receive = network.send(change)
            if receive.status == "Success":
                menuStart.updatePlayerName(name)
                accountControl.updatePlayerName(name)
                changeName.reset()
                
            notifications.append(Notification.Notification(min(Constant.Screen_Width*0.7,700),Constant.Screen_Height*0.5,receive.status,receive.message))
        elif rsClick == "Back": InterfaceStep = "AccountControl"

def handleEventSetting(event):
    global InterfaceStep,running
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        rsClick = setting.checkClick(pos)
        if rsClick == "Back": InterfaceStep = "MenuStart"
        elif rsClick == "Control": InterfaceStep = "SettingControl"
        elif rsClick == "Sound": InterfaceStep = "SettingSound"

def handleEventSettingControl(event):
    global InterfaceStep,running,settingControlData,settingControl
    settingControl.handle_event(event)
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        rsClick = settingControl.checkClick(pos)
        if rsClick == "Back": InterfaceStep = "Setting"
        elif rsClick == "Save": settingControlData = HandleFile.readFile("Keys.json")["keys"]

def handleEventSettingSound(event):
    global InterfaceStep,running, settingSoundData, settingSound
    if settingSound.handle_event(event):
        settingSoundData = HandleFile.readFile("Sound.json")
        SoundEffect.backgroundMusic.set_volume(settingSoundData["BackgroundMusic"]/100)
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        rsClick = settingSound.checkClick(pos)
        if rsClick == "Back": InterfaceStep = "Setting"

def handleEventMenuStart(event):
    global InterfaceStep,running,playerName,playerID,characterProperties,singlePlayer,selectCharacter
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        rsClick = menuStart.checkClick(pos)
        if rsClick == "SinglePlayer":
            InterfaceStep = "SinglePlayer"
            try: 
                control.step = "GetCharacterProperties"
                characterProperties = network.send(control)
            except: pass
            singlePlayer = SelectCharacter.SelectCharacter("Play",characterProperties)
        elif rsClick == "MultiPlayer": 
            InterfaceStep = "MultiPlayer"
            
        elif rsClick == "Setting": InterfaceStep = "Setting"
        elif rsClick == "AccountControl": InterfaceStep = "AccountControl"
        elif rsClick == "Exit": running = False

def handleEventSinglePlayer(event):
    global InterfaceStep,running
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        rsClick = singlePlayer.checkClick(pos)
        if rsClick == "Back": InterfaceStep = "MenuStart"
        if rsClick == "Select":
            characterName = singlePlayer.characterName
            initGame(characterName)
        
def handleEventSelectCharacter(event):
    global InterfaceStep,running
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        rsClick = selectCharacter.checkClick(pos)
        if rsClick == "Back": InterfaceStep = "WaitingRoom"
        if rsClick == "Select":
            control.step = "ChangeCharacter"
            control.characterName = selectCharacter.characterName
            network.send(control)
            InterfaceStep = "WaitingRoom"
       
def handleEventMultiPlayer(event):
    global InterfaceStep,running,selectCharacter
    multiPlayer.handle_event(event)
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        rsClick = multiPlayer.checkClick(pos)
        if rsClick == "Back":
            InterfaceStep = "MenuStart"
        elif rsClick == "CreateRoom":
            control.step = "MultiPlayerCreateRoom"
            receive = network.send(control)
            InterfaceStep = "WaitingRoom"
            selectCharacter = SelectCharacter.SelectCharacter("Select",receive.characterProperties)
            waitingRoom.updateRoomID(str(receive.roomID))
            waitingRoom.thisPlayerID = playerID
        elif rsClick == "JoinRoom":
            control.step = "MultiPlayerJoinRoom"
            control.roomID = multiPlayer.joinRoomBox.text
            receive = network.send(control)
            if receive.status == "Success":
                InterfaceStep = "WaitingRoom"
                selectCharacter = SelectCharacter.SelectCharacter("Select",receive.characterProperties)
                waitingRoom.updateRoomID(str(control.roomID))
                waitingRoom.thisPlayerID = playerID
            else:
                notifications.append(Notification.Notification(min(Constant.Screen_Width*0.7,700),Constant.Screen_Height*0.5,"Error",receive.message))

def handleEventWaitingRoom(event):
    global InterfaceStep
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        rsClick = waitingRoom.checkClick(pos)
        if rsClick == "Back":
            InterfaceStep = "MultiPlayer"
            control.step = "LeaveRoom"
            network.send(control)
        elif rsClick == "Start":
            control.step = "StartGame"
            network.send(control)
        elif rsClick == "ChangeCharacter":
            InterfaceStep = "SelectCharacter"
        
def handleEventPlayGame(event):
    global InterfaceStep,player,mainData,InterfaceInGameStep,followPlayerID

    if event.type == pygame.KEYDOWN:
        if (isFinishGame and finishGame.isClose) or not isFinishGame:
            if not messageBox.input.active:
                HandleControl.handleKeys(event,mainData,player,settingControlData,settingSoundData)
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        if isFinishGame and not finishGame.isClose:
            pos = pygame.mouse.get_pos()
            finishGame.checkClick(pos)
        else:
            pos = pygame.mouse.get_pos()
            rs = interactInGame.checkClick(pos)
            if rs != "":
                InterfaceInGameStep = rs
                if InterfaceInGameStep == "CharacterProperties":
                    showCharacterProperties.update(player)
            else:
                mainData.mousePos = pos

            if isFinishGame:
                if finishGame.checkClick(pos) == "Exit":
                    if isMultiPlayGame == True:
                        isMultiPlayGame == False
                        InterfaceStep = "WaitingRoom"
                    else:
                        InterfaceStep = "MenuStart"
                    mainData.status = "ExitGame"
                    network.send(mainData)
                    return

    messageBox.handle_event(event,mainData)

def handleEventMenuInGame(event): 
    global InterfaceStep, mainData, InterfaceInGameStep, settingSoundData, settingControlData, comfirmExit
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                InterfaceInGameStep = ""

    if InterfaceInGameStep == "Menu":
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()    
            rsClick = menuInGame.checkClick(pos)
            if rsClick == "Exit":
                comfirmExit = Notification.Comfirm(min(Constant.Screen_Width*0.7,700),Constant.Screen_Height*0.5,"Alert","Are you sure you want to exit the game?",(255, 181, 124),(198, 61, 47))
                InterfaceInGameStep = "ComfirmExitGame"
            elif rsClick == "Setting":
                InterfaceInGameStep = "Setting"
            elif rsClick == "Back":
                InterfaceInGameStep = ""

    elif InterfaceInGameStep == "ComfirmExitGame":
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            rsClick = comfirmExit.checkClick(pos)
            if rsClick == True:
                InterfaceInGameStep = ""
                if isMultiPlayGame == True:
                    isMultiPlayGame == False
                    InterfaceStep = "WaitingRoom"
                else:
                    InterfaceStep = "MenuStart"
                mainData.status = "ExitGame"
                network.send(mainData)
                return
            elif rsClick == False:
                InterfaceInGameStep = "Menu"
                comfirmExit = None

    elif InterfaceInGameStep == "Setting":
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            rsClick = setting.checkClick(pos)
            if rsClick == "Back":
                InterfaceInGameStep = "Menu"
            elif rsClick == "Control":
                InterfaceInGameStep = "SettingControl"
            elif rsClick == "Sound":
                InterfaceInGameStep = "SettingSound"

    elif InterfaceInGameStep == "SettingControl":
        settingControl.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            rsClick = settingControl.checkClick(pos)
            if rsClick == "Back":
                InterfaceInGameStep = "Setting"
            elif rsClick == "Save":
                settingControlData = HandleFile.readFile("Keys.json")["keys"]

    elif InterfaceInGameStep == "SettingSound":
        if settingSound.handle_event(event):
            settingSoundData = HandleFile.readFile("Sound.json")
            SoundEffect.backgroundMusic.set_volume(settingSoundData["BackgroundMusic"]/100)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            rsClick = settingSound.checkClick(pos)
            if rsClick == "Back":
                InterfaceInGameStep = "Setting"
    elif InterfaceInGameStep == "Achievement":
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if achievement.checkClick(pos) == "Back":
                InterfaceInGameStep = ""
    elif InterfaceInGameStep == "CharacterProperties":
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if showCharacterProperties.checkClick(pos) == "Back":
                InterfaceInGameStep = ""

def handleEventGameOver(event):
    global InterfaceStep,running, followPlayerID, followPlayer
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        rsClick = gameOver.checkClick(pos,canObserveOtherPlayer)
        if gameOver.isObserve:
            if rsClick == "Back":
                gameOver.isObserve = False
                followPlayerID = None
                followPlayer = None
            else:
                for i in inforCharacterOtherPlayer:
                    if inforCharacterOtherPlayer[i].rect.collidepoint(pos):
                        for oPl in dataReceive.other_players:
                            if oPl.id == i:
                                if not oPl.isDead:
                                    followPlayerID = i
                                break
                        break
        else:
            if rsClick == "Exit":
                if isMultiPlayGame == True:
                    isMultiPlayGame == False
                    InterfaceStep = "WaitingRoom"
                else:
                    InterfaceStep = "MenuStart"
                mainData.status = "ExitGame"
                network.send(mainData)
                return
            
            elif rsClick == "Revival":
                if player.diamond >= 5:
                    mainData.status = "Revival"
                    network.send(mainData)
                    mainData.status = "getData"
                    return
                else:
                    notifications.append(Notification.Notification(min(Constant.Screen_Width*0.7,700),Constant.Screen_Height*0.5,"Error","You don't have enough diamond",(255, 181, 124),(198, 61, 47)))
                    
            elif rsClick == "Observe":
                gameOver.isObserve = True
                followPlayerID, followPlayer = getObserveOtherPlayer(dataReceive.other_players)

def getObserveOtherPlayer(otherPlayers):
    for oPlayer in otherPlayers:
        if not oPlayer.isDead:
            return oPlayer.id,oPlayer
    return None,None

def getBackgroundGame(index):
    global backgroundGame
    if index == 0: name = "Background1"
    elif index == 1: name = "Desert"
    elif index == 2: name = "Jungle" 
    elif index == 3: name = "DarkTower"
    elif index == 4: name = "LightForest"
    else: name = "DarkForest"
    backgroundGame = pygame.image.load(join(getcwd(),"assets","Image","Background",(name + ".png"))).convert_alpha()
    backgroundGame = pygame.transform.scale(backgroundGame,(Constant.Screen_Width,Constant.Screen_Height))

def initGame(characterName):
    global player,mainData,inforCharacter,InterfaceStep,menuSkill,initWorld,dataReceive, offset_x, offset_y, showCharacterProperties, inforCharacterOtherPlayer, followPlayer, followPlayerID, canObserveOtherPlayer, isFinishGame, interactInGame, messageBox, gameOver, finishGame, achievement, menuInGame, backgroundName,comfirmExit
    if characterName!=None: 
        control.step = "SinglePlayer"
        control.characterName = characterName
    receive = network.send(control)

    player = receive.player
    
    initWorld = DataWorld.InitWorld(receive.blocks,receive.trees,receive.plants,receive.rocks,receive.gates,receive.mapLimit)
    getBackgroundGame(receive.background)
    dataReceive = DataWorld.DataReceive()
    mainData = MainData.MainData()
    offset_x, offset_y = Func.resetRectScreen(player,initWorld.mapLimit)
    inforCharacterOtherPlayer = {}
    followPlayer = None
    followPlayerID = None

    canObserveOtherPlayer = False
    isFinishGame = False

    inforCharacter = InforCharacter.DrawInfor(player,10,10,300,80,2)
    menuSkill = MenuSkill.Menu(0,0,Constant.Screen_Width,Constant.Screen_Height,player,settingControlData)
    interactInGame = InteractInGame.InteracInGame(0,0,Constant.Screen_Width,Constant.Screen_Height)
    messageBox = MessageBox.Message(0,0,Constant.Screen_Width,Constant.Screen_Height)
    showCharacterProperties = ShowCharacterProperties.ShowCharacterProperties(0,0,Constant.Screen_Width,Constant.Screen_Height,player)
    menuInGame = MenuInGame.MenuInGame(0,0,Constant.Screen_Width,Constant.Screen_Height)
    
    achievement = Achievement.Achievement(0,0,Constant.Screen_Width,Constant.Screen_Height,[player])
    gameOver = GameOver.GameOver(0,0,Constant.Screen_Width,Constant.Screen_Height)
    finishGame = FinishGame.FinishGame(0,0,Constant.Screen_Width,Constant.Screen_Height)
    comfirmExit = None
    InterfaceStep = "PlayGame"

def callServer():
    global mainData,player,followPlayer, inforCharacterOtherPlayer, canObserveOtherPlayer, isFinishGame,followPlayerID, followPlayer
    mainData.offset = (offset_x,offset_y)
    getData = network.send(mainData)
    if(getData.status == "dataInit"):
        initWorld.updateWorld(getData.blocks,getData.trees,getData.plants,getData.rocks,getData.gates,getData.mapLimit)
        getBackgroundGame(getData.background)
    else:
        if getData.status == "Finish":
            if not isFinishGame:
                SoundEffect.soundEffectChannel["FinishGame"].play(SoundEffect.AllSoundEffect["FinishGame"])
            isFinishGame = True
            
        dataReceive.updateData(getData.enemys,getData.boss,getData.traps,getData.textDamages,getData.listDropItems)
        dataReceive.clearOtherPlayers()

        achievement.update(getData.players)

        if gameOver.isObserve: followPlayer = None
        for pl in getData.players:
            if(pl.id != playerID):     
                dataReceive.other_players.append(pl)
                if gameOver.isObserve and followPlayer == None and followPlayerID != None and followPlayerID == pl.id:
                    if pl.isDead: 
                        followPlayerID, followPlayer = getObserveOtherPlayer(dataReceive.other_players)
                        if followPlayer == None: 
                            gameOver.isObserve = False
                    else: followPlayer = pl
            else: player = pl
        
        if player.isDead and not gameOver.isObserve:
            followPlayerID, followPlayer = getObserveOtherPlayer(dataReceive.other_players)
            if followPlayer == None: canObserveOtherPlayer = False
            else: canObserveOtherPlayer = True
        if gameOver.isObserve and len(dataReceive.other_players) == 0:
            gameOver.isObserve = False
            followPlayerID = None
            followPlayer = None

        if len(dataReceive.other_players) != len(inforCharacterOtherPlayer):
            inforCharacterOtherPlayer = {}
            for i,otherPlayer in enumerate(dataReceive.other_players):
                infor = InforCharacter.DrawInfor(otherPlayer,10, 20 + 80 + 80*i,250,70,2)
                inforCharacterOtherPlayer[otherPlayer.id] = infor

    mainData.resetKeys()
    mainData.resetMessage()
    mainData.resetMousePos()

def mainGame():
    global InterfaceStep,player,offset_x,offset_y
    screen.blit(backgroundGame,(0,0))
    if not messageBox.input.active and (not isFinishGame or (isFinishGame and finishGame.isClose)):
        HandleControl.handleKeysPressed(mainData,settingControlData,settingSoundData)

    callServer()
    
    if player.isDead and gameOver.isObserve and followPlayer != None:
        offset_x, offset_y = Func.resetRectScreen(followPlayer,initWorld.mapLimit)
    else:
        offset_x, offset_y = Func.screenFollowX(player,offset_x,offset_y,initWorld.mapLimit)
        # offset_x, offset_y = Func.checkOverScreen(player,offset_x,offset_y,initWorld.mapLimit)
    for tree in initWorld.trees:
        Block.drawTree(screen,offset_x,offset_y,tree)
    for plant in initWorld.plants:
        Block.drawPlant(screen,offset_x,offset_y,plant)
    for rock in initWorld.rocks:
        Block.drawRock(screen,offset_x,offset_y,rock)
    for obj in initWorld.blocks:
        Block.drawObject(screen,offset_x,offset_y,obj)
    if(initWorld.gates != None):
        Gates.drawGates(screen,offset_x,offset_y,initWorld.gates)
    for enemy in dataReceive.enemys:
        if enemy.isDead: continue
        Enemy.drawEnemy(screen,offset_x,offset_y,enemy)
    for bos in dataReceive.boss:
        if bos.isDead: continue
        Boss.drawBoss(screen,offset_x,offset_y,bos)
        for skill in bos.skills:
            BossSkills.drawBossSkill(screen,offset_x,offset_y,skill,bos.characterName)
    for trap in dataReceive.traps:
        Trap.drawTrap(screen,offset_x,offset_y,trap)
    for item in dataReceive.listDropItems:
        Item.drawItem(screen,offset_x,offset_y,item)

    if(player.pets != None):
        Pet.drawPet(screen,offset_x,offset_y,player.pets)
    
    Player.drawPlayer(screen,offset_x,offset_y,player)
    Player.drawEnemyTarget(screen,offset_x,offset_y,player)

    for otherPlayer in dataReceive.other_players:
        if(otherPlayer.pets != None):
            Pet.drawPet(screen,offset_x,offset_y,otherPlayer.pets)
        Player.drawOtherPlayer(screen,offset_x,offset_y,otherPlayer)
        MessageBox.drawMessage(screen,offset_x,offset_y,otherPlayer)
        for skill in otherPlayer.skills:
            Skill.DrawSkill(screen,offset_x,offset_y,skill,True)
        for atk in otherPlayer.normalAttack:
            NormalAttack.DrawNormalAttack(screen,offset_x,offset_y,atk,False)
        inforCharacterOtherPlayer[otherPlayer.id].draw(screen,otherPlayer)
                
    for skill in player.skills:
        Skill.DrawSkill(screen,offset_x,offset_y,skill,False)
    for atk in player.normalAttack:
        NormalAttack.DrawNormalAttack(screen,offset_x,offset_y,atk,False)

    for textDamage in dataReceive.textDamages:
        TextDamage.drawDamages(screen,offset_x,offset_y,textDamage)
    MessageBox.drawMessage(screen,offset_x,offset_y,player)
    
    messageBox.draw(screen)
    inforCharacter.draw(screen,player)

    menuSkill.draw(screen,player)
    interactInGame.draw(screen)
   
def handleEvent(event):
    global InterfaceStep,settingControl,backgroundGame, Poster
    if event.type == pygame.VIDEORESIZE:
        Constant.Screen_Width = event.w
        Constant.Screen_Height = event.h
        authenticationPlayer.resize(Constant.Screen_Width,Constant.Screen_Height)
        login.resize(Constant.Screen_Width,Constant.Screen_Height)
        signUp.resize(Constant.Screen_Width,Constant.Screen_Height)
        accountControl.resize(Constant.Screen_Width,Constant.Screen_Height)
        changeName.resize(Constant.Screen_Width,Constant.Screen_Height)
        changePassword.resize(Constant.Screen_Width,Constant.Screen_Height)
        if InterfaceStep == "SinglePlayer":
            singlePlayer.resize(Constant.Screen_Width,Constant.Screen_Height)
        multiPlayer.resize(Constant.Screen_Width,Constant.Screen_Height)
        waitingRoom.resize(Constant.Screen_Width,Constant.Screen_Height)
        if InterfaceStep == "WaitingRoom": 
            selectCharacter.resize(Constant.Screen_Width,Constant.Screen_Height)
        menuStart.resize(Constant.Screen_Width,Constant.Screen_Height)
        setting.resize(Constant.Screen_Width,Constant.Screen_Height)
        settingSound.resize(Constant.Screen_Width,Constant.Screen_Height)
        settingControl.resize(Constant.Screen_Width,Constant.Screen_Height)
        Poster = pygame.transform.scale(Poster,(Constant.Screen_Width,Constant.Screen_Height))

        for noti in notifications:
            noti.resize(Constant.Screen_Width,Constant.Screen_Height)
        if InterfaceStep == "PlayGame":
            menuInGame.resize(Constant.Screen_Width,Constant.Screen_Height)
            menuSkill.resize(Constant.Screen_Width,Constant.Screen_Height)
            messageBox.resize(Constant.Screen_Width,Constant.Screen_Height)
            interactInGame.resize(Constant.Screen_Width,Constant.Screen_Height)
            gameOver.resize(Constant.Screen_Width,Constant.Screen_Height)
            finishGame.resize(Constant.Screen_Width,Constant.Screen_Height)
            showCharacterProperties.resize(Constant.Screen_Width,Constant.Screen_Height)
            achievement.resize(Constant.Screen_Width,Constant.Screen_Height)
            backgroundGame = pygame.transform.scale(backgroundGame,(Constant.Screen_Width,Constant.Screen_Height))

    if len(notifications) > 0:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if notifications[0].checkClose(pos):
                notifications.pop(0)

    elif InterfaceStep == "AuthenticationPlayer":
        handleEventAuthenticationPlayer(event)
    elif InterfaceStep == "Login":
        handleEventLogin(event)
    elif InterfaceStep == "SignUp":
        handleEventSignUp(event)
    elif InterfaceStep == "AccountControl":
        handleEventAccountControl(event)
    elif InterfaceStep == "ChangeName":
        handleEventChangeName(event)
    elif InterfaceStep == "ChangePassword":
        handleEventChangePassword(event)
    elif InterfaceStep == "MenuStart":
        handleEventMenuStart(event)
    elif InterfaceStep == "Setting":
        handleEventSetting(event)
    elif InterfaceStep == "SettingControl":
        handleEventSettingControl(event)
    elif InterfaceStep == "SettingSound":
        handleEventSettingSound(event)
    elif InterfaceStep == "SinglePlayer":
        handleEventSinglePlayer(event)
    elif InterfaceStep == "MultiPlayer":
        handleEventMultiPlayer(event)
    elif InterfaceStep == "WaitingRoom":
        handleEventWaitingRoom(event)   
    elif InterfaceStep == "SelectCharacter":
        handleEventSelectCharacter(event)
    elif InterfaceStep == "PlayGame":
        if player.isDead: 
            handleEventGameOver(event)
        elif InterfaceInGameStep != "": 
            handleEventMenuInGame(event)
        else: 
            handleEventPlayGame(event)

def handleDraw(screen):
    global isMultiPlayGame
    
    if InterfaceStep == "AuthenticationPlayer":
        screen.blit(Poster,(0,0))
        authenticationPlayer.draw(screen)
    elif InterfaceStep == "Login":
        login.draw(screen)
    elif InterfaceStep == "SignUp":
        signUp.draw(screen)
    elif InterfaceStep == "AccountControl":
        accountControl.draw(screen)
    elif InterfaceStep == "ChangeName":
        changeName.draw(screen)
    elif InterfaceStep == "ChangePassword":
        changePassword.draw(screen)
    elif InterfaceStep == "MenuStart":
        screen.blit(Poster,(0,0))
        menuStart.draw(screen)
    elif InterfaceStep == "Setting":
        setting.draw(screen)
    elif InterfaceStep == "SettingControl":
        settingControl.draw(screen)
    elif InterfaceStep == "SettingSound":
        settingSound.draw(screen)
    elif InterfaceStep == "SinglePlayer":
        singlePlayer.loop()
        singlePlayer.draw(screen)
    elif InterfaceStep == "MultiPlayer":
        multiPlayer.draw(screen)
    elif InterfaceStep == "WaitingRoom":
        control.step = "getData"
        receive = network.send(control)
        waitingRoom.updateRoom(receive)
        if receive.gameStart and playerID not in receive.exitPlayer:
            initGame(None)
            isMultiPlayGame = True
            return
        waitingRoom.loop()
        waitingRoom.draw(screen)
    elif InterfaceStep == "SelectCharacter":
        selectCharacter.loop()
        selectCharacter.draw(screen)
    elif InterfaceStep == "PlayGame":
        mainGame()
        if player.isDead:
            gameOver.draw(screen,canObserveOtherPlayer,player.diamond)   
        elif InterfaceInGameStep == "Menu":
            menuInGame.draw(screen)
        elif InterfaceInGameStep == "CharacterProperties":
            showCharacterProperties.draw(screen)
        elif InterfaceInGameStep == "Achievement":
            achievement.draw(screen)
        elif InterfaceInGameStep == "Setting":
            setting.draw(screen)
        elif InterfaceInGameStep == "SettingControl":
            settingControl.draw(screen)
        elif InterfaceInGameStep == "SettingSound":
            settingSound.draw(screen)
        if isFinishGame:
            finishGame.draw(screen)
        if comfirmExit != None:
            comfirmExit.draw(screen)
    if len(notifications) > 0:
        notifications[0].draw(screen)

while running:
    screen.fill((196, 223, 223))
    pygame.time.Clock().tick(Constant.FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        handleEvent(event)
    handleDraw(screen)
    pygame.display.update()
pygame.quit()
