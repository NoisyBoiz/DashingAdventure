from Interact import Button,InputBox
from System import Constant

class JoinRoom:
    def __init__(self,x,y,width,height):
        self.interactInit(width,height)
        
    def interactInit(self,width,height):
        buttonWidth = 200
        buttonHeight = 50
        gap = 10
        top = (height - buttonHeight*4 - gap*2)//2
        self.createNewRoom = Button.Button("Create New Room", (width - buttonWidth)//2,top,buttonWidth,buttonHeight,4,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.joinRoomBox = InputBox.Text("Room ID",(width - buttonWidth)//2,top + buttonHeight*2,buttonWidth,buttonHeight)
        self.joinRoom = Button.Button("Join In Room", (width - buttonWidth)//2,top + buttonHeight*3+gap,buttonWidth,buttonHeight,4,(255, 120, 90),(250, 240, 228),(255, 255, 255))
        self.backButton = Button.Button("Back",10, Constant.Screen_Height - 60,150,50,4,(255, 120, 90),(250, 240, 228),(255, 255, 255))

    def resize(self,width,height):
        buttonWidth = 200
        buttonHeight = 50
        gap = 10
        top = (height - buttonHeight*4 - gap*2)//2
        self.createNewRoom.resize((width-200)//2, top ,buttonWidth,buttonHeight)
        self.joinRoomBox.resize((width - buttonWidth)//2, top + buttonHeight*2 ,buttonWidth,buttonHeight)
        self.joinRoom.resize((width-buttonWidth)//2, top + buttonHeight*3 + gap,buttonWidth,buttonHeight)
        self.backButton.resize(10, Constant.Screen_Height - 60,150,buttonHeight)

    def checkClick(self,pos):
        if self.createNewRoom.rect.collidepoint(pos):
            return "CreateRoom"
        if self.joinRoom.rect.collidepoint(pos) and self.joinRoomBox.text != "":
            return "JoinRoom"
        if self.backButton.rect.collidepoint(pos):
            return "Back"
        return ""
    
    def handle_event(self,event):
        self.joinRoomBox.handle_event(event)

    def draw(self,screen):
        self.joinRoomBox.draw(screen)
        self.joinRoom.draw(screen)
        self.createNewRoom.draw(screen)
        self.backButton.draw(screen)


        