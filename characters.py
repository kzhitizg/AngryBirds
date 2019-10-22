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
        self.health= size*100
        self.max_health= self.health
        self.sp= space
        self.sp.add(self.pbody, self)
        self.color= [0, 225, 150]

    def update_color(self):
        if self.health <= .75*self.max_health and self.health > self.max_health/2:
            self.color[0]= 75
        elif self.health <= self.max_health/2 and self.health > self.max_health/4:
            self.color[0]= 150
        elif self.health <= self.max_health/4:
            self.color[0]= 225

    def show(self, screen):
        '''Util fun to show bird on screen'''
        pos= to_pygame(*self.pbody.position)
        # print(pos)
        pygame.draw.circle(screen, self.color, pos, int(self.pradius))

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
        # self.pos= (point[0]-self.h//2, point[1]-self.w//2)
        self.pos= point
        self.r= 2
        self.pbody= pymunk.Body(self.pmass, pymunk.moment_for_poly(self.pmass, self.points, radius=5))
        super(Plank, self).__init__(self.pbody, self.points, radius=self.r)
        self._set_collision_type(3)
        self.pbody.position= self.pos
        self.elasticity= .5
        self.friction= 0.9
        self.sp= space
        space.add(self.pbody, self)
        self.color1= [0, 220, 120]
        self.color2= [0, 150, 120]
        self.health= self.h*self.w/10
        self.max_health= self.health

    def update_color(self):
        if self.health <= .75*self.max_health and self.health > self.max_health/2:
            self.color1[0]= 75
            self.color2[0]= 75
        elif self.health <= self.max_health/2 and self.health > self.max_health/4:
            self.color1[0]= 150
            self.color2[0]= 150
        elif self.health <= self.max_health/4:
            self.color1[0]= 225
            self.color2[0]= 225
        else:
            self.color1[0]= 0
            self.color2[0]= 0

    def show(self, screen):
        pts= []
        vtx= self.get_vertices()
        for pt in vtx:
            x, y= pt.rotated(self.body.angle) + self.body.position
            pts.append(to_pygame(x, y))
        pygame.draw.polygon(screen, self.color1, pts)
        pygame.draw.polygon(screen, self.color2, pts, 4)