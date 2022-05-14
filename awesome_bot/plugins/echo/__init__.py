from .._gb import *


echo0 = on_command('echo', aliases={'echo'}, permission=SUPERUSER, rule=Check_('echo'), priority=1)
echo1 = on_command('test', permission=SUPERUSER, rule=Check_('test'), priority=1)

cmds = [
'echo',
'test'
]
con.addcmds('基础功能', cmds)

@echo0.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    await con.send(bot, event, str(event.get_message()))
    await echo0.finish()

@echo1.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    await con.send(bot, event, str(event.get_message()), auto_escape=True)
    await echo1.finish()
