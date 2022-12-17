import pygame
import random
import cv2
from pathlib import Path
import numpy as rp

#속도 조정 FPS=게임 내 프레임, countTime : 카운트 감소 시간 1000 = 1초
FPS = 30
countTime = 2000
WHITE = (255,255,255)
BLACK = (0,0,0)

def draw_text(text, size, color, x, y):
    global screen
    font = pygame.font.SysFont('Consolas', size)
    text_surface = font.render(text, True, color,(255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def wait_for_key():
    global screen
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                waiting = False

def show_start_screen():
    global screen,bg
        # game splash/start screen
    screen.fill(WHITE)
    draw_text("CNU ESCAPE!!", 48, BLACK,screen_width /2, screen_height/4)
    draw_text(": Home From University",22, BLACK, screen_width /2, screen_height/4 + 50)
    draw_text("Press a key to play", 22, BLACK, screen_width /2, screen_height* 3/4)
    pygame.display.flip()
    wait_for_key()
    
def show_defeat_screen():
    global screen,bg,play
        # game splash/start screen
    bg = pygame.image.load("images/강의실.jpg")
    bg = pygame.transform.scale(bg, (screen_width,screen_height))
    screen.blit(bg,(0,0))
    draw_text("ESCAPE!! Fail", 48, BLACK,screen_width /2, screen_height/4)
    draw_text("Press a key to Exit", 22, BLACK, screen_width /2, screen_height* 3/4)

    pygame.display.flip()
    wait_for_key()
    play= False
    
def show_Victory_screen():
    global screen,bg,play
        # game splash/start screen
    bg = pygame.image.load("images/집.jpg")
    bg = pygame.transform.scale(bg, (screen_width,screen_height))
    screen.blit(bg,(0,0))
    draw_text("ESCAPE!! Success!!", 48, BLACK,screen_width /2, screen_height/4)
    draw_text("Press a key to Exit", 22, BLACK, screen_width /2, screen_height* 3/4)

    pygame.display.flip()
    wait_for_key()
    play= False

class Player(pygame.sprite.Sprite):
    # 플레이어 이미지 로딩 및 설정 함수
    def __init__(self):
        super().__init__()
        self.playerStatus = "nomal"
        self.playerHP = 3;
        self.boolDamged = False
        self.damgedCnt = 0
        
        # 플레이어 사진 불러오기
        self.image = pygame.image.load('images/player/nomal1.png')
        
        # 이미지 크기의 직사각형 모양 불러오기
        self.image = pygame.transform.scale(self.image, (88,96))
        self.rect = self.image.get_rect()
        # rec 크기 축소(충돌판정 이미지에 맞추기 위함)
        self.rect = self.rect.inflate(-20,-20)
        # 이미지 시작 위치 설정
        self.rect.center = (100, 500)
    
        #애니메이션용 리스트
        self.nomalAnimation = [pygame.image.load('images/player/nomal1.png'),pygame.image.load('images/player/nomal2.png')\
                              ,pygame.image.load('images/player/nomal3.png'),pygame.image.load('images/player/nomal4.png')\
                              ,pygame.image.load('images/player/nomal5.png'),pygame.image.load('images/player/nomal6.png')\
                              ,pygame.image.load('images/player/nomal7.png'),pygame.image.load('images/player/nomal8.png')\
                              ,pygame.image.load('images/player/nomal9.png'),pygame.image.load('images/player/nomal10.png')\
                              ,pygame.image.load('images/player/nomal11.png')]
    #플레이어 상태 변경 멤버함수
    def setPlayerStatus(self,status = "nomal"):
        self.playerStatus = status
        if status == "bow":
            self.image = pygame.image.load('images/player/bow.png')
            self.image = pygame.transform.scale(self.image, (88,48))
            self.rect.centery = 550
          
        elif status == "defense":
            self.image = pygame.image.load('images/player/defense.png')
            self.image = pygame.transform.scale(self.image, (88,96))
        elif status == "attack":
            self.image = pygame.image.load('images/player/attack.png')
            self.image = pygame.transform.scale(self.image, (120,96))
        else:
            self.rect.centery = 500
            self.image = pygame.image.load('images/player/nomal1.png')
            self.image = pygame.transform.scale(self.image, (88,96))
    
    def isDamaged(self):
        if self.boolDamged == True:
            if self.damgedCnt >= 8:
                self.damgedCnt = 0
                self.boolDamged = False
            self.rect.x -= 5
            self.damgedCnt +=1

class Enemy(pygame.sprite.Sprite):
    # 플레이어 이미지 로딩 및 설정 함수
    def __init__(self):
        super().__init__()
        
        #적 속도
        self.speed = 60
        self.enemytype =""
        
        #랜덤 적 0 : 엎드려 , 1: 공격, 2:방어
        enemynum = random.randint(0, 2) 
        
        
        if enemynum == 0: # 엎드려야하는 적
            self.image = pygame.image.load('images/enemy/enemy_bow.png')
            self.enemytype = "bow";
        elif enemynum == 1: # 공격해야하는 적 
            self.image = pygame.image.load('images/enemy/enemy_attack.png')
            self.enemytype = "attack"
        elif enemynum == 2: # 방어해야하는 적
            self.image = pygame.image.load('images/enemy/enemy_defense.png')
            self.enemytype = "defense"
        # 이미지 크기의 직사각형 모양 불러오기
        self.image = pygame.transform.scale(self.image, (88,96))
        self.rect = self.image.get_rect()
        # rec 크기 축소(충돌판정 이미지에 맞추기 위함)
        self.rect = self.rect.inflate(-20,-20)
        # 이미지 시작 위치 설정
        self.rect.center = (800, 500)
    
    def __del__(self):
        print("공격물체 객체 소멸")
    
    def enemymove(self):
        self.rect.x -= self.speed
        
    def setEnemySpeed(self, speed):
        self.speed = speed
    
    def deleteself(self):
        del self
        
BODY_PARTS = { "Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14,
                "Background": 15 }

POSE_PAIRS = [ ["Head", "Neck"], ["Neck", "RShoulder"], ["RShoulder", "RElbow"],
                ["RElbow", "RWrist"], ["Neck", "LShoulder"], ["LShoulder", "LElbow"],
                ["LElbow", "LWrist"], ["Neck", "Chest"], ["Chest", "RHip"], ["RHip", "RKnee"],
                ["RKnee", "RAnkle"], ["Chest", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"] ]                

    
# 각 파일 path
protoFile = "pose_deploy_linevec_faster_4_stages.prototxt"
weightsFile= "pose_iter_160000.caffemodel"

net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

capture = cv2.VideoCapture(0) 

inputWidth=320
inputHeight=240
inputScale=1.0/255

pygame.init() #초기화

clock = pygame.time.Clock() #시계 설정

screen_width = 800 #가로 크기
screen_height = 600 #세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

bg = pygame.image.load("images/공대7호관.jpg")
bg = pygame.transform.scale(bg, (screen_width,screen_height))

#화면 타이틀 설정
pygame.display.set_caption("CNU ESCAPE")

boss = pygame.image.load("images/교수님.png")
boss = pygame.transform.scale(boss, (88,96))

counter, text = 30, '30'
nomalAnimatonCount =0

pygame.time.set_timer(pygame.USEREVENT, countTime)
font = pygame.font.SysFont('Consolas', 70)
font2 = pygame.font.SysFont('Consolas', 20)


play = True

p = Player()
e = Enemy()
onEnemy = True

show_start_screen()


while play:
     exe = 99
     hasFrame, frame = capture.read()  
     if not hasFrame:
        cv2.waitKey()
        break

     frameWidth = frame.shape[1]
     frameHeight = frame.shape[0]
    
     inpBlob = cv2.dnn.blobFromImage(frame, inputScale, (inputWidth, inputHeight), (0, 0, 0), swapRB=False, crop=False)
     
     imgb=cv2.dnn.imagesFromBlob(inpBlob)
    
     net.setInput(inpBlob)

     output = net.forward()

     points = []
     for i in range(0,15):
        probMap = output[0, i, :, :]
    
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

        x = (frameWidth * point[0]) / output.shape[3]
        y = (frameHeight * point[1]) / output.shape[2]

        if prob > 0.1 :    
            cv2.circle(frame, (int(x), int(y)), 3, (0, 255, 255), thickness=-1, lineType=cv2.FILLED) # circle(그릴곳, 원의 중심, 반지름, 색)
            cv2.putText(frame, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, lineType=cv2.LINE_AA)
            points.append((int(x), int(y)))
        else :
            points.append(None)
    
     for pair in POSE_PAIRS:
        partA = pair[0]             # Head
        partA = BODY_PARTS[partA]   # 0
        partB = pair[1]             # Neck
        partB = BODY_PARTS[partB]   # 1
        
        if points[partA] and points[partB]:
            cv2.line(frame, points[partA], points[partB], (0, 255, 0), 2)
    

     if (points[3] is not None) and (points[5] is not None)and(points[6] is not None) and(points[7] is not None):
        point_4 = points[4] #왼쪽 손목
        point_2 = points[2] #왼쪽 어깨
        point_7 = points[7] #오른쪽 손목
        point_5 = points[5] #오른쪽 어깨
        point_3 = points[3] #왼쪽 팔꿈치
        point_6 = points[6] #오른쪽 팔꿈치

        if(point_4[0] < point_7[0] and point_3[1]>point_5[1] and point_6[1] > point_7[1]):
         cv2.putText(frame, "DEFENCE",(0,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
         exe = 1

     if (points[12] is not None) and (points[11] is not None)and(points[9] is not None) and(points[8] is not None): 
        point_11 = points[11] #오른쪽 엉덩이
        point_12 = points[12] #오른쪽 무릎
        point_8 = points[8] #왼쪽 엉덩이
        point_9 = points[9] #왼쪽 무릎
        if(point_12[1] < point_11[1] or point_9[1] < point_8[1]):
         cv2.putText(frame, "ATTACK",(0,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
         exe = 2

     if (points[0] is not None) and (points[2] is not None) and (points[5] is not None):
        point_0 = points[0] #머리
        point_2 = points[2] #왼쪽 어깨        
        point_5 = points[5] #오른쪽 어깨

        if(point_0[1] > point_2[1] ) or (point_0[1] > point_5[1]):
         cv2.putText(frame, "BOW",(0,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
         exe = 3
     cv2.imshow("Output-Keypoints",frame)
     for event in pygame.event.get():
         #30초 카운트 관련 이벤트들
         if event.type == pygame.USEREVENT: 
             counter -= 1
             if counter >0: # 화면에 카운트 숫자를 줄임
                 text = str(counter)
             elif counter < -10: # 30초 후 10초가 더 지나면 나타나는 이벤트
                 show_Victory_screen()
             else:
                 text = 'Boss!' 
                 e.setEnemySpeed(100)
             
             if counter == 15:
                 bg = pygame.image.load("images/시계탑.png")
                 bg = pygame.transform.scale(bg, (screen_width,screen_height))
             elif counter == 0:
                 bg = pygame.image.load("images/후문.jpg")
                 bg = pygame.transform.scale(bg, (screen_width,screen_height))
                 
         #창 종료시 발상하는 이벤트
         if event.type == pygame.QUIT:
             play = False
             
             #캠 연동전 테스트용 이벤트 키보드Q = 엎드리기, 키보드W = 방어, 키보드E = 공격
             
             keys = pygame.key.get_pressed()
             if keys[pygame.K_q]:
                 p.setPlayerStatus("bow")
             elif keys[pygame.K_w]:
                 p.setPlayerStatus("defense")
             elif keys[pygame.K_e]:
                 p.setPlayerStatus("attack")
             else:
                 p.setPlayerStatus("nomal")

         if exe == 1:
             p.setPlayerStatus("defense")
         elif exe ==2:
             p.setPlayerStatus("attack")
         elif exe == 3:    
             p.setPlayerStatus("bow")


    
     #플레이어 체력 0되면 발생하는 이벤트
     if p.playerHP == 0: 
         show_defeat_screen()
     
     #플레이어 와 공격물체 충돌 이벤트
     if pygame.sprite.collide_rect(p, e): #
         if p.playerStatus != e.enemytype:
             p.boolDamged = True
             p.playerHP -=1
         onEnemy = False
         e.deleteself()
     
     #화면에 공격물체가 없을시 생성하는 이벤트
     if onEnemy == False:
         randomspeed = random.randint(50, 70)
         e = Enemy()
         e.setEnemySpeed(randomspeed)
         onEnemy = True
         
     #화면 업데이트
     screen.blit(bg,(0,0))
     screen.blit(font.render(text, True, (0, 0, 0),WHITE), (350, 50))
     screen.blit(font.render("HP : "+str(p.playerHP), True, (0, 0, 0),WHITE), (0, 0))
     screen.blit(p.image,p.rect)
     screen.blit(e.image, e.rect)
     if counter <= 0: #
         screen.blit(boss,(600,450))
         screen.blit(font2.render("Hey Student, Where are you going?", True, (0, 0, 0),WHITE), (430, 400))
     
     e.enemymove()
     if p.playerStatus == "nomal":
         if(nomalAnimatonCount >10): 
             nomalAnimatonCount = 0
         p.image = p.nomalAnimation[nomalAnimatonCount]
         p.image = pygame.transform.scale(p.image, (88,96))

     p.isDamaged()    
     nomalAnimatonCount +=1
     pygame.display.flip()
     clock.tick(FPS)
    

capture.release()
cv2.destroyAllWindows()    
pygame.quit()

