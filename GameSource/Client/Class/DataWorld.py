class InitWorld:
    def __init__(self,blocks,trees,plants,rocks,gates,mapLimit):
        self.blocks = blocks
        self.trees = trees
        self.plants = plants
        self.rocks = rocks
        self.gates = gates
        self.mapLimit = mapLimit
        
    def updateWorld(self,blocks,trees,plants,rocks,gates,mapLimit):
        self.blocks = blocks
        self.trees = trees
        self.plants = plants
        self.rocks = rocks
        self.gates = gates
        self.mapLimit = mapLimit

    def clearWorld(self):
        self.blocks = []
        self.trees = []
        self.plants = []
        self.rocks = []
        self.gates = None
        self.mapLimit = (0,0)

class DataReceive:
    def __init__(self):
        self.enemys = []
        self.boss = []
        self.traps = []
        self.textDamages = []
        self.other_players = []
        self.listDropItems = []
    def updateData(self,enemys,boss,traps,textDamages,listDropItems):
        self.enemys = enemys
        self.boss = boss
        self.traps = traps
        self.textDamages = textDamages
        self.listDropItems = listDropItems
    def clearOtherPlayers(self):
        self.other_players = []
    



