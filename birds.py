import pymunk, pygame
from utils import *

class Bird(pymunk.Circle):
    collision_type=1
    def __init__(self, space, m=10, r=12):
        self.is_avail= True                 #used to track if a bird is on sling
        self.b_m= m                         #mass and radius of bird
        self.b_r= r
        self.timer= 800
        self.sp= space
        self.color= (0, 0, 255)
        self.a_avail= False
        '''
        Creates a new bird and add it to space, returns its shape
        '''
        self.bbody= pymunk.Body(body_type= pymunk.Body.KINEMATIC)
        self.bbody.position= to_pygame(*sling_init)
        super(Bird, self).__init__(self.bbody, self.b_r)
        # self.shape= pymunk.Circle(self.body, self.b_r)
        self.elasticity= .95
        self.friction= .8
        self._set_collision_type(Bird.collision_type)
        space.add(self.bbody, self)
        # self.bird= self.new_bird(space)     #creates new bird and add to space

    def new_bird(self, space):
        '''
        Creates a new bird and add it to space, returns its shape
        '''
        self.body= pymunk.Body(body_type= pymunk.Body.KINEMATIC)
        self.body.position= to_pygame(*sling_init)
        super(Bird, self).__init__(self.body, self.b_r)
        # self.shape= pymunk.Circle(self.body, self.b_r)
        self.elasticity= .95
        self.friction= .8
        self.collision_type=Bird.collision_type
        space.add(self.body, self)
        return

    def shoot_bird(self, impulse):
        '''
        Shoots the bird with given amount of impulse
        '''
        self.a_avail= True
        self.body.body_type= pymunk.Body.DYNAMIC
        self.body.mass=self.b_m
        self.body.moment= pymunk.moment_for_circle(self.b_m, 0, self.b_r)
        self.body.apply_impulse_at_local_point(impulse)

    
    def show(self, screen):
        '''Util fun to show bird on screen'''
        pos= to_pygame(*self.body.position)
        pygame.draw.circle(screen, self.color, pos, int(self.b_r))
    
    def sling_bird(self, mouse, screen):
        '''defines the sling behaviour'''
        pos= list(map(int, stretch(mouse)))
        self.body.position= to_pygame(*pos)
        pygame.draw.line(screen, (0,0,0), pos, sling_right)
        self.show(screen)
        pygame.draw.line(screen, (0,0,0), pos, sling_left)


class ThreeBird(Bird):
    def __init__(self, space, m=2.5, r=10):
        super(ThreeBird, self).__init__(space, m, r)

    def split(self, arr):
        imp= self.body.velocity*self.b_m
        
        b1= Bird(self.sp, self.b_m, self.b_r)
        b1.body.position= self.body.position
        imp.rotate_degrees(10)
        b1.shoot_bird(imp)
        # b1.color= (100, 100, 100)
        arr.append(b1)

        b2= Bird(self.sp, self.b_m, self.b_r)
        b2.body.position= self.body.position
        # b2.color= (200, 200, 200)
        imp.rotate_degrees(-20)
        b2.shoot_bird(imp)
        arr.append(b2)
        self.a_avail=False
        b1.a_avail= False
        b2.a_avail= False
        return
