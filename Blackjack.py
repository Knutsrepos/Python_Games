"""
Blackjack
"""

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
CARD_IMAGES = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
CARD_BACK = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize global variables that are changed during the programm
in_play_G = False
score_G = 0

# Define global constants for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}



class Card:
    """
    The card class. Gives information of a card like suits and rank and draws a card.
    """
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
    
    #draws a card  
    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(CARD_IMAGES, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1]
                          + CARD_CENTER[1]], CARD_SIZE)
        

class Hand:
    """
    The hand class. Adds a card to a hand, calculates the value of a hand and draws a card
    on the appropriate site.  
    """
    def __init__(self):
        self.hand_list=[]	

    def __str__(self):
        return str(self.hand_list)

    def add_card(self, card):
            """
            Add a card to a hand
            """
            return self.hand_list.append(str(card))
            
    def get_value(self):
        """
        Get the value of a hand. An ace is valued as eleven if the remaining cards are summing up to
        below 12. Otherwise it has the value one. 
        """
        hand_value=0
        is_ace=False
        for i in self.hand_list:
                hand_value+=VALUES[list(i)[1]]
                #check the hand for aces
                if list(i)[1]=='A':
                    is_ace=True
        #if aces are in the hand and the value is below 12 add 10            
        if is_ace and hand_value<=11:
            hand_value+=10
        return hand_value
   
    def draw(self, canvas,pos):
        """
        Sets cards in a hand on the canvas.
        """
        for i in self.hand_list:
            Hand_draw=Card(SUITS[SUITS.index(list(i)[0])],RANKS[RANKS.index(list(i)[1])])
            Hand_draw.draw(canvas,pos)
            pos[0]+=CARD_SIZE[0]
            

class Deck:
    """
    The deck class. Gives a clean deck and contains methods to shuffle the deck and deal out cards.
    """
    def __init__(self):
        # Create a Deck object
        self.deck_list=[]
        count=0
        for i in SUITS:
            for j in RANKS:
                self.deck_list.append(str(Card(i,j)))
    
    def __str__(self):
        return "Deck contains "+str(self.deck_list)
    
    def shuffle(self):
        """
        Shuffles the deck
        """
        return random.shuffle(self.deck_list)

    def deal_card(self):
        """
        Deals the last card from the deck and removes it from the deck list 
        """
        self.deal_deck=self.deck_list[-1]
        self.deck_list.pop(-1)
        # Deal a card object from the deck
        return self.deal_deck	
    



def deal():
    """
    The deal button. Starts a new game. Player and computer get each two new cards
    from a shuffled deck.  
    """
    global first_message_G,second_message_G,in_play_G,score_G
    global myDeck_G,playerHand_G,dealerHand_G
    first_message_G="Hit or stand?"
    second_message_G=""
    #If the play is still running while the player hits deal button print message and reduce score 
    if in_play_G:
        score_G-=1
        first_message_G="You Lost! New Deal!"
        second_message_G="Hit or stand?"
    in_play_G=True
    #Get a new deck
    myDeck_G=Deck()
    #Shuffle deck
    myDeck_G.shuffle()
    #Give player hand
    playerHand_G=Hand()
    #Give dealer's hand
    dealerHand_G=Hand()
    #Add two cards to each hand
    playerHand_G.add_card(myDeck_G.deal_card())
    dealerHand_G.add_card(myDeck_G.deal_card())
    playerHand_G.add_card(myDeck_G.deal_card())
    dealerHand_G.add_card(myDeck_G.deal_card())
  
def hit():
    """
    The hit button. Gives player a new card if he's not busted. Otherwise it gives a message,
    updates the score and asks for a new game.  
    """
    global in_play_G,first_message_G,second_message_G,score_G
    if playerHand_G.get_value()<=21:
        playerHand_G.add_card(myDeck_G.deal_card())    
        if playerHand_G.get_value()>21:
            first_message_G="You have busted!"
            second_message_G="New Deal?"
            in_play_G=False
            score_G-=1

    
def stand():
    """
    The stand button. If the player isn't busted, the dealer keeps taking cards unless he
    is at least equal to 17. Afterwards hands are compared. 
    """
    global in_play_G,first_message_G,second_message_G,score_G
    # Check if hand is in play
    in_play_G=False
    #Check if player is busted
    if playerHand_G.get_value()<=21:
        first_message_G="Dealer's turn!"
        #Dealer takes cards unless he is under 17
        while dealerHand_G.get_value()<17:
            dealerHand_G.add_card(myDeck_G.deal_card())
        #Give message and increment player score if dealer's point is over 21
        if dealerHand_G.get_value()>21:
            first_message_G="Dealer has busted!"
            second_message_G="New Deal?"
            score_G+=1
        else:
            #If not anybody is busted, compare player and computer hands, declare the winner and
            #adjust score accordingly.  
            if dealerHand_G.get_value()>=playerHand_G.get_value():
                first_message_G="Dealer wins by "+str(dealerHand_G.get_value())+" to "+str(playerHand_G.get_value())+"!"
                second_message_G="New Deal?"
                score_G-=1
            else:
                first_message_G="Player wins by "+str(playerHand_G.get_value())+" to "+str(dealerHand_G.get_value())+"!"
                second_message_G="New Deal?"
                score_G+=1
    else:
        first_message_G="You have busted!"
        second_message_G="New Deal?"

   
def draw(canvas):
    """
    The draw handler.    
    """
    global in_play_G,score_G
    #Draw "Blackjack"
    canvas.draw_text("Blackjack",(250,100),55,'Red','monospace')
    #Draw messages
    canvas.draw_text(first_message_G,(150,300),40,'Aqua')
    canvas.draw_text(second_message_G,(150,350),40,'Aqua')
    #Draw players cards
    canvas.draw_text('Player',(50,390),25,'Silver')
    playerHand_G.draw(canvas,[50,400])
    #Draw dealers cards
    canvas.draw_text('Dealer',(50,140),25,'Silver')
    dealerHand_G.draw(canvas,[50,150])
    #Draw scores
    canvas.draw_text("Your Score",(410,520),40,'Aqua')
    canvas.draw_text(str(score_G),(490,570),40,'Aqua')
    #If it's player's turn, hide the first dealer's card
    if in_play_G:
        canvas.draw_image(CARD_BACK,CARD_BACK_CENTER,CARD_BACK_SIZE, [50+CARD_BACK_CENTER[0],
                          150+CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    

"""
Main
"""
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
