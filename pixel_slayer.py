import pygame
import random

pygame.init()

WIDTH, HEIGHT = 500, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Slayer")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ATTACK_COLOR = (255, 100, 100)

# FPS 설정
clock = pygame.time.Clock()
FPS = 60
FONT = pygame.font.Font(None, 36)

class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT //2, 40, 40)
        self.speed = 6
        self.attack_range = pygame.Rect(self.rect.x - 30, self.rect.y -30, 100, 100)
        self.lives = 3
        self.invincible = False
        self.invinsible_timer = 0
        self.attacking = False
        self.attack_timer = 0

   

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        

        self.attack_range.topleft = (self.rect.x - 30, self.rect.y - 30)

    def attack(self, enemies):
        if not self.attacking:
            self.attacking = True
            self.attack_timer = 12
            enemies[:] = [enemy for enemy in enemies if not self.attack_range.colliderect(enemy.rect)]

            """
            enemies = []
            for enemy in enemies:
            if not self.attack_range.colliderect(enemy.rect)
            enemies.append(enemy)
            """

    def update(self):
        if self.attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attacking = False

    
    
    def draw(self):
        pygame.draw.rect(SCREEN, (0, 0, 255), self.rect)
        if self.attacking:
            pygame.draw.rect(SCREEN, (255, 100, 100), self.attack_range, 2)
        else:
            pygame.draw.rect(SCREEN, (0, 0, 0), self.attack_range, 1)
        for i in range(self.lives):
                pygame.draw.rect(SCREEN, (255, 0, 0), (10 + i * 30, 10, 20, 20))

class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH-30), random.randint(0, HEIGHT-30), 30, 30)
        self.speed = 1.5
    
    def draw(self):
        pygame.draw.rect(SCREEN, (255, 0, 0), self.rect)

    def move_towards(self, target):
        if self.rect.x < target.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > target.rect.x:
            self.rect.x -= self.speed

        if self.rect.y < target.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > target.rect.y:
            self.rect.y -= self.speed

def main():
    run = True
    player = Player()
    enemies = [Enemy() for _ in range(3)]

    while run:
        clock.tick(FPS)
        SCREEN.fill((255, 255, 255))

        for event in pygame.event.get():
            if  event.type == pygame.QUIT:
                run = False

        for enemy in enemies:
            enemy.move_towards(player)

        for enemy in enemies[:]:
            if player.rect.colliderect(enemy.rect):
                player.lives -= 1
                enemies.remove(enemy)

        for enemy in enemies:
            enemy.draw()
        
        if player.lives <= 0:
            print("GAME OVVER")
            pygame.time.delay(2000)
            run = False

        pygame.display.update()

        keys = pygame.key.get_pressed()
        player.move(keys)

        if keys[pygame.K_SPACE]:
            player.attack(enemies)
        
        player.update()
        player.draw()

        for enemy in enemies:
            enemy.draw()

        

        pygame.display.update()

    pygame.quit()
    exit()

if __name__ == "__main__":
    main()

