import random, sys, os
from day11_cards_ascii import cards_ascii

base_deck = {
    'ace' : 11,
    '2' : 2,
    '3' : 3,
    '4' : 4,
    '5' : 5,
    '6' : 6,
    '7' : 7,
    '8' : 8,
    '9' : 9,
    '10' : 10,
    'J' : 10,
    'Q' : 10,
    'K' : 10,
}

suits = ['spades','hearts','diamonds','clubs']

class Decks:

    def __init__(self,num_decks) -> None:
        self.num_decks = num_decks
        self.deck = {}
        for suit in suits:
            self.deck[suit] = [key for key in base_deck.keys()] * num_decks
        
    def get_card(self):
        while True:
            try:
                suit = random.choice(list(self.deck))
                card_index = random.randint(0,len(list(self.deck[suit]))-1)
                card = self.deck[suit].pop(card_index)
            except ValueError:
                pass
            else:        
                return([suit,card])
        # return(self.deck.pop(card))

class Player:
    def __init__(self,name) -> None:
        self.name = name
        self.hand = []
        self.count = 0
        self.has_used_ace = False

    def calc_count(self):
        print(f"{self.name}'s count:\n- {self.count}")
    
    def show_hand(self):
        print(f"{self.name}'s hand:")
        for pieces in zip(*(cards_ascii[card[0]][card[1]].splitlines() for card in self.hand)):
            print("  ".join(pieces))
    
    def draw_card(self,deck:Decks):
        card = deck.get_card()
        if card[1] == 'ace':
            self.has_used_ace = False
        self.hand.append(card)
        self.count += base_deck[card[1]]

# Sets classes
house_deck = Decks(1)
player1 = Player("Player")
dealer = Player("Dealer")

def cls():
    # Quick function to clear the console
    os.system('cls' if os.name=='nt' else 'clear')

def display_round():
    cls()
    print("################################")
    print("######## Current game ##########")
    print("################################\n")
    player1.show_hand()
    player1.calc_count()
    print("\n###########\n")
    dealer.show_hand()
    dealer.calc_count()
    print("\n################################\n")

def game_over(outcome):
    outcomes ={
        'bust':"Bust! You went over 21, the house wins!",
        'house-bust':"The dealer's hand busts! You win!",
        '21':"You made it to 21, you win!",
        'house-21':"Dealer has 21, the house wins!",
        'draw':"It's a draw!",
        'win':"Your count is higher than the dealer's! You win!",
        'lost':"The dealer's count is higher than yours! You lose!",
    }
    # cls()
    display_round()
    print(outcomes[outcome])
    sys.exit()

def main():
    cls()
    # Get player1 cards
    print("You got two cards from the deck:")
    player1.draw_card(house_deck)
    player1.draw_card(house_deck)

    # Get dealer card
    dealer.draw_card(house_deck)

    display_round()

    if player1.count == 21:
        dealer.draw_card(house_deck)
        if dealer.count == 21:
            game_over('draw') 
        else:
            game_over('21')    

    # Player's turn, until his stands:
    while input("Hit or stand?: ") == 'hit':
    
        player1.draw_card(house_deck)
        
        display_round()

        if player1.count == 21:
            dealer.draw_card(house_deck)
            if dealer.count == 21:
                game_over('draw')
            else:
                game_over('21')
        elif player1.count > 21:
            if any('ace' in card for card in player1.hand):
                if not player1.has_used_ace:
                    player1.count -= 10
                    player1.has_used_ace = True
                    display_round()
                else:
                    game_over('bust')
            else:
                game_over('bust')
    
    # User stood, so now it's the Dealer's turn:
    while True:
        display_round()
        if dealer.count < 17:
            dealer.draw_card(house_deck)
            if dealer.count > 21:
                if any('ace' in card for card in dealer.hand):
                    if not dealer.has_used_ace:
                        dealer.count -= 10
                        dealer.has_used_ace = True
                else:
                    game_over('house-bust')
        else:
            break
    if player1.count == dealer.count:
        game_over('draw')
    elif player1.count > dealer.count:
        game_over('win')
    elif dealer.count > player1.count:
        game_over('lost')

if __name__ == "__main__":
    main()