import os
import json


class DataList:
    data : dict = {}
    path :str
    def __init__(self, name: str):
        path2 = os.path.abspath(os.path.dirname(__file__))
        dir = os.path.join(path2, "..", "..", "..", "..","Database","Data_all")
        try:
            os.mkdir(dir)
        except:
            pass
        self.path = os.path.join(dir, name + ".json")
        try:
            with open(self.path, mode="r", encoding="utf-8") as f:
                self.data = json.loads(f.read())
        except:
            pass

    async def output(self):
        with open(self.path, mode="w", encoding="utf-8") as f:
            f.write(json.dumps(self.data))