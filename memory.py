# implementation of card game - Memory

import simplegui
import random
m_list = [0,1,2,3,4,5,6,7] * 2
#print m_list
random.shuffle(m_list)
#print m_list
exposed = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
state = 0
turns = 0
          


# helper function to initialize globals
def new_game():
    global turns,state,m_list,exposed
    turns = 0
    state = 0
    random.shuffle(m_list)
    exposed = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
    

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state,firstclick,secondclick,turns
    i = pos[0] / 50
    #print i
    if  exposed[i] == False:
        exposed[i] = True
    else:
        return
    #print exposed
    
    #print exposed
    if state == 0:
        firstclick = i
        state = 1
    elif state == 1:
        secondclick = i
        state = 2
        turns += 1
    elif state == 2:
        if (m_list[firstclick] != m_list[secondclick]):
            exposed[firstclick] = False
            exposed[secondclick] = False
        state = 1
        firstclick = i
       
        #print turns
    else:
        state = 1
    #print exposed
        
    
    
    #print state
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global m_list,turns
    x = 15
    counter = 0
    x1 = 0
    x2 = 49
    for n in m_list:
        if exposed[counter] == True:
            canvas.draw_text(str(n),(x,75),50,'White')
        else :
            canvas.draw_polygon([(x1,0),(x2,0),(x2,99),(x1,99)],1,'Brown','Green')
        counter += 1
        x = x + 50
        x1 += 50
        x2 += 50
        #print n
    label.set_text('Turns = ' + str(turns))

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


