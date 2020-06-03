#Imports
import random
import sys
###COMMENT
##This branch is to understand the occurence of below bug and fix it.
##ISSUES
##Bug: After stand game doesn't show win or lose in some situation.
##Remove Unnecessary Code
##Try to beautify code a little

SUITS = ['H','S','D','C']
RANKS = ['10','10']


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
        print("Player's Hand value: {}".format(self.hand_value))

    def inc_amnt(self, bet_amnt):
        self.amount += bet_amnt * 2


    def hit(self, deck):
        if self.hand_value >= 21:
            return False           ##Needs editing

        self.player.append(deck.draw())
        self.calc_value()
        self.player[-1].show_format()
        print("Player's Hand value: {}".format(self.hand_value))


    def bet(self):
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
            return False

    def reset(self, deck):
        self.player.clear()
        self.player = [deck.draw() for _ in range(2)]
        self.hand_value = 0
        self.ace = (0, False)
        for card in self.player:
            self.hand_value, self.ace = card.get_value(self.hand_value, self.ace)




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
        while(self.hand_value < 17):
            self.dealer.append(deck.draw())
            self.calc_value()


    def get_value(self):
        return self.hand_value




def check_win(player_value, dealer_value = 0, stand = False):
    if player_value == 21:
        return 'WIN'
    elif player_value > 21:
        return 'LOSE'
    elif dealer_value > 21:
        return 'WIN'
    elif dealer_value == 21:
        return 'LOSE'
    elif player_value > dealer_value and stand == True:
        return 'WIN'
    elif player_value <= dealer_value and stand == True:
        return 'LOSE'
    return


def stmnt(player, dealer, bet_amnt, stand = False):

    if(check_win(player.get_value(), dealer.get_value(), stand) == 'WIN'):
        print("\nPlayer's cards are: ")
        player.show()
        print("Player's Hand value: {}".format(player.get_value()))
        print("\nDealer's cards are: ")
        dealer.show(hidden = False)
        print('Your hand value is: {}'.format(player.get_value()))
        print("Dealer's hand value is: {}".format(dealer.get_value()))
        player.inc_amnt(bet_amnt)
        choice = input("YOU WON\nYou Have in hand money: {}\nYour Luck seems great Today? Want to have another go?(Y/N): ".format(player.get_amnt()))
        if(choice in ['y','Y','yes','Yes']):
            return 'Y'
        else:
            return 'N'
    elif(check_win(player.get_value(), dealer.get_value(), stand) == 'LOSE'):
        print("\nPlayer's cards are: ")
        player.show()
        print("Player's Hand value: {}".format(player.get_value()))
        print("\nDealer's cards are: ")
        dealer.show(hidden = False)
        print('Your hand value is: {}'.format(player.get_value()))
        print("Dealer's hand value is: {}".format(dealer.get_value()))
        if(player.get_amnt() > 49):

            print("YOU LOSE\nYou Have in hand money: {}\nIf at first you don't succeed, Try, try, try again.".format(player.get_amnt()))
            choice = input('Wanna have another go?(Y/N): ')
            if(choice in ['y','Y','yes','Yes']):
                return 'Y'
            else:
                return 'N'
        else:
            print("Thanks for donating that money\nNow Shoo away!")
            return 'N'
    return


#PRObABLY IMPLEMENT MENU FUNCTION HERE

def Game(deck, player):
    dealer = Dealer(deck)                                        #Initialize Dealer
    print('WELCOME TO BLACKJACK')
    print("Player's amount: {}".format(player.get_amnt()))
    bet_amnt = player.bet()
    i = 0
    while not bet_amnt and i < 10:
        bet_amnt = player.bet()
        i += 1
    if not bet_amnt:
        print("Sad you don't wanna play")
        return 'N'
    #If doesn't want to play anymore, return NO
    print("\n\nPlayer's cards are: ")
    player.show()
    print("\n\nDealer's cards are: ")
    dealer.show()
    playing = stmnt(player, dealer, int(bet_amnt))
    if(playing == 'N'):
        return 'N'
    #If want to continue playing, return blank to increase game iteration
    elif(playing == 'Y'):
        return
    while True:
        print("1. Hit\n2. Stand\n3. See Yours\n4. See Dealer's\n5. See Amount\n6. Exit ")
        choice = input('Enter Your Choice: ')
        if choice == '1':
            if(player.get_value() >= 21):
                dealer.hit(deck)
                if(stmnt(player, dealer, int(bet_amnt), stand = True) == 'N'):
                    return 'N'
                else:
                    return
            else:
                player.hit(deck)

        elif choice == '2':
            dealer.hit(deck)
            if (stmnt(player, dealer, int(bet_amnt), stand = True) == 'N'):
                return 'N'
            else:
                return

        elif choice == '3':
            print("\nPlayer's cards are: ")
            player.show()


        elif choice == '4':
            print("\nDealer's cards are: ")
            dealer.show()

        elif choice == '5':
            print("Player's amount: {}".format(player.get_amnt()))

        else:
            print('We hope to see you again')
            return 'N'
        if(player.get_value() == 21):
            if (stmnt(player, dealer, int(bet_amnt), stand = True) == 'N'):
                return 'N'
            else:
                return
        elif(player.get_value() > 21):
            if (stmnt(player, dealer, int(bet_amnt), stand = True) == 'N'):
                return 'N'
            else:
                return



def main():
    #Initialize Deck
    deck = Deck()
    #Initialize Player
    player = Player(deck)
    for i in range(10):
        player.reset(deck)
        playing = Game(deck, player)
        if(playing == 'N'):
            break
    if(i == 9 and playing != 'N'):
        print("Sorry, you can only win this much.")


if __name__ == '__main__':
    main()
