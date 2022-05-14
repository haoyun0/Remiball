import nonebot
from nonebot.rule import Rule
from nonebot.typing import T_State
from .gb_config import Config
from .gb_control import con
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from nonebot.adapters import Bot, Event, MessageSegment

global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())


async def _private_only(bot: "Bot", event: "Event", state: T_State) -> bool:
    return event.message_type == 'private'

async def _group_only(bot: "Bot", event: "Event", state: T_State) -> bool:
    return event.message_type == 'group'


def Check_(cmd: str, type: str = None) -> Rule:
    async def is_ban(bot: "Bot", event: "Event", state: T_State) -> bool:
        msg = str(event.get_message()).strip()
        try:
            if event.group_id in plugin_config.ban:
                if 'cmd_head' in plugin_config.ban[event.group_id]:
                    for q in plugin_config.ban[event.group_id]['cmd_head']:
                        if q in msg:
                            if msg.index(q) == 0:
                                return False
                if 'user' in plugin_config.ban[event.group_id]:
                    for q in plugin_config.ban[event.group_id]['user']:
                        if event.user_id == q:
                            return False
        except:
            pass
        return True
    async def is_open(bot: "Bot", event: "Event", state: T_State) -> bool:
        if cmd:
            return con.check(event, cmd)
        else:
            return True
    if type:
        if type == 'group' or type == 'GROUP':
            return Rule(is_ban, is_open, _group_only)
        elif type == 'private' or type == 'PRIVATE':
            return Rule(is_ban, is_open, _private_only)
        else:
            return Rule(is_ban, is_open)
    else:
        return Rule(is_ban, is_open)
