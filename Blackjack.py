import time
import random

class NegativeError(Exception):
    pass

class ChoiceException(Exception):
    pass

class Card:
    # class variables
    ranks_value_dict = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8 ,"9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
    all_ranks = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
    all_suits = ("Hearts", "Clubs", "Spades", "Diamonds")

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def __repr__(self):
        special_names = {"A": "Ace", "J": "Jack", "Q": "Queen", "K": "King"}
        if self.rank in special_names:
            return "The {name} of {suit}".format(name = special_names[self.rank], suit = self.suit)    
        else:
            return "The {rank} of {suit}".format(rank = self.rank, suit = self.suit)

    def getValue(self, handValue = 0): # gets the value of the card from its rank. 
        value = 0
        if self.rank == "A" and (handValue + 11 > 21): # special case where Ace can be 11 or 1
                    value = 1
                    return value
        for rankKey in Card.ranks_value_dict:
            if self.rank == rankKey:
                value = Card.ranks_value_dict[rankKey]
                
        return value

class Player:
    
    def __init__(self, name, wallet):
        self.name = name
        self.wallet = wallet 
        self.hand = [] #array of cards
        self.splithand = []
        self.wins = 0
        self.loses = 0
        self.net_earnings = 0
        self.dealer = None

    def __repr__(self):
        return """
        Name: {name}
        Wallet: ${wallet}
        Winning hands: {wins}
        Losing hands:  {loses}
        Net earnings: {net_earnings}
        """.format(name = self.name, wallet = self.wallet, wins = self.wins, loses = self.loses, net_earnings = self.net_earnings)

    def placeBet(self): #place bet in table intervals
        print("Wallet: ${wallet}".format(wallet=self.wallet))
        while True:
            try:
                multiplier = int(input("How many ${minBet} bets do you want to make: ".format(minBet = self.dealer.bet)))
                if multiplier <= 0:
                    raise NegativeError
            except (ValueError, NegativeError):
                print("Please enter a positive integer(whole number)")
                time.sleep(1.5)
                continue
            else:
                break
        mainBet = self.dealer.bet * multiplier
        if mainBet <= self.wallet:
            self.wallet -= mainBet
            self.dealer.mainPot += mainBet 
            print("You made a ${bet} bet".format(bet=mainBet))
            time.sleep(1.5)
            print("Wallet: ${wallet}".format(wallet=self.wallet))
            time.sleep(1.5)
            return mainBet
        else:
            return False
        

    def placeInsurance(self, bet): #place an insurance bet, up to half of your main bet if the dealer has an ace upturned incase dealer has blackjack
        insuranceBet = 0
        while True:
            choice = input("Do you want to place an insurance bet? (y/n): ")
            if choice.lower() != "y" and choice.lower() != "n":
                print("Not a valid choice")
                time.sleep(1.5)
                continue
            else:
                break
        if choice.lower() == "y":
            while insuranceBet <=  0 or insuranceBet > (bet/2):
                try:
                    insuranceBet = float(input("Enter an insurance bet up to half (${half}) of your main bet: ".format(half = bet/2)))
                except ValueError:
                    print("Please only enter numbers")
                    time.sleep(1.5)
                    continue
        if insuranceBet > self.wallet: #in the case that the insurance is larger than the players wallet 
            self.wallet = 0
        self.wallet -= insuranceBet
        self.dealer.insurancePot += insuranceBet
        return insuranceBet

    def hit(self): #take one card from the deck
        rand_suit = random.randint(0,len(Card.all_suits)-1)
        rand_rank = random.randint(0,len(Card.all_ranks)-1)
        card = self.dealer.deck[rand_suit][rand_rank]
        self.hand.append(card)
        return card

    def stand(self): #end turn with hand
        return True
    
    def doubledown(self, mainBet): #double bet and take a card
        self.wallet -= mainBet
        self.dealer.mainPot += mainBet
        print("You drew", self.hit())

    
    def split(self): #split current hand into 2 hands and play with them seperately, draw a card for each hand
        dupe_card = self.hand.pop()
        self.splithand.append(dupe_card)
         

    def fold(self, mainBet): #forfeit half your bet to end your turn
        self.dealer.mainPot -= mainBet/2
        self.wallet += mainBet/2

    def joinTable(self, dealer):
        self.dealer = dealer

    def leaveTable(self):
        self.dealer = None

    def displayHand(self):
        print("Your hand:")
        for card in self.hand:
            print(card)

    def clearHand(self):
        self.hand = []
    
    def playAgain(self):
        while True:
            playAgain = input("play again (y/n): ")
            if playAgain.lower() != "y" and playAgain.lower() != "n":
                print("Not a valid choice")
            else:
                break
        if playAgain.lower() == "y":
            self.clearHand()
            self.dealer.clearHand()
            return True
        return False

