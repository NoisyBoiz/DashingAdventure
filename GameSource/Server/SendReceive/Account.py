class Login:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.email = ""
        self.step = ""
        self.remember = False

class ReplyLogin:
    def __init__(self,status,message,playerID,name,token):
        self.status = status
        self.message = message
        self.playerID = playerID
        self.name = name
        self.token = token

class SignUp:
    def __init__(self):
        self.email = ""
        self.name = ""
        self.username = ""
        self.password = ""
        self.step = ""

class ChangePassword:
    def __init__(self):
        self.oldPassword = ""
        self.newPassword = ""
        self.step = ""

class ChangeName:
    def __init__(self):
        self.name = ""
        self.password = ""
        self.step = ""
        
        