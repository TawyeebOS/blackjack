class Card:
    # class variables
    ranks_value_dict = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8 ,"9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
    all_ranks = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
    all_suits = ("Hearts", "Clubs", "Spades", "Diamonds")

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def __repr__(self):
        return "This card is the {rank} of {suit}".format(rank = self.rank, suit = self.suit)

    def getValue(self, handValue = 0): # gets the value of the card from its rank. 
        value = 0
        if self.rank == "A" and (handValue + 11 <= 21): # special case where Ace can be 11 or 1
                    value = 11
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
        pass

    def placeInsurance(self, mainBet): #place an insurance bet, up to half of your main bet if the dealer has an ace upturned incase dealer has blackjack
        pass

    def hit(self): #take one card from the deck
        pass

    def stand(self): #end turn with hand
        pass
    
    def doubledown(self): #double bet and take a card
        pass
    
    def split(self): #split current hand into 2 hands and play with them seperately, draw a card for each hand
        pass

    def fold(self): #forfeit half your bet to end your turn
        pass
    
    def joinTable(self, dealer):
        self.dealer = dealer

    def leaveTable(self):
        self.dealer = None
    
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

    def __repr__(self):
        return "This table plays in intervals of ${bet} as bets. The dealer's name is {name}".format(bet = self.bet, name = self.name)

    def deal(self): #take a random card from the deck, give 2 to the player and 2 to yourself
        pass

    def checkValue(self, hand): #check the value of a hand
        pass

    def hit(self): #draw one card from deck
        pass
        