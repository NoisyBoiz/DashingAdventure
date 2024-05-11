import Function.Func as Func
import System.Constant as Constant

characterSetting = {
    "healer": {"path":["MainCharacters","Healer"],"ori_width":32, "ori_height":32,"new_width":Constant.player_size,"new_height":Constant.player_size,"get_length":True,"direction":True},
    "wizard": {"path":["MainCharacters","Wizard"],"ori_width":32, "ori_height":32,"new_width":Constant.player_size,"new_height":Constant.player_size,"get_length":True,"direction":True},
    "assassin": {"path":["MainCharacters","Assassin"],"ori_width":32, "ori_height":32,"new_width":Constant.player_size,"new_height":Constant.player_size,"get_length":True,"direction":True},
    "paladin": {"path":["MainCharacters","Paladin"],"ori_width":32, "ori_height":32,"new_width":Constant.player_size,"new_height":Constant.player_size,"get_length":True,"direction":True},
    "paladinGreen": {"path":["MainCharacters","PaladinGreen"],"ori_width":32, "ori_height":32,"new_width":Constant.player_size,"new_height":Constant.player_size,"get_length":True,"direction":True}
}

mainCharacters = {}
lengthMainCharacters = {}
mainCharactersShowSelect = []
mainCharactersSelect = []
mainCharactersSelectIcon = []
for sprite in characterSetting:
    mainCharacters[sprite],lengthMainCharacters[sprite] = Func.splitSprite(characterSetting[sprite]["path"],characterSetting[sprite]["ori_width"],characterSetting[sprite]["ori_height"],characterSetting[sprite]["new_width"],characterSetting[sprite]["new_height"],characterSetting[sprite]["get_length"],characterSetting[sprite]["direction"])
    mainCharactersSelectIcon.append(Func.splitSprite(characterSetting[sprite]["path"],characterSetting[sprite]["ori_width"],characterSetting[sprite]["ori_height"],Constant.player_size,Constant.player_size, False, False))
    mainCharactersShowSelect.append(Func.splitSprite(characterSetting[sprite]["path"],characterSetting[sprite]["ori_width"],characterSetting[sprite]["ori_height"],Constant.player_size*3,Constant.player_size*3, False, False))
    mainCharactersSelect.append(Func.splitSprite(characterSetting[sprite]["path"],characterSetting[sprite]["ori_width"],characterSetting[sprite]["ori_height"],Constant.player_size*1.6,Constant.player_size*1.6, False, False))

switchSelect = {
    0:"healer",
    1:"wizard",
    2:"assassin",
    3:"paladin",
}
switchSelectIndex = {
    "healer":0,
    "wizard":1,
    "assassin":2,
    "paladin":3,
}

enemysSetting = {
    "slime":{"path":["Enemy","Slime"],"ori_width":100, "ori_height":100,"new_width":Constant.player_size,"new_height":Constant.player_size,"get_length":True,"direction":True},
    "slimeGreen":{"path":["Enemy","SlimeGreen"],"ori_width":100, "ori_height":100,"new_width":Constant.player_size,"new_height":Constant.player_size,"get_length":True,"direction":True},
    "slimeRed":{"path":["Enemy","SlimeRed"],"ori_width":100, "ori_height":100,"new_width":Constant.player_size,"new_height":Constant.player_size,"get_length":True,"direction":True},
    "buffalo":{"path":["Enemy","Buffalo"],"ori_width":100, "ori_height":100,"new_width":Constant.player_size,"new_height":Constant.player_size,"get_length":True,"direction":True},
    "eye":{"path":["Enemy","Eye"],"ori_width":100, "ori_height":100,"new_width":Constant.player_size,"new_height":Constant.player_size,"get_length":True,"direction":True},
    "thorn":{"path":["Enemy","Thorn"],"ori_width":100, "ori_height":100,"new_width":Constant.player_size,"new_height":Constant.player_size,"get_length":True,"direction":True},
    "worm":{"path":["Enemy","Worm"],"ori_width":100, "ori_height":100,"new_width":Constant.player_size,"new_height":Constant.player_size,"get_length":True,"direction":True},
    "thornYellow":{"path":["Enemy","ThornYellow"],"ori_width":100, "ori_height":100,"new_width":Constant.player_size,"new_height":Constant.player_size,"get_length":True,"direction":True}
}

