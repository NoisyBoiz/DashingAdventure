from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, INTEGER, VARCHAR, NVARCHAR, ForeignKey, DATETIME, String, PrimaryKeyConstraint
from sqlalchemy import exists
from typing import Union
from datetime import datetime
import time
'''
'''

db_user = 'sa'
db_user_password = '12'
host = 'NoisyBoy'
port = '1433'
db_name = 'GameDatabase'


#engine = create_engine(f'mssql+pyodbc://{db_user}:{db_user_password}@{host}:{port}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server'
#                       '&TrustServerCertificate=yes')

engine = create_engine('sqlite:///GameDatabase.db')

Base = declarative_base()

class AccountInfor(Base):
    __tablename__ = 'account'
    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    username = Column(VARCHAR(30), unique=True, nullable=False)
    password = Column(VARCHAR(20), nullable=False)
    email = Column(VARCHAR(50), nullable=False, unique=True)
    name = Column(VARCHAR(20), nullable=False)
    token = Column(VARCHAR(50), nullable=True)
    createAt = Column(DATETIME, nullable=False)
    diamond = Column(INTEGER)
    baned = Column(INTEGER)

class CharacterInfor(Base):
    __tablename__ = "character_infor"
    id = Column(INTEGER, ForeignKey('account.id'))
    char_name = Column(VARCHAR(50))
    max_hp = Column(INTEGER)
    max_mp = Column(INTEGER)
    physical_damage = Column(INTEGER)
    magic_damage = Column(INTEGER)
    crit_rate = Column(INTEGER)
    crit_damage = Column(INTEGER)
    life_steal = Column(INTEGER)
    physical_armor = Column(INTEGER)
    magic_armor = Column(INTEGER)
    physical_armor_penetration = Column(INTEGER)
    magic_armor_penetration = Column(INTEGER)
    attack_speed = Column(INTEGER)
    speed_run = Column(INTEGER)
    skills = Column(String(50))
    level = Column(INTEGER)
    __table_args__ = (
        PrimaryKeyConstraint(id, char_name),
        {},
    )

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def getCharacter(id, charName):
    char = session.query(CharacterInfor).filter_by(id=id,char_name=charName).first()
    properties = {
        "max_hp": char.max_hp,
        "max_mp": char.max_mp,
        "physical_damage": char.physical_damage,
        "magic_damage": char.magic_damage,
        "crit_rate": char.crit_rate,
        "crit_damage": char.crit_damage,
        "life_steal": char.life_steal,
        "physical_armor": char.physical_armor,
        "magic_armor": char.magic_armor,
        "physical_armor_penetration": char.physical_armor_penetration,
        "magic_armor_penetration": char.magic_armor_penetration,
        "attack_speed": char.attack_speed,
        "speed_run": char.speed_run,
        "skills": char.skills,
        "level": char.level
    }
    return properties

def createChar(id, charName):
    try:
        char = CharacterInfor(id=id, char_name=charName)
        session.add(char)
        session.commit()
        return True
    except:
        return False

def getAllCharProperties(id)-> dict:
    infor = {}
    allChar = session.query(CharacterInfor).filter_by(id=id).all()
    for char in allChar:
        infor[char.char_name] = getCharacter(id=id, charName=char.char_name)
    return infor


def updateChar(id, charName, properties):
    char = session.query(CharacterInfor).filter_by(id=id, char_name=charName).first()
    if char == None:
        #create if char doesn's exists
        createChar(id=id, charName=charName)
        char = session.query(CharacterInfor).filter_by(id=id, char_name=charName).first()
    char.max_hp = properties["max_hp"]
    char.max_mp = properties["max_mp"]
    char.physical_damage = properties["physical_damage"]
    char.magic_damage = properties["magic_damage"]
    char.crit_rate = properties["crit_rate"]
    char.crit_damage = properties["crit_damage"]
    char.life_steal = properties["life_steal"]
    char.physical_armor = properties["physical_armor"]
    char.magic_armor = properties["magic_armor"]
    char.physical_armor_penetration = properties["physical_armor_penetration"]
    char.magic_armor_penetration= properties["magic_armor_penetration"]
    char.attack_speed = properties["attack_speed"]
    char.speed_run = properties["speed_run"]
    char.skills = properties["skills"]
    char.level = properties["level"]
    session.commit()

