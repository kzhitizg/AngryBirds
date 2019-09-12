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
        self.w, self.h= W, H
        self.gameDisplay= pygame.display.set_mode((self.w, self.h))
        self.clock= pygame.time.Clock()
        
        #pymunk init
        self.space= pymunk.Space()
        self.space.gravity= (0,-900)

        self.sl_bird= Bird(self.space)
        self.birds=[]

        seg= pymunk.Segment(self.space.static_body, (0, 10), (self.w, 10), 5)
        seg.elasticity= 0.9
        seg.collision_type=1
        seg.friction= 0.5
        self.space.add(seg)
        draw_options = pymunk.pygame_util.DrawOptions(self.gameDisplay)
        
        def func(arbiter, space, data):
            print(arbiter.total_impulse.length)
            return True

        col= self.space.add_collision_handler(0, 1)
        col.post_solve= func
        self.mb_down=False
        self.counter=-1
        while True:
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type== KEYDOWN and event.key== K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.type== 5 and event.button==1 and self.sl_bird.is_avail==True:
                    # print(event, H-event.pos[1]-self.bird.body.position[1])
                    if all([abs(event.pos[0]-self.sl_bird.body.position[0])<50, abs(H-event.pos[1]-self.sl_bird.body.position[1])<50]):
                        self.mb_down=True
                        pos=event.pos
                elif event.type==4 and self.mb_down:
                    pos= event.pos

                elif event.type==6 and self.mb_down:
                    self.sl_bird.is_avail=False
                    self.mb_down=False
                    p=power(event.pos)
                    f=120
                    impulse= pymunk.Vec2d(p*f, 0)
                    try:
                        impulse.rotate(math.atan2((event.pos[1]-sling_init[1]),-(event.pos[0]-sling_init[0])))
                    except ZeroDivisionError:
                        impulse= pymunk.Vec2d(0, p*f)
                    self.sl_bird.shoot_bird(impulse)
                    self.birds.append(self.sl_bird)
                    self.counter=10
                    # self.sl_bird=Bird(self.space)
                # print(event)
            if self.counter==0:
                self.counter-=1
                self.sl_bird=Bird(self.space)
            elif self.counter>0:
                self.counter-=1
            self.gameDisplay.fill((255,255,255))
            if self.mb_down:
                self.sl_bird.sling_bird(pos, self.gameDisplay)
            else:
                self.sl_bird.show_bird(self.gameDisplay)
            for bird in self.birds:
                bird.show_bird(self.gameDisplay)
                if bird.body.position.y<0 or bird.body.position.x<0 or bird.body.position.x>self.w:
                    self.space.remove(bird.shape, bird.body)
                    self.birds.remove(bird)
                    print("Bird Removed")
            pygame.draw.line(self.gameDisplay, (225, 180, 255), to_pygame(*seg.a), to_pygame(*seg.b), 5)
            # self.space.debug_draw(draw_options)
            self.space.step(1/80.0)
            pygame.display.flip()
            self.clock.tick(60)

Main()