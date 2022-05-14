from .gb_database import DataList
import time
import random

class LUCK:
    def __init__(self):
        self.datax = DataList('luck')
        self.data = self.datax.data

    async def GetLuck(self, uid: str) -> int:
        uid = str(uid)
        if not uid in self.data:
            self.data[uid] = {
                'date': -1,
                'luck': -1
            }
        now = time.localtime(time.time())
        day = int(time.strftime("%j", now))
        if self.data[uid]['date'] != day:
            self.data[uid]['date'] = day
            x = random.randint(1, 1000) % 20 + 1
            if x <= 1:
                x = 0
            elif x <= 3:
                x = 1
            elif x <= 6:
                x = 2
            elif x <= 10:
                x = 3
            elif x <= 17:
                x = 4
            elif x <= 20:
                x = 5
            self.data[uid]['luck'] = x
            await self.datax.output()
        return self.data[uid]['luck']

Luck = LUCK()