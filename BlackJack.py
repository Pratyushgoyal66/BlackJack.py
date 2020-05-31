#Imports
import random
import sys
##PROBABLY IMPLEMENT STAND ALONE MENU FUNCTION
##USE WHILE TRUE FOR LOOPING INSIDE GAME
##ONLY AFTER THAT START IMPLEMENTING THE REAL GAME
##Remeber PLayer is Human in this project
##So Create the game and check win functions accordingly
##Probably decide what the game function is going to look like, then decide about win check
##And finally see if globabl playing parameter is needed or not
##Most probably, 'stand' parameter would be needed to be added to the 'hit' function
##Game function needs to overhauled. There will be a main function which will do the main initialisations, while
##    the game function will run the game and take deck, player and dealer as parameters. Dealer might be created
##    anew.
##Add a add_amnt function to the player class which will increase player's amount if he wins.

#GLOBAL CONSTANTS
SUITS = ['H','S','D','C']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']


class Card:


    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        values = {'A':11, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
                  '10':10, 'J':10, 'Q':10, 'K':10}
        self.value = values[rank]


    def __str__(self):
        return str(self.rank) + ' of ' + str(self.suit)


    def get_value(self, hand_value, ace = (0, False)):
        no_of_A, adjusted = ace
        hand_value += self.value
        if adjusted == False and self.rank == 'A' and hand_value > 21 and no_of_A <= 1:
            no_of_A += 1
            adjusted = True
            hand_value = hand_value - self.value + 1
        ace = (no_of_A, adjusted)
        return hand_value, ace



    def show_format(self):
        print('------')
        print('|{0:<2}  |'.format(self.rank))
        print('|    |')
        print('|    |')
        print('|  {0:>2}|'.format(self.rank))
        print('------\n')




class Deck:


    def __init__(self):
        self.deck = [Card(suit,rank) for suit in SUITS for rank in RANKS]


    def __str__(self):
        deck_contents = ''
        for card in self.deck:
            deck_contents += card.__str__() + '\n'
        return deck_contents


    def __repr__(self):
        deck_contents = ''
        for card in self.deck:
            deck_contents += card.__str__() + '\n'
        return deck_contents


    def shuffle(self):
        random.shuffle(self.deck)


    def refill(self):
        if (self.deck):
            #Returns Not Empty if deck is not empty, False for easier conditional access
            return False
        else:
            self.deck = [Card(suit,rank) for suit in SUITS for rank in RANKS]


    def draw(self):
        if (not self.deck):
            self.refill()
        self.shuffle()
        return self.deck.pop()


    ## Return Value function to be removed if it is deemed useles... Otherwise compltete the function
    ## as and when needed.
    #def return_value(self):
     #   pass



 class Player:


    def __init__(self, deck, amount = 100):
        self.player = [deck.draw() for _ in range(2)]
        self.amount = amount
        self.hand_value = 0
        self.ace = (0, False)
        for card in self.player:
            self.hand_value, self.ace = card.get_value(self.hand_value, self.ace)



    def __str__(self):
        contents = 'Amount Available = ' + str(self.amount) + '\nCards:-\n'
        for card in self.player:
            contents += card.__str__() + '\n'
        return contents


    def __repr__(self):
        show_str = ''
        for card in self.player:
            show_str += '------\n' + '|{0:<2}  |'.format(card.rank) + '\n|    |\n'
            show_str += '|    |\n' + '|  {0:>2}|'.format(card.rank) + '\n------\n'
        return show_str


    def calc_value(self):
        if len(self.player) > 2:
            self.hand_value, self.ace = self.player[-1].get_value(self.hand_value, self.ace)

    def get_amnt(self):
        return self.amount


    def show(self):
        for card in self.player:
            card.show_format()

    def inc_amnt(self, bet_amnt):
        self.amount += bet_amnt * 2


    def hit(self, deck):
        if self.hand_value > 21:
            return False           ##Needs editing

        self.player.append(deck.draw())
        self.calc_value()
        self.player[-1].show_format()


    def bet(self, ctr = 0):
        if(ctr == 10):
            print("\nIt seems like you don't want to actually play the game\n")
            return
        bet_amnt = input('Player bet (50 or 100): ')
        if(bet_amnt == '50' or bet_amnt == '100'):
            if(int(bet_amnt) <= self.amount):
                self.amount -= int(bet_amnt)
                print('Successfull bet of {}$'.format(bet_amnt))
                return bet_amnt
            else:
                #If amount > 50 < 100, betting should be possible with decreased amount.
                #If amount <50, betting should be impossible and the game should end.
                print('Insufficient Funds')
        else:
            print('Bet can only be 50 or 100')
            self.bet(ctr + 1)

    ##Probably Create Stand Function, Depend on class Game and if it is needed or not.


    def get_value(self):
        return self.hand_value



