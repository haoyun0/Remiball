from .gb_database import DataList

class Card:
    def __init__(self):
        self.datax = DataList('card_user')
        self.data = self.datax.data
    async def new_user(self, uid: str):
        self.data[uid] = {
            'single': 0,
            'ten': 0,
            'times': 0,
            'card': {}
        }
        await self.datax.output()
    async def modify(self, uid: str, type: str, num: int):
        if type == 'single':
            self.data[uid]['single'] += num
        elif type == 'ten':
            self.data[uid]['ten'] += num
        await self.datax.output()
    async def get(self, uid: str, type: str = 'single') -> int:
        uid = str(uid)
        if uid in self.data:
            if type == 'single':
                return self.data[uid]['single']
            elif type == 'ten':
                return self.data[uid]['ten']
        else:
            return -1
    async def new_card(self, uid: str, level: str, idx: str) -> int:
        uid = str(uid)
        idx = str(idx)
        if not level in self.data[uid]['card']:
            self.data[uid]['card'][level] = {}
        if not idx in self.data[uid]['card'][level]:
            self.data[uid]['card'][level][idx] = {
                'n': 0,#num
                'star': 0#star, fix s to star
            }
            if level == '甲球':
                self.data[uid]['card'][level][idx]['day'] = -1
                self.data[uid]['card'][level][idx]['times'] = 0
        self.data[uid]['card'][level][idx]['n'] += 1
        ans = 0
        if self.data[uid]['card'][level][idx]['n'] == 1:
            ans = 1
            self.data[uid]['card'][level][idx]['star'] = 1
        elif self.data[uid]['card'][level][idx]['n'] == 2:
            ans = 2
            self.data[uid]['card'][level][idx]['star'] = 2
        elif self.data[uid]['card'][level][idx]['n'] == 4:
            ans = 3
            self.data[uid]['card'][level][idx]['star'] = 3
        elif self.data[uid]['card'][level][idx]['n'] == 8:
            ans = 4
            self.data[uid]['card'][level][idx]['star'] = 4
        elif self.data[uid]['card'][level][idx]['n'] == 16:
            ans = 5
            self.data[uid]['card'][level][idx]['star'] = 5
        await self.datax.output()
        return ans
card = Card()
