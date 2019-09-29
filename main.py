import pymunk
from pygame.locals import *
import pygame
import pymunk.pygame_util

import math
from birds import Bird
from utils import *

class Main():
    def __init__(self):
        #pygame init
        pygame.init()
        self.w, self.h= W, H     #width and height
        self.gameDisplay= pygame.display.set_mode((self.w, self.h))
        self.clock= pygame.time.Clock()
        
        #pymunk init
        self.space= pymunk.Space()
        self.space.gravity= (0,-900)         #gravity

        '''
        Create a new bird, it is sl_bird
        birds array stores the shooted birds
        '''
        self.sl_bird= Bird(self.space)    #sling bird, bird on sling
        self.birds=[]

        '''
        creates a base(ground) and added to the space as a horizontal static bar
        '''
        seg= pymunk.Segment(self.space.static_body, (0, 10), (self.w, 10), 5)
        #lower elasticity
        seg.elasticity= 0.6
        seg.collision_type=1
        seg.friction= 0.5
        self.space.add(seg)
        # draw_options = pymunk.pygame_util.DrawOptions(self.gameDisplay)
        
        #added as trial function, will be used to define the behaviour of collisions
        def func(arbiter, space, data):
            print(arbiter.total_impulse.length)
            return True

        col= self.space.add_collision_handler(0, 1)
        col.post_solve= func
        #end of trail

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
                elif event.type== 5 and event.button==1 and self.sl_bird.is_avail==True:
                    '''
                    Add the bird to click down event, drag with mouse
                    added constrain to accept the drag event if click within 50pix distance max
                    '''
                    # print(event, H-event.pos[1]-self.bird.body.position[1])
                    if all([abs(event.pos[0]-self.sl_bird.body.position[0])<50, abs(H-event.pos[1]-self.sl_bird.body.position[1])<50]):
                        self.mb_down=True
                        pos=event.pos      #stores current pos of mouse
                elif event.type==4 and self.mb_down:
                    '''Just to store new position of mouse'''
                    pos= event.pos

                elif event.type==6 and self.mb_down:
                    '''
                    If mouse is up, then shoot
                    '''
                    self.sl_bird.is_avail=False    #bird not available to shoot
                    self.mb_down=False
                    p=power(event.pos)             #calculate impulse to be applied
                    f=120                          #factor
                    impulse= pymunk.Vec2d(p*f, 0)  #net impluse to apply
                    try:
                        impulse.rotate(math.atan2((event.pos[1]-sling_init[1]),-(event.pos[0]-sling_init[0])))
                    except ZeroDivisionError:
                        #to handle tan 90 case
                        impulse= pymunk.Vec2d(0, p*f)
                    self.sl_bird.shoot_bird(impulse)
                    self.birds.append(self.sl_bird)
                    self.counter=10       #10 frames to next bird add
                    # self.sl_bird=Bird(self.space)
                # print(event)
            if self.counter==0:
                #add new bird
                self.counter-=1
                self.sl_bird=Bird(self.space)
            elif self.counter>0:
                #decrease countdown
                self.counter-=1

            #graphics behaviour
            self.gameDisplay.fill((255,255,255))

            #show first bird
            if self.mb_down:
                self.sl_bird.sling_bird(pos, self.gameDisplay)
            else:
                self.sl_bird.show_bird(self.gameDisplay)
            
            #show other birds
            for bird in self.birds:
                bird.show_bird(self.gameDisplay)
                #if bird gous out of screen
                if bird.body.position.y<0 or bird.body.position.x<0 or bird.body.position.x>self.w:
                    self.space.remove(bird.shape, bird.body)
                    self.birds.remove(bird)
                    # print("Bird Removed")
            
            pygame.draw.line(self.gameDisplay, (225, 180, 255), to_pygame(*seg.a), to_pygame(*seg.b), 5)
            # self.space.debug_draw(draw_options)

            #delta t= 1/80
            self.space.step(1/80.0)
            pygame.display.flip()
            #60 fps
            self.clock.tick(60)

Main()