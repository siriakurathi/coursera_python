# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
Lives = 3
time = 0.5
rock_group = set()
missile_group = set()
started = True

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.9)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.forward = [0,0]
        
    def draw(self,canvas):
        if self.thrust == False:
             canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)
        else:
            canvas.draw_image(self.image,(self.image_center[0] + self.image_size[0],self.image_center[1]),self.image_size,self.pos,self.image_size,self.angle)
                
        
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        #print "vel" + str(self.vel)
        #print "pos" + str(self.pos)
        self.angle += self.angle_vel
        self.forward = angle_to_vector(self.angle)
        if self.thrust == True:
            self.vel[0] += 0.2*self.forward[0]
            self.vel[1] += 0.2*self.forward[1]
        self.vel[0] *= 0.99
        self.vel[1] *= 0.99
        
    def keydown(self,key):
 
        if key == simplegui.KEY_MAP["left"]:
            self.angle_vel = -.03
        if key == simplegui.KEY_MAP["right"]:
            #self.angle = -self.angle
            self.angle_vel =  .03
        if key == simplegui.KEY_MAP["up"]:
            self.thrust_fun(True)
        if key == simplegui.KEY_MAP["space"]:
            self.shoot()

    def keyup(self,key):
        self.thrust_fun(False)
        self.angle_vel = 0
        #self.vel[0] = 5
        #self.vel[1] = 5
        
    def thrust_fun(self,on):
        self.thrust = on
        if on == True:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
            
    def shoot(self):
        #global a_missile
        #print "siri"
        global missile_group
        m_pos = [0,0]
        m_vel = [0,0]
        #a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
        m_pos[0] = self.pos[0] + self.radius*self.forward[0]
        m_pos[1] = self.pos[1] + self.radius*self.forward[1] 
        m_vel[0] = self.vel[0] + (4 * self.forward[0])
        m_vel[1] = self.vel[1] + (4 * self.forward[1])
        #a_missile = Sprite([2 *WIDTH /3, 2 * HEIGHT / 3], m_pos, m_vel, 0, missile_image, missile_info, missile_sound)
        a_missile = Sprite(m_pos, m_vel,0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
    def get_pos(self):
        return self.pos
    
    def get_rad(self):
        return self.radius
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)
    
    def update(self):
         self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
         self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
         self.angle += self.angle_vel
        #forward = angle_to_vector(self.angle)
        #if self.thrust == True:
         #   self.vel[0] += forward[0]
          #  self.vel[1] += forward[1]
        #self.vel[0] *= 0.96
        #self.vel[1] *=0.96
         self.age += 1
         if(self.age >= self.lifespan):
            return True
         else:
            return False
    def get_pos(self):
        return self.pos
    
    def get_rad(self):
        return self.radius
    def collide(self,other_object):
        collision = False
        if dist(self.get_pos(), other_object.get_pos()) < (self.get_rad() + other_object.get_rad()):
            collision = True
        return collision
        
  
def draw(canvas):
    global time
    global Lives,rock_group
    global score,started
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text('Lives', (100,50),30,'White')
    canvas.draw_text(str(Lives), (125,75),25,'White')
    canvas.draw_text('Score', (600,50),30, 'White')
    canvas.draw_text(str(score),(625,75),25,'White')
    # draw ship and sprites
    my_ship.draw(canvas)
    #a_rock.draw(canvas)
    #a_missile.draw(canvas)
    process_sprite_group(rock_group,canvas)
    process_sprite_group(missile_group,canvas)
    
    # update ship and sprites
    my_ship.update()
    #a_rock.update()
    #a_missile.update()
    if(group_collide(rock_group,my_ship) == True):
        Lives -= 1
    group_group_collide(missile_group,rock_group)
    if (Lives == 0):
        #print "siri"
        canvas.draw_image(splash_image,splash_info.get_center(),splash_info.get_size(),[WIDTH / 2, HEIGHT / 2], [WIDTH/2, HEIGHT/2])
        started = False
        for r in rock_group:
            rock_group.discard(r)
 
# timer handler that spawns a rock    
def rock_spawner():
    #global a_rock 
    #a_rock = None
    global rock_group,started
    pos = [0,0]
    vel = [0,0]
    pos[0] = random.randrange(WIDTH)
    pos[1] = random.randrange(HEIGHT)
    lower = 0
    upper = 3
    range_width = upper - lower
    vel[0] = random.random() * range_width + lower
    vel[1] = random.random() * range_width + lower
    lower = 0
    upper = 0.2
    range_width = upper - lower
    ang_vel = random.random() * range_width + lower
    positive = random.random()
    if positive < 0.5:
        ang_vel = -ang_vel
    #print len(rock_group)
    if (len(rock_group) < 12)and (started == True):
        m = my_ship.get_pos()
        if (dist(m,pos) > my_ship.get_rad() + 100 ):
             a_rock = Sprite(pos, vel, 0, ang_vel, asteroid_image, asteroid_info)
             rock_group.add(a_rock)

    #vel[0] = random.randint(0,1)
    #vel[1] = random.randint(0,1)
    #ang_vel = random.randint(1,5)
    #print vel,ang_vel,pos
    #a_rock = Sprite(pos, vel, 0, ang_vel, asteroid_image, asteroid_info) 
    #a_rock.update()
def process_sprite_group(group,canvas):
    new_set = set(group)
    for a in new_set:
        if (a.update() == True):
            group.remove(a)
        a.draw(canvas)
    
def group_collide(group,other_object):
    new_group = set(group)
    collide = False
    for a in new_group:
        #a.collide(other_object)
        if a.collide(other_object) == True:
            group.remove(a)
            collide = True
    return collide 
def group_group_collide(group1,group2):
    global score 
    new_group1 =  group1
    for g in new_group1:
        if(group_collide(group2,g) == True):
            score += 10
            group1.discard(g)
            
def click(pos):
    global Lives,score,splash_info,started,soundtrack
    pos = splash_info.get_size
    Lives = 3
    score = 0
    started = True
    soundtrack.rewind()
    soundtrack.play()

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [3, 3], 0, 0.07, asteroid_image, asteroid_info)
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

#def keydown(key):
#    my_ship.keydown(key)
#def keyup(key):
#    my_ship.keyup(key)
 
# register handlers
frame.set_draw_handler(draw)
frame.set_keyup_handler(my_ship.keyup)
frame.set_keydown_handler(my_ship.keydown)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)
soundtrack.play()
# get things rolling
timer.start()
frame.start()
