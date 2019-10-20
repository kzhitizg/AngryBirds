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
    def __init__(self, height, width, point, mass, space):
        self.h= height
        self.w= width
        self.points=[(self.w//2, self.h//2),
            (-self.w//2, self.h//2),
            (-self.w//2, -self.h//2),
            (self.w//2, -self.h//2)]
        self.pmass= mass
        self.pos= point
        self.pbody= pymunk.Body(mass, pymunk.moment_for_poly(mass, self.points, radius=5))
        super(Plank, self).__init__(self.pbody, self.points)
        self.pbody.position= self.pos
        self.elasticity= .95
        self.friction= 1.0
        self.health=self.h*self.w/10
        self.sp= space
        space.add(self.pbody, self)

    def show(self, screen):
        pts= []
        vtx= self.get_vertices()
        for pt in vtx:
            pts.append(to_pygame(pt[0]+self.pbody.position[0], pt[1]+self.pbody.position[1]))
        pygame.draw.polygon(screen, [0, 120, 120], pts)