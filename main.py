import pymunk
from pygame.locals import *
import pygame
import pymunk.pygame_util as pgutil

import time
import math
from birds import Bird
from utils import *
from characters import *
from levels import *

class Main():
    def __init__(self):
        #pygame init
        pygame.init()
        self.w, self.h= W, H     #width and height
        self.gameDisplay= pygame.display.set_mode((self.w, self.h))
        self.clock= pygame.time.Clock()
        
        #pymunk init
        self.space= pymunk.Space()
        self.space.gravity= (0, -1000)         #gravity
        self.space.damping= 0.5

        draw_options = pgutil.DrawOptions(self.gameDisplay)
        draw_options.flags= pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
        
        #Create Level
        self.level= Level(self.space, self.gameDisplay)
        
        #the collision handling for bird and pig
        bpgcol= self.space.add_collision_handler(1,2)
        bpgcol.data["pigs"]= self.level.pigs
        bpgcol.pre_solve= bird_pig_col

        #the collision handling for bird and plank
        bpl_col= self.space.add_collision_handler(1, 3)
        bpl_col.data["objs"]= self.level.objects
        bpl_col.pre_solve= bird_plank_col

        #the collision handling for bird and plank
        ppl_col= self.space.add_collision_handler(2, 3)
        ppl_col.data["objs"]= self.level.objects
        ppl_col.data["pigs"]= self.level.pigs
        ppl_col.pre_solve= pig_plank_col

        #the collision handling for pig with ground
        pg_col= self.space.add_collision_handler(0, 2)
        pg_col.data["objs"]= self.level.pigs
        pg_col.pre_solve= ground_col

        #the collision handling for plank with ground
        pg_col= self.space.add_collision_handler(0, 3)
        pg_col.data["objs"]= self.level.objects
        pg_col.pre_solve= ground_col

        self.mb_down=False     #to hold the bird

        self.counter=-1        #to add gap between bird shoot and new bird addition

        while True:
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type== KEYDOWN and event.key== K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.type == KEYDOWN and event.key == K_SPACE and type(self.level.birds[-1]) == ThreeBird and self.level.birds[-1].a_avail:
                    self.level.birds[-1].split(self.level.birds)
                elif event.type== 5 and event.button==1 and self.level.sl_bird.is_avail==True:
                    '''
                    Add the bird to click down event, drag with mouse
                    added constrain to accept the drag event if click within 50pix distance max
                    '''
                    # print(event, H-event.pos[1]-self.bird.body.position[1])
                    if all([abs(event.pos[0]-self.level.sl_bird.body.position[0])<50,
                         abs(H-event.pos[1]-self.level.sl_bird.body.position[1])<50]):
                        self.mb_down=True
                        pos=event.pos      #stores current pos of mouse
                elif event.type==4 and self.mb_down:
                    '''Just to store new position of mouse'''
                    pos= event.pos

                elif event.type==6 and self.mb_down:
                    '''
                    If mouse is up, then shoot
                    '''
                    self.level.sl_bird.is_avail=False    #bird not available to shoot
                    self.mb_down=False
                    p=power(event.pos)             #calculate impulse to be applied
                    f= self.level.sl_bird.b_m*15          #factor
                    impulse= pymunk.Vec2d(p*f, 0)  #net impluse to apply
                    try:
                        impulse.rotate(math.atan2((event.pos[1]-sling_init[1]),-(event.pos[0]-sling_init[0])))
                    except ZeroDivisionError:
                        #to handle tan 90 case
                        impulse= pymunk.Vec2d(0, p*f)
                    self.level.sl_bird.shoot_bird(impulse)
                    self.level.birds.append(self.level.sl_bird)
                    self.counter=10       #10 frames to next bird add
            if self.counter==0:
                #add new bird
                self.counter-=1
                self.level.sl_bird=Bird(self.space)
            elif self.counter>0:
                #decrease countdown
                self.counter-=1

            #graphics behaviour
            self.gameDisplay.fill((255,255,255))

            #show first bird
            if self.mb_down:
                self.level.sl_bird.sling_bird(pos, self.gameDisplay)
            else:
                self.level.sl_bird.show(self.gameDisplay)
            
            #show other birds
            
            for bird in self.level.birds:
                bird.show(self.gameDisplay)
                #bird self destruct
                bird.timer-=1
                if bird.timer<0:
                    self.space.remove(bird, bird.body)
                    self.level.birds.remove(bird)
                    continue
                # if bird goes out of screen
                if bird.body.position.y<0 or bird.body.position.x<0 or bird.body.position.x>self.w:
                    self.space.remove(bird, bird.body)
                    self.level.birds.remove(bird)
                    # print("Bird Removed")
            
            for pig in self.level.pigs:
                #show pig
                if pig:
                    pig.show(self.gameDisplay)
                #pig cleanup
                if pig.body.position.y<0 or pig.body.position.x<0 or pig.body.position.x>self.w:
                    self.space.remove(pig.body, pig)
                    self.level.pigs.remove(pig)
                    print("Pig Removed")

            pygame.draw.line(self.gameDisplay, (225, 180, 255), to_pygame(*self.level.ground.a), to_pygame(*self.level.ground.b), 20)
            # self.space.debug_draw(draw_options)
            for obj in self.level.objects:
                obj.show(self.gameDisplay)
            # for ele in self.level.objects:
            #     pygame.draw.circle(self.gameDisplay, [0, 0, 0], to_pygame(*ele.pos), 5)

            # delta t= 1/80
            self.space.step(1/80.0)
            pygame.display.flip()
            #60 fps
            self.clock.tick(60)
            # time.sleep(0.1)

Main()