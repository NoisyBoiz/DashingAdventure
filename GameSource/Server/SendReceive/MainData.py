class MainData():
    def __init__(self):
        self.players = []
        self.enemys = []
        self.boss = []
        self.traps = []
        self.textDamages = []
        self.listDropItems = []
        self.listMessage = []
        self.status = "data"

    def clearNextMap(self):
        self.enemys = []
        self.boss = []
        self.traps = []
        self.textDamages = []
        self.listDropItems = []
        self.listMessage = []
    
    def clearAll(self):
        self.players = []
        self.enemys = []
        self.traps = []
        self.boss = []
        self.textDamages = []
        self.listDropItems = []
        self.listMessage = []
        self.status = "data"

    def finishGame(self):
        self.enemys = []
        self.boss = []
        self.status = "Finish"