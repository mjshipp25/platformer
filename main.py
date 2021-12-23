'''
Image Source are  by "analogStudios_" on itch.io for the camelot_ pack (https://analogstudios.itch.io/camelot)
Beginner source code for sprite animation from Neal Holtschulte at "https://www.youtube.com/watch?v=vO_7lpN2Kkk"
'''

import pygame 
import sys

from pygame.sprite import spritecollide


'''
Variables
'''
screenx = 1600
screeny = 900
tx = 64
ty = 64
fps = 30

walk_speed = 4
run_speed = 5
jump_speed = 100
screen = pygame.display.set_mode([screenx, screeny])

scaling = 3
dwell = 3

set_index = 0
frame_set_start = set_index*4
frame_set_end = frame_set_start+3

idle_right = 0
idle_left = 1
walking_right = 2
walking_left = 3
jumping_right = 4
jumping_left = 5

jumpcount = 0
GRAVITY = 3

TITLE = "Knights Crossing"
ICON = pygame.image.load("images/icon.jpg")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ARTHUR_PENDRAGON = pygame.image.load("images/arthurPendragon_.png").convert()
ARTHUR_PENDRAGON.convert_alpha
ARTHUR_PENDRAGON.set_colorkey(BLACK)


'''
Objects
'''
class Player(pygame.sprite.Sprite):
    # Setup player Objects
    def __init__(self, screen, x, y, frames):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.x = x
        self.y = y
        self.velx = 0
        self.vely = 0
        self.index = 0
        self.frames = frames
        self.rect = self.frames[self.index].get_rect()
        self.dwell_countdown = dwell
           
    def advanceImage(self):
        self.dwell_countdown -=1
        if self.dwell_countdown < 0:
            self.dwell_countdown = dwell
            self.index = (self.index+1)%(frame_set_end+1)
            if self.index<frame_set_start:
                self.index = frame_set_start

    def draw(self):
        self.screen.blit(self.frames[self.index], 
                        (int(self.x-self.rect.width/2),
                        int(self.y-self.rect.height/2)))
    
    def gravity(self):
        self.vely += GRAVITY

    def update(self):
        self.y += self.vely

        # Check scren bounds
        if self.y > screeny-ty:
            self.vely = 0
            self.y = screeny-ty
        
        if self.y < 0:
            self.vely = 0
            self.y = 0

        if self.x > screenx and self.velx > 0:
            self.x = 0
        
        if self.x < 0 and self.velx > 0:
            self.x = screenx
'''
Setup
'''
clock = pygame.time.Clock()
pygame.init()
running = True

screen.fill(WHITE)
pygame.display.flip()
pygame.display.set_caption(TITLE)
pygame.display.set_icon(ICON)

def strip_from_sheet(sheet, rows, cols):
        r = sheet.get_rect()
        img_width = r.w/cols
        img_height = r.h/rows

        frames = []
        for row in range(rows):
            for col in range(cols):
                rect = pygame.Rect(col*img_width, row*img_height, img_width, img_height)
                frames.append(sheet.subsurface(rect))
        return frames

arthurPendragonFrames = strip_from_sheet(ARTHUR_PENDRAGON, 6, 8)
dimensions = arthurPendragonFrames[0].get_rect()
dimensions = (int(dimensions.w*scaling), int(dimensions.h*scaling))
for i in range(len(arthurPendragonFrames)):
    arthurPendragonFrames[i] = pygame.transform.scale(
                            arthurPendragonFrames[i],
                            dimensions)

player = Player(screen, screenx/2, screeny/2, arthurPendragonFrames)

'''
Main Loop
'''
while running:
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        player.x-=player.velx
    if pressed[pygame.K_RIGHT]:
        player.x+=player.velx
    if pressed[pygame.K_LEFT] and pressed[pygame.K_LSHIFT]:
        player.velx = run_speed
        player.x-=player.velx
    if pressed[pygame.K_RIGHT] and pressed[pygame.K_LSHIFT]:
        player.velx = run_speed
        player.x+=player.velx
    if pressed[pygame.K_SPACE]:
        player.y-=player.vely

    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            pygame.quit()
            try:
                sys.exit()
            finally:
                running = False
        elif event.type == pygame.KEYDOWN:
            # print(event.key) # Print value of key press 
            if event.key == pygame.K_RIGHT:
                set_index = walking_right
                player.velx = walk_speed
            elif event.key == pygame.K_LEFT:
                set_index = walking_left
                player.velx = walk_speed
            elif set_index == walking_right and event.key == pygame.K_SPACE and jumpcount == 0:
                player.vely+=3
                set_index = jumping_right
                jumpcount+=1
            elif set_index == walking_left and event.key == pygame.K_SPACE and jumpcount == 0:
                player.vely+=3
                set_index = jumping_left
                jumpcount+=1

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                set_index = idle_right
                player.velx = 0
            elif event.key == pygame.K_LEFT:
                set_index = idle_left
                player.velx = 0
            elif event.key == pygame.K_LSHIFT:
                player.velx = walk_speed
            elif event.key == pygame.K_SPACE:
                player.vely-=3
                set_index = walking_right
                jumpcount = 0
            elif event.key == pygame.K_SPACE:
                player.vely-=3
                set_index = walking_left
                jumpcount = 0
            

        frame_set_start = set_index*4
        frame_set_end = frame_set_start+3

    screen.fill(WHITE)

    player.gravity()
    player.update() 

    player.draw()
    player.advanceImage()
    pygame.display.flip()
    clock.tick(30)
