from .gb_database import DataList

class CardSets:
    def __init__(self):
        self.datax = DataList('card_sets')
        self.data = self.datax.data
cardset = CardSets()
