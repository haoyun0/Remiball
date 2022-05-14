from .gb_database import DataList
import time

class Coin:
    def __init__(self):
        self.datax = DataList('coin')
        self.data = self.datax.data
    async def get(self, uid: str):
        uid = str(uid)
        if uid in self.data:
            return self.data[uid]['coins']
        else:
            return -1

    async def modify(self, uid: str, num: int):
        uid = str(uid)
        if num > 0:
            if 'loan' in self.data[uid]:
                if self.data[uid]['loan'] > 0:
                    x = num // 4
                    if x <= self.data[uid]["loan"]:
                        self.data[uid]["loan"] -= x
                        num -= x
                    else:
                        num -= self.data[uid]["loan"]
                        self.data[uid]["loan"] = 0
        self.data[uid]['coins'] += num

        await self.datax.output()

    async def get_love(self, uid: str):
        uid = str(uid)
        if uid in self.data:
            return self.data[uid]['love']
        else:
            return -1

    async def get_last_day(self, uid: str):
        uid = str(uid)
        day = int(time.strftime("%j", time.localtime(time.time())))
        if self.data[uid]["last"] == day or self.data[uid]['last'] >= 365 or self.data[uid]["last"] == day - 1:
            pass
        else:
            self.data[uid]["last_day"] = 0
        if uid in self.data:
            return self.data[uid]["last_day"]
        else:
            return -1

    async def modify_love(self, uid: str, num: int):
        uid = str(uid)
        self.data[uid]['love'] += num
        await self.datax.output()
coin = Coin()