"""class PlayerInfor(Base):
    __tablename__ = 'player'
    id = Column(INTEGER, ForeignKey('account.id'), primary_key=True)
    name = Column(NVARCHAR(40), nullable=True)
    character = Column(VARCHAR(40))
    level = Column(INTEGER)
    exp = Column(INTEGER)"""

def getTimeNow():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
def banAccount(id = None, username = None):
    try:
        acc = None
        if username is not None:
            acc = getAccInfor(username=username)
        elif id is not None:
            acc = getAccInfor(id=id)
        if acc is None:
            return False
        else:
            acc.baned=1
            session.commit()
    except Exception as e:
        print(str(e))
        return False


def createToken(id):
    expTime = str((int(time.time()) + 60*60*24))
    token = str(id) +"."+ expTime
    return token

def checkTokenExp(token):
    expTime = int(token.split(".")[-1])
    timeNow = round(time.time())
    if expTime > timeNow:
        return True
    return False

def checkExistUsername(username):
    '''
    return True if account already exists.
    return False if not.
    '''
    try:
        session.query(AccountInfor).filter_by(username=username).one()
        return True
    except :
        return False
    
def checkExistEmail(email):
    '''
    return True if account already exists.
    return False if not.
    '''
    try:
        session.query(AccountInfor).filter_by(email = email).one()
        return True
    except :
        return False

def insertNewAcc(name, username, password, email=None):
    try:
        acc = AccountInfor(name = name, username=username, password=password, email=email, token=None, createAt=datetime.now(),diamond = 50, baned=0)
        session.add(acc)
        session.commit()
        return True
    except Exception as e:
        print(str(e))
        return False
    
def getAccInfor(username=None, id=None):
    '''return an instance of AccountInfor class. None if Not Found
    '''
    if id is not None:
        acc = session.query(AccountInfor).filter_by(id=id).first()
    else:
        acc = session.query(AccountInfor).filter_by(username=username).first()
    return acc 

def getAccList():
    '''return a list of instances of AccountInfor Class
    '''
    accs = session.query(AccountInfor).all()
    return accs
      
def updatePassword(id, oldpassword:str, newpassword:str):
    '''
    return True if update successful
    return Flase if password is wrong or account is NotFound
    '''
    try:
        acc = getAccInfor(id=id)
        if acc.password == oldpassword:
            acc.password = newpassword
            session.commit()
            return True
        else:
            return False
    except:
        return False

def updateName(id, password, newname:str):
    try:
        acc = getAccInfor(id=id)
        if acc.password == password:
            acc.name = newname
            session.commit()
            return True
        else:
            return False
    except:
        return False
    
def setToken(id = None, acc = None, token = None):
    '''
    update token of account with id
    return True if update successful
    return False if account is not found
    '''
    try:
        if acc == None:
            acc = session.query(AccountInfor).filter_by(id = id).one()
        acc.token = token
        session.commit()
        return True
    except Exception as e:
        print(str(e))
        return False
    
def getDiamond(id):
    acc = session.query(AccountInfor).filter_by(id=id).one()
    return acc.diamond

def setDiamond(id, diamond):
    acc = session.query(AccountInfor).filter_by(id=id).one()
    acc.diamond = diamond
    session.commit()
    return True

def loginByToken(token):
    try:
        id = int(token.split(".")[0])
        acc = session.query(AccountInfor).filter_by(id = id).one()
        if acc.token == token:
            if(checkTokenExp(token) == False):
                setToken(id = None,acc = acc,remove=True)
                return None
            return acc
        return None
    except:
        return None
    
def checkPlayerNameExists(name):
    '''
    Check if a player name already exists.
    Return bool
    '''
    result = session.query(AccountInfor).filter_by(name=name).first()
    if result is None:
        return False
    else:
        return True