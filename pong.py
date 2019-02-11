# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_pos = ((HEIGHT / 2)-(HALF_PAD_HEIGHT))
paddle2_pos = ((HEIGHT / 2)-(HALF_PAD_HEIGHT))
paddle1_vel = 0
paddle2_vel = 0
ball_vel = [0,0]
left_score = 0
right_score = 0
                            

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2,HEIGHT / 2]
    #ball_vel = [0.5,0.5]
    if (direction == LEFT):
        ball_vel[0] = -random.randrange(120,240)/100.0
        ball_vel[1] = -random.randrange(60,80)/100.0
        #print ball_vel
    else:
        ball_vel[0] = random.randrange(120,240)/100.0
        ball_vel[1] = -random.randrange(60,80)/100.0
        #print ball_vel
        
        

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global left_score, right_score  # these are ints
    spawn_ball(LEFT)
    left_score = 0
    right_score = 0
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel,paddle2_vel,PAD_HEIGHT,left_score, right_score

        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    if ((ball_pos[1] + BALL_RADIUS)  >= HEIGHT - 1) or ((ball_pos[1] - BALL_RADIUS) <= 0):
        ball_vel[1] = -ball_vel[1]
    elif((ball_pos[0] + BALL_RADIUS) >= (WIDTH - PAD_WIDTH -1)) or ((ball_pos[0]-BALL_RADIUS) <= PAD_WIDTH + 1):
         ball_vel[0] = -ball_vel[0]
         if ((ball_pos[1] >= paddle1_pos) and (ball_pos[1] <= (paddle1_pos + PAD_HEIGHT)) and ball_vel[0] > 0 ):
            ball_vel[0] += ball_vel[0]*0.1
            ball_vel[1] += ball_vel[1]*0.1
         elif((ball_pos[1] >= paddle2_pos) and (ball_pos[1] <= (paddle2_pos + PAD_HEIGHT)) and ball_vel[0] < 0):
            ball_vel[0] += ball_vel[0]*0.1
            ball_vel[1] += ball_vel[1]*0.1
         else:
             if ball_vel[0] <= 0:
                 left_score += 1
                 spawn_ball(LEFT)
             else:
                 right_score += 1
                 spawn_ball(RIGHT)
                    

    # draw ball
    canvas.draw_circle(ball_pos,BALL_RADIUS,2,"RED","WHITE")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    if(paddle1_pos  <= 0) :
        paddle1_pos = 0
    elif((paddle1_pos + PAD_HEIGHT )>= 399):
            paddle1_pos = HEIGHT - PAD_HEIGHT
    if (paddle2_pos <= 0):
        paddle2_pos = 0
    elif((paddle2_pos +PAD_HEIGHT)>= 399):
        paddle2_pos = HEIGHT - PAD_HEIGHT
    
    # draw paddles
    canvas.draw_polygon([(0,paddle1_pos),(7,paddle1_pos),(7,(paddle1_pos + PAD_HEIGHT)),(0,(paddle1_pos + PAD_HEIGHT))],1,"BLACK","WHITE")
    canvas.draw_polygon([(593,paddle2_pos),(600,paddle2_pos),(600,(paddle2_pos + PAD_HEIGHT)),(593,(paddle2_pos + PAD_HEIGHT))],1,"BLACK","WHITE")
                                                  
    # draw scores
    canvas.draw_text(str(left_score), (200,125), 30, "White") 
    canvas.draw_text(str(right_score), (400,125), 30, "White") 
    
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    #print key
    #print chr(key)
   
    if chr(key) == "W":        
        paddle1_vel = -2       
    elif chr(key) == "S":
        paddle1_vel = 2
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 2
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -2 
    
    #print paddle1_vel,paddle2_vel
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0


def btn_handler():
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
btn = frame.add_button("Restart", btn_handler)


# start frame
new_game()
frame.start()
