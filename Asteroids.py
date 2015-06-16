"""
Asteroids. 
"""

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random
import pygame

#Global constants
WIDTH = 800
HEIGHT = 600

class ImageInfo:
    """
    Get information from graphics. This includes center, size, radius, lifespan and if
    its animated or not (e.g. explosions)
    """
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

"""
Load graphics
"""
#Debris images 
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris1_brown.png")
#Nebula images
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")
#Ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")
#Missile image
missile_info = ImageInfo([5,5], [10, 10], 3, 50) 
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")
#Asteroid images 
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_brown.png")
#Animated explosion
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

class Ship:
    """
    The ship class. Draws the ship, changes its position, velocity and rotation angle and lets it shoot missiles. 
    """
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
        
    def draw(self,canvas):
        """
        Draws the ship with and without fire trail. 
        """
        if self.thrust:
            canvas.draw_image(self.image,[self.image_center[0]+self.image_size[0],self.image_center[1]],
                              self.image_size,self.pos,self.image_size,self.angle)
        else:
            canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,
                              self.image_size,self.angle)
        

    def update(self):
        """
        Changes position, velocity and the rotation angle. 
        """
        #Update position
        self.pos[0]+=self.vel[0]
        self.pos[1]+=self.vel[1]
        #Periodic boundary conditions
        self.pos[0]%=WIDTH
        self.pos[1]%=HEIGHT
        #Friction
        self.vel[0]*=1-0.01
        self.vel[1]*=1-0.01
        #Angle velocity
        self.angle+=self.angle_vel
        #Determine acceleration vector
        self.forward_vector=angle_to_vector(self.angle)
        #Acceleration
        if self.thrust:
            self.vel[0]+=0.25*self.forward_vector[0]
            self.vel[1]+=0.25*self.forward_vector[1]
    
    def shoot(self,missile):
        """
        Shoots missiles in the flight direction of the ship.
        """
        missile_pos=2*[None]
        missile_pos[0]=self.pos[0]+self.forward_vector[0]*self.image_size[0]/2
        missile_pos[1]=self.pos[1]+self.forward_vector[1]*self.image_size[0]/2
        missile_vel=2*[None]
        missile_vel[0]=self.vel[0]+7*self.forward_vector[0]
        missile_vel[1]=self.vel[1]+7*self.forward_vector[1]        
        missile.add(Sprite(missile_pos,missile_vel,0,0,missile_image, missile_info))
        

class Sprite:
    """
    The sprite class. Draws sprite, updates its position and rotation angle and defines if two objects
    collide. The sprite could be a rock, a missile or an animated explosion.
    """   
    def __init__(self, pos, vel, ang, ang_vel, image, info):
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
   
    def draw(self, canvas):
        """
        Animates explosion if self.animated==True. Otherwise a rock or a missile is drawn.
        """
        if self.animated:
            #Animation consists of 64 pictures. After each age step another picture is shown. 
            animate_index=(self.age%64)//1
            animate_center=[explosion_info.get_center()[0]+animate_index*explosion_info.get_size()[0],
                            explosion_info.get_center()[1]]
            canvas.draw_image(explosion_image,animate_center,explosion_info.get_size(),self.pos,
                            explosion_info.get_size())
        else:
            canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,
                            self.angle)
            
    def update(self):
        """
        Updates position,rotation angle and age of sprite. A sprite only lives for a
        certain time span. 
        """        
        #Update position
        self.pos[0]+=self.vel[0]
        self.pos[1]+=self.vel[1]
        #Periodic boundary conditions
        self.pos[0]%=WIDTH
        self.pos[1]%=HEIGHT
        #Angle velocity
        self.angle+=self.angle_vel
        #Increase age of sprite
        self.age+=1
        #Check if sprite is older than its lifespan
        if self.age>=self.lifespan:
            return True        

    def collide(self,other_object):
        """
        Defines if two objects collide. If the distance between two objects is smaller
        than the sum of their radii, they collide. 
        """
        max_dist=(self.radius+other_object.radius)         
        real_dist=dist(self.pos,other_object.pos)
        if real_dist<max_dist:
            return True
        else:
            return False
    
    
