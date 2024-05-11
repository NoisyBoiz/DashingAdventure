class WaitingRoom:
    def __init__(self):
        self.host = None
        self.players = {}
        self.readyPlayer = []
        self.exitPlayer = []
        self.gameStart = False
    def deletePlayer(self,playerID):
        if playerID in self.readyPlayer:
            self.readyPlayer.remove(playerID)
        if playerID in self.exitPlayer:
            self.exitPlayer.remove(playerID)
        if playerID in self.players:
            self.players.pop(playerID)
    def changeHost(self):
        self.host = list(self.players.keys())[0]

class CreateInforPlayer:
    def __init__(self,id,name):
        self.id = id
        self.name = name
        self.characterName = "healer"