import System.Func as Func
import System.Setting as Setting
import System.Object as Object
import pygame

listGrass = ["Grass", "GrassPink", "Desert", "Snow"]

class Action:
    def __init__ (self,objectGroups):
        self.objectGroups = objectGroups

    def handleShiftBlock(self,mousePos,status):
        if status.objSelected != None:
            status.objSelected.updatePos(mousePos,status)
            status.haveChange = True

    def handleRemoveBlock(self,mousePos,status):
        mousePoint = Func.getPoint(mousePos,status.offset_x,status.offset_y)
        mouseRealPosition = Func.getRealPosition(mousePos,status.offset_x,status.offset_y)
        for obj in self.objectGroups:
            if obj.rect.collidepoint(mouseRealPosition):
                if status.mouseCollision == "mask" and obj.mask.get_at((mouseRealPosition[0]-obj.rect.x,mouseRealPosition[1]-obj.rect.y)) == 0: continue
                if obj.type in listGrass:
                    self.handleRemoveGrass(mousePoint)
                
                self.objectGroups.remove(obj)
                status.haveChange = True
                return

    def handleEditBlock(self,mousePos,type,status):
        pos = Func.getRealPosition(mousePos,status.offset_x,status.offset_y)
        for obj in self.objectGroups:
            if obj.rect.collidepoint(pos):
                if status.mouseCollision == "mask" and obj.mask.get_at((pos[0]-obj.rect.x,pos[1]-obj.rect.y)) == 0: continue
                if obj.type == type:
                    return
            
                if type == "character":
                    self.handleOnlyCharacter()
                if type in listGrass:
                    obj.updateIndex(self.handleIndexAddGrass(pos,type))
                if obj.type in listGrass:
                    self.handleRemoveGrass(pos)
                    
                obj.updateType(type,status.indexBlock)
                status.haveChange = True
                return
        
    def handleAddBlock(self,mousePos,type,status):
        if type == None: return
        pos = Func.getPoint(mousePos,status.offset_x,status.offset_y)
        
        for obj in self.objectGroups:
            if obj.rect.collidepoint(Func.getPoint(mousePos,status.offset_x,status.offset_y)) and not (Setting.blockSetting[type]["overload"] or Setting.blockSetting[obj.type]["overload"]):
                # if obj.mask.get_at((pos[0]-obj.rect.x,pos[1]-obj.rect.y)) == 1:
                    return

        newObj = Object.Object(pos,type)

        if type == "character":
            self.handleOnlyCharacter()

        if type in listGrass:  
            index = self.handleIndexAddGrass(pos,type)  
            newObj.updateIndex(index)
            
        if newObj != None:
            self.objectGroups.add(newObj)
            if Setting.blockSetting[type]["indexChange"] == True:
                newObj.updateIndex(status.indexBlock)

            status.haveChange = True
                
    # grass có bốn loại hình ảnh (cỏ bên trái "grass-0",chỉ có có phía trên "grass-1", cỏ bên phải "grass-2", không có cỏ "grass-3")
    # nếu vị trí phía TRÊN có tồn tại 1 grass khác thì hình ảnh sẽ là KHÔNG CÓ CỎ
    # nếu vị trí BÊN TRÁI và BÊN PHẢI đều có 1 grass khác thì hình ảnh sẽ là CHỈ CÓ CỎ Ở TRÊN
    # nếu chỉ tồn tại 1 bên có grass:
    #   # nếu là BÊN TRÁI thì hình ảnh sẽ là CÓ CỎ BÊN PHẢI
    #   # nếu là BÊN PHẢI thì hình ảnh sẽ là CÓ CỎ BÊN TRÁI

    # khi thêm grass phải check xem có grass xung quanh hay không để chuyển về loại hợp lí
    # đồng thời chuyển cả những grass xung quanh đó về loại hợp lí
    def handleIndexAddGrass(self,pos,type):
        top = [pos[0],pos[1]-Setting.block_size]
        bottom = [pos[0],pos[1]+Setting.block_size]
        left = [pos[0]-Setting.block_size,pos[1]]
        right = [pos[0]+Setting.block_size,pos[1]]
        
        topExist = False
        leftExist = False
        rightExist = False

        for obj in self.objectGroups:
            if obj.type in listGrass:
                if obj.pos == top:
                    topExist = True
                if obj.pos == bottom:
                    obj.updateIndex(3)
                if obj.pos == left:
                    leftExist = True
                    if obj.index != 3:
                            # nếu nó là grass CÓ CỎ BÊN PHẢI thì chắc chắn bên trái nó đã có 1 grass nên chuyển về loại chỉ CÓ CỎ PHÍA TRÊN
                        if obj.index == 2:
                            obj.updateIndex(1)
                        # nếu nó là grass chỉ CÓ CỎ PHÍA TRÊN thì chắc chắn bên trái nó không có grass nào nên chuyển về loại chỉ CÓ CỎ BÊN TRÁI
                        else:
                            obj.updateIndex(0)
                if obj.pos == right:
                    rightExist = True
                    if obj.index != 3:
                        if obj.index == 0:
                            obj.updateIndex(1)
                        else:
                            obj.updateIndex(2)

            elif obj.type == "block":
                if obj.pos == top:
                    topExist = True
                if obj.pos == left:
                    leftExist = True
                if obj.pos == right:
                    rightExist = True


        if topExist == True:
            return 3
        elif leftExist == True and rightExist == False:
            return 2
        elif leftExist == False and rightExist == True:
            return 0
        else:
            return 1

        
    def handleRemoveGrass(self,pos):
        bottom = [pos[0],pos[1]+Setting.block_size]
        left = [pos[0]-Setting.block_size,pos[1]]
        right = [pos[0]+Setting.block_size,pos[1]]

        for obj in self.objectGroups:
            if obj.type in listGrass:
                if obj.pos == bottom:
                    obj.updateIndex(1)
                    pleft = [bottom[0] - Setting.block_size,bottom[1]]
                    pright = [bottom[0] + Setting.block_size,bottom[1]]
                    ileft = self.checkExist(pleft,obj.type)
                    iright = self.checkExist(pright,obj.type)
                    if ileft!=None and iright !=None:
                        obj.updateIndex(1)
                    elif ileft!=None and iright ==None:
                        obj.updateIndex(2)
                    elif ileft==None and iright !=None:
                        obj.updateIndex(0)
                    
                if obj.pos == left:
                    if obj.index != 3:
                        if obj.index == 0:
                            obj.updateIndex(1)
                        else:
                            obj.updateIndex(2)

                if obj.pos == right:
                    if obj.index != 3:
                        if obj.index == 2:
                            obj.updateIndex(1)
                        else:
                            obj.updateIndex(0)

    # chỉ cho phép có một vị trí của nhân vật
    def handleOnlyCharacter(self):
        obj = self.checkExistChar(None,"character")
        if obj != None:
            self.objectGroups.remove(obj)

    def checkExistChar(self,pos,type):
        for obj in self.objectGroups:
            if obj.type == type:
                if pos == None:
                    return obj
                elif obj.pos == pos:
                    return obj
        return None
    
    # ham kiểm tra tại vị trí này có tồn tại block không / hay có tồn tại block có cùng loại hay không
    def checkExist(self,pos,type):
        for obj in self.objectGroups:
            if obj.type in listGrass:
                if pos == None:
                    return obj
                elif obj.pos == pos:
                    return obj
        return None
    

    def handleMouseClick(self,mousePos,status):
        mousePosition = Func.getRealPosition(mousePos,status.offset_x,status.offset_y)
        if (status.actionType=="add"):
            self.handleAddBlock(mousePos,status.blockType,status)
        if (status.actionType=="shift"):
            for obj in self.objectGroups:
                if obj.rect.collidepoint(mousePosition) and Setting.blockSetting[obj.type]["shift"] == True:
                    if status.mouseCollision == "mask" and obj.mask.get_at((mousePosition[0]-obj.rect.x,mousePosition[1]-obj.rect.y)) == 0: continue
                    status.objSelected = obj
                    status.shift_x_cursor = obj.pos[0] - mousePosition[0]
                    status.shift_y_cursor = obj.pos[1] - mousePosition[1]
                    break
        elif(status.actionType=="edit"):
            self.handleEditBlock(mousePos,status.blockType,status)
        elif(status.actionType=="delete"):
            self.handleRemoveBlock(mousePos,status)

    def hanldeMouseMotion(self,mousePos,status):
        if status.actionType == "move":
            status.offset_x += (mousePos[0] - status.preMousePos[0])
            status.offset_y += (mousePos[1] - status.preMousePos[1])
            status.preMousePos = mousePos
        elif(status.actionType=="add"):
            self.handleAddBlock(mousePos,status.blockType,status)
        elif(status.actionType=="shift"):
            self.handleShiftBlock(mousePos,status)
        elif(status.actionType=="edit"):
            self.handleEditBlock(mousePos,status.blockType,status)
        elif(status.actionType=="delete"):
            self.handleRemoveBlock(mousePos,status)