enemys = {}
lengthEnemys = {}
for enemy in enemysSetting:
    enemys[enemy],lengthEnemys[enemy] = Func.splitSprite(enemysSetting[enemy]["path"],enemysSetting[enemy]["ori_width"],enemysSetting[enemy]["ori_height"],enemysSetting[enemy]["new_width"],enemysSetting[enemy]["new_height"],enemysSetting[enemy]["get_length"],enemysSetting[enemy]["direction"])


bossSetting = {
    "slime":{"path":["Enemy","Slime"],"ori_width":100, "ori_height":100,"new_width":Constant.player_size*3,"new_height":Constant.player_size*3,"get_length":True,"direction":True},
    "slimeGreen":{"path":["Enemy","SlimeGreen"],"ori_width":100, "ori_height":100,"new_width":Constant.player_size*3,"new_height":Constant.player_size*3,"get_length":True,"direction":True},
    "slimeRed":{"path":["Enemy","SlimeRed"],"ori_width":100, "ori_height":100,"new_width":Constant.player_size*3,"new_height":Constant.player_size*3,"get_length":True,"direction":True},
    "buffalo":{"path":["Enemy","Buffalo"],"ori_width":100, "ori_height":100,"new_width":Constant.player_size*3,"new_height":Constant.player_size*3,"get_length":True,"direction":True},
    "eye":{"path":["Enemy","Eye"],"ori_width":100, "ori_height":100,"new_width":Constant.player_size*3,"new_height":Constant.player_size*3,"get_length":True,"direction":True},
    "thorn":{"path":["Enemy","Thorn"],"ori_width":100, "ori_height":100,"new_width":Constant.player_size*3,"new_height":Constant.player_size*3,"get_length":True,"direction":True},
    "worm":{"path":["Enemy","Worm"],"ori_width":100, "ori_height":100,"new_width":Constant.player_size*3,"new_height":Constant.player_size*3,"get_length":True,"direction":True},
    "thornYellow":{"path":["Enemy","ThornYellow"],"ori_width":100, "ori_height":100,"new_width":Constant.player_size*3,"new_height":Constant.player_size*3,"get_length":True,"direction":True}
}

allBoss = {}
lengthAllBoss = {}
for boss in bossSetting:
    allBoss[boss],lengthAllBoss[boss] = Func.splitSprite(bossSetting[boss]["path"],bossSetting[boss]["ori_width"],bossSetting[boss]["ori_height"],bossSetting[boss]["new_width"],bossSetting[boss]["new_height"],bossSetting[boss]["get_length"],bossSetting[boss]["direction"])


skillSetting = {
    "dragon":{"path":["Skills","Dragon"],"ori_width":50, "ori_height":50,"new_width":Constant.player_size,"new_height":Constant.player_size,"get_length":True,"direction":True},
    "buff":{"path":["Skills","Buff"],"ori_width":150, "ori_height":150,"new_width":Constant.player_size*1.3,"new_height":Constant.player_size*1.5,"get_length":True,"direction":False},
    "explosion":{"path":["Skills","Explosion"],"ori_width":150, "ori_height":150,"new_width":Constant.player_size*3.7,"new_height":Constant.player_size*3.7,"get_length":True,"direction":False},
    "teleport":{"path":["Skills","Teleport"],"ori_width":200, "ori_height":200,"new_width":Constant.player_size*2,"new_height":Constant.player_size*2,"get_length":True,"direction":False},
    "slash":{"path":["Skills","Slash"],"ori_width":100, "ori_height":100,"new_width":Constant.player_size,"new_height":Constant.player_size,"get_length":True,"direction":True},
    "meteorites": {"path":["Skills","Meteorites"],"ori_width":200, "ori_height":200,"new_width":Constant.player_size,"new_height":Constant.player_size,"get_length":True,"direction":False},
    "fireBall": {"path":["Skills","FireBall"],"ori_width":200, "ori_height":200,"new_width":Constant.player_size,"new_height":Constant.player_size,"get_length":True,"direction":False},
    "fireBallSmall":{ "path":["Skills","FireBall"],"ori_width":200, "ori_height":200,"new_width":Constant.player_size*0.4,"new_height":Constant.player_size*0.4,"get_length":True,"direction":False},
    "flash":{"path":["Skills","Flash"],"ori_width":1000, "ori_height":200,"new_width":Constant.player_size*5,"new_height":Constant.player_size,"get_length":True,"direction":True},
    "burn": {"path":["Skills","Burn"],"ori_width":200, "ori_height":200,"new_width":Constant.player_size,"new_height":Constant.player_size,"get_length":True,"direction":False},
}

