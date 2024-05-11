from System.DatabaseConnect import getAllCharProperties, updateChar

def dictDumpsProperties(player):
    # lấy dữ liệu nhân vật của người chơi chuyển về dạng dict
    properties = {
        "max_hp": player.max_hp,
        "max_mp": player.max_mp,
        "physical_damage": player.physical_damage,
        "magic_damage": player.magic_damage,
        "crit_rate": player.crit_rate,
        "crit_damage": player.crit_damage,
        "life_steal": player.life_steal,
        "physical_armor": player.physical_armor,
        "magic_armor": player.magic_armor,
        "physical_armor_penetration": player.physical_armor_penetration,
        "magic_armor_penetration": player.magic_armor_penetration,
        "attack_speed": player.attack_speed,
        "speed_run": player.speed_run,
        "skills": None,
        "level": player.level
    }
    return properties

def updateCharacterProperties(userInfor,player):
    # cập nhật dữ liệu nhân vật của người chơi
    charProperties = dictDumpsProperties(player)
    userInfor.characterProperties[player.characterName] = charProperties

def saveUserInfor(userInfor):
    # lưu thông tin nhân vật
    allCharacterProperties = userInfor.characterProperties
    for char in allCharacterProperties:
        updateChar(id=userInfor.playerID, charName=char, properties=allCharacterProperties[char])

def getCharacterProperties(playerID):
    # lấy ra thông tin nhân vật
    return getAllCharProperties(id=playerID)
   






