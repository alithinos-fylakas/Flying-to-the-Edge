import pygame, sys
from random import randint

FPS = 60
WIDTH = 1280
HEIGHT = 720
BLACK = 0, 0, 0
BLUE = pygame.color.Color(0, 191, 255)
YELLOW = pygame.color.Color(51,51,0)
BACKGROUND = pygame.Color('#E01B80')

class Map:
    def __init__(self):
        self.size = (WIDTH, HEIGHT)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(BACKGROUND)

class spaceShip:
    def __init__ (self):
        self.size = (48, 96)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(BLUE)
        self.rect = self.surface.get_rect( center = ( randint(48, WIDTH - 48), 16 ) )

        self.direction = pygame.math.Vector2(0, 0)
        self.spd = 12
    
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
    
    def move(self):
        if self.direction != (0, 0):
            self.direction = self.direction/pygame.math.Vector2.magnitude(self.direction)
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

    def update(self):
        self.getInput()
        self.move()
        self.borderCollision()

class asteroid:
    def __init__(self):
        self.size = (96, 96)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(YELLOW)
        self.rect = self.surface.get_rect()

        self.direction = pygame.math.Vector2(0, 1)
        self.spd = randint(6, 20)
    
    def move(self):
        self.rect.center += self.direction * self.spd

    def end(self):
        if self.rect.top > HEIGHT + aster.size[1]:
            del self

    def update(self):
        self.move()

class AsteroidGroup:

    def __init__(self):
        self.list = []

    def createAsteroid(self):
        aster = asteroid()
        return aster
    
    def appendL(self):
        wait = False

        if not wait:
            start = pygame.time.get_ticks()
            wait = True

        if wait:
            current = pygame.time.get_ticks()
            if (current - start >= 500):
                aster = createAsteroid()
                self.list.append(aster)
    
    def updateAsteroid(self):
        for aster in self.list:
            print("Asteróide existe sfd")
            aster.update()
    
    def end(self):
        for aster in self.list:
            if (aster.rect.top > HEIGHT + aster.size[1]):
                aster.end()
                self.list.pop()
    
    def update(self):
        #self.createAsteroid()
        self.appendL()
        self.updateAsteroid()
        self.end()

def main():
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    Nave = spaceShip()
    Nave.rect.center = (WIDTH/2, HEIGHT//4 * 3)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        Nave.update()

        AsterGroup.update()

        screen.fill(BLACK)

        screen.blit(Nave.surface, Nave.rect)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()