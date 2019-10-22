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

#converts given pymunk coords to pygame
def to_pygame(x, y):
    return int(x), int(H-y)

#distance between point p and r
def dist(p, r):
    return ((p[0]- r[0])**2 + (p[1] - r[1])**2) **(0.5)

#sling constants
sling_w=5
sling_init=(200, 500)
sling_left=(200+sling_w, 500)
sling_right=(200-sling_w, 500)
sling_mx= 80

#stretch the sling with mouse
def stretch(mouse):
    d= dist(mouse, sling_init)
    if (d<=sling_mx):
        return mouse
    else:
        x= sling_mx*(mouse[0]-sling_init[0])/d+ sling_init[0]
        y= sling_mx*(mouse[1]-sling_init[1])/d+ sling_init[1]
        # print(mouse, x, y)
        return x,y

#return the power value by which the bird shall be launched
def power(mouse):
    d= dist(mouse, sling_init)
    if (d<=sling_mx):
        return d
    else:
        return sling_mx
#collision limits
birdpig_limit= 3000000
birdplank_limit= 5000000
pigplank_limit= birdplank_limit*10
ground_limit= pigplank_limit

#the collision handler for bird and pig
def bird_pig_col(arbiter, space, data):
    bird, pig= (arbiter.shapes)
    limit= birdpig_limit
    impulse= bird.body.kinetic_energy + pig.body.kinetic_energy
    pig.health-= (impulse/limit)*125
    pig.update_color()
    if pig.health<=0 and pig in data["pigs"]:
        space.remove(pig.body, pig)
        data["pigs"].remove(pig)
        return False
    else:
        return True

#collision handler for bird and plank
def bird_plank_col(arbiter, space, data):
    bird, plank= (arbiter.shapes)
    limit= birdplank_limit
    impulse= bird.body.kinetic_energy + plank.body.kinetic_energy
    plank.health-= (impulse/limit)*150
    plank.update_color()
    if plank.health<=0 and plank in data["objs"]:
        space.remove(plank.body, plank)
        data["objs"].remove(plank)
        imp= bird.body.velocity*bird.body.mass/3
        imp.rotate_degrees(180)
        bird.body.apply_impulse_at_local_point(imp)
        return False
    else:
        return True

#pig_plank_col
def pig_plank_col(arbiter, space, data):
    pig, plank= arbiter.shapes
    limit= pigplank_limit
    impulse= pig.body.kinetic_energy + plank.body.kinetic_energy
    if impulse< 300000:
        return True
    plank.health-= (impulse/limit)*150
    pig.health-= (impulse/limit)*100
    plank.update_color()
    pig.update_color()
    # print(plank.health, pig.health)
    if plank.health<=0 and plank in data["objs"]:
        space.remove(plank.body, plank)
        data["objs"].remove(plank)
        return False
    elif pig.health<=0 and pig in data["pigs"]:
        space.remove(pig.body, pig)
        data["pigs"].remove(pig)
        return False
    else:
        return True

#ground collision of pig and plank
def ground_col(arbiter, space, data):
    obj= arbiter.shapes[1]
    limit= ground_limit
    impulse= obj.body.kinetic_energy
    if impulse < 200000:
        return True
    obj.health= obj.health - (impulse/limit)*125
    obj.update_color()
    if obj.health<=0 and obj in data["objs"]:
        space.remove(obj.body, obj)
        data["objs"].remove(obj)
        return False
    else:
        return True