def angle_to_vector(ang):
    """
    Transforms angle to vector
    """
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    """
    The distance between two points
    """
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def compose(canvas):
    """
    Puts everything together. Draws background, player's lives and scores, missiles, rocks,
    the ship and explosions.  
    """
    global time_G,live_G,score_G,started_G
    # Animiate background. The nebula stands still while the debris is moving.
    time_G += 1
    wtime = (time_G / 4) % WIDTH
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(),
                      [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, debris_info.get_center(),debris_info.get_size(),
                      (wtime - WIDTH / 2, HEIGHT / 2),(WIDTH, HEIGHT))
    canvas.draw_image(debris_image, debris_info.get_center(),debris_info.get_size(),
                      (wtime + WIDTH / 2, HEIGHT / 2),(WIDTH, HEIGHT))        
    #Draw lives and scores
    canvas.draw_text('Lives',(50,50),30,'Silver')
    canvas.draw_text(str(live_G),(78,80),30,'Silver')
    canvas.draw_text('Score',(690,50),30,'Silver')
    canvas.draw_text(str(score_G),(720,80),30,'Silver')
    #If the game is running draw ships, rocks and missiles
    if started_G:
        #Draw ship
        myShip_G.draw(canvas)
        myShip_G.update()
        #Draw and update rocks, missiles and explosions        
        process_sprite_group(rock_group_G,canvas)
        process_sprite_group(missile_group_G,canvas)
        process_sprite_group(explosion_group_G,canvas)
        #Decrease live if a ship collides with a rock, increase score if a missile
        #collides with a rock
        if group_collide(rock_group_G,myShip_G):
            live_G-=1
        score_G+=group_group_collide(missile_group_G,rock_group_G)
        if live_G==0:
            started_G=False
            score_G=0
    #If the game is not running draw the welcome display        
    else:        
        canvas.draw_polygon([[250,250], [550,250], [550,350], [250,350]], 12, 'Grey','Grey')
        canvas.draw_text('Asteroids',(310,290),45,'Purple')
        canvas.draw_text('Click to start',(340,330),25,'Blue')

def process_sprite_group(set_group,canvas):
    """
    Draws and updates the position, velocity and angle rotation of all objects within a group 
    """
    for element in set(set_group):
        element.draw(canvas)
        element.update()
        if element.update():
            set_group.discard(element)
        
    
def rock_spawner():
    """
    Gives birth to rocks. At every tick of the timer a rock is spawned at a random location. Thereby
    the rock never arises to close to the ship and the number of rocks exisitng at the same time
    is limited to twelve. The mean value of the random velocity of the rocks increases with
    the player's score (increasing level of difficulty)
    """
    global rock_group_G
    rock_pos=[WIDTH*random.random(), HEIGHT*random.random()]
    if dist(rock_pos,myShip_G.pos)>(2*asteroid_info.get_radius()+myShip_G.radius):
        myRock=Sprite(rock_pos,[2*random.random(), (score_G/100+1)*random.random()],6.28*random.random(),
                    0.2*random.random(), asteroid_image, asteroid_info)
        #Add rocks every tick. But not more than 12
        if len(rock_group_G)<12:
            rock_group_G.add(myRock)
    

def group_collide(set_group,other_object):
    """
    If a single object (e.g. the ship) collides with another object (e.g. a rock), remove the other
    object (rock) and animate an explosion    
    """
    hit=False
    for element in set(set_group):
        if element.collide(other_object):
            set_group.discard(element)
            hit=True
            explosion_group_G.add(Sprite(element.pos,[0,0],0,0,explosion_image,explosion_info))
    return hit

def group_group_collide(set_group,other_set_group):
    """
    If an object from a group (e.g. missile) collides with an object from another group (e.g. rock)
    remove the corresponding objects from each group and animate an explosion.
    """
    score_increment=0
    for element in set(set_group):
        if group_collide(other_set_group,element):
            set_group.discard(element)	            
            score_increment+=10
    return score_increment 
        
def mouse_click(pos):
    """
    At the welcome display the game starts with a click. Otherwise nothing happens.
    """
    global started_G
    if not started_G:
        new_game()
    timer.start()
    started_G=True

def key_down(key):
    """
    The controls of the ship. Rotates the ship left or right, accelerates the ship and shoots missiles.  
    """
    if key==simplegui.KEY_MAP["left"]:
        myShip_G.angle_vel=-0.2        
    if key==simplegui.KEY_MAP["right"]:
        myShip_G.angle_vel=0.2
    if key==simplegui.KEY_MAP["up"]:
        myShip_G.thrust=True
    if key==simplegui.KEY_MAP["space"]:    
        myShip_G.shoot(missile_group_G)       

def key_up(key):
    """
    If you release the keys the ship stops accelerating and rotating 
    """
    if key==simplegui.KEY_MAP["left"] or key==simplegui.KEY_MAP["right"]:
        myShip_G.angle_vel=0        
    if key==simplegui.KEY_MAP["up"]:
        myShip_G.thrust=False

def stop_timer():
    """
    Stops the timer if the quit button is pushed.
    """
    timer.stop()
    
def new_game():
    """
    Initialize global variables when the game starts.
    """
    global started_G,live_G,score_G,time_G
    global myShip_G,rock_group_G,explosion_group_G,missile_group_G
    timer.stop()
    myShip_G = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    score_G = 0
    time_G = 0.5
    started_G=False
    live_G=3
    score_G=0
    rock_group_G=set()
    missile_group_G=set()
    explosion_group_G=set()

"""
Main
"""
# Initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
# Register handlers
frame.set_draw_handler(compose)
frame.set_mouseclick_handler(mouse_click)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
#Get some empty space on the control panel
for i in range(0,3):
    frame.add_label("")
#Add buttons    
frame.add_button('Stop',stop_timer, 200)
frame.add_label('Before you close the window', 200)
frame.add_label("")
frame.add_button('Restart',new_game, 200)
#Get some empty space on the control panel
for i in range(0,8):
    frame.add_label("")
frame.add_label("Controls: 'up', 'right' and 'left'.", 200)
frame.add_label("Missiles: 'space'.", 200)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
new_game()
frame.start()