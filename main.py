
import pygame
import random
import os

FPS = 60
WIDTH = 500
HEIGHT = 600

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
# 設定好就不會更動的變數名稱就會全大寫 有個提醒的效果

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("遊戲標題")
clock = pygame.time.Clock()

#載入圖片
background_img = pygame.image.load(os.path.join("Img", "background.png")).convert()
player_img = pygame.image.load(os.path.join("Img", "player.png")).convert()
rock_img = pygame.image.load(os.path.join("Img", "rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("Img", "bullet.png")).convert()

class Player(pygame.sprite.Sprite): #繼承內建的sprite類別，位置如括號內
    def __init__(self): #初始函式有固定的寫法
        pygame.sprite.Sprite.__init__(self) #sprite內建的初始函式
        #需要有image和rect屬性
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() #定位
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = rock_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = self.rect.width / 2 * 0.85
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0 :
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)            

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0: #子彈出視窗後就刪掉
            self.kill()

all_sprites = pygame.sprite.Group() #創建一個所有sprite的群組
rocks = pygame.sprite.Group() #創建一個所有sprite的群組
bullets = pygame.sprite.Group() #創建一個所有sprite的群組
player = Player() #實例化 
all_sprites.add(player) #用add將player加入群組
for i in range(8):
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)

running = True

while running:
    clock.tick(FPS)
    # 取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: #空白鍵
                player.shoot()

    # 更新遊戲
    all_sprites.update() #執行群組內每個物件的update函式
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    if hits:   ###這邊原本是 for hit in hits 不知道差在哪?
        rock = Rock()
        all_sprites.add(rock)
        rocks.add(rock)

    hits = pygame.sprite.spritecollide(player, rocks, False, pygame.sprite.collide_circle)

    # 畫面顯示
    screen.fill(BLACK)
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen) #將all_sprites群組內的每個東西畫到畫面上
    pygame.display.update()

pygame.quit() 

