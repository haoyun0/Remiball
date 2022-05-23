from .gb_database import DataList

class CardPools:
    def __init__(self):
        self.datax = DataList('card_pool')
        self.data = self.datax.data
cardpool = CardPools()