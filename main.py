from pygame import *
from random import *
w, h = 700, 500
window = display.set_mode((w, h))

display.set_caption("Asteroids")

clock = time.Clock()
game = True
finish = False


class GameSprite(sprite.Sprite):
    def __init__(self, pImage, pX, pY, sizeX, sizeY, pSpeed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(pImage), (sizeX, sizeY))
        self.speed = pSpeed
        self.rect = self.image.get_rect()
        self.rect.x = pX
        self.rect.y = pY
    
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx-7, self.rect.top, 15, 30, -15)
        bullets.add(bullet)

bullets = sprite.Group()

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global hearts
        if self.rect.y > h:
            try:
                hearts.pop(0)
            except:
                pass
            #hearts.pop(len(hearts)-1)
            self.rect.x = randint(0, w-80)
            self.rect.y = 0
            lost += 1

background = transform.scale(image.load("galaxy.jpg"), (w, h))

ship = Player("rocket.png", 10, h-100, 65, 95, 4)

asteroids = sprite.Group()
for i in range(6):
    randpic = randint(1,2)
    if randpic == 1:
        pic = "asteroid.png"
    if randpic == 2:
        pic = "ufo.png"
    asteroid = Enemy(pic, randint(10, w-50), -40, 50, 50, 
                     randint(1, 3))
    asteroids.add(asteroid)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill() 
ship_fire = mixer.Sound("fire.ogg")
ship_fire.set_volume(0.1)
score = 0
font.init()
mainfont = font.SysFont("Arial", 40)

reload_time = False
num_fire = 0
from time import time as timer 

lives = 10
hearts = []
hX = 300
for i in range(lives):
    heart = GameSprite("heart.png", hX, 10, 40, 38, 0)
    hearts.append(heart)
    hX += 40

restart = GameSprite("restart.png", 242, 200, 200, 120, 0)

def gameloop():
    global game, finish, score, reload_time, num_fire, lost, hearts

    while game:
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if num_fire < 5 and reload_time == False:
                        ship.fire()
                        ship_fire.play()
                        num_fire += 1
                    if num_fire >= 5 and reload_time == False:
                        reload_start = timer()
                        reload_time = True
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if restart.rect.collidepoint(x,y):
                    for a in asteroids:
                        a.rect.y = -100
                        a.rect.x = randint(0, w-100)
                    finish, lost, score = 0,0,0
                    lives = 10
                    hearts = []
                    hX = 300
                    for i in range(lives):
                        heart = GameSprite("heart.png", hX, 10, 40, 38, 0)
                        hearts.append(heart)
                        hX += 40


        if not finish:
            window.blit(background, (0,0))
            score_text = mainfont.render("Killed:" + str(score), True, (0,255,0))
            lost_text = mainfont.render("Missed:" + str(lost), True, (0,255,0))
            window.blit(score_text, (5,10))
            window.blit(lost_text, (5,50))
            ship.draw()
            ship.update()

            bullets.draw(window)
            bullets.update()

            asteroids.draw(window)
            asteroids.update()

            collides = sprite.groupcollide(bullets, asteroids, True, True)
            for c in collides:
                score += 1
                randpic = randint(1,2)
                if randpic == 1:
                    pic = "asteroid.png"
                if randpic == 2:
                    pic = "ufo.png"
                asteroid = Enemy(pic, randint(10, w-50), -40, 50, 50, 
                                 randint(1, 3))
                asteroids.add(asteroid)

            if reload_time == True:
                reload_end = timer()
                if reload_end - reload_start < 3:
                    reload = mainfont.render("RELOADING", True, (0, 250, 0))
                    window.blit(reload, (200, 200))
                else:
                    num_fire = 0
                    reload_time = False

            if sprite.spritecollide(ship, asteroids, False):
                restart.draw()
                lose = mainfont.render("YOU LOSE", True, (0, 250, 0))
                window.blit(lose, (240, 200))
                finish = True

            for heart in hearts:
                heart.draw()

            if len(hearts) <= 0:
                restart.draw()
                lose = mainfont.render("YOU LOSE", True, (0, 250, 0))
                window.blit(lose, (240, 200))
                finish = True


        display.update()
        clock.tick(60)

gameloop()