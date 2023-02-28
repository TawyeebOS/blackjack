class Card:
    # class variables
    ranks_value_dict = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8 ,"9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
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
        if self.rank == "A" and (handValue + 11 <= 21): # special case where Ace can be 11 or 1
                    value = 11
                    return value
        for rankKey in Card.ranks_value_dict:
            if self.rank == rankKey:
                value = Card.ranks_value_dict[rankKey]
                
        return value

import random

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

    def placeBet(self, multiplier): #place bet in table intervals
        #multiplier = int(input("Enter a multipler for the min bet as a main bet: "))
        mainBet = self.dealer.bet * multiplier
        self.wallet -= mainBet
        self.dealer.mainPot += mainBet 
        return mainBet

    def placeInsurance(self, insuranceBet): #place an insurance bet, up to half of your main bet if the dealer has an ace upturned incase dealer has blackjack
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
        print(self.hit())

    
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

    def clearHand(self):
        self.hand = []
    
    def playAgain(self):
        playAgain = input("play again: ")
        if playAgain == "y":
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
        print("The Dealer has", self.hit())
        self.hit

    def checkValue(self, hand): #check the value of a hand
        totalValue = 0
        for card in hand:
            totalValue += card.getValue()
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
        elif winType == "insurance":
            player.wallet += 2*self.insurancePot
        elif winType == "blackjack":
            player.wallet += 2.5*self.mainPot
        elif winType == "draw":
            player.wallet += self.mainPot
    
    def clearHand(self):
        self.hand = []
