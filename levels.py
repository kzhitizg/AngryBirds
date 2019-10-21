import pymunk, pygame
from utils import *
from birds import *
from characters import *

class Level:
    def __init__(self, space, screen):
        self.space= space
        self.screen= screen
        self.w, self.h= W, H

        #The ground--------
        self.ground= pymunk.Segment(self.space.static_body, (0, 10), (self.w, 10), 10)
        self.ground.elasticity= 0.6
        self.ground.collision_type=0
        self.ground.friction= 0.5
        self.space.add(self.ground)
        #------------------

        #The birds---------

        '''
        Create a new bird, it is sl_bird
        birds array stores the shooted birds
        '''
        self.sl_bird= Bird(self.space)    #sling bird, bird on sling
        self.birds=[]
        #------------------

        #The objects-------
        self.objects= [Plank(100, 20, (750,80), 50000, self.space),
                        Plank(100, 20, (670,80), 50000, self.space),
                        Plank(20, 100, (710,140), 50000, self.space),
                        Plank(100, 20, (750,200), 50000, self.space),
                        Plank(100, 20, (670,200), 50000, self.space),
                        Plank(20, 100, (710,260), 50000, self.space),
                        ]
        #------------------

        #The pigs----------
        '''
        Create a pig, at say, 600, 50, just to test
        '''
        self.pigs= [Pig(1.5, self.space, (700, 170))]
        #------------------

