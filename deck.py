import random
from enums import Suits
from card import Card

class Deck:
    def __init__(self):
        self.__cards = list()
        self.ranks = {
            "2" : 2,
            "3" : 3,
            "4" : 4,
            "5" : 5,
            "6" : 6,
            "7" : 7,
            "8" : 8,
            "9" : 9,
            "10" : 10,
            "J" : 10,
            "Q" : 10,
            "K" : 10,
            "A" : 11
        }
        self.__create_cards()

    def __create_cards(self):
        for suit in Suits:
            for rank, value in self.ranks:
                self.__cards.append(Card(suit, rank, value))
        random.shuffle(self.__cards)
    
    def give_a_card(self):
        if len(self.__cards) == 0:
            self.__create_cards()
        return self.__cards.pop()