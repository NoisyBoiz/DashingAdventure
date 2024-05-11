import pygame
pygame.init()
import System.Setting as Setting
screen = pygame.display.set_mode((Setting.screen_width,Setting.screen_height),pygame.RESIZABLE)
surfaceAlpha = pygame.Surface((Setting.screen_width,Setting.screen_height),pygame.SRCALPHA)
surfaceAlpha.set_alpha(100)

import System.Ruler as Ruler
import System.Menu as Menu
import System.Action as Action
import System.Notification as Notification
import System.File as File

def handleCursor(status):
    if status.actionType == "shift":
        pygame.mouse.set_cursor(*Setting.imageCursor[status.actionShift_direction])
    else:
        pygame.mouse.set_cursor(pygame.cursors.arrow)

class Status:
    def __init__(self):
        self.actionType = "move"
        self.blockType = "character"
        self.indexBlock = 0
        self.isMouseDown = False
        self.actionShift_direction = "vertical"
        self.objSelected = None
        self.isQuit = False
        self.shift_x_cursor = 0
        self.shift_y_cursor = 0
        self.sticky = False
        self.haveChange = False
        self.offset_x = Setting.screen_width//2
        self.offset_y = Setting.screen_height//2
        self.preMousePos = (self.offset_x,self.offset_y)
        self.mouseCollision = "mask"

    def handleChangeShiftDirection(self):
        if self.actionShift_direction == "vertical":
            self.actionShift_direction = "horizontal"
        elif self.actionShift_direction == "horizontal":
            self.actionShift_direction = "all"
        else:
            self.actionShift_direction = "vertical"


objectGroups = pygame.sprite.Group()
File.read(objectGroups)

ruler = Ruler.Ruler()
status = Status()
menu = Menu.Menu()
action = Action.Action(objectGroups)
notification = Notification.Notification()

running = True
fontPos = pygame.font.SysFont("Arial",20,bold=True)
pygame.mouse.set_cursor(pygame.cursors.arrow)

while running:
    screen.fill((238, 241, 255))
    surfaceAlpha.fill((255,255,255,0))
    if(status.isQuit == False):
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            # check có thoát không
            if event.type == pygame.QUIT:
                status.isQuit = True
                pygame.mouse.set_cursor(pygame.cursors.arrow)
                break
            if event.type == pygame.VIDEORESIZE:
                Setting.screen_width = event.w
                Setting.screen_height = event.h
                # screen = pygame.display.set_mode((Setting.screen_width,Setting.screen_height),pygame.RESIZABLE)
                surfaceAlpha = pygame.Surface((Setting.screen_width,Setting.screen_height),pygame.SRCALPHA)
                surfaceAlpha.set_alpha(100)
                menu.resize()
             
        
            if event.type == pygame.MOUSEMOTION:
                # hành động nhấn và di chuyển chuột
                if status.isMouseDown:
                    if mousePos[1]>Setting.block_size:
                        action.hanldeMouseMotion(mousePos,status)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if status.actionType == "save":
                    notification.checkClick(mousePos,status,objectGroups)
                else:
                    # check chọn trên thanh công cụ
                    if(mousePos[1]<=Setting.block_size):
                        menu.handleClick(mousePos,status)
                        handleCursor(status)
                    else:
                        action.handleMouseClick(mousePos,status)
                status.preMousePos = mousePos
                status.isMouseDown = True

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                status.isMouseDown = False
                if status.objSelected != None:
                    status.objSelected = None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if status.actionType == "shift":
                    status.handleChangeShiftDirection()
                    pygame.mouse.set_cursor(*Setting.imageCursor[status.actionShift_direction])
                else:
                    menu.checkChangeIndexBlock(status)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    status.sticky = not status.sticky
                if event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                    if status.mouseCollision == "mask":
                        status.mouseCollision = "rect"
                    else:
                        status.mouseCollision = "mask"
                menu.checkPressKey(event.key,status)


        # vẽ hình ảnh ra màn hình
        for obj in objectGroups:
            obj.draw(screen,status.offset_x,status.offset_y)

        # hiện hình ảnh xem trước của block
        if status.actionType == "add" or status.actionType == "edit":
            if mousePos[1]>Setting.block_size:
                shift_x = status.offset_x%Setting.block_size
                shift_y = status.offset_y%Setting.block_size
                mousePoint = ((mousePos[0]-shift_x)//Setting.block_size*Setting.block_size + shift_x, (mousePos[1]-shift_y)//Setting.block_size*Setting.block_size + shift_y)
                if Setting.blockSetting[status.blockType]["indexChange"]:
                    surfaceAlpha.blit(Setting.imageBlock[status.blockType][status.indexBlock],(mousePoint[0],mousePoint[1]))
                else:
                    surfaceAlpha.blit(Setting.imageBlock[status.blockType][Setting.blockSetting[status.blockType]["defaultIndex"]],(mousePoint[0],mousePoint[1]))
                screen.blit(surfaceAlpha,(0,0))

        ruler.draw(screen,status.offset_x,status.offset_y)

        menu.draw(screen,status)
        textPos = fontPos.render("x: "+str(mousePos[0]-status.offset_x) + " / y: " + str(mousePos[1]-status.offset_y),True,(0, 0, 0))
        screen.blit(textPos,(0,Setting.block_size))


        # hiện thông báo xác nhận lưu hay không
        if status.actionType == "save":
            notification.draw(screen)
        
    else:

        # kiểm tra xem có thay đổi gì không 
        # nếu không thoát luôn 
        # nếu có hiện thông báo xác nhận có lưu lại không
        if status.haveChange == True:
            # thông báo có lưu lại dữ liệu không trước khi thoát
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mousePos = pygame.mouse.get_pos()
                    if(notification.checkClick(mousePos,status,objectGroups)):
                        running = False
            notification.draw(screen)
        else:
            running = False
    pygame.display.update()