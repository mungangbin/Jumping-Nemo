import pygame
import sys
import random

pygame.init()
screen_width = 500
screen_height = 300
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("[기말고사] Jummping Nemo - 202292022 문강빈")

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

# [NEW] 점수 관련 전역변수
score = 0
high_score = 0

# [NEW] 최고 점수 불러오기
def load_high_score():
    global high_score
    try:
        with open("score.txt", "r") as f:
            high_score = int(f.read())
    except:
        high_score = 0

# [NEW] 최고 점수 저장하기
def save_high_score():
    global score, high_score
    if score > high_score:
        high_score = score
        with open("score.txt", "w") as f:
            f.write(str(high_score))

class Nemo(pygame.sprite.Sprite):
    def __init__(self, width, height, color) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width,height), pygame.SRCALPHA).convert_alpha()
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.vel = 0
        self.clicked = False
        self.jump_cnt = 0

    def update(self):
        if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            self.clicked = True
            if self.jump_cnt < 2:
                self.vel = -15
                self.jump_cnt += 1

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.vel += 1
        if self.vel > 10:
            self.vel = 10

        self.rect.y += int(self.vel)
        if self.rect.y >= screen_height - self.rect.height:
            self.rect.y = screen_height - self.rect.height
            self.jump_cnt = 0

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, width, height, color) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width,height), pygame.SRCALPHA).convert_alpha()
        pt = [(width/2, 0), (0,height),(width,height)]
        pygame.draw.polygon(self.image, color, pt)
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = screen_height - self.rect.height

        # [MODIFIED] 난이도 조절
        if score <= 5: self.vel = 4
        elif score <= 10: self.vel = 5
        elif score <= 15: self.vel = 7
        elif score <= 24: self.vel = 10
        elif score <= 25: self.vel = 9
        elif score <= 35: self.vel = 6
        elif score <= 40: self.vel = 9
        elif score <= 50: self.vel = 11
        elif score <= 60: self.vel = 13
        else: self.vel = 15

    def update(self):
        self.rect.x -= int(self.vel)

    def check_screen_out(self):
        return self.rect.x < 0

def show_gameover():
    global game_over
    game_over = True

    font = pygame.font.SysFont("고딕", 60)
    over_text = font.render(f"Game Over", True, (0,255,255))
    screen.blit(over_text, (int(screen_width/2 - over_text.get_width()/2), int(screen_height/3)))

    font = pygame.font.SysFont("고딕", 30)
    over_text = font.render(f"Replay = SPACE", True, (200,200,255))
    screen.blit(over_text, (int(screen_width/2 - over_text.get_width()/2), int(screen_height/4*2)))

# [MODIFIED] 게임 재시작 시 최고점 저장
def restart_game():
    global game_over, score
    save_high_score()
    game_over = False
    obstacles.empty()
    score = 0

# [MODIFIED] 점수와 최고점수 모두 출력
def show_score():
    font = pygame.font.SysFont("고딕", 30)
    score_text = font.render(f"Score : {score}", True, (0,0,0))
    screen.blit(score_text, (10, 10))

    high_text = font.render(f"High Score : {high_score}", True, (128, 0, 128))
    screen.blit(high_text, (10, 50))

    font = pygame.font.SysFont("고딕", 50)
    rank = "E"
    color = (153,153,153)
    if score <= 10: rank, color = "D", (0,255,51)
    elif score <= 15: rank, color = "C", (0,255,255)
    elif score <= 25: rank, color = "B", (255,153,102)
    elif score <= 35: rank, color = "A", (255,102,102)
    elif score <= 40: rank, color = "A+", (255,0,153)
    elif score <= 50: rank, color = "S", (255,255,102)
    elif score <= 60: rank, color = "SS", (255,255,153)
    else: rank, color = "SSS", (255,255,204)

    rank_text = font.render(f"Rank : {rank}", True, color)
    screen.blit(rank_text, (330, 0))

nemo = pygame.sprite.Group()
nemo.add(Nemo(20,20,red))
obstacles = pygame.sprite.Group()
game_over = False
clock = pygame.time.Clock()
fps = 60
t_tick = -1

load_high_score()  # [NEW] 게임 시작 시 최고 점수 로드

while True:
    clock.tick(fps)
    t_tick += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_high_score()  # [NEW] 종료 전 최고 점수 저장
            sys.exit()

    key_event = pygame.key.get_pressed()
    if key_event[pygame.K_SPACE] and game_over:
        restart_game()

    screen.fill(white)

    if game_over:
        show_gameover()
    else:
        if t_tick % random.randint(25,60) == 0:
            t_tick = 0
            color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            n = random.randint(25,70)
            obstacles.add(Obstacle(20,n,color))

        if pygame.sprite.groupcollide(nemo, obstacles, False, False):
            show_gameover()

        del_obstacle = []
        for o in obstacles:
            if o.check_screen_out():
                score += 1
                del_obstacle.append(o)
        for d in del_obstacle:
            obstacles.remove(d)

        nemo.update()
        obstacles.update()

    show_score()
    nemo.draw(screen)
    obstacles.draw(screen)

    pygame.display.update()