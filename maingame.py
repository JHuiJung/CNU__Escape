import pygame

class Player(pygame.sprite.Sprite):
    # 플레이어 이미지 로딩 및 설정 함수
    def __init__(self):
        super().__init__()
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

pygame.init() #초기화

clock = pygame.time.Clock() #시계 설정

screen_width = 800 #가로 크기
screen_height = 600 #세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

bg = pygame.image.load("images/BackGround_Test.png")

#화면 타이틀 설정
pygame.display.set_caption("CNU ESCAPE")

counter, text = 30, '30'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 70)

play = True

p = Player()

while play:
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT: 
            counter -= 1
            text = str(counter).rjust(3) if counter > 0 else 'Boss!'
        if event.type == pygame.QUIT:
            play = False
            
    
    screen.blit(bg,(0,0))
    screen.blit(font.render(text, True, (0, 0, 0)), (320, 50))
    screen.blit(p.image,p.rect)
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()