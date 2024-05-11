import socket
import threading
import pickle
import os
from os.path import isfile, join

import random
from time import sleep

from Entities import Player, Item
from SendReceive import UserInfor, DataInit, MainData, Control, WaitingRoom, Account
from System import Constant
from Function import LoadMap, HandleCharacterProperties, HandleAccount, HandleFile
from System.DatabaseConnect import setToken,setDiamond

host = HandleFile.readFile("Host.json")
server = host["host"]
port = host["port"]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as msg:
    print("Socket creation Error: " + str(msg))

s.listen(2)
print("Waiting for a connection, Server Started")

pathMap = os.path.join(os.getcwd(),'Assets', "Map")  
listMap = [f for f in os.listdir(pathMap) if isfile(join(pathMap, f))]
print("List Map:",listMap)
limitEndGame = 3

class AllRoom:
    def __init__(self):
        self.listRoom = {}
        self.listRoomID = []
    def createNewRoom(self,roomID):
        data = {
            "waitingRoom":None,
            "dataInit":None,
            "mainData":None,
            "playerInGates":[],
            "playerUpdateMap":[],
            "isChangeMap":False,
            "mapCount":[],
            "gameLoopStart":False,
        }
        self.listRoom[roomID] = data
        return self.listRoom[roomID]
    
    def resetRoomMulti(self,roomID):
        if roomID in self.listRoom:
            self.listRoom[roomID]["mainData"] = None
            self.listRoom[roomID]["dataInit"] = None
            self.listRoom[roomID]["waitingRoom"].gameStart = False
            self.listRoom[roomID]["waitingRoom"].exitPlayer = []
            self.listRoom[roomID]["isChangeMap"] = False
            self.listRoom[roomID]["mapCount"] = []
            self.playerInGates = []
            self.playerUpdateMap = []

    def deleteRoom(self,roomID):
        if roomID in self.listRoom:
            self.listRoom.pop(roomID)
        if roomID in self.listRoomID:
            self.listRoomID.remove(roomID)
            print("RoomID:",roomID,"deleted")

playerOnline = []
allRoom = AllRoom()
limitPlayerInRoom = 4

def createRoomID():
    while True:
        newId = random.randint(10000,99999)
        if newId not in allRoom.listRoomID:
            allRoom.listRoomID.append(newId)
            return newId

def handleMouse(mainData,player,mousePos,offset,userInfor):
    # kiểm tra xem chuột có bấm vào quái hay không 
    for enemy in mainData.enemys:
        if enemy.isDead: continue
        if enemy.rect.x < mousePos[0] + offset[0] < enemy.rect.x + enemy.rect.width and enemy.rect.y < mousePos[1] + offset[1] < enemy.rect.y + enemy.rect.height:
            player.enemy_target = enemy
            if(player.pets!=None):
                player.pets.enemy_target = enemy
    for bos in mainData.boss:
        if bos.isDead: continue
        if bos.rect.x < mousePos[0] + offset[0] < bos.rect.x + bos.rect.width and bos.rect.y < mousePos[1] + offset[1] < bos.rect.y + bos.rect.height:
            player.enemy_target = bos
            if(player.pets!=None):
                player.pets.enemy_target = bos

    for item in mainData.listDropItems:
        if item.rect.x < mousePos[0] + offset[0] < item.rect.x + item.rect.width and item.rect.y < mousePos[1] + offset[1] < item.rect.y + item.rect.height:
            if item.itemName == "diamond":
                player.diamond += 1
                userInfor.diamond += 1
                mainData.listDropItems.remove(item)
                setDiamond(userInfor.playerID, userInfor.diamond)
    player.handleNormalAttack()

def handlePlayer(mainData,dataInit):
    for player in mainData.players:
        player.loop(dataInit.blocks,dataInit.mapLimit)
        if player.pets != None:
            player.pets.loop(dataInit.blocks)
        for skill in player.skills:
            if skill.end: player.skills.remove(skill)
            else: skill.loop(player,mainData.enemys,mainData.boss,dataInit.blocks,dataInit.mapLimit)
        for atk in player.normalAttack:
            atk.loop(mainData.enemys,mainData.boss,dataInit.blocks)
        player.conditionSkill.loop()

