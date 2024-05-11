from System.DatabaseConnect import *

def checkLoginToken(token):
    acc = loginByToken(token)
    if acc != None:
        return {"status":"Success","message":"Success","id":acc.id,"name":acc.name,"diamond":acc.diamond,"token":None}
    return {"status":"Error","message":"Token is expired"}
   
def checkAccountLogin(username, password, remember):
    acc = getAccInfor(username = username, id = None)
    if acc != None:
        if acc.password == password:
            if remember:
                token = createToken(acc.id)
                setToken(acc = acc, token = token)
            else:
                if acc.token != None:
                    setToken(acc = acc)
                token = None
            return {"status":"Success","message":"Success","id":acc.id,"name":acc.name,"diamond":acc.diamond,"token":token}
        return {"status":"Error","message":"Password is incorrect"}
    return {"status":"Error","message":"Username is not exist"}

def checkAccountSignUp(name, username, email, password):
    if checkExistUsername(username):
        return {"status":"Error","message":"Username already exists"}
    if email != "" and checkExistEmail(email): 
        return {"status":"Error","message":"Email already exists"}
    if email == "": email = None
    insertNewAcc(name, username, password, email)
    return {"status":"Success","message":"Success"}

def changePassword(id,oldPassword,newPassword):
    if updatePassword(id = id,oldpassword = oldPassword,newpassword = newPassword):
        return {"status":"Success","message":"Success"}
    return {"status":"Error","message":"Old Password is incorrect"}
   
def changeName(id,name,password):
    if updateName(id = id, password= password, newname= name):
        return {"status":"Success","message":"Success"}
    return {"status":"Error","message":"Password is incorrect"}
    