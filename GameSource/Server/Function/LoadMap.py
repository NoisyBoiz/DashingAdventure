from System import Constant
from Function import HandleFile
from Entities import Block, Trap, Enemy, Gates, Boss, Item

def LoadMap(mapName,mainData,dataInit,hightestLevel):
    dataFile = HandleFile.readFile("Map/" + mapName)

    idEnemys = 0
    idBoss = 0
    for data in dataFile:
        type = data["type"].split("-")[0]
        if type == "block":
            obj = Block.Block(data["pos"][0],data["pos"][1],Constant.block_size,Constant.block_size, int(data["type"].split("-")[2]) , data["type"].split("-")[1])
            dataInit.blocks.append(obj)
            if data["pos"][0] < dataInit.mapLimit[0]:
                dataInit.mapLimit =  (data["pos"][0],dataInit.mapLimit[1])
            if data["pos"][0] + Constant.block_size > dataInit.mapLimit[1]:
                dataInit.mapLimit = (dataInit.mapLimit[0], data["pos"][0] + Constant.block_size)
        if type == "tree":
            obj = Block.Block(data["pos"][0],data["pos"][1],Constant.block_size*4,Constant.block_size*4, int(data["type"].split("-")[1]) ,"tree")
            dataInit.trees.append(obj)
        if type == "plant120x120":
            obj = Block.Block(data["pos"][0],data["pos"][1],Constant.block_size,Constant.block_size, int(data["type"].split("-")[1]) ,"plant120x120")
            dataInit.plants.append(obj)
        if type == "plant120x240":
            obj = Block.Block(data["pos"][0],data["pos"][1],Constant.block_size,Constant.block_size*2, int(data["type"].split("-")[1]) ,"plant120x240")
            dataInit.plants.append(obj)
        if type == "rock":
            obj = Block.Block(data["pos"][0],data["pos"][1],Constant.block_size,Constant.block_size, int(data["type"].split("-")[1]) ,"rock")
            dataInit.rocks.append(obj)
        if type == "character":
            dataInit.playerPos = data["pos"]
        if type == "traps":
            name = data["type"].split("-")[1]
            if name == "BlueFire" or name == "Fire":
                w = Constant.block_size//2
                h = Constant.block_size
            elif name == "Flower":
                w = Constant.block_size
                h = Constant.block_size
            elif name == "Thorn":
                w = Constant.block_size
                h = Constant.block_size//4
            trap = Trap.Trap(data["pos"][0],data["pos"][1],w,h, name)
            mainData.traps.append(trap)
        if type == "enemy":
            enemy = Enemy.Enemy(idEnemys,data["pos"][0],data["pos"][1],Constant.player_size,Constant.player_size,data["type"].split("-")[1])
            enemy.textDamages = mainData.textDamages
            mainData.enemys.append(enemy)
            enemy.setProperties(hightestLevel)
            idEnemys += 1
        if type == "boss":
            boss = Boss.Boss(idBoss,data["pos"][0],data["pos"][1],Constant.player_size*3,Constant.player_size*3,data["type"].split("-")[1])
            boss.textDamages = mainData.textDamages
            boss.setProperties(hightestLevel)
            mainData.boss.append(boss)
            idBoss += 1
        if type == "gates":
            gates = Gates.Gates(data["pos"][0],data["pos"][1],Constant.block_size*2,Constant.block_size*2, int(data["type"].split("-")[1]))
            dataInit.gates = gates
        if type == "item":
            item = Item.Item(data["pos"][0],data["pos"][1],30,(220/270)*30,data["type"].split("-")[1])
            mainData.listDropItems.append(item)
   