class Dealer():


    def __init__(self, deck):
        self.dealer = [deck.draw() for _ in range(2)]
        self.hand_value = 0
        self.ace = (0, False)
        for card in self.dealer:
            self.hand_value, self.ace = card.get_value(self.hand_value, self.ace)


    def __str__(self):
        for card in self.dealer:
            contents += card.__str__() + '\n'
        return contents


    def __repr__(self):
        show_str = ''
        for card in self.dealer:
            show_str += '------\n' + '|{0:<2}  |'.format(card.rank) + '\n|    |\n'
            show_str += '|    |\n' + '|  {0:>2}|'.format(card.rank) + '\n------\n'
        return show_str


    def calc_value(self):
        if len(self.dealer) > 2:
            self.hand_value, self.ace = self.dealer[-1].get_value(self.hand_value, self.ace)


    def show(self, hidden = True):
        if not hidden:
            for card in self.dealer:
                card.show_format()
        else:
            for card in self.dealer[:-1]:
                card.show_format()


    def hit(self, deck):
        if (self.hand_value) > 21:
            return False  ##needs editing
        while(self.hand_value < 17):
            self.dealer.append(deck.draw()
            self.calc_value()


    def get_value(self):
        return self.hand_value




def check_win(player_value, dealer_value = 0, stand = False):
    if player_value == 21:
        return 'WIN'
    elif dealer_value > 21:
        return 'WIN'
    elif player_value > dealer_value and player_value < 22:
        return 'WIN'
    elif player_value > 21:
        return 'LOSE'
    elif player_value < dealer_value and stand = True:
        return 'LOSE'
    return


def stmnt(player, dealer, stand = False):
    if(check_win(player.get_value(), dealer.get_value(), stand) == 'WIN'):
        player.inc_amnt(bet_amnt)
        choice = input('Your Luck seems great Today? Want to have another go?(Y/N)')
        if(choice in ['y','Y','yes','Yes']):
            return 'Y'
        else:
            return 'N'
    elif(check_win(player.get_value(), dealer.get_value(), stand) == 'LOSE'):
        if(player.get_amnt() > 49):
            choice = input('You seem to still have some money. Wanna have another go?(Y/N)')
            if(choice in ['y','Y','yes','Yes']):
                return 'Y'
            else:
                return 'N'
        else:
            print("We don't cater to people without money.")
            return 'N'
    return

#PRObABLY IMPLEMENT MENU FUNCTION HERE

def Game(deck, player):
    dealer = Dealer(deck)                                        #Initialize Dealer
    print('WELCOME TO BLACKJACK')
    bet_amnt = player.bet()
    #If bet amount is None (Player doesn't want to play game), end game
    if(not bet_amnt):
        return 'N'
    #If doesn't want to play anymore, return NO
    if(stmnt(player, dealer) == 'N'):
        return 'N'
    #If want to continue playing, return blank to increase game iteration
    elif(stmnt(player,dealer) == 'Y'):
        return
    print('1. Hit\n 2.Stand\n3. See\n4. Show\n5. Exit ')
    choice = input('Enter Your Choice: ')
    if choice == '1':
        #Needs editing for not able to hit condition
        #Also add condition if after hit the hand value crosses 21
        if(not player.hit(deck)):
            break
    elif choice == '2':
        print('Your hand value is: {}'.format(player.get_value()))
        dealer.hit(deck)
        print("Dealer's hand value is: {}".format(dealer.get_value()))
        if (stmnt(player, dealer, stand = True) == 'N'):
            return 'N'
        else:
            return
    elif choice == '3':
        print("Dealer's cards are: ")
        dealer.show()

    elif choice == '4':
        print("Player's cards are: ")
        player.show()

    else:
        print('We hope to see you again')
        return 'N'





"""
def main():
    #Initialize Deck
    deck = Deck()
    #Initialize Player
    player = Player(deck)
    for i in range(10):
        if(Game(deck, player) == 'N'):
            break


if __name__ == '__main__':
    main()
"""