class Dealer:

    @staticmethod
    def makeDeck(): #generates a 52 card deck of Card objects
        deck = [[],[],[],[]]
        for i in range(4):
            for j in range(13):
                deck[i].append(Card(Card.all_ranks[j], Card.all_suits[i]))
        return deck

    #def randomCardGen():
    
    def __init__(self, name, bet):
        self.name = name
        self.bet = bet
        self.hand = []
        self.deck = Dealer.makeDeck()
        self.mainPot = 0
        self.splitPot = 0
        self.insurancePot = 0

    def __repr__(self):
        return "This table plays in intervals of ${bet} as bets. The dealer's name is {name}".format(bet = self.bet, name = self.name)

    def deal(self, player): #take a random card from the deck, give 2 to the player and 2 to yourself
        print("You have", player.hit(), "and", player.hit())
        time.sleep(2)
        print("The Dealer has", self.hit())
        self.hit()
        time.sleep(2)

    def checkValue(self, hand): #check the value of a hand
        totalValue = 0
        for i in range(len(hand)):
            totalValue += hand[i].getValue(totalValue)
        return totalValue

    def hit(self): #draw one card from deck
        rand_suit = random.randint(0,len(Card.all_suits)-1)
        rand_rank = random.randint(0,len(Card.all_ranks)-1)
        card = self.deck[rand_suit][rand_rank]
        self.hand.append(card)
        return card
         
    def payPlayer(self, player, winType):
        if winType == "win":
            player.wallet += 2*self.mainPot
            print("You won ${money}".format(money=2*self.mainPot))
        elif winType == "insurance":
            player.wallet += 2*self.insurancePot
            print("You won ${money}".format(money=2*self.insurancePot))
        elif winType == "blackjack":
            player.wallet += 2.5*self.mainPot
            print("You won ${money}".format(money=2.5*self.mainPot))
        elif winType == "draw":
            player.wallet += self.mainPot
            print("You won ${money}".format(money=self.mainPot))

    def doesPlayerDrawCards(self, player, bet):
        while True:
            choice = input("""
            Choose an option:
            1. Hit
            2. Double Down
            3. Stand

            Enter choice: """)
            if choice == "1" or choice.lower() == "hit":
                print("You drew", player.hit())
                return True
            elif choice == "2" or choice.lower() == "double down":
                player.doubledown(bet)
                return True
            elif choice == "3" or choice.lower() == "stand":
                player.stand()
                return False
            else:
                print("Not a valid choice")
                

    def doesPlayerFold(self, round):
        if round == 1: #if this is the first round, asks the user if he wants to fold
            while True:
                foldChoice = input("Fold? (y/n):")
                if foldChoice.lower() != "y" and foldChoice.lower() != "n":
                    print("Not a valid choice")
                else:
                    break
            if foldChoice == "y":
                self.player.fold(bet)
                return True
        return False

    def checkIfBust(self, hand):
        if self.checkValue(hand) > 21:
            return True
        else:
            return False 

    def checkSoft17(self):
        print("The dealers hole card is", self.hand[1])
        while self.checkValue(self.hand) < 17:
            time.sleep(1.5)
            print("The dealer drew", self.hit())
                
    def checkWinDrawLose(self, player):
        playerHandValue = self.checkValue(player.hand)
        dealerHandValue = self.checkValue(self.hand)
        print("The dealer hand has a value of", dealerHandValue)
        time.sleep(1.5)
        print("Your hand has a value of", playerHandValue)
        time.sleep(1.5)
        if dealerHandValue > 21 or dealerHandValue < playerHandValue:
            print("You win")
            self.payPlayer(player, "win")
        elif dealerHandValue == playerHandValue:
            print("Draw")
            self.payPlayer(player, "draw")
        else:
            print("You lose")


    def clearHand(self):
        self.hand = []


