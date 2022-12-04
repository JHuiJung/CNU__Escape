import pygame
import time
import sys


pygame.init()

white = (255, 255, 255)

startImg = pygame.image.load("C:/users/김태연/appdata/roaming/python/python37/site-packages/photo/starticon.png")
startImg = pygame.transform.scale(startImg,(100,100))
quitImg = pygame.image.load("C:/users/김태연/appdata/roaming/python/python37/site-packages/photo/quiticon.png")
quitImg = pygame.transform.scale(quitImg,(100,100))
clickStartImg = pygame.image.load("C:/users/김태연/appdata/roaming/python/python37/site-packages/photo/clickedStartIcon.png")
clickStartImg = pygame.transform.scale(clickStartImg,(100,100))
clickQuitImg = pygame.image.load("C:/users/김태연/appdata/roaming/python/python37/site-packages/photo/clickedQuitIcon.png")
clickQuitImg = pygame.transform.scale(clickQuitImg,(100,100))



gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption("CNU escape")

clock = pygame.time.Clock()



class Button:
    def __init__(self, img_in, x, y, width, height, img_act, x_act, y_act, action = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + width > mouse[0] > x and y + height < mouse[1] > y:
            gameDisplay.blit(img_act,(x_act, y_act))
            if click[0] and action != None:
                time.sleep(1)
                action()
        else:
            gameDisplay.blit(img_in,(x,y))

def quitgame():
    pygame.quit()
    sys.exit()


def mainmenu():

    menu = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        gameDisplay.fill(white)
        
        font = pygame.font.Font(None,100)
        text = font.render("CNU escape",True,(28,0,0))
        gameDisplay.blit(text, (200,130))

        startButton = Button(startImg,240,400,60,20,clickStartImg,238,400,None)
        quitButton = Button(quitImg,500,400,60,20,clickQuitImg,498,400,quitgame)
        pygame.display.update()
        clock.tick(15)
        

mainmenu()
game_loop()
