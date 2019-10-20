import pymunk, pygame
from utils import *
'''
Pig object will inherit from circle class, so that the attributes can be defined for health
'''
class Pig(pymunk.Circle):
    collision_type=2
    def __init__(self, size, space, pos):
        self.pradius= size*10
        self.pmass= size*20
        self.pbody= pymunk.Body(self.pmass, pymunk.moment_for_circle(self.pmass, 0, self.pradius), body_type= pymunk.Body.DYNAMIC)
        self.pbody.position= pos
        super(Pig, self).__init__(self.pbody, self.pradius)
        self._set_collision_type(2)
        # self.pig= self.create(space, size, pos)
        self.elasticity= .95
        self.friction= 1.0
        self.health=size*100
        self.sp= space
        self.sp.add(self.pbody, self)

    # def create(self, space, size, pos):
    #     self.body.position= pos
    #     self.shape= pymunk.Circle(self.body, self.radius)
    #     self.shape.elasticity= .95
    #     self.shape.friction= 1.0
    #     self.shape.collision_type=Pig.collision_type
    #     space.add(self.body, self.shape)
    #     return self.shape

    def show(self, screen):
        '''Util fun to show bird on screen'''
        pos= to_pygame(*self.pbody.position)
        # print(pos)
        pygame.draw.circle(screen, (0, 225, 150), pos, int(self.pradius))

class Plank(pymunk.Poly):
    collision_type=3
    def __init__(self, height, width, point, density, space):
        self.h= height
        self.w= width
        self.points=[(self.w//2, self.h//2),
            (-self.w//2, self.h//2),
            (-self.w//2, -self.h//2),
            (self.w//2, -self.h//2)]
        self.pmass= density/(self.h*self.w)
        self.pos= point
        self.r= 5
        self.pbody= pymunk.Body(self.pmass, pymunk.moment_for_poly(self.pmass, self.points, radius=5))
        super(Plank, self).__init__(self.pbody, self.points, radius=self.r)
        self._set_collision_type(3)
        self.pbody.position= self.pos
        self.elasticity= .85
        self.friction= 0.9
        self.health=self.h*self.w/10
        self.max_health= self.health
        self.sp= space
        space.add(self.pbody, self)

    def show(self, screen):
        pts= []
        vtx= self.get_vertices()
        for pt in vtx:
            x, y= pt.rotated(self.body.angle) + self.body.position
            pts.append(to_pygame(x, y))
        pygame.draw.polygon(screen, [0, 120, 120], pts)