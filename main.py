import pygame, sys
from random import randint

FPS = 60
WIDTH = 1280
HEIGHT = 720
BLACK = 0, 0, 0
BLUE = pygame.color.Color(0, 191, 255)
YELLOW = pygame.color.Color(51,51,0)
BACKGROUND = pygame.Color('#E01B80')

#Screens

class Screen:
    def __init__(self):
        self.surface = pygame.Surface( (WIDTH, HEIGHT) )
    
    def gMinput(self):
        pass

    def run(self):
        pass

class Menu(Screen):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 96)

        self.play = self.font.render("JOGAR", False, BACKGROUND)
        self.quit = self.font.render("SAIR", False, BACKGROUND)

        self.playR = self.play.get_rect()
        self.quitR = self.play.get_rect()

        self.playR.topleft = (WIDTH/2 - self.playR.size[0], HEIGHT/2 - self.playR.size[1])
        self.quitR.topleft = (WIDTH/2 - self.quitR.size[0], HEIGHT/2 + self.playR.size[1] - self.quitR.size[1])

        self.state = "menu"
    
    def action(self):
        mousepos = pygame.mouse.get_pos()
        mousepressed = pygame.mouse.get_pressed()

        if mousepressed[0] == 1 and self.playR.collidepoint(mousepos):
            self.state = "game"
        if mousepressed[0] == 1 and self.quitR.collidepoint(mousepos):
            self.state = "quit"

    def run(self):
        self.action()
        self.surface.blit(self.play, self.playR )
        self.surface.blit(self.quit, self.quitR )

class Game(Screen):
    def __init__(self):
        super().__init__()
        self.collider = colliderAdmin()
    
    def run(self):
        self.collider.update()

        self.surface.fill(BLACK)

        self.collider.asterGroup.list.draw(self.surface)
        self.collider.Nave.bulletGroup.list.draw(self.surface)

        self.surface.blit(self.collider.Nave.surface, self.collider.Nave.rect)

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

