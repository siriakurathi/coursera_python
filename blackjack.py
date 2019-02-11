# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
deck = None
player = None
dealer = None
message = ""


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
            CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
            
# define hand class
class Hand:
    def __init__(self):
        self.hand = []
      
    def __str__(self):
        handstr = "Hand contains "
        for n in self.hand:
            handstr += " " + str(n)
        return handstr

    def add_card(self, card):
        self.hand.append(card)
    def get_value(self):
        value = 0
        a_count = 0
        for c in self.hand:
            rank = c.get_rank()
            value += VALUES[rank]
            if rank == 'A':
                a_count += 1
        
        if a_count == 0:
            return value
        else:
            if (value + 10) <= 21:
                return value + 10
            else:
                return value

    def draw(self, canvas, pos):
        global CARD_SIZE
        card_pos = pos
        
        for m in self.hand:
            m.draw(canvas,card_pos)
            #print card_pos
            #print CARD_SIZE
            card_pos[0] += CARD_SIZE[0] + 20 
        

# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for x in SUITS:
             for y in VALUES:
                    mycard = Card(x,y)
                    self.deck.append(mycard)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
        
    def __str__(self):
        deckstr = "Deck contains"
        for d in self.deck:
            deckstr += " " + str(d)
        return  deckstr


#define event handlers for buttons
def deal():
    global outcome, in_play , player , dealer , deck,message,score
    if in_play == True:
        outcome = "Player lost"
        score = score - 1
        message = "New Deal?"
    else:
        outcome = ""
        message ="Hit or Stand"
    deck = Deck()
    deck.shuffle()
    player = Hand()
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer = Hand()
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    #print "player " +str(player)
    #print "dealer " +str(dealer)
    in_play = True

def hit():
    global player,deck,outcome,message,in_play,score
    if in_play == False:
        return
    if player.get_value() <= 21:
        player.add_card(deck.deal_card())
        if player.get_value() > 21:
            outcome = "You have busted"
            message = "New Deal?"
            score = score - 1
            in_play = False
    #print player.get_value()   

def stand():
    global player,dealer,deck,outcome,message,in_play,score
    if player.get_value() > 21:
        outcome = "You have busted"
    else:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
            #print dealer.get_value()
        if dealer.get_value() > 21:
            outcome = "Dealer got busted"
            score = score + 1
        elif dealer.get_value() >= player.get_value():
            outcome = "Dealer wins"
            score = score - 1
        else:
            outcome = "Player wins"
            score = score + 1
    message = "New Deal?"
    in_play = False

# draw handler    
def draw(canvas):
    
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("BLACKJACK",(170,70),35,'Black')
    canvas.draw_text("Dealer",(100,175),30,'Red')
    canvas.draw_text("Player",(100,385),30,'Red')
    canvas.draw_text(outcome,(350,180),28,'Red')
    canvas.draw_text(message, (350,375),30,'Red')
    canvas.draw_text("score=" + str(score),(400,100),30,'Red')
    #card = Card("S", "A")
    #card.draw(canvas, [300, 300])
    player.draw(canvas,[100,405])
    dealer.draw(canvas,[100,200])
    #print in_play
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [100 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]], CARD_SIZE)    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric