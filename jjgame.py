# [프로그래밍기초와실습] - 기말고사 개인별 미니프로젝트 
#
# ------------------------------------------------------
#                     2022-12-12(월)
#
#                   202292022 - 문강빈
#
# ------------------------------------------------------
import pygame
import sys
import random

pygame.init()                                                                       # 초기화
screen_width = 500
screen_height = 300                                                                 # 화면 크기
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("[기말고사] Jummping Nemo - 202292022 문강빈")            # 게임 이름

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
#pygame.mixer.init()
#pygame.mixer.music.load("C:/Users/Administrator/Documents/카카오톡 받은 파일/종합만~1/종합 만드는 중/Secret_Laboratory.mp3")
#pygame.mixer.music.play(-1)                                                        # 노래 - 저작권 없는 자작 BGM - Secret_Laboratory
  
class Nemo(pygame.sprite.Sprite):                                                  # nemo 클래스 설정 [Class 앞에는 무조권 대문자]
    def __init__(self, width, height, color) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((width,height), pygame.SRCALPHA).convert_alpha()
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.vel = 0
        self.clicked = False                                                       # Jump = 마우스
        self.jump_cnt = 0 

    def update(self):
        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            if self.jump_cnt < 2:                                                  # 최대 연속 2번의 점프까지 가능
                self.vel = -15                                                     # 점프 높이
                self.jump_cnt += 1
         
            
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.vel += 1                                                              # 1 씩 아래로 떨어진다
        if self.vel > 10:                                                          # 10 이상 초과 불가능
            self.vel = 10
        
        if self.rect.bottom <= screen_height :
            self.rect.y += int(self.vel) 
            if self.rect.y >= screen_height - self.rect.height:                    # Nemo 윗 부분이 바닥에서 올라온곳
                self.rect.y = screen_height - self.rect.height
                self.jump_cnt = 0                                                  # 바닥에 떨어지면 점프횟수 초기화

class Obstacle(pygame.sprite.Sprite):                                              # 클래스 장애물 설정
    def __init__(self, width, height, color) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((width,height), pygame.SRCALPHA).convert_alpha() 
                                                                                   # 장애물인 삼각형 만들기
        pt = [(width/2, 0), (0,height),(width,height)]
        pygame.draw.polygon(self.image, color, pt)
        
        self.rect = self.image.get_rect()
        self.vel = 4                                                               # 속도 4
        self.rect.x = screen_width                                                 # 오른쪽에서 Nemo쪽으로 이동
        self.rect.y = screen_height - self.rect.height
        
        if score <= 5:                                                             # 난이도 설정
            self.vel = 4
        elif score <= 10:
            self.vel = 5
        elif score <= 15:                                                          # [간략히] 스코어 n 달성시 난이도 변화
            self.vel = 7                                                           # 점점 빨라지다가 중간에 다시 느려지기도 하며 난이도 조절
        elif score <= 24:
            self.vel = 10
        elif score <= 25:
            self.vel = 9
        elif score <= 35:
            self.vel = 6
        elif score <= 40:
            self.vel = 9
        elif score <= 50:
            self.vel = 11
        elif score <= 60:
            self.vel = 13
        else:
            self.vel = 15
            
        
    def update(self):
        self.rect.x -= int(self.vel)
    
    def check_screen_out(self):                                                    # 화면 밖으로 나가면 점수 획득
        result = False 
        if self.rect.x < 0:
            result = True
        return result

def show_gameover():                                                               # 게임 종료 (Nemo 가 장애물에 부딪칠시)
    global game_over
    game_over = True

    font = pygame.font.SysFont("고딕", 60)
    over_text = font.render(f"Game Over", True, (0,255,255))                      
    screen.blit(over_text, (int(screen_width/2 -  over_text.get_width()/2), int(screen_height/3)))

    font = pygame.font.SysFont("고딕", 30)
    over_text = font.render(f"Replay = SPACE", True, (200,200,255))
    screen.blit(over_text, (int(screen_width/2 -  over_text.get_width()/2), int(screen_height/4*2)))  # Game over, Replay = SPACE 문구 출력

