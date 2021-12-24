'''
Image Source are  by "analogStudios_" on itch.io for the camelot_ pack (https://analogstudios.itch.io/camelot)
Beginner source code for sprite animation from Neal Holtschulte at "https://www.youtube.com/watch?v=vO_7lpN2Kkk"
'''
import os
import pygame 
import sys
from pygame.sprite import spritecollide


def main():
    '''
    Variables
    '''
    SCREENX = 1600
    SCREENY = 896
    SCREEN = pygame.display.set_mode([SCREENX, SCREENY])

    TX = 32
    TY = 32
    FPS = 30

    SCALING = 4
    DWELL = 3

    set_index = 0
    frame_set_start = set_index*4
    frame_set_end = frame_set_start+3

    WALK_SPEED = 4
    RUN_SPEED = 5
    JUMP_HEIGHT = 30
    jumpcount = 0
    GRAVITY = 3

    IDLE_RIGHT = 0
    IDLE_LEFT = 1
    WALKING_RIGHT = 2
    WALKING_LEFT = 3
    JUMPING_RIGHT = 4
    JUMPING_LEFT = 5

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    
    '''
    Objects
    '''
    class Platform(pygame.sprite.Sprite):
        def __init__(self, xloc, yloc, imgw, imgh, img):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(os.path.join("images", img)).convert()
            self.image.convert_alpha()
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.y = yloc
            self.rect.x = xloc


    class Player(pygame.sprite.Sprite):
        # Setup player Objects
        def __init__(self, SCREEN, x, y, frames):
            pygame.sprite.Sprite.__init__(self)
            self.SCREEN = SCREEN
            self.x = x
            self.y = y
            self.velx = 0
            self.vely = 0
            self.index = 0
            self.frames = frames
            self.rect = self.frames[self.index].get_rect()
            self.DWELL_countdown = DWELL
            
        def advanceImage(self):
            self.DWELL_countdown -=1
            if self.DWELL_countdown < 0:
                self.DWELL_countdown = DWELL
                self.index = (self.index+1)%(frame_set_end+1)
                if self.index<frame_set_start:
                    self.index = frame_set_start

        def draw(self):
            self.SCREEN.blit(self.frames[self.index], 
                            (int(self.x-self.rect.width/2),
                            int(self.y-self.rect.height/2)))
        
        def gravity(self):
            self.vely += GRAVITY

            if self.y > SCREENY-TY:
                self.vely = 0
                self.y = SCREENY-TY

        def update(self):
            self.y += self.vely

            # Check scren bounds
            if self.y < 0:
                self.vely = 0
                self.y = 0

            if self.x > SCREENX and self.velx > 0:
                self.x = 0
            
            if self.x < 0 and self.velx > 0:
                self.x = SCREENX

    class Level:
        def ground(lvl, gloc, tx, ty):
            ground_list = pygame.sprite.Group()
            i = 0
            if lvl == 1:
                while i < len(gloc):
                    ground = Platform(gloc[i], SCREENY - ty, tx, ty, "ground.png")
                    ground_list.add(ground)
                    i+=1
            
            if lvl == 2:
                print("level" + str(lvl))

            return ground_list

        def platform(lvl, tx, ty):
            plat_list = pygame.sprite.Group()
            ploc = []
            i = 0
            if lvl == 1:
                ploc.append((200, SCREENY - ty - 128, 3))
                ploc.append((300, SCREENY - ty - 256, 3))
                ploc.append((500, SCREENY - ty - 128, 4))
                while i < len(ploc):
                    j = 0
                    while j <= ploc[i][2]:
                        plat = Platform((ploc[i][0] + (j*tx)), ploc[i][1], tx, ty, "ground.png")
                        plat_list.add(plat)
                        j+=1
                    print("run"+ str(i) + str(ploc[i][2]))
                    i+=1

            if lvl == 2:
                print("level" + str(lvl))   

            return plat_list     


    '''         
    Setup
    '''
    clock = pygame.time.Clock()
    pygame.init()
    running = True

    ARTHUR_PENDRAGON = pygame.image.load("images/arthurPendragon_.png").convert()
    ARTHUR_PENDRAGON.convert_alpha
    ARTHUR_PENDRAGON.set_colorkey(BLACK)

    BACKDROP = pygame.image.load("images/stage.png")
    BACKDROPBOX = SCREEN.get_rect()

    TITLE = "Knights Crossing"
    ICON = pygame.image.load("images/icon.jpg")

    GLOC = []
    i = 0
    while i <= (SCREENX / TX) + TX:
        GLOC.append(i * TX)
        i+=1

    ground_list = Level.ground(1, GLOC, TX, TY)
    plat_list = Level.platform(1, TX, TY)

    # SCREEN.fill(WHITE)
    pygame.display.set_caption(TITLE)
    pygame.display.set_icon(ICON)
    pygame.display.flip()

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
    dimensions = (int(dimensions.w*SCALING), int(dimensions.h*SCALING))
    for i in range(len(arthurPendragonFrames)):
        arthurPendragonFrames[i] = pygame.transform.scale(
                                arthurPendragonFrames[i],
                                dimensions)

    player = Player(SCREEN, SCREENX/2, SCREENY/2, arthurPendragonFrames)
    player_list = pygame.sprite.Group()
    player_list.add(player)

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
            player.velx = RUN_SPEED
            player.x-=player.velx
        if pressed[pygame.K_RIGHT] and pressed[pygame.K_LSHIFT]:
            player.velx = RUN_SPEED
            player.x+=player.velx
        if pressed[pygame.K_SPACE]:
            player.y-=JUMP_HEIGHT
            player.velx = WALK_SPEED

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
                    set_index = WALKING_RIGHT
                    player.velx = WALK_SPEED
                elif event.key == pygame.K_LEFT:
                    set_index = WALKING_LEFT
                    player.velx = WALK_SPEED
                elif set_index == WALKING_RIGHT and event.key == pygame.K_SPACE and jumpcount == 0:
                    player.vely+=3
                    set_index = JUMPING_RIGHT
                    jumpcount+=1
                elif set_index == WALKING_LEFT and event.key == pygame.K_SPACE and jumpcount == 0:
                    player.vely+=3
                    set_index = JUMPING_LEFT
                    jumpcount+=1

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    set_index = IDLE_RIGHT
                    player.velx = 0
                elif event.key == pygame.K_LEFT:
                    set_index = IDLE_LEFT
                    player.velx = 0
                elif event.key == pygame.K_LSHIFT:
                    player.velx = WALK_SPEED
                elif event.key == pygame.K_SPACE:
                    player.vely-=3
                    set_index = WALKING_RIGHT
                    jumpcount = 0
                elif event.key == pygame.K_SPACE:
                    player.vely-=3
                    set_index = WALKING_LEFT
                    jumpcount = 0
                

            frame_set_start = set_index*4
            frame_set_end = frame_set_start+3

        # SCREEN.fill(WHITE)
        SCREEN.blit(BACKDROP, BACKDROPBOX)

        player.draw()
        player.gravity()
        player.update() 
        player.advanceImage()

        ground_list.draw(SCREEN)
        plat_list.draw(SCREEN)
        
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()