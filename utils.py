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
birdpig_limit=100

#the collision handler for bird and pig
def bird_pig_col(arbiter, space, data):
    bird, pig= (arbiter.shapes)
    limit= birdpig_limit
    if bird.body.velocity.get_length() > limit:
        space.remove(pig.body, pig)
        data["pigs"].remove(pig)
        print("Pig Removed")
        return False
    else:
        pig.health-=bird.body.velocity.get_length()/(limit/2)
        # print(pig.health)
        return True

