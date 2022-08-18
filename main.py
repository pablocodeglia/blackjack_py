import random, sys, os
from day11_cards_ascii import cards_ascii
from pyfiglet import Figlet

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

class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = base_deck[rank]


class Decks:
    def __init__(self,num_decks) -> None:
        self.num_decks = num_decks
        self.current_deck = {}
        for suit in suits:
            self.current_deck[suit] = [key for key in base_deck.keys()] * num_decks
        

class Player:
    def __init__(self,name) -> None:
        self.name = name
        self.hand = []
        self.count = 0

        self.has_used_ace = False

    def calc_count(self):
        self.count = 0
        for card in self.hand:
            self.count += card.value
        # 
        return self.count
    
    def has_aces(self):
        if any('ace' in card.rank for card in self.hand):
                for card in self.hand:
                    if card.rank == 'ace' and card.value == 11:
                        card.value = 1
                        return True
        else:
            return False

    def show_hand(self):
        print(f"{self.name}'s hand:")
        if len(self.hand) == 1:
            for pieces in zip(*(cards_ascii[self.hand[0].suit][self.hand[0].rank].splitlines(),cards_ascii['back']['back'].splitlines())):
                print("  ".join(pieces))
        else:
            for pieces in zip(*(cards_ascii[card.suit][card.rank].splitlines() for card in self.hand)):
                print("  ".join(pieces))


class GameLogic:
    def __init__(self, deck: Decks, player: Player, dealer: Player):
        self.deck = deck
        self.player1 = player
        self.dealer = dealer
    
    def draw_card(self, player):
        # print(house_deck.current_deck)
        suit = random.choice(list(self.deck.current_deck))
        # get random card of this suit, from cards left on deck
        card_index = random.randint(0,len(list(self.deck.current_deck[suit]))-1)
        rank = self.deck.current_deck[suit][card_index]
        # adds card to player's hand
        player.hand.append(Card(suit,rank))
        # remove card from deck dict
        self.deck.current_deck[suit].pop(card_index)
    
    def check_gameover(self):
        if self.player1.calc_count() == 21:
            if self.dealer.calc_count() == 21:
                self.game_over('draw')
            else:
                self.game_over('21_won')
        elif self.dealer.calc_count() == 21:
            self.game_over('21_lost')
        elif self.player1.calc_count() > 21:
            self.game_over('player_bust')
        elif self.dealer.calc_count() > 21:
            self.game_over('dealer_bust')
        elif self.dealer.calc_count() > self.player1.calc_count():
            self.game_over('lost')
        elif self.player1.calc_count() > self.dealer.calc_count():
            self.game_over('won')

    def deal_round_1(self):
        # Get player1 cards
        self.draw_card(player1)
        self.draw_card(player1)
        # Get dealer card
        self.draw_card(dealer)

        display_round()

        if self.player1.calc_count() == 21:
            self.draw_card(dealer)
            display_round()
            self.check_gameover()
        
        self.deal_round_2()
    
    def deal_round_2(self):
        # Player's turn, until his stands:
        while input("Hit or stand?: ") == 'hit':
            self.draw_card(player1)
            if self.player1.calc_count() > 21 and self.player1.has_aces():
                pass
            elif self.player1.calc_count() >= 21:
                self.check_gameover()
            display_round()        
            
        self.deal_round_3()
    
    def deal_round_3(self):
        while True:
            display_round()
            if self.dealer.calc_count() < 17:
                self.draw_card(dealer)
                if self.dealer.calc_count() > 21 and self.dealer.has_aces():
                    pass 
            else:
                break

        self.check_gameover()
    
    def game_over(self, outcome):
        outcomes ={
            'player_bust':"Bust! You went over 21, the house wins!",
            'dealer_bust':"The dealer's hand busts! You win!",
            '21_won':"You made it to 21, you win!",
            '21_lost':"Dealer has 21, the house wins!",
            'draw':"It's a draw!",
            'won':"Your count is higher than the dealer's! You win!",
            'lost':"The dealer's count is higher than yours! You lose!",
        }
        display_round()
        print(outcomes[outcome])
        
        while True:
            play_again = (input('Do you want to play again? Y/N')).lower()
            try:
                play_again in ['y','n']
            except ValueError:
                pass
            else:
                if play_again == 'y':
                    main()
                else:
                    sys.exit()
    

def cls():
    # Quick function to clear the console
    os.system('cls' if os.name=='nt' else 'clear')

def title_screen():
    cls()
    f = Figlet(font='big')
    print(f.renderText('PY Blackjack'))
    input("\n Press Enter to continue...")


def display_round():
    cls()
    print("################################")
    print("######## Current game ##########")
    print("################################\n")
    player1.show_hand()
    print(f'Player\'s count: {player1.calc_count()}\n')
    for card in player1.hand:
                print(f"card: {card.rank} of {card.suit} (value: {card.value})")
    print("\n###########\n")
    dealer.show_hand()
    print(f'Dealer\'s count: {dealer.calc_count()}')
    print("\n################################\n")


# Sets classes
house_deck = Decks(1)
player1 = Player("Player")
dealer = Player("Dealer")
game = GameLogic(house_deck, player1, dealer)

def main():

    title_screen()
    game.deal_round_1()

if __name__ == "__main__":
    main()