import pygame
import System.Setting as Setting


# thanh công cụ
class Menu:
    def __init__(self):

        self.listAction = ["save","move","shift","add","edit","delete"]
        self.listKeyAction = ["S","Q","W","A","E","X"]
        self.rectAction = pygame.Rect(0,0,Setting.block_size*len(self.listAction),Setting.block_size)
        self.listRectAction = []
        
        self.listBlock = []
        self.listKeyBlock = []
        self.rectBlock = pygame.Rect((Setting.block_size*len(self.listAction)+1),0,Setting.screen_width-Setting.block_size*len(self.listAction),Setting.block_size)

        self.listRectBlock = []
        self.listIndexBlock = []

        # giới hạn hiển thị block trên thanh 
        self.pageBlock = 0
        self.limitPageBlock = Setting.screen_width//Setting.block_size - len(self.listAction)
        
        self.shift_x_icon = (Setting.block_size - Setting.blockIcon_size)//2
        self.shift_y_icon = (Setting.block_size - Setting.blockIcon_size)//2

        self.font = pygame.font.SysFont("Arial",20,bold=True)
        self.textKeyAction = []
        self.textKeyBlock = []

        self.getListBlock()
        self.initRectIcon()
        self.getIndexBlock()
        self.initTextKey()
    def resize(self):
        self.rectBlock = pygame.Rect((Setting.block_size*len(self.listAction)+1),0,Setting.screen_width-Setting.block_size*len(self.listAction),Setting.block_size)
        self.limitPageBlock = Setting.screen_width//Setting.block_size - len(self.listAction)
        self.listRectAction.clear()
        self.listRectBlock.clear()
        self.initRectIcon()
    def getListBlock(self):
        for i,key in enumerate(Setting.imageBlock):
            self.listBlock.append(key)
            self.listKeyBlock.append(chr(ord("1")+i))
            
    def getIndexBlock(self):
        for i in range(len(Setting.blockSetting)):
            self.listIndexBlock.append(0)

        for i,key in enumerate(Setting.blockSetting):
            self.listIndexBlock[i] = Setting.blockSetting[key]["defaultIndex"]

    # tính tọa độ để vẽ các icon
    def initRectIcon(self):
        for i in range(len(self.listAction)):
            self.listRectAction.append((i*Setting.block_size,0,Setting.block_size,Setting.block_size))

        shift_x = len(self.listAction)*Setting.block_size
        for i in range(len(self.listBlock)):
            self.listRectBlock.append((i%self.limitPageBlock*Setting.block_size+shift_x,0,Setting.block_size,Setting.block_size))

    def initTextKey(self):
        for i in self.listKeyAction:
            text = self.font.render(i,True, (255, 36, 66))
            self.textKeyAction.append(text)

        for i in self.listKeyBlock:
            text = self.font.render(i,True, (255, 36, 66))
            self.textKeyBlock.append(text)

    # phím tắt
    def checkPressKey(self,key,status):
        for i,k in enumerate(self.listKeyAction):
            if key == ord(k.lower()) or key == ord(k):
                status.actionType = self.listAction[i]
                return
            
        for i,k in enumerate(self.listKeyBlock):
            if key == ord(k):
                status.blockType = self.listBlock[i]
                return
   
    def handleClick(self,mousePos,status):
        # check chọn loại hành động (save,move,edit,delete)
        for i,rect in enumerate(self.listRectAction):
            if rect[0] <= mousePos[0] <= rect[0]+rect[2] and rect[1] <= mousePos[1] <= rect[1]+rect[3]:
                status.actionType = self.listAction[i]
                return 
            
        # check chọn loại block
        for i,rect in enumerate(self.listRectBlock):
            if rect[0] <= mousePos[0] <= rect[0]+rect[2] and rect[1] <= mousePos[1] <= rect[1]+rect[3]:
                status.blockType = self.listBlock[i]
                status.indexBlock = self.listIndexBlock[i]
                return 

    def checkChangeIndexBlock(self,status):
        if Setting.blockSetting[status.blockType]["indexChange"] == True:
            i = self.listBlock.index(status.blockType)
            self.listIndexBlock[i] += 1
            if self.listIndexBlock[i] >= Setting.limitIndexBlock[self.listBlock[i]]:
                self.listIndexBlock[i] = 0
            status.indexBlock = self.listIndexBlock[i]
               
    def draw(self,screen,status):
        pygame.draw.rect (screen,(96, 150, 180),(self.rectAction))
        pygame.draw.rect (screen,(234, 199, 199),(self.rectBlock))
        for i in range(Setting.screen_width//Setting.block_size):
            pygame.draw.rect(screen,(0,0,0),(i*Setting.block_size,0,Setting.block_size,Setting.block_size),1)
    
        for i,action in enumerate(self.listRectAction):
            screen.blit(Setting.imageAction[self.listAction[i]],(action[0]+self.shift_x_icon,action[1]+self.shift_y_icon))
            if status.actionType == self.listAction[i]:
                pygame.draw.rect(screen,(199, 0, 57),(action[0],action[1],action[2],action[3]),6)
            screen.blit(self.textKeyAction[i],(action[0]+2,action[1]-3))

        for i,block in enumerate(self.listRectBlock):
            screen.blit(Setting.imageBlockIcon[self.listBlock[i]][self.listIndexBlock[i]],(block[0]+self.shift_x_icon,block[1]+self.shift_y_icon))
            if status.blockType == self.listBlock[i]:
                pygame.draw.rect(screen,(150, 210, 20),(block[0],block[1],block[2],block[3]),6)
            screen.blit(self.textKeyBlock[i],(block[0]+2,block[1]-3))