def handleEnemy(mainData,dataInit):
    for enemy in mainData.enemys:
        if enemy.isDead:
            mainData.enemys.remove(enemy)
            randomDrop = random.randint(0,100)
            if randomDrop == 25:
                mainData.listDropItems.append(Item.Item(enemy.rect.x,enemy.rect.y,30,(220/270)*30,"diamond"))  
        else: enemy.loop(dataInit.blocks,dataInit.mapLimit)
    for bos in mainData.boss:
        if bos.isDead:
            mainData.boss.remove(bos)
            randomQuantity = random.randint(1,len(mainData.players)+1)
            for i in range(randomQuantity):
                mainData.listDropItems.append(Item.Item(bos.rect.x + i*(bos.rect.width//randomQuantity), bos.rect.y,30,(220/270)*30,"diamond"))
        else:
            bos.loop(dataInit.blocks,dataInit.mapLimit)
            for skill in bos.skills:
                skill.loop(mainData.players,dataInit.blocks,dataInit.mapLimit)

def gameLoop(dataRoom,roomID):
    mainData = dataRoom["mainData"]
    dataInit = dataRoom["dataInit"]
    
    # lặp cho đến khi tất cả người chơi thoát khỏi world
    while True:
        sleep(1/Constant.FPS)
        if not dataRoom["gameLoopStart"]:
            # kiểm tra nếu không còn người chơi trong phòng thì xóa phòng
            if dataRoom["waitingRoom"] == None or (dataRoom["waitingRoom"] !=None and len(dataRoom["waitingRoom"].players) == 0):
                allRoom.deleteRoom(roomID)
            # nếu vẫn còn người chơi trong phòng thì chỉ xóa dữ liệu game
            elif dataRoom["waitingRoom"]!=None:
                allRoom.resetRoomMulti(roomID)
            break
        try:
            handleEnemy(mainData,dataInit)
            handlePlayer(mainData,dataInit)

            for textDamage in mainData.textDamages:
                textDamage.loop(mainData.textDamages)

            isFinish = True if mainData.status == "Finish" else False
            for trap in mainData.traps:
                trap.loop(mainData.players,isFinish)

            for item in mainData.listDropItems:
                item.loop(dataInit.blocks)

        except Exception:
            break
    
def handleEvent(conn,thisPlayer,userInfor,dataRoom):
    mainData = dataRoom["mainData"]
    dataInit = dataRoom["dataInit"]
    playerID = userInfor.playerID
    reply = ""
    while True: 
        try: 
            # nhận yêu cầu từ client
            receive = pickle.loads(conn.recv(32768))
            # yêu cầu thoát khỏi game
            if receive.status == "ExitGame":
                conn.sendall(pickle.dumps("")) 
                if dataRoom["waitingRoom"] != None:
                    dataRoom["waitingRoom"].exitPlayer.append(playerID)
                break
            elif receive.status == "Revival":
                if userInfor.diamond >= 5:
                    thisPlayer.diamond -= 5
                    userInfor.diamond -= 5
                    setDiamond(userInfor.playerID,userInfor.diamond)
                    thisPlayer.revival(thisPlayer.max_hp*0.5, thisPlayer.max_mp*0.5)
                conn.sendall(pickle.dumps(mainData)) 
                continue

            # kiểm tra xem người chơi có đang trong cổng không
            if not thisPlayer.isDead:
                if(playerID not in dataRoom["playerInGates"]):
                    # xử lý sự kiện từ bàn phím
                    thisPlayer.handleMove(dataInit.blocks,dataInit.mapLimit,receive.keys)
                    thisPlayer.handleUseSkill(mainData.players,receive.keys)

                    # xử lý sự kiện từ chuột
                    if receive.mousePos != None:
                        handleMouse(mainData,thisPlayer,receive.mousePos,receive.offset,userInfor)

                        if(dataInit.gates != None and dataInit.gates.checkEnter(thisPlayer,receive.mousePos,receive.offset)) and len(mainData.boss) == 0:
                            if(playerID not in dataRoom["playerInGates"]):
                                dataRoom["playerInGates"].append(playerID)
                                thisPlayer.isInGates = True
                                playerAlive = 0
                                for player in mainData.players:
                                    if not player.isDead:
                                        playerAlive +=1
                                if(len(dataRoom["playerInGates"]) >= playerAlive):
                                    mainData.clearNextMap()
                                    dataInit.clearNextMap()
                                    dataRoom["playerInGates"].clear()

                                    indexMap = random.randint(0,len(listMap)-1)
                                    while indexMap in dataRoom["mapCount"]:
                                        indexMap = random.randint(0,len(listMap)-1)
                                    dataInit.indexMap = indexMap
                                    dataRoom["mapCount"].append(indexMap)

                                    hightestLevel = 1
                                    for pl in mainData.players:
                                        hightestLevel = max(hightestLevel,pl.level)
                            
                                    LoadMap.LoadMap(listMap[indexMap],mainData,dataInit,hightestLevel)
                                    if len(dataRoom["mapCount"]) >= limitEndGame:
                                        dataInit.gates = None

                                    dataRoom["isChangeMap"] = True

                    # xử lý tin nhắn từ người chơi
                    if receive.message != None:
                        thisPlayer.message = receive.message
                        thisPlayer.message_time_life = 5 * Constant.FPS
                            
                # nếu người chơi đang trong cổng nếu bấm phím x thì sẽ thoát khỏi cổng         
                elif not dataRoom["isChangeMap"]:
                    if receive.keys["escapeGate"]:
                        dataRoom["playerInGates"].remove(playerID)
                        for player in mainData.players:
                            if player.id == playerID:
                                player.isInGates = False

            # nếu tất cả người chơi đang trong cổng thì sẽ chuyển map
            if(dataRoom["isChangeMap"] and playerID not in dataRoom["playerUpdateMap"]):
                reply = dataInit
                dataRoom["playerUpdateMap"].append(playerID)
                if(len(dataRoom["playerUpdateMap"]) >= len(mainData.players)):
                    dataRoom["playerUpdateMap"].clear()
                    dataRoom["isChangeMap"] = False
                    for player in mainData.players:
                        player.nextMap(dataInit.playerPos[0],dataInit.playerPos[1],mainData.textDamages)
                       
            else:
                if len(dataRoom["mapCount"]) >= limitEndGame and len(mainData.boss)==0 and not dataRoom["isChangeMap"]:
                    mainData.finishGame()
                reply = mainData

            conn.sendall(pickle.dumps(reply)) 
            
        except Exception as ex:
            break

    print("User (ID:",userInfor.playerID,"- Name:",userInfor.playerName+")","// Out World")

    # xóa người chơi khỏi world
    mainData.players.remove(thisPlayer)
    # lưu thông tin nhân vật của người chơi
    HandleCharacterProperties.updateCharacterProperties(userInfor,thisPlayer)
    if len(mainData.players) == 0:
        dataRoom["gameLoopStart"] = False

def checkLogin(conn):
    while True: 
        try:
            # nhận yêu cầu từ client
            receive = pickle.loads(conn.recv(32768))
            # yêu cầu thoát khỏi game
            if(receive.step == "Exit"):
                print("User (ID:",userInfor.playerID,"- Name:",userInfor.playerName+")","// Exit Game")
                exit()
        
            elif receive.step == "CheckToken" or receive.step == "Login":
                # yêu cầu đăng nhập bằng token
                if receive.step == "CheckToken":
                    result = HandleAccount.checkLoginToken(receive.token)
                # yêu cầu đăng nhập bằng tài khoản
                if receive.step == "Login":
                    result = HandleAccount.checkAccountLogin(receive.username,receive.password,receive.remember)
                
                # kiểm tra đăng nhập thành công hay không và gửi kết quả về cho client
                if result["status"] == "Success":
                    if result["id"] not in playerOnline:
                        replyLogin = Account.ReplyLogin("Success","Login Success",result["id"],result["name"],result["token"])
                        conn.send(pickle.dumps(replyLogin))

                        # đăng nhập thành công gửi dữ liệu về client
                        userInfor = UserInfor.UserInfor()
                        userInfor.playerID = result["id"]
                        userInfor.playerName = result["name"]
                        userInfor.diamond = result["diamond"]
                        userInfor.characterProperties = HandleCharacterProperties.getCharacterProperties(result["id"])
                        print("User (ID:",userInfor.playerID,"- Name:",userInfor.playerName+")","// Login Success")
                        return userInfor
                    else:
                        ReplyLogin = Account.ReplyLogin("Error","Account is online",None,None,None)
                        conn.send(pickle.dumps(ReplyLogin))
                        continue
                else:
                    ReplyLogin = Account.ReplyLogin(result["status"],result["message"],None,None,None)
                    conn.send(pickle.dumps(ReplyLogin))
                    continue    
                    
            # yêu cầu đăng ký tài khoản
            elif receive.step == "SignUp":
                result = HandleAccount.checkAccountSignUp(receive.name,receive.username, receive.email,receive.password)
                ReplyLogin = Account.ReplyLogin(result["status"],result["message"],None,None,None)
                if(result["status"] == "Success"):
                    print("Sign Up (User:",receive.name, receive.username, receive.email, receive.password+") // Success")
                else:
                    print("Sign Up (User:",receive.name, receive.username, receive.email, receive.password+") // Failed -- Message:", result["message"])
                conn.send(pickle.dumps(ReplyLogin))
                continue
                
        except Exception:
            break

    print("Lost connection to player")
    exit()

def createNewWorld(dataRoom,hightestLevel):
    # tạo dữ liệu cho thế giới mới
    mainData = MainData.MainData()
    dataInit = DataInit.DataInit()
    indexMap = random.randint(0,len(listMap)-1)
    dataRoom["mapCount"].append(indexMap)
    LoadMap.LoadMap(listMap[indexMap],mainData,dataInit,hightestLevel)
    if len(dataRoom["mapCount"]) >= limitEndGame:
        dataInit.gates = None
    dataInit.background = indexMap
    dataRoom["mainData"] = mainData
    dataRoom["dataInit"] = dataInit

def initPlayer(charName,userInfor,dataRoom):
    # tạo các dữ liệu nhân vật theo tên nhân vật
    if charName == "wizard":
        initPlayer = Player.Wizard(userInfor.playerID,dataRoom["dataInit"].playerPos[0],dataRoom["dataInit"].playerPos[1],Constant.player_size,Constant.player_size,charName)
        if charName in userInfor.characterProperties:
            initPlayer.setProperties(userInfor.characterProperties[charName])
    elif charName == "healer":
        initPlayer = Player.Healer(userInfor.playerID,dataRoom["dataInit"].playerPos[0],dataRoom["dataInit"].playerPos[1],Constant.player_size,Constant.player_size,charName)
        if charName in userInfor.characterProperties:
            initPlayer.setProperties(userInfor.characterProperties[charName])
    elif charName == "assassin":
        initPlayer = Player.Assassin(userInfor.playerID,dataRoom["dataInit"].playerPos[0],dataRoom["dataInit"].playerPos[1],Constant.player_size,Constant.player_size,charName)
        if charName in userInfor.characterProperties:
            initPlayer.setProperties(userInfor.characterProperties[charName])
    elif charName == "paladin":
        initPlayer = Player.Paladin(userInfor.playerID,dataRoom["dataInit"].playerPos[0],dataRoom["dataInit"].playerPos[1],Constant.player_size,Constant.player_size,charName)
        if charName in userInfor.characterProperties:
            initPlayer.setProperties(userInfor.characterProperties[charName])
    else:
        initPlayer = Player.Player(userInfor.playerID,dataRoom["dataInit"].playerPos[0],dataRoom["dataInit"].playerPos[1],Constant.player_size,Constant.player_size,charName)
    
    initPlayer.name = userInfor.playerName
    initPlayer.diamond = userInfor.diamond
    initPlayer.textDamages = dataRoom["mainData"].textDamages
    dataRoom["mainData"].players.append(initPlayer)
    dataRoom["dataInit"].player = initPlayer
    return initPlayer

def startSinglePlayer(conn,userInfor,characterName):
    try:
        # tạo thế giới mới cho người chơi
        roomID = createRoomID()

        dataRoom = allRoom.createNewRoom(roomID)
        if characterName in userInfor.characterProperties:
            hightestLevel = userInfor.characterProperties[characterName]["level"]
        else:
            hightestLevel = 1
        createNewWorld(dataRoom,hightestLevel)
        dataRoom["gameLoopStart"] = True

        # tạo luồng chạy mới cho game
        game = threading.Thread(target=gameLoop, args=(dataRoom,roomID))
        game.start()

        # tạo dữ liệu cho nhân vật
        player = initPlayer(characterName,userInfor,dataRoom)

        conn.send(pickle.dumps(dataRoom["dataInit"]))
        
        # xử lý sự kiện cho nhân vật
        handleEvent(conn,player,userInfor,dataRoom)

    except Exception as ex:
        return False

def createWaitingRoomMultiPlayer(conn,userInfor,roomID):
    # nếu roomID = None thì tạo phòng mới
    if roomID == None:
        waitingRoom = WaitingRoom.WaitingRoom()
        waitingRoom.players[userInfor.playerID] = WaitingRoom.CreateInforPlayer(userInfor.playerID,userInfor.playerName)
        waitingRoom.host = userInfor.playerID

        control = Control.Control()
        roomID = createRoomID()
        print("create new roomID:",roomID)

        # gửi thông tin các nhân vật cho người chơi
        control.roomID = roomID
        control.characterProperties = userInfor.characterProperties
        conn.send(pickle.dumps(control))

        dataRoom = allRoom.createNewRoom(control.roomID)
        dataRoom["waitingRoom"] = waitingRoom
    else:
        # đưa người chơi mới vào phòng chờ
        waitingRoom = allRoom.listRoom[roomID]["waitingRoom"]
        waitingRoom.players[userInfor.playerID] = WaitingRoom.CreateInforPlayer(userInfor.playerID,userInfor.playerName)

    handleWaitingRoom(conn,userInfor,waitingRoom,roomID)

def handleWaitingRoom(conn,userInfor,waitingRoom,roomID):
    playerID = userInfor.playerID
    leaveRoom = False
    while True:
        try:
            # nhận yêu cầu từ client
            receive = pickle.loads(conn.recv(32768))

            # nếu game đã bắt đầu đưa người chơi vào trong game
            if waitingRoom.gameStart and playerID not in waitingRoom.exitPlayer:
                conn.send(pickle.dumps(waitingRoom))
                receive = pickle.loads(conn.recv(32768))

                dataRoom = allRoom.listRoom[roomID]
                # tạo dữ liệu mới cho nhân vật
                player = initPlayer(waitingRoom.players[playerID].characterName,userInfor,dataRoom)
                conn.send(pickle.dumps(dataRoom["dataInit"]))

                # xử lý sự kiện cho nhân vật
                handleEvent(conn,player,userInfor,dataRoom)

            # yêu cầu lấy thông tin các người chơi khác trong phòng
            elif receive.step == "getData":
                conn.send(pickle.dumps(waitingRoom))
                continue
            else:
                # yêu cầu thoát khỏi phòng
                if receive.step == "LeaveRoom":
                    conn.send(pickle.dumps("LeaveRoom"))
                    leaveRoom = True
                    break
                # yêu cầu bắt đầu game
                elif receive.step == "StartGame":
                    # nếu người chơi không phải chủ phòng thì chỉ được sẵn sàng hoặc không sẵn sàng
                    if playerID != waitingRoom.host:
                        if playerID not in waitingRoom.readyPlayer:
                            waitingRoom.readyPlayer.append(playerID)
                        else:
                            waitingRoom.readyPlayer.remove(playerID)

                    # nếu người chơi là chủ phòng kiểm tra xem tất cả người chơi đã sẵn sàng hay chưa
                    elif playerID == waitingRoom.host:
                        if len(waitingRoom.readyPlayer) == len(waitingRoom.players) - 1:
                            # nếu tất cả người chơi đã săn sàng thì bắt đầu game
                            # tạo dữ liệu cho game
                            dataRoom = allRoom.listRoom[roomID]
                            
                            hightestLevel = 1
                            for plId in dataRoom["waitingRoom"].players:
                                player = dataRoom["waitingRoom"].players[plId]
                                properties = hightestLevel,HandleCharacterProperties.getCharacterProperties(plId)
                                if dataRoom["waitingRoom"].players[plId].characterName in properties[1]:
                                    hightestLevel = max(hightestLevel,properties[1][player.characterName]["level"])

                            createNewWorld(dataRoom,hightestLevel)
                            dataRoom["gameLoopStart"] = True

                            # tạo luồng chạy mới cho game
                            game = threading.Thread(target=gameLoop, args=(dataRoom,roomID))
                            game.start()

                            waitingRoom.gameStart = True
                            waitingRoom.readyPlayer = []
                            
                # gửi thông tin thay đổi lựa chọn nhân vật của người chơi
                elif receive.step == "ChangeCharacter":
                    waitingRoom.players[playerID].characterName = receive.characterName

                conn.send(pickle.dumps(waitingRoom))
        except Exception as ex:
            print(ex)
            break


    if leaveRoom == False:
        print("Lost connection to player in waitting room: ", playerID)

    if len(waitingRoom.players) == 1:
        allRoom.deleteRoom(roomID)
    else:
        waitingRoom.deletePlayer(playerID)
        if waitingRoom.host == playerID:
            waitingRoom.changeHost()
            print("New host:",waitingRoom.host)

def threaded_client(conn):
    userInfor = None
    # luồng mới chạy cho đến khi client ngắt kết nối
    while True:
        # kiểm tra xem client đã đăng nhập hay chưa
        if userInfor == None:
            userInfor = checkLogin(conn)
            playerOnline.append(userInfor.playerID)
        else:
            try:
                # nhận yêu cầu từ client
                receive = pickle.loads(conn.recv(32768))
                # yêu cầu đăng xuất
                if receive.step == "LogOut":
                    # xóa token ghi nhớ người chơi
                    print("User (ID:",userInfor.playerID,"- Name:",userInfor.playerName+")","// Logout")
                    setToken(id = userInfor.playerID,token = None)
                    # lưu thông tin nhân vật của người chơi vào database
                    HandleCharacterProperties.saveUserInfor(userInfor)
                    playerOnline.remove(userInfor.playerID)
                    # gán userInfor = None để đăng nhập lại
                    userInfor = None
                    conn.send(pickle.dumps("Logout Success"))
                    continue
                # thay đổi tên 
                elif receive.step == "ChangeName":
                    result = HandleAccount.changeName(userInfor.playerID,receive.name,receive.password)
                    reply = Account.ReplyLogin(result["status"],result["message"],None,None,None)
                    if result["status"] == "Success":
                        userInfor.playerName = receive.name
                    conn.send(pickle.dumps(reply))
                    continue
                # thay đổi mật khẩu
                elif receive.step == "ChangePassword":
                    result = HandleAccount.changePassword(userInfor.playerID,receive.oldPassword,receive.newPassword)
                    reply = Account.ReplyLogin(result["status"],result["message"],None,None,None)
                    conn.send(pickle.dumps(reply))
                    continue
                # lấy thông tin nhân vật của người chơi
                elif receive.step == "GetCharacterProperties":
                    conn.send(pickle.dumps(userInfor.characterProperties))
                    continue
                # chế độ chơi một người
                elif receive.step == "SinglePlayer":
                    startSinglePlayer(conn,userInfor,receive.characterName)
                # tạo phòng mới cho chế độ chơi nhiều người
                elif receive.step == "MultiPlayerCreateRoom":
                    createWaitingRoomMultiPlayer(conn,userInfor,None)
                    continue
                # gia nhập vào phòng cho chế độ chơi nhiều người
                elif receive.step == "MultiPlayerJoinRoom":
                    roomID = int(receive.roomID)
                    # kiểm tra xem phòng có tồn tại hay không
                    if roomID not in allRoom.listRoomID:
                        ReplyJoinRoom = Control.ReplyJoinRoom("Error","Room not found",None)
                        conn.send(pickle.dumps(ReplyJoinRoom))
                    # kiểm tra phòng đã đầy hay chưa
                    elif len(allRoom.listRoom[roomID]["waitingRoom"].players) >= limitPlayerInRoom:
                        ReplyJoinRoom = Control.ReplyJoinRoom("Error","Room is full",None)
                        conn.send(pickle.dumps(ReplyJoinRoom))
                    # kiêm tra xem phòng này đã bắt đầu chơi chưa
                    elif allRoom.listRoom[roomID]["waitingRoom"].gameStart:
                        ReplyJoinRoom = Control.ReplyJoinRoom("Error","Game is started",None)
                        conn.send(pickle.dumps(ReplyJoinRoom))
                    else:
                        ReplyJoinRoom = Control.ReplyJoinRoom("Success","Join world",userInfor.characterProperties)
                        conn.send(pickle.dumps(ReplyJoinRoom))
                        createWaitingRoomMultiPlayer(conn,userInfor,roomID)
                    continue
                # yêu cầu thoát game
                elif receive == "exit":
                    break
            except Exception as ex:
                print("->>> line 430:", ex)
                break

    # lưu lại thông tin người chơi nếu thoát đột ngột 
    if userInfor != None:
        playerOnline.remove(userInfor.playerID)
        HandleCharacterProperties.saveUserInfor(userInfor)

    # đóng kết nối
    conn.close()
    print("Connection Closed")
    
while True:
    # chờ yêu cầu kết nối từ client và accept
    conn, addr = s.accept()
    print("Connected to:", addr)
    conn.send(pickle.dumps("Wellcome to the game!"))
    # tạo một luồng mới cho client
    t = threading.Thread(target=threaded_client, args=(conn,))
    t.start()
    
