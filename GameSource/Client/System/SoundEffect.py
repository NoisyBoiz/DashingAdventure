from pygame import mixer
from os import getcwd
from os.path import join
from Function import HandleFile
mixer.init()

mixer.set_num_channels(20)

listSoundEffect = ["AttackSound","ExplosionSound","HealingSound","JumpSound","TeleportSound","SummonSound","HealSkill","FinishGame"]
soundEffectChannel = {}
AllSoundEffect = {}
backgroundMusic = None

def InitSoundEffect():
    for i,sound in enumerate(listSoundEffect):
        AllSoundEffect[sound] = mixer.Sound(join(getcwd(), 'assets', 'Sound', sound + ".wav"))
        soundEffectChannel[sound] = mixer.Channel((i+1))

def InitBackgroundMusic():
    global backgroundMusic
    backgroundMusic = mixer.Sound(join(getcwd(), "assets", "Sound", "BackgroundMusic.wav"))
