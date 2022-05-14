import nonebot
from .gb_config import Config
from nonebot.permission import Permission
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from nonebot.adapters import Bot, Event


global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())

async def _superuser(bot: "Bot", event: "Event") -> bool:
    return str(event.user_id) in plugin_config.SUPERUSERS

async def _owner(bot: "Bot", event: "Event") -> bool:
    return event.sender.role == 'owner'

async def _admin(bot: "Bot", event: "Event") -> bool:
    return event.sender.role == 'admin'

def Special_list(mylist: list) -> Permission:
    async def _on_list(bot: "Bot", event: "Event") -> bool:
        return str(event.user_id) in mylist
    return Permission(_on_list)

def SSpecial_list(mylist: list) -> Permission:
    async def _on_list(bot: "Bot", event: "Event") -> bool:
        return str(event.user_id) in mylist or str(event.user_id) in plugin_config.SUPERUSERS
    return Permission(_on_list)

SUPERUSER = Permission(_superuser)
OWNER = Permission(_superuser, _owner)
ADMIN = Permission(_superuser, _owner, _admin)