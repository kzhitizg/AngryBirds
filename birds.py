import pymunk, pygame
from utils import *

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
