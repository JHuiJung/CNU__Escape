import pygame
import random

class Player(pygame.sprite.Sprite):
    # 플레이어 이미지 로딩 및 설정 함수
    def __init__(self):
        super().__init__()
        self.playstatus = "nomal"
        
        # 플레이어 사진 불러오기
        self.image = pygame.image.load('images/player/1.png')
        # 이미지 크기의 직사각형 모양 불러오기
        self.image = pygame.transform.scale(self.image, (88,96))
        self.rect = self.image.get_rect()
        # rec 크기 축소(충돌판정 이미지에 맞추기 위함)
        self.rect = self.rect.inflate(-20,-20)
        print("플레이어: ",self.rect)
        # 이미지 시작 위치 설정
        self.rect.center = (100, 450)

class Enemy(pygame.sprite.Sprite):
    # 플레이어 이미지 로딩 및 설정 함수
    def __init__(self):
        super().__init__()
        #적 속도
        self.speed = 5
        
        #랜덤 적 0 : 엎드려 , 1: 공격, 2:방어
        enemynum = random.randint(0, 2) 
        
        if enemynum == 0: # 엎드려야하는 적
            self.image = pygame.image.load('images/enemy/enemy_bow.png')
            
        elif enemynum == 1: # 공격해야하는 적 
            self.image = pygame.image.load('images/enemy/enemy_attack.png')
            
        elif enemynum == 2: # 방어해야하는 적
            self.image = pygame.image.load('images/enemy/enemy_defense.png')
        
        # 이미지 크기의 직사각형 모양 불러오기
        self.image = pygame.transform.scale(self.image, (88,96))
        self.rect = self.image.get_rect()
        # rec 크기 축소(충돌판정 이미지에 맞추기 위함)
        self.rect = self.rect.inflate(-20,-20)
        print("플레이어: ",self.rect)
        # 이미지 시작 위치 설정
        self.rect.center = (800, 450)
    
    def __del__(self):
        global onEnemy
        onEnemy = False
    
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

bg = pygame.image.load("images/BackGround_Test.png")

#화면 타이틀 설정
pygame.display.set_caption("CNU ESCAPE")

EnemySpawnCounter = 2;
spawntime = 2
counter, text = 30, '30'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 70)

play = True

p = Player()
e = Enemy()
onEnemy = True

while play:
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT: 
            counter -= 1
            EnemySpawnCounter -= 1
            if counter >0:
                text = str(counter).rjust(3)
            elif counter < -10:
                text = 'VICTORY'
                play = False
            else:
                text = 'Boss!'
                e.setEnemySpeed(20)
             
        if event.type == pygame.QUIT:
            play = False
        
        
    screen.blit(bg,(0,0))
    screen.blit(font.render(text, True, (0, 0, 0)), (320, 50))
    screen.blit(p.image,p.rect)
    screen.blit(e.image, e.rect)
    
    e.enemymove()
    if e.rect.x < 0:
        randomspeed = random.randint(5, 10)
        e.deleteself()
        e = Enemy()
        e.setEnemySpeed(randomspeed)
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()

