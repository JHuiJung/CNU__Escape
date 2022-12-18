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
        

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

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


with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        exe = 99
        ret, frame = cap.read()
        

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)
    
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        try:
            landmarks = results.pose_landmarks.landmark

                    
            p2 = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]#왼어
            p4 = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]#왼손
            p3 = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y] #왼팔    
            p5 = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y] #오어
            p7 = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y] #오손
            p6 = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y] #오팔

            if(p4[0] < p7[0] and p5[1]< p3[1] and p7[1]<p6[1]):
             cv2.putText(image, "DEFENCE",(0,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
             exe = 1
           
            p8 = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            p9 = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            p11 = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            p12 = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

            if(p12[1] < p11[1] or p9[1] < p8[1]):
             cv2.putText(image, "ATTACK",(0,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
             exe = 2



            p0 = [landmarks[mp_pose.PoseLandmark.NOSE.value].x,landmarks[mp_pose.PoseLandmark.NOSE.value].y] #코
            if(p2[1] < p0[1] or p5[1] < p0[1]):
             cv2.putText(image, "BOW",(0,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
             exe=3



        except:
            pass

  
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


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
         break
    
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
 


    cap.release()
    cv2.destroyAllWindows() 
    pygame.quit()


    