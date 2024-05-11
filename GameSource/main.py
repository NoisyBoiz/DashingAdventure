import pygame
from os import listdir, getcwd
from os.path import isfile, join

screen = pygame.display.set_mode((800, 600))  



# hàm để lật ảnh trái phải
def Flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

# hàm để cắt ảnh thành các miếng nhỏ xong lưu vào mảng
def splitSprite(path, original_width, original_height, new_width, new_height, direction=False):
    fullPath = join(getcwd(),path)

    files = [f for f in listdir(fullPath) if isfile(join(fullPath, f))]

    all_sprites = {}
    for file in files:
        sprite_sheet = pygame.image.load(join(fullPath, file))

        sprites = []
        for i in range(sprite_sheet.get_width() // original_width):
            surface = pygame.Surface((original_width, original_height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * original_width, 0, original_width, original_height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale(surface,(new_width,new_height)))
        if direction:
            all_sprites[file.replace(".png", "") + "_right"] = sprites
            all_sprites[file.replace(".png", "") + "_left"] = Flip(sprites)
        else:
            all_sprites[file.replace(".png", "")] = sprites
    return all_sprites

# class rồng
class Dragon:
    def __init__(self,player):
        self.skillName = "dragon"
        self.rect = pygame.Rect(player.rect.x,player.rect.y,60,60)

        # khoảng cách tối đa mà rồng bay được
        self.attack_range = 600

        # vận tốc bay của rồng
        self.speed_run = 10

        # hướng di chuyển của rồng sẽ giống hướng di chuyển của nhân vật
        self.direction = player.direction

        self.animation_count = 0
        self.animation_delay = 2
        self.status = "init"
        self.index = 0

        self.end = False

    def loop(self):
        if(self.direction == "right"):
            self.rect.x += self.speed_run
        else:
            self.rect.x -= self.speed_run

        self.animation_count += 1
        self.index = self.animation_count // self.animation_delay
        if self.index >= 10:
            self.status = "initUp"
            self.index -= 10

        # nếu rồng bay quá khoảng cách tối đa thì rồng sẽ biến mất
        self.attack_range -= self.speed_run
        if(self.attack_range <= 0):
            self.end = True
            return
        
    def draw(self,screen):
        if(self.status == "initUp"):
            self.index = self.index%4
        screen.blit(dragonSprites[self.status+"_"+self.direction][self.index],self.rect)
        
# class Nhân Vật
class Player:
    def __init__(self):
        self.rect = pygame.Rect(60, 60, 60, 60)
        self.direction = "right"
    def draw(self,screen):
        pygame.draw.rect(screen,(255,0,0),self.rect)

# khởi tạo nhân vật
player = Player()

# khởi tạo mảng để chứa rồng đã tạo
skillShow = []

# khởi tạo mảng chứa các ảnh của rồng
dragonSprites = splitSprite("Dragon", 50, 50, 60, 60, True)


running = True
clock = pygame.time.Clock()
while running:
    # Tô màu nền trắng
    screen.fill((255, 255, 255))

    # đặt tốc độ khung hình là 60 khung hình / giây
    clock.tick(60)

    # bắt sự kiện nhấn phím, nhấn chuột
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Nhấn R để tạo rồng
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            skillShow.append(Dragon(player))

    # vẽ nhân vật
    player.draw(screen)

    # vẽ rồng
    for skill in skillShow:
        skill.loop()
        skill.draw(screen)
        if(skill.end):
            skillShow.remove(skill)

    pygame.display.flip()

pygame.quit()