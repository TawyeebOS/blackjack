class Card:
    # class variables
    ranks_value_dict = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8 ,"9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
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