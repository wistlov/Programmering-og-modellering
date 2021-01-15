import pygame
import random
import os
import time

WIDTH = 800
HEIGHT = 600
FPS = 30

# Some variabels 
player_x_dir = 0        #Direction of player (x value)  It resets to 0 evey loop
player_y_dir = 0        #Direction of player (y value)  It resets to 0 evey loop
pxd = 0                 #Also player direction, but it does not reset (its for the bullets)    
pyd = 0                 #Also player direction, but it does not reset (its for the bullets)
speed = 5
reload_time = 50        #n = frames
player_x_pos = 0
player_y_pos = 0
enemy_speed = 2
enemy_nr = 0
enemy_nr_cap = 50       # Highest amount of enemies on screen at the same time
spawn_time = 0      #If this is 0, an enemy will spawn, unless there are 50 enemies already
difficulty_lvl = 0      #As this increases, enemies will spawn more often

# Color template
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (0, 255, 255)
purple = (255, 0, 255)

# Set up assets
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

#####################################################################

class Player(pygame.sprite.Sprite):
    #Sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "hitman1_gun_up.png")).convert() 
        self.rect =  self.image.get_rect()
        self.image.set_colorkey(black)
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        
    
    def update(self):
        self.rect.x += player_x_dir
        self.rect.y += player_y_dir
        if player_x_dir < 0:
            self.image = pygame.image.load(os.path.join(img_folder, "hitman1_gun_left.png")).convert()
            self.image.set_colorkey(black)

        if player_x_dir > 0:
            self.image = pygame.image.load(os.path.join(img_folder, "hitman1_gun_right.png")).convert()
            self.image.set_colorkey(black)

        if player_y_dir > 0:
            self.image = pygame.image.load(os.path.join(img_folder, "hitman1_gun_down.png")).convert()
            self.image.set_colorkey(black)

        if player_y_dir < 0:
            self.image = pygame.image.load(os.path.join(img_folder, "hitman1_gun_up.png")).convert()
            self.image.set_colorkey(black)
        
        global player_x_pos
        global player_y_pos
        player_x_pos = self.rect.x
        player_y_pos = self.rect.y


            
    def shoot_left(self):
        bullet = Bullet(self.rect.left + 10, self.rect.centery - 7)
        all_sprites.add(bullet)
        bullets.add(bullet)
        
    def shoot_right(self):
        bullet = Bullet(self.rect.right - 10, self.rect.centery + 11)
        all_sprites.add(bullet)
        bullets.add(bullet)
        
    def shoot_down(self):
        bullet = Bullet(self.rect.centerx - 9, self.rect.bottom)
        all_sprites.add(bullet)
        bullets.add(bullet)
        
    def shoot_up(self):
        bullet = Bullet(self.rect.centerx + 9, self.rect.top + 10)
        all_sprites.add(bullet)
        bullets.add(bullet)
         
#####################################################################

class Bug(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "enemy_down.png")).convert()
        self.rect =  self.image.get_rect()
        self.image.set_colorkey(white) 
        self.rect.centery = y
        self.rect.centerx = x
    
    def update(self):
        
        #if abs(self.rect.x - player_x_pos) > abs(self.rect.y - player_y_pos):

            if self.rect.x < player_x_pos - enemy_speed:
                self.image = pygame.image.load(os.path.join(img_folder, "enemy_right.png")).convert()
                self.image.set_colorkey(white) 
                self.rect.x += enemy_speed
            
            elif self.rect.y < player_y_pos - enemy_speed:
                self.image = pygame.image.load(os.path.join(img_folder, "enemy_down.png")).convert()
                self.image.set_colorkey(white) 
                self.rect.y += enemy_speed
        
            elif self.rect.x > player_x_pos + enemy_speed:
                self.image = pygame.image.load(os.path.join(img_folder, "enemy_left.png")).convert()
                self.image.set_colorkey(white) 
                self.rect.x += -enemy_speed

            elif self.rect.y  > player_y_pos + enemy_speed:
                self.image = pygame.image.load(os.path.join(img_folder, "enemy_up.png")).convert()
                self.image.set_colorkey(white) 
                self.rect.y += -enemy_speed
    

