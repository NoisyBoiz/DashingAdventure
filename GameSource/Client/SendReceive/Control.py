class Control:
    def __init__(self):
        self.step = ""
        self.roomID = ""
        self.playerID = ""
        self.characterName = ""

class ReplyJoinRoom:
    def __init__(self,status,message,characterProperties):
        self.status = status
        self.message = message
        self.characterProperties = characterProperties