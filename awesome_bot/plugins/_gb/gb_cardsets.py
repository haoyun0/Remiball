from .gb_database import DataList

class CardSets:
    def __init__(self):
        self.datax = DataList('card_sets')
        self.data = self.datax.data
    async def new_card(self, level, idx):
        idx = str(idx)
        if not level in self.data:
            self.data[level] = {}
        self.data[level][idx] = {
            'cover': None,
            'desc': None,
            'name': None,
            'skill_name': None,
            'skill_desc': None,
            'skill_limit': None,
            'output': None
        }
        await self.datax.output()
    async def output(self, level, idx):
        pass
cardset = CardSets()