class Blackjack:
    #static variables
    dealer_1 = Dealer("Poof", 5)
    dealer_2 = Dealer("Cosmo", 10)
    dealer_3 = Dealer("Wanda", 20)
    dealer_4 = Dealer("Timmy", 50)
    dealer_5 = Dealer("Vicky", 100)
    dealers = (dealer_1, dealer_2, dealer_3, dealer_4, dealer_5)

    def __init__(self, player = None):
        self.player = player


    def createPlayer(self):
        if self.player == None:
            name = input("What is your name?: ")
            self.player = Player(name, 500)

    def showDealers(self):
        n = 1
        for dealer in Blackjack.dealers:
            print("Table", n, ":", dealer)
            n += 1
        time.sleep(3)

    def assignTable(self):
        if self.player.dealer == None:
            self.showDealers()
            while True:
                try:
                    choice = int(input("Which table number do you want to play at?: "))
                except ValueError:
                    print("not a valid choice, please enter a number")
                    time.sleep(1.5)
                else:
                    if choice > 0 and choice <= len(Blackjack.dealers):
                        self.player.joinTable(Blackjack.dealers[choice-1])
                        break
                    else:
                        print("not a valid choice")
                        time.sleep(1.5)
                        

    def game(self):
        self.createPlayer()
        self.assignTable()

        while True:
            bet = self.player.placeBet()
            if bet == False:
                print("Your too broke. Leave or go to a different table")
                break

            self.player.dealer.deal(self.player)
            if self.player.dealer.hand[0].rank == "A": #checks whether the player can place an insurance bet or not
                self.player.placeInsurance(bet) 

            if self.player.dealer.checkValue(self.player.hand) == 21: #this code block checks if the player has blackjack, then checks whether the dealer also has blackjack, then ends the game
                print("{name} has BlackJack".format(name=self.player.name))
                time.sleep(1.5)
                if self.player.dealer.checkValue(self.player.dealer.hand) == 21:
                    print("The dealers hole card is", self.player.dealer.hand[1])
                    time.sleep(1.5)
                    print("Dealer has blackjack, unlucky draw")
                    time.sleep(1.5)
                    self.player.dealer.payPlayer(self.player, "insurance")
                else:
                    print("Dealer doesn't have blackjack, you win")
                    time.sleep(1.5)
                    self.player.dealer.payPlayer(self.player, "blackjack")
                if self.player.playAgain():
                    continue
                else:
                    break
            
            if self.player.dealer.checkValue(self.player.dealer.hand) == 21: #this checks whether or not the dealer has blackjack. then ends the game
                print("The dealers hole card is", self.player.dealer.hand[1])
                time.sleep(1.5)
                print("Dealer has blackjack")
                time.sleep(1.5)
                self.player.dealer.payPlayer(self.player, "insurance")
                if self.player.playAgain():
                    continue
                else:
                    break

            isHandABust = self.player.dealer.checkIfBust(self.player.hand)

            if not isHandABust:
                if self.player.dealer.doesPlayerFold(bet):
                    if self.player.playAgain():
                        continue
                    else:
                        break
            
            while not isHandABust:
                if not self.player.dealer.doesPlayerDrawCards(self.player, bet): # asks the user if they want to hit, doubledown or stand
                    break #breaks the loop if the player stands
                
                isHandABust = self.player.dealer.checkIfBust(self.player.hand)
                self.player.displayHand()
                
            if isHandABust:
                print("Bust. No win")
                time.sleep(1.5) 
                if self.player.playAgain():
                    continue
                else:
                    break

            self.player.dealer.checkSoft17() # checks if the dealer's hand has a value of 17, if not then it draws until so
            time.sleep(1.5)
            self.player.dealer.checkWinDrawLose(self.player)
            time.sleep(1.5)
            if self.player.playAgain():
                continue
            else:
                break