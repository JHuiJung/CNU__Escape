import pygame
import random
import cv2
from pathlib import Path
import numpy as rp

class Player(pygame.sprite.Sprite):
    # 플레이어 이미지 로딩 및 설정 함수
    def __init__(self):
        super().__init__()
        self.playerStatus = "nomal"
        self.playerHP = 3
        
        # 플레이어 사진 불러오기
        self.image = pygame.image.load("C:\CNU__Escape-JHJ\images\player/1.png")
        
        # 이미지 크기의 직사각형 모양 불러오기
        self.image = pygame.transform.scale(self.image, (88,96))
        self.rect = self.image.get_rect()
        # rec 크기 축소(충돌판정 이미지에 맞추기 위함)
        self.rect = self.rect.inflate(-20,-20)
        # 이미지 시작 위치 설정
        self.rect.center = (100, 450)
    
    #플레이어 상태 변경 멤버함수
    def setPlayerStatus(self,status = "nomal"):
        self.playerStatus = status

class Enemy(pygame.sprite.Sprite):
    # 플레이어 이미지 로딩 및 설정 함수
    def __init__(self):
        super().__init__()
        
        #적 속도
        self.speed = 70
        self.enemytype =""
        
        #랜덤 적 0 : 엎드려 , 1: 공격, 2:방어
        enemynum = random.randint(0, 2) 
        
        
        if enemynum == 0: # 엎드려야하는 적
            self.image = pygame.image.load("C:\CNU__Escape-JHJ\images\enemy/enemy_bow.png")
            self.enemytype = "bow"
        elif enemynum == 1: # 공격해야하는 적 
            self.image = pygame.image.load("C:\CNU__Escape-JHJ\images\enemy/enemy_attack.png")
            self.enemytype = "attack"
        elif enemynum == 2: # 방어해야하는 적
            self.image = pygame.image.load("C:\CNU__Escape-JHJ\images\enemy/enemy_defense.png")
            self.enemytype = "defense"
        # 이미지 크기의 직사각형 모양 불러오기
        self.image = pygame.transform.scale(self.image, (88,96))
        self.rect = self.image.get_rect()
        # rec 크기 축소(충돌판정 이미지에 맞추기 위함)
        self.rect = self.rect.inflate(-20,-20)
        # 이미지 시작 위치 설정
        self.rect.center = (800, 450)
    
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
protoFile = "C:\CNU__Escape-JHJ\pose_deploy_linevec_faster_4_stages.prototxt"
weightsFile= "C:\CNU__Escape-JHJ\pose_iter_160000.caffemodel"

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

bg = pygame.image.load("C:\CNU__Escape-JHJ\images\BackGround_Test.png")

#화면 타이틀 설정
pygame.display.set_caption("CNU ESCAPE")


counter, text = 30, '30'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 70)
font2 = pygame.font.SysFont('Consolas', 50)


play = True

p = Player()
e = Enemy()
onEnemy = True


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
                text = str(counter).rjust(3)
            elif counter < -10: # 30초 후 10초가 더 지나면 나타나는 이벤트
                text = 'VICTORY'
                play = False
            else:
                text = 'Boss!' 
                e.setEnemySpeed(100)
                
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

        if exe == 1:
            p.setPlayerStatus("defense")
        elif exe ==2:
            p.setPlayerStatus("attack")
        elif exe == 3:    
            p.setPlayerStatus("bow")


    
    #플레이어 체력 0되면 발생하는 이벤트
     if p.playerHP == 0: 
        play = False
        #break
    
    #플레이어 와 공격물체 충돌 이벤트
     if pygame.sprite.collide_rect(p, e): #
        if p.playerStatus != e.enemytype:
            p.playerHP -=1
        onEnemy = False
        e.deleteself()
    
    #화면에 공격물체가 없을시 생성하는 이벤트
     if onEnemy == False:
        randomspeed = random.randint(50, 100)
        e = Enemy()
        e.setEnemySpeed(randomspeed)
        onEnemy = True
        
    #화면 업데이트
     screen.blit(bg,(0,0))
     screen.blit(font.render(text, True, (0, 0, 0)), (320, 50))
     screen.blit(font2.render("HP : "+str(p.playerHP), True, (0, 0, 0)), (0, 550))
     screen.blit(p.image,p.rect)
     screen.blit(e.image, e.rect)
    
     e.enemymove()

        
     pygame.display.flip()
     clock.tick(60)
    

capture.release()
cv2.destroyAllWindows()    
pygame.quit()

