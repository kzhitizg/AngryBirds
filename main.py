import pymunk
from pygame.locals import *
import pygame
import pymunk.pygame_util

import math

b_m=10
b_r= 10

'''
slingshot
object- wood
pigs
'''
H=600
W=1200

def to_pygame(x, y):
    return int(x), int(H-y)

def dist(p, r):
    return ((p[0]- r[0])**2 + (p[1] - r[1])**2) **(0.5)

sling_w=5
sling_init=(200, 400)
sling_left=(200+sling_w, 400)
sling_right=(200-sling_w, 400)
sling_mx= 100
    
def stretch(mouse):
    d= dist(mouse, sling_init)
    if (d<=sling_mx):
        return mouse
    else:
        x= sling_mx*(mouse[0]-sling_init[0])/d+ sling_init[0]
        y= sling_mx*(mouse[1]-sling_init[1])/d+ sling_init[1]
        # print(mouse, x, y)
        return x,y

def power(mouse):
    d= dist(mouse, sling_init)
    if (d<=sling_mx):
        return d
    else:
        return sling_mx

class Bird:
    def __init__(self, space):
        self.bird= self.new_bird(space)
        self.is_avail= True
        self.b_m=10
        self.b_r= 10

    def shoot_bird(self, impulse):
        self.bird.body.body_type= pymunk.Body.DYNAMIC
        self.bird.body.mass=self.b_m
        self.bird.body.moment= pymunk.moment_for_circle(self.b_m, 0, self.b_r)
        print(impulse)
        self.body.apply_impulse_at_local_point(impulse)
        
        print(self.body.velocity)

    def new_bird(self, space):
        self.body= pymunk.Body(body_type= pymunk.Body.KINEMATIC)
        self.body.position= 200, 200
        self.shape= pymunk.Circle(self.body, b_r)
        self.shape.elasticity= .95
        self.shape.friction= .8
        self.shape.collision_type=0
        space.add(self.body, self.shape)
        return self.shape

    def show_bird(self, screen):
        pos= to_pygame(*self.body.position)
        # print(pos)
        pygame.draw.circle(screen, (0, 0, 225), pos, int(self.b_r))
    
    def sling_bird(self, mouse, screen):
        pos= list(map(int, stretch(mouse)))
        self.body.position= to_pygame(*pos)
        # print(pos)
        pygame.draw.line(screen, (0,0,0), pos, sling_right)
        # pygame.draw.circle(screen, (0, 0, 225), pos, int(self.b_r))
        self.show_bird(screen)
        pygame.draw.line(screen, (0,0,0), pos, sling_left)

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
                    impulse= pymunk.Vec2d(p*85, 0)
                    try:
                        impulse.rotate(math.atan2((event.pos[1]-sling_init[1]),-(event.pos[0]-sling_init[0])))
                    except ZeroDivisionError:
                        impulse= pymunk.Vec2d(0, p*85)
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
            pygame.draw.line(self.gameDisplay, (225, 180, 255), to_pygame(*seg.a), to_pygame(*seg.b), 5)
            # self.space.debug_draw(draw_options)
            self.space.step(1/50.0)
            pygame.display.flip()
            self.clock.tick(50)

    # def show_bird(self, b):
    #     pos= to_pygame(*b.body.position)
    #     # print(pos)
    #     pygame.draw.circle(self.gameDisplay, (0, 0, 225), pos, int(b.radius))

    # def shoot_bird(self, bird):
    #     bird.body.body_type= pymunk.Body.DYNAMIC
    #     bird.body.mass=b_m
    #     bird.body.moment= pymunk.moment_for_circle(b_m, 0, b_r)
    #     bird.body.apply_impulse_at_world_point((2500, 2500))
    #     # print(bird.body)


Main()