from pygame import KEYDOWN, K_RETURN
from pygame.draw import rect
from Interact import InputBox
from System import Font

class Message:
    def __init__(self,x,y,width,height):
        self.rect = (x,y,width,height)
        self.inputWidth = 200
        self.inputHeight = 40
        self.input = InputBox.Text("Chat", 10, height - self.inputHeight - 10, self.inputWidth, self.inputHeight)

    def resize(self,width,height):
        self.input.resize(10, height - self.inputHeight - 10, self.inputWidth, self.inputHeight)

    def handle_event(self,event,dataClass):
        if event.type == KEYDOWN:
            if event.key == K_RETURN and self.input.text != "":
                dataClass.message = self.input.text
                self.input.resetAll()
    
        self.input.handle_event(event)

    def draw(self,screen):
        self.input.draw(screen)


def drawMessage(screen,offset_x,offset_y,player):
    if player.message != None:
        string = player.message.split(" ")
       
        arrText = []
        ms = ""
        textRect = None
        for i in string:
            if len(ms) > 20:
                txt = Font.Arial20.render(ms, True, (0,0,0))
                arrText.append(txt) 
                if textRect == None:
                    textRect = txt.get_rect()
                else:
                    textRect.width = max(textRect.width,txt.get_rect().width)
                ms = ""
            ms += i + " "
       
        if ms != "":
            txt = Font.Arial20.render(ms, True, (0,0,0))
            arrText.append(txt)
            if textRect == None:
                textRect = txt.get_rect()
            else:
                textRect.width = max(textRect.width,txt.get_rect().width)

        x = player.rect.x - offset_x + player.rect.width//2 - textRect.width//2
        y = player.rect.y - offset_y - player.rect.height - textRect.height*len(arrText)
        rect(screen, (255, 255, 255), (x - 10,y - 10,textRect.width + 20,textRect.height*len(arrText) + 20))
        rect(screen, (0, 0, 0), (x - 10,y - 10,textRect.width + 20,textRect.height*len(arrText) + 20),2)
        for i in range(len(arrText)):
            screen.blit(arrText[i],(x,y + i*textRect.height))
        