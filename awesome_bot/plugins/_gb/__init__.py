from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot import require, export
from nonebot import on_command
from .gb_database import DataList
from .gb_control import con
from .gb_card import card
from .gb_coin import coin
from .gb_luck import Luck
from .gb_rule import Check_
from .gb_permission import SUPERUSER, ADMIN, OWNER, SSpecial_list, Special_list
import time
import random


async def GetLuck(uid: str) -> int:
    return await Luck.GetLuck(uid)

def get_bot():
    from nonebot import get_bots
    bots = get_bots()
    for i in bots:
        return bots[i]

def segement(type: str, **kwargs):
    msg = {'type': type, 'data': kwargs}
    return msg
