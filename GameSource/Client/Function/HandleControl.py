from pygame import key,K_LEFT, K_RIGHT, K_SPACE, K_UP
from System import SoundEffect

SoundEffect.InitSoundEffect()

def playSound(name,settingSound):
    SoundEffect.soundEffectChannel[name].play(SoundEffect.AllSoundEffect[name],0)
    SoundEffect.soundEffectChannel[name].set_volume(settingSound["SoundEffect"]/100)

def handleKeys(event,data,player,settingControl,settingSound):
    if player.characterName == "assassin":
        if event.key == settingControl["skill1"] and player.conditionSkill.slash(player=player):
            playSound("AttackSound",settingSound)
            data.keys["skill1"] = 1
        if event.key == settingControl["skill2"] and player.conditionSkill.flash(player=player):
            data.keys["skill2"] = 1
        if event.key == settingControl["skill3"] and player.conditionSkill.assassinBuff(player=player):
            data.keys["skill3"] = 1
        if event.key == settingControl["skill4"] and player.conditionSkill.teleport(player=player):
            playSound("TeleportSound",settingSound)
            data.keys["skill4"] = 1
    if player.characterName == "wizard":
        if event.key == settingControl["skill1"] and player.conditionSkill.dragon(player=player):
            data.keys["skill1"] = 1
        if event.key == settingControl["skill2"] and player.conditionSkill.meteorites(player=player):
            data.keys["skill2"] = 1
        if event.key == settingControl["skill3"] and player.conditionSkill.burn(player=player):
            data.keys["skill3"] = 1
        if event.key == settingControl["skill4"] and player.conditionSkill.fireBall(player=player):
            data.keys["skill4"] = 1
    if player.characterName == "healer":
        if event.key == settingControl["skill1"] and player.conditionSkill.heal(player=player):
            playSound("HealSkill",settingSound)
            data.keys["skill1"] = 1
        if event.key == settingControl["skill2"] and player.conditionSkill.debuffEnemy(player=player):
            data.keys["skill2"] = 1
        if event.key == settingControl["skill3"] and player.conditionSkill.buffPlayers(player=player):
            data.keys["skill3"] = 1
        if event.key == settingControl["skill4"] and player.conditionSkill.revival(player=player):
            playSound("HealSkill",settingSound)
            data.keys["skill4"] = 1
    if player.characterName == "paladin":
        if event.key == settingControl["skill1"] and player.conditionSkill.buffArmor(player=player):
            data.keys["skill1"] = 1
        if event.key == settingControl["skill2"] and player.conditionSkill.explosion(player=player):
            playSound("ExplosionSound",settingSound)
            data.keys["skill2"] = 1
        if event.key == settingControl["skill3"] and player.conditionSkill.autoHealth(player=player):
            data.keys["skill3"] = 1
        if event.key == settingControl["skill4"] and player.conditionSkill.summonPet(player=player):
            data.keys["skill4"] = 1
            
    if event.key == settingControl["health"] and player.hpPotion != 0 and player.hpCDCount == 0:
        playSound("HealingSound",settingSound)
        data.keys["health"] = 1
    if event.key == settingControl["mana"] and player.mpPotion != 0 and player.mpCDCount == 0:
        playSound("HealingSound",settingSound)
        data.keys["mana"] = 1
    if event.key == settingControl["escapeGate"]:
        data.keys["escapeGate"] = 1
    if (event.key == settingControl["up"] or event.key == K_SPACE or event.key == K_UP) and player.jump_count < 2 :
        playSound("JumpSound",settingSound)
        data.keys["up"] = 1

def handleKeysPressed(data,settingControl,settingSound):
    event = key.get_pressed()
    if event[settingControl["right"]] or event[K_RIGHT]:
        data.keys["right"] = 1
    if event[settingControl["left"]] or event[K_LEFT]:
        data.keys["left"] = 1