def restart_game():                                                                # 다시 플레이 = SPACE
    global game_over, score
    game_over = False
    obstacles.empty()
    score = 0

def show_score():                                                                  # 게임중 자신의 스코어 
    font = pygame.font.SysFont("고딕", 50)
    score_text = font.render(f"Score : {score}", True, (0,0,0))
    screen.blit(score_text, (0,0))

    if score <= 5:                                                                 # [간략히] 스코어에 비례하여 랭크를 수여
        font = pygame.font.SysFont("고딕", 50)                                     # 스코어 10을 초과할시 D 랭크 / 랭크 변화 시스템
        score_text = font.render(f"Rank : E ", True, (153,153,153))                # 사소한 재미를 위해 추가
        screen.blit(score_text, (330,0))
        
    elif score <= 10:                                                              # 가장 낮은 E 등급부터 SSS 등급까지 제작
        font = pygame.font.SysFont("고딕", 50)
        score_text = font.render(f"Rank : D ", True, (0,255,51))
        screen.blit(score_text, (330,0))
        

    elif score <= 15:
        font = pygame.font.SysFont("고딕", 50)
        score_text = font.render(f"Rank : C ", True, (0,255,255))
        screen.blit(score_text, (330,0))
    
    elif score <= 25:
        font = pygame.font.SysFont("고딕", 50)
        score_text = font.render(f"Rank : B ", True, (255,153,102))
        screen.blit(score_text, (330,0))

    elif score <= 35:
        font = pygame.font.SysFont("고딕", 50)
        score_text = font.render(f"Rank : A ", True, (255,102,102))
        screen.blit(score_text, (330,0))
    
    elif score <= 40:
        font = pygame.font.SysFont("고딕", 50)
        score_text = font.render(f"Rank : A+ ", True, (255,0,153))
        screen.blit(score_text, (330,0))
    elif score <= 50:

        font = pygame.font.SysFont("고딕", 50)
        score_text = font.render(f"Rank : S ", True, (255,255,102))
        screen.blit(score_text, (330,0))

    elif score <= 60:
        font = pygame.font.SysFont("고딕", 50)
        score_text = font.render(f"Rank : SS ", True, (255,255,153))
        screen.blit(score_text, (330,0))

    else:
        font = pygame.font.SysFont("고딕", 50)
        score_text = font.render(f"Rank : SSS ", True, (255,255,204))
        screen.blit(score_text, (310,0))


nemo = pygame.sprite.Group()
nemo.add(Nemo(20,20,red))                                                          # Nemo의 크기

obstacles = pygame.sprite.Group()

game_over = False
score = 0
clock = pygame.time.Clock()
fps = 60
t_tick = -1
while True:
    clock.tick(fps)
    t_tick += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    key_event = pygame.key.get_pressed()                                         # 다시플레이 = 키 SPACE
    if key_event[pygame.K_SPACE] and game_over:
        restart_game()                                                           # 리셋


    if game_over == True:                                                        # 장애물 생성
        show_gameover()
    else:
        if t_tick % random.randint(25,60) == 0:                                  # 범위는 25-60 사이
            t_tick = 0
            color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            n = random.randint(25,70)                                            
            obstacles.add(Obstacle(20,n,color))                                 # 크기는 가로크기는 피하기 힘들어 20으로 고정
                                                                                # 새로크기는 25-70 사이의 랜덤크기

     
        if pygame.sprite.groupcollide(nemo, obstacles, False, False) :          # 충돌
            show_gameover()                                                     # 게임 오버

                                                                               
        del_obstacle = []                                                       # 장애물이 왼쪽 밖으로 넘어간 걸 체크
        for o in obstacles:
            if o.check_screen_out():
                score += 1
                del_obstacle.append(o)
                                                                                #장애물 제거
        for d in del_obstacle:
            obstacles.remove(d)

        if score < 10:
            t_tick % random.randint(20,30)


        screen.fill(white)
        show_score()

        nemo.update()
        nemo.draw(screen)

        obstacles.update()
        obstacles.draw(screen)


    pygame.display.update()
