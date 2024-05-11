class DataInit():
    def __init__(self):
        self.player = None
        self.playerPos = None
        self.blocks = []
        self.trees = []
        self.plants = []
        self.rocks = []
        self.gates = None
        self.background = None
        self.mapLimit = (0,0)
        self.status = "dataInit"
        
    def clearNextMap(self):
        self.player = None
        self.playerPos = None
        self.blocks = []
        self.trees = []
        self.plants = []
        self.rocks = []
        self.background = None
        self.gates = None
        self.mapLimit = (0,0)

    def clearAll(self):
        self.player = None
        self.playerPos = None
        self.blocks = []
        self.trees = []
        self.plants = []
        self.rocks = []
        self.background = None
        self.gates = None
        self.mapLimit = (0,0)
        self.status = "dataInit"