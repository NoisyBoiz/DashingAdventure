import pygame
import System.Setting as Setting
# vẽ các ô trên màn hình
class Ruler:
    def draw(self,screen,offset_x,offset_y):
        shift_x = offset_x%Setting.block_size
        shift_y = offset_y%Setting.block_size
        for i in range(shift_x,Setting.screen_width+shift_x,Setting.block_size):
            # vẽ trục x
            if(i-offset_x==0):
                pygame.draw.line(screen,(255,0,0),(i,0),(i,Setting.screen_height),2)
            else:
                self.drawDrashedLine(screen,i,Setting.screen_height,3,"vertical")
        for j in range(shift_y,Setting.screen_height+shift_y,Setting.block_size):
            # vẽ trục y
            if(j-offset_y==0):
                pygame.draw.line(screen,(255,0,0),(0,j),(Setting.screen_width,j),2)
            else:
                self.drawDrashedLine(screen,j,Setting.screen_width,3,"horizontal")
        
    def drawDrashedLine(self,screen,pos,length,step,direction):
        if direction == "vertical":
            for i in range(0,length,step*3):
                pygame.draw.line(screen,(0,0,0),(pos,i),(pos,i+step))
        else:
            for i in range(0,length,step*3):
                pygame.draw.line(screen,(0,0,0),(i,pos),(i+step,pos))