#####################################################################
class Bullet(pygame.sprite.Sprite):
    # sprite for the bullet the player is firering
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "bullet_up.png")).convert()
        self.image.set_colorkey(black) 
        if pxd < 0:
            self.image = pygame.image.load(os.path.join(img_folder, "bullet_left.png")).convert()
            self.image.set_colorkey(black)
            self.speedy = 0
            self.speedx = -20
        elif pxd > 0:
            self.image = pygame.image.load(os.path.join(img_folder, "bullet_right.png")).convert()
            self.image.set_colorkey(black)
            self.speedy = 0
            self.speedx = 20
        elif pyd > 0:
            self.image = pygame.image.load(os.path.join(img_folder, "bullet_down.png")).convert()
            self.image.set_colorkey(black)
            self.speedy = 20
            self.speedx = 0
        elif pyd < 0:
            self.image = pygame.image.load(os.path.join(img_folder, "bullet_up.png")).convert()
            self.image.set_colorkey(black) 
            self.speedy = -20
            self.speedx = 0
        self.rect =  self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.bottom = y
        self.rect.centerx = x
        
        

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # If it moves out of the screen, it is removed
        if self.rect.bottom < 0:
            self.kill()
            
#####################################################################

def spawn_enemy():
        # This segment give the enemy x and y values that is on the edge of the screen
    n = random.randint(0, 2)
    if n == 0:
        x = random.randint(1, WIDTH)
        n = random.randint(0, 2)
        if n == 0:
            y = 0
        else:
            y = HEIGHT
    else:
        y = random.randint(1, HEIGHT)
        n = random.randint(0, 2)
        if n == 0:
            x = 0
        else:
            x = WIDTH
                
    bug = Bug(x, y)
    all_sprites.add(bug)
    enemies.add(bug)

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("bug massacre EXTREME")          #Name of the game
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
spawn_enemy()
spawn_enemy()

# Adding a small delay before the game starts


# Game loop
running = True
while running == True:
    clock.tick(FPS)
    
    # process input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x_dir = -speed
        pxd = -speed
        pyd = 0
    elif keys[pygame.K_RIGHT]:
        player_x_dir = speed
        pxd = speed
        pyd = 0
    elif keys[pygame.K_UP]:
        player_y_dir = -speed
        pyd = -speed
        pxd = 0
    elif keys[pygame.K_DOWN]:
        player_y_dir = speed
        pyd = speed
        pxd = 0

    # This handles the shooting command
    if keys[pygame.K_SPACE]:
        if reload_time == 0:
            if pxd < 0:
                player.shoot_left()
            if pxd > 0:
                player.shoot_right()
            if pyd > 0:
                player.shoot_down()
            if pyd < 0:
                player.shoot_up()
            reload_time = 5
        
    # for loop that makes it possible to quit the loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # update
    all_sprites.update()
    player_x_dir = 0
    player_y_dir = 0
    if reload_time != 0:
        reload_time += -1
    elif reload_time < 0:
        reload_time = 0
        
    if spawn_time  == 0:
        spawn_enemy()
        spawn_enemy()
        spawn_time = round(random.randint(5,100)- difficulty_lvl)
        if spawn_time < 0:
            spawn_time = 1
    elif spawn_time != 0:
        spawn_time += -1
    elif spawn_time < 0:
        spawn_time = 0
    
    if difficulty_lvl != 90:
        difficulty_lvl += 0.02
    elif difficulty_lvl > 90:
        difficulty_lvl = 90
    
    enemy_speed = 2 + (difficulty_lvl/40)
    
    # Does a bullet hit an enemy?
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    
    # Is the player being eaten?
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        running = False
    
    
    # render
    screen.fill(white)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()