import pymunk, pygame
from utils import *

class Bird:
    collision_type=1
    def __init__(self, space):
        self.bird= self.new_bird(space)     #creates new bird and add to space
        self.is_avail= True                 #used to track if a bird is on sling
        self.b_m=10                         #mass and radius of bird
        self.b_r= 10

    def new_bird(self, space):
        '''
        Creates a new bird and add it to space, returns its shape
        '''
        self.body= pymunk.Body(body_type= pymunk.Body.KINEMATIC)
        self.body.position= to_pygame(*sling_init)
        self.shape= pymunk.Circle(self.body, b_r)
        self.shape.elasticity= .95
        self.shape.friction= .8
        self.shape.collision_type=Bird.collision_type
        space.add(self.body, self.shape)
        return self.shape

    def shoot_bird(self, impulse):
        '''
        Shoots the bird with given amount of impulse
        '''
        self.bird.body.body_type= pymunk.Body.DYNAMIC
        self.bird.body.mass=self.b_m
        self.bird.body.moment= pymunk.moment_for_circle(self.b_m, 0, self.b_r)
        # print(impulse)
        self.body.apply_impulse_at_local_point(impulse)
        # print(self.body.velocity)
    
    def show(self, screen):
        '''Util fun to show bird on screen'''
        pos= to_pygame(*self.body.position)
        # print(pos)
        pygame.draw.circle(screen, (0, 0, 225), pos, int(self.b_r))
    
    def sling_bird(self, mouse, screen):
        '''defines the sling behaviour'''
        pos= list(map(int, stretch(mouse)))
        self.body.position= to_pygame(*pos)
        # print(pos)
        pygame.draw.line(screen, (0,0,0), pos, sling_right)
        # pygame.draw.circle(screen, (0, 0, 225), pos, int(self.b_r))
        self.show(screen)
        pygame.draw.line(screen, (0,0,0), pos, sling_left)