class colliderAdmin:
    def __init__(self):
        self.Nave = SpaceShip()
        self.Nave.rect.center = (WIDTH/2, HEIGHT//4 * 3)

        self.lastPDMG = 0

        self.asterGroup = AsterGroup()
        print(f"{self.Nave.HP}")

        self.counterspd = 20
        self.knockDir = pygame.math.Vector2(0, 0)

    def bulletCollider(self):
        self.horizontalBullet()
        self.verticalBullet()
    
    def horizontalBullet(self):
        for aster in self.asterGroup.list.sprites():
            for bullet in self.Nave.bulletGroup.list.sprites():
                if aster.rect.colliderect(bullet):
                    if bullet.direction.x != 0:
                        aster.HP -= 1
                        self.Nave.bulletGroup.delete(bullet)
                        print("bala bateu no asteroide")
    
    def verticalBullet(self):
        for aster in self.asterGroup.list.sprites():
            print(f"{aster.HP}")
            for bullet in self.Nave.bulletGroup.list.sprites():
                if aster.rect.colliderect(bullet):
                    if bullet.direction.y != 0:
                        aster.HP -= 1
                        print(f"{aster.HP}")
                        self.Nave.bulletGroup.delete(bullet)
                        print("bala bateu no asteroide")

    def dealDamage(self):
        if self.Nave.TakeDamage:
            self.Nave.HP -= 1
            self.Nave.TakeDamage = False
            self.lastPDMG = pygame.time.get_ticks()
        
    def timerDMG(self):
        current = pygame.time.get_ticks()
        if current - self.lastPDMG >= 500:
            self.Nave.TakeDamage = True
    
    def resetCounterSPD(self):
        if self.counterspd <= 0:
            self.counterspd = 16
            self.knockDir.x = 0
            self.knockDir.y = 0
            self.Nave.inKnockback = False
            self.Nave.spd = 12

    def knockback(self):

        if not self.Nave.inKnockback:
            return

        self.Nave.spd = 0

        if self.knockDir != (0, 0):
            self.knockDir = pygame.math.Vector2.normalize(self.knockDir)
        
        self.Nave.rect.center += self.knockDir * self.counterspd

        self.counterspd -= 0.2
        self.counterspd = int(self.counterspd)
            

    def horizontalCollider(self):
        for aster in self.asterGroup.list.sprites():
            if self.Nave.rect.colliderect(aster.rect):
                if self.Nave.direction.x > 0:
                    self.Nave.rect.right = aster.rect.left
                    self.knockDir.x = -1
                
                if self.Nave.direction.x < 0:
                    self.Nave.rect.left = aster.rect.right
                    self.knockDir.x = 1
                
                self.dealDamage()
                self.Nave.inKnockback = True
                    

    def verticalCollider(self):
        for aster in self.asterGroup.list.sprites():
            if self.Nave.rect.colliderect(aster.rect):
                if self.Nave.direction.y < 0:
                    self.Nave.rect.top = aster.rect.bottom
                    self.knockDir.y = 1

                if self.Nave.direction.y > 0:
                    self.Nave.rect.bottom = aster.rect.top
                    self.knockDir.y = -1

                self.dealDamage()
                self.Nave.inKnockback = True

    def colliderShipAster(self):
        self.horizontalCollider()
        self.verticalCollider()
    
    def update(self):
        self.Nave.update()
        self.Nave.bulletGroup.update()
        self.asterGroup.update()
        self.colliderShipAster()

        self.timerDMG()

        self.knockback()
        self.resetCounterSPD()

        self.bulletCollider()

class SpaceShip:
    def __init__ (self):
        self.size = (48, 96)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(BLUE)
        self.rect = self.surface.get_rect()

        self.direction = pygame.math.Vector2(0, 0)
        self.spd = 12

        self.bulletGroup = BulletGroup()
        self.canShoot = True
        self.start = 0

        self.alive = True
        self.HP = 5

        self.TakeDamage = True

        self.inKnockback = False
    
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

        spd = randint(25, 32)

        bullet = Bullet(16, 16, x0, y0, spd)
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

        self.HP = randint(1, 5)

class AsterGroup:
    def __init__(self):
        self.list = pygame.sprite.Group()
        self.start = pygame.time.get_ticks()

    def createAster(self):
        position = randint(64, WIDTH - 64), 0
        aster = Asteroid(128, 128, position[0], position[1], randint(8, 16))
        self.list.add(aster)
        print("Asteroide criado")
    
    def delete(self, aster):
        aster.kill()
        del aster

    def timer(self):
        current = pygame.time.get_ticks()
        if current - self.start >= 2000:
            self.createAster()
            self.start = current
    
    def outScreen(self, aster = Asteroid(1, 1, 0, 0, 1).rect):
        if aster.rect.centery >= HEIGHT + aster.rect.height:
                self.delete(aster)
                print("Asteroide destruído")

    def killed(self, aster):
        if aster.HP < 0:
            self.delete(aster)

    def destroy(self):
        for aster in self.list.sprites():
            self.outScreen(aster)
            self.killed(aster)

    def update(self):
        self.timer()
        self.list.update()
        self.destroy()

def main():
    pygame.init()
    clock = pygame.time.Clock()

    display = pygame.display.set_mode((WIDTH, HEIGHT))

    #collider = colliderAdmin()

    state = "menu" #It can be "menu" or "game" or "quit"

    menu = Menu()

    game = Game()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        """collider.update()

        display.fill(BLACK)

        collider.asterGroup.list.draw(display)
        collider.Nave.bulletGroup.list.draw(display)

        display.blit(collider.Nave.surface, collider.Nave.rect)"""

        match state:
            case "menu":
                menu.run()

                display.blit(menu.surface, (0, 0))

                state = menu.state

            case "game":
                game.run()

                display.blit(game.surface, (0, 0))

                if game.collider.Nave.HP <= 0:
                    game.collider.Nave.HP = 5
                    state = "menu"
            case "quit":
                pygame.quit()
                sys.exit()
                break

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()