from pygame import Rect

class Block():
    def __init__(self,x,y,width,height,index,name):
        self.rect = Rect(x,y,width,height)
        self.index = index
        self.blockName = name
   
    