class MainData():
    def __init__(self):
        self.status = "getData"
        self.keys = {"left": 0,"right": 0,"up": 0,"down": 0,"skill1": 0,"skill2": 0,"skill3": 0,"skill4": 0,"skill5": 0,"health": 0,"mana": 0,"escapeGate":0,"escapeGame":0}
        self.mousePos = None
        self.offset = (0,0)
        self.message = None
    def resetMousePos(self):
        self.mousePos = None
    def resetMessage(self):
        self.message = None
    def resetKeys(self):
        self.keys = {"left": 0,"right": 0,"up": 0,"down": 0,"skill1": 0,"skill2": 0,"skill3": 0,"skill4": 0,"skill5": 0,"health": 0,"mana": 0,"escapeGate":0,"escapeGame":0}
    def updatePlayer(self,player):
        self.player = player
    def updateEnemy(self,enemys):
        self.enemys = enemys
    def updateDataAttack(self,dataAttack):
        self.dataAttack = dataAttack

