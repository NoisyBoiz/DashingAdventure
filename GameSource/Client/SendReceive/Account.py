class Login:
    def __init__(self,step,username="",password="",token="",remember=""):
        self.step = step
        self.username = username
        self.password = password
        self.token = token
        self.remember = remember

class SignUp:
    def __init__(self,step,email,name,username,password):
        self.step = step
        self.email = email
        self.name = name
        self.username = username
        self.password = password

class ReplyLogin:
    def __init__(self):
        self.status = ""
        self.message = ""
        self.playerID = ""
        self.name = ""
        self.token = ""
      
class ChangePassword:
    def __init__(self,step,oldPassword,newPassword):
        self.step = step
        self.oldPassword = oldPassword
        self.newPassword = newPassword
       
class ChangeName:
    def __init__(self,step,name,password):
        self.step = step
        self.name = name
        self.password = password