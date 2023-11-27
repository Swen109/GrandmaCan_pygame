from typing import Any
import pygame
import random
import os

WIDTH = 500
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (225, 0, 0)
GREEN = (0, 225, 0)

FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('太空生存戰')

player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
player_img.set_colorkey(BLACK)
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
bullet_img.set_colorkey(BLACK)
rocks_img = []
for i in range(7):
    rocks_img.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())
for i in rocks_img:
    i.set_colorkey(BLACK)
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (25, 25)))


shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
expl_sound = [
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
    ]

pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
pygame.mixer.music.set_volume(0.4)

clock = pygame.time.Clock()

def new_rock():
    r = Rock()
    rocks.add(r)
    all_sprites.add(r)

font_name = os.path.join("font.ttf")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    elif hp > 100:
        hp = 100
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, WHITE, outline_rect)
    pygame.draw.rect(surf, GREEN, fill_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 40)) 
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        self.health = 100

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
        bullet = Bullet(self.rect.center, self.rect.top)
        bullets.add(bullet)
        all_sprites.add(bullet)
        shoot_sound.play()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = x
        self.rect.bottom = y
        self.speedy = -20

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rocks_img)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width / 2
        self.rect.right = random.randrange(0, WIDTH + self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedx = random.randrange(-5, 5)
        self.speedy = random.randrange(2, 10)
        self.rot_degree = random.randrange(-3, 3)
        self.total_degree = 0
        
    def rotate(self):
        self.total_degree += self.rot_degree
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.top > HEIGHT:
            self.kill()
            new_rock()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
    #     self.image = expl_anim[self.size][0]
    #     self.rect = self.image.get_rect()
    #     self.radius = self.rect.width / 2
    #     self.rect.right = random.randrange(0, WIDTH + self.rect.width)
    #     self.rect.y = random.randrange(-180, -100)
    #     self.speedx = random.randrange(-5, 5)
    #     self.speedy = random.randrange(2, 10)
    #     self.rot_degree = random.randrange(-3, 3)
    #     self.total_degree = 0

    # def update(self):
    #     self.rotate()
    #     self.rect.x += self.speedx
    #     self.rect.y += self.speedy
    #     if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.top > HEIGHT:
    #         self.kill()
    #         new_rock()

all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
for i in range(8):
    new_rock()

all_sprites.add(player)

score = 0
pygame.mixer.music.play(-1)

#遊戲迴圈
running = True
while running:
    clock.tick(FPS)
    #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()         
    #
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        new_rock()
        score += int(hit.radius)
        random.choice(expl_sound).play()

    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.health -= int(hit.radius) / 2
    #
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 20, WIDTH /  2, 10)
    draw_health(screen, player.health, 5, 10)

    pygame.display.update()

pygame.quit()