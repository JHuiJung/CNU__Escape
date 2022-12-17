import pygame
import time
import random

class Player(pygame.sprite.Sprite):
    # 플레이어 이미지 로딩 및 설정 함수
    def __init__(self):
        super().__init__()
        self.playerStatus = "nomal"
        self.playerHP = 3;
        
        # 플레이어 사진 불러오기
        self.image = pygame.image.load('images/player/nomal1.png')
        
        # 이미지 크기의 직사각형 모양 불러오기
        self.image = pygame.transform.scale(self.image, (88,96))
        self.rect = self.image.get_rect()
        # rec 크기 축소(충돌판정 이미지에 맞추기 위함)
        self.rect = self.rect.inflate(-20,-20)
        # 이미지 시작 위치 설정
        self.rect.center = (100, 450)
    
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
            self.rect.center = (100,500)
          
        elif status == "defense":
            self.image = pygame.image.load('images/player/defense.png')
            self.image = pygame.transform.scale(self.image, (88,96))
        elif status == "attack":
            self.image = pygame.image.load('images/player/attack.png')
            self.image = pygame.transform.scale(self.image, (120,96))
        else:
            self.rect.center = (100,450)
            self.image = pygame.image.load('images/player/nomal1.png')
            self.image = pygame.transform.scale(self.image, (88,96))
    

class Enemy(pygame.sprite.Sprite):
    # 플레이어 이미지 로딩 및 설정 함수
    def __init__(self):
        super().__init__()
        
        #적 속도
        self.speed = 5
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
        self.rect.center = (800, 450)
    
    def __del__(self):
        print("공격물체 객체 소멸")
    
    def enemymove(self):
        self.rect.x -= self.speed
        
    def setEnemySpeed(self, speed):
        self.speed = speed
    
    def deleteself(self):
        del self
        

pygame.init() #초기화

clock = pygame.time.Clock() #시계 설정

screen_width = 800 #가로 크기
screen_height = 600 #세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

bg = pygame.image.load("images/공대7호관.jpg")
bg = pygame.transform.scale(bg, (screen_width,screen_height))

#화면 타이틀 설정
pygame.display.set_caption("CNU ESCAPE")


counter, text = 30, '30'.rjust(3)
nomalAnimatonCount =0

pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 70)
font2 = pygame.font.SysFont('Consolas', 50)


play = True

p = Player()
e = Enemy()
onEnemy = True


while play:
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
                e.setEnemySpeed(20)
            
            if counter == 15:
                bg = pygame.image.load("images/시계탑.pngw")
                bg = pygame.transform.scale(bg, (screen_width,screen_height))
            elif counter == 0:
                eeeeebg = pygame.image.load("images/후문.jpg")
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
        
        if event.type == pygame.KEYUP:
            p.setPlayerStatus("nomal")
    
    #플레이어 체력 0되면 발생하는 이벤트
    if p.playerHP == 0: 
        play = False
    
    #플레이어 와 공격물체 충돌 이벤트
    if pygame.sprite.collide_rect(p, e): #
        if p.playerStatus != e.enemytype:
            p.playerHP -=1
        onEnemy = False
        e.deleteself()
    
    #화면에 공격물체가 없을시 생성하는 이벤트
    if onEnemy == False:
        randomspeed = random.randint(5, 10)
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
    if p.playerStatus == "nomal":
        if(nomalAnimatonCount >10): 
            nomalAnimatonCount = 0
        p.image = p.nomalAnimation[nomalAnimatonCount]
        p.image = pygame.transform.scale(p.image, (88,96))

    nomalAnimatonCount +=1
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()

