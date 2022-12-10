import pygame, sys
from random import randint

FPS = 60
WIDTH = 1280
HEIGHT = 720
BLACK = 0, 0, 0
BLUE = pygame.color.Color(0, 191, 255)
YELLOW = pygame.color.Color(51,51,0)
BACKGROUND = pygame.Color('#E01B80')

# TILES
class Block(pygame.sprite.Sprite):
    def __init__(self, width, height, posx, posy):
        super().__init__()
        self.image = pygame.Surface( (width, height) )
        self.rect = self.image.get_rect(center = (posx, posy))
    
class mvBlock(Block):
    def __init__(self, width, height, posx, posy, spd):
        super().__init__(width, height, posx, posy)

        self.spd = spd
        self.direction = pygame.math.Vector2(0, 0)
    
    def move(self):

        if self.direction != (0, 0):
            self.direction = pygame.math.Vector2.normalize(self.direction)

        self.rect.center += self.direction * self.spd
    
    def update(self):
        self.move()

class SpaceShip:
    def __init__ (self):
        self.size = (48, 96)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(BLUE)
        self.rect = self.surface.get_rect( center = ( randint(48, WIDTH - 48), 16 ) )

        self.direction = pygame.math.Vector2(0, 0)
        self.spd = 12

        self.bulletGroup = BulletGroup()
        self.canShoot = True
        self.start = 0
    
    def getInput(self):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_d]):
            self.direction.x = 1
        elif (keys[pygame.K_a]):
            self.direction.x = -1
        else:
            self.direction.x = 0
        
        if (keys[pygame.K_w]):
            self.direction.y = -1
        elif (keys[pygame.K_s]):
            self.direction.y = 1
        else:
            self.direction.y = 0

        if (keys[pygame.K_SPACE]) and self.canShoot:
            self.start = pygame.time.get_ticks()
            self.shoot()
            self.canShoot = False
    
    def move(self):
        if self.direction != (0, 0):
            self.direction = pygame.math.Vector2.normalize(self.direction)
        self.rect.center += self.direction * self.spd

    def borderCollision(self):
        if (self.rect.right >= WIDTH):
            self.rect.right = WIDTH
            self.direction.x = 0
        if (self.rect.left <= 0):
            self.rect.left = 0
            self.direction.x = 0
        
        if (self.rect.top <= 0):
            self.rect.top = 0
            self.direction.y = 0
        if (self.rect.bottom >= HEIGHT):
            self.rect.bottom = HEIGHT
            self.direction.y = 0

    def timerShoot(self):
        current = pygame.time.get_ticks()
        if current - self.start >= 200:
            self.canShoot = True

    def shoot(self):
        self.bulletGroup.createBullet(self.rect.centerx, self.rect.centery)

    def update(self):
        self.getInput()
        self.move()
        self.borderCollision()
        self.timerShoot()

def cursor():
    cursor = pygame.mouse.get_pos()
    return cursor
class Bullet(mvBlock):
    def __init__(self, width, height, posx, posy, spd):
        super().__init__(width, height, posx, posy, spd)
        self.image.fill((0, 80, 0))

class BulletGroup:
    def __init__(self):
        self.list = pygame.sprite.Group()
    
    def createBullet(self, x0, y0):
        bullet = Bullet(8, 16, x0, y0, 8)
        bullet.direction.x = cursor()[0] - x0
        bullet.direction.y = cursor()[1] - y0
        self.list.add(bullet)
        print("Shoot")
        print(f"{bullet.direction.x}, {bullet.direction.y}")
    
    def delete(self, bul):
        bul.kill()
        del bul
        print("Bala destruída")

    def destroy(self):
        for bul in self.list.sprites():
            if bul.rect.centerx >= WIDTH or bul.rect.centerx <= 0:
                self.delete(bul)
                return
            if bul.rect.centery >= HEIGHT or bul.rect.centery <= 0:
                self.delete(bul)
                return
    
    def update(self):
        self.list.update()
        self.destroy()

class Asteroid(mvBlock):
    def __init__(self, width, height, posx, posy, spd):
        super().__init__(width, height, posx, posy, spd)
        self.image.fill(YELLOW)
        self.direction.y = 1

class AsterGroup:
    def __init__(self):
        self.list = pygame.sprite.Group()
        self.start = pygame.time.get_ticks()

    def createAster(self):
        position = randint(64, WIDTH - 64), 0
        aster = Asteroid(128, 128, position[0], position[1], randint(8, 16))
        self.list.add(aster)
        print("Asteroide criado")
    
    def timer(self):
        current = pygame.time.get_ticks()
        if current - self.start >= 2000:
            self.createAster()
            self.start = current
    
    def destroy(self):
        for aster in self.list.sprites():
            if aster.rect.centery >= HEIGHT + aster.rect.height:
                aster.kill()
                del aster
                print("Asteroide destruído")

    def update(self):
        self.timer()
        self.list.update()
        self.destroy()

def main():
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    Nave = SpaceShip()
    Nave.rect.center = (WIDTH/2, HEIGHT//4 * 3)

    asterGroup = AsterGroup()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        Nave.update()
        Nave.bulletGroup.update()

        asterGroup.update()

        screen.fill(BLACK)

        asterGroup.list.draw(screen)
        Nave.bulletGroup.list.draw(screen)

        screen.blit(Nave.surface, Nave.rect)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()