import pygame

class Player(pygame.sprite.Sprite):
    # 플레이어 이미지 로딩 및 설정 함수
    def __init__(self):
        super().__init__()
        # 플레이어 사진 불러오기
        self.image = pygame.image.load('C:/Users/195338/Desktop/CNU_ESCAPE/CNU__Escape/images/player/1.png')
        # 이미지 크기의 직사각형 모양 불러오기
        self.rect = self.image.get_rect()
        # rec 크기 축소(충돌판정 이미지에 맞추기 위함)
        self.rect = self.rect.inflate(-20,-20)
        print("플레이어: ",self.rect)
        # 이미지 시작 위치 설정
        self.rect.center = (540, 390)

pygame.init() #초기화

screen_width = 800 #가로 크기
screen_height = 600 #세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill((255,153,153))

#화면 타이틀 설정
pygame.display.set_caption("CNU ESCAPE")


play = True

p = Player()

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
            
            
            
pygame.quit()