skills = {}
lengthSkills = {}
for skill in skillSetting:
    skills[skill], lengthSkills[skill] = Func.splitSprite(skillSetting[skill]["path"],skillSetting[skill]["ori_width"],skillSetting[skill]["ori_height"],skillSetting[skill]["new_width"],skillSetting[skill]["new_height"],skillSetting[skill]["get_length"],skillSetting[skill]["direction"])


allObject = Func.splitSprite(["Terrain"],50,50,Constant.block_size,Constant.block_size,False)
tree = Func.splitSprite(["Tree"],300,300,Constant.block_size*4,Constant.block_size*4,False)
plant120x120 = Func.splitSpriteImgPath(["Plant","plant120x120"],120,120,Constant.block_size,Constant.block_size,False)["plant120x120"]
plant120x240 = Func.splitSpriteImgPath(["Plant","plant120x240"],120,240,Constant.block_size,Constant.block_size*2,False)["plant120x240"]
rock = Func.splitSpriteImgPath(["Rock","rock"],120,120,Constant.block_size,Constant.block_size,False)["rock"]
gates = Func.splitSprite(["Gates"],240,240,Constant.block_size*2,Constant.block_size*2,False)["gates"]

diamond = Func.splitSpriteImgPath(["Items","Diamond","Diamond"],270,220,30,int(220/270*30),False,False)["Diamond"]
allItems = {"diamond":diamond}

allBossSkill,lengthAllBossSkill = Func.splitSprite(["BossSkills"],200,200,Constant.player_size*1.4,Constant.player_size*1.4,True,True)
IconSkills = Func.splitSprite(["IconSkills"],200,200,Constant.player_size,Constant.player_size,False,False)

settingTraps = {
    "BlueFire":{ "path":["Traps","BlueFire"],"ori_width":200, "ori_height":300,"new_width":Constant.block_size*2/3,"new_height":Constant.block_size,"get_length":True,"direction":False},
    "Fire": {"path":["Traps","Fire"],"ori_width":200, "ori_height":300,"new_width":Constant.block_size*2/3,"new_height":Constant.block_size,"get_length":True,"direction":False},
    "Thorn": {"path":["Traps","Thorn"],"ori_width":200, "ori_height":50,"new_width":Constant.block_size,"new_height":Constant.block_size//4,"get_length":True,"direction":False},
    "Flower": {"path":["Traps","Flower"],"ori_width":200, "ori_height":200,"new_width":Constant.block_size,"new_height":Constant.block_size,"get_length":True,"direction":False},
}

AllTraps = {}
AllLengthTraps = {}
for trap in settingTraps:
    AllTraps[trap], AllLengthTraps[trap] = Func.splitSprite(settingTraps[trap]["path"],settingTraps[trap]["ori_width"],settingTraps[trap]["ori_height"],settingTraps[trap]["new_width"],settingTraps[trap]["new_height"],settingTraps[trap]["get_length"],settingTraps[trap]["direction"])

normalAttackFar, lengthNormalAttackFar = Func.splitSprite(["NormalAttack","Far"],200,200,30,30,True,True)
normalAttackNear, lengthNormalAttackNear = Func.splitSprite(["NormalAttack","Near"],200,200,Constant.block_size,Constant.block_size,True,True)
magicRod = Func.splitSpriteImgPath(["Weapon","magicRod"],340,340,Constant.block_size,Constant.block_size,False,True)
sword = Func.splitSpriteImgPath(["Weapon","sword"],200,200,Constant.block_size,Constant.block_size,False,True)