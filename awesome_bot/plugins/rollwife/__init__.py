from .._gb import *


rollwife = on_command("扭蛋", rule=Check_('扭蛋', 'group'), priority=6)
rollwife2 = on_command("rollwife", rule=Check_('rollwife', 'group'), priority=6)
rollwife3 = on_command("rolldad", rule=Check_('rolldad', 'group'), priority=6)
rollwife4 = on_command("rollson", rule=Check_('rollson', 'group'), priority=6)
rollwife5 = on_command("rollmom", rule=Check_('rollmom', 'group'), priority=6)
rollwife6 = on_command("rolldaughter", rule=Check_('rolldaughter', 'group'), priority=6)

cmds=[
'扭蛋',
'rollwife',
'rolldad',
'rollson',
'rollmom',
'rolldaughter'
]

con.addcmds('基础功能',cmds)
con.addcmds('扭蛋',cmds)
con.addhelp('扭蛋',"""
扭蛋帮助：
扭蛋：随机扭一个群友
附加功能：
rolldad
rollmom
rollwife
rollson
rolldaughter
""".strip())


@rollwife.handle()
async def handle_rollwife(bot: Bot, event: Event, state: T_State):   
    if str(event.message).strip():
        return
    mystr = await get_random_member(bot, event)
    await bot.send(event, f"你扭到了{mystr}", at_sender=True)

@rollwife2.handle()
async def handle_rollwife2(bot: Bot, event: Event, state: T_State):    
    if str(event.message).strip():
        return
    mystr = await get_random_member(bot, event)
    await bot.send(event, f"你的老婆是{mystr}", at_sender=True)

@rollwife3.handle()
async def handle_rollwife3(bot: Bot, event: Event, state: T_State): 
    if str(event.message).strip():
        return
    mystr = await get_random_member(bot, event)
    await bot.send(event, f"你的爸爸是{mystr}", at_sender=True)  

@rollwife4.handle()
async def handle_rollwife4(bot: Bot, event: Event, state: T_State): 
    if str(event.message).strip():
        return
    mystr = await get_random_member(bot, event)
    await bot.send(event, f"你的儿子是{mystr}", at_sender=True) 

@rollwife5.handle()
async def handle_rollwife5(bot: Bot, event: Event, state: T_State): 
    if str(event.message).strip():
        return
    mystr = await get_random_member(bot, event)
    await bot.send(event, f"你的妈妈是{mystr}", at_sender=True)   

@rollwife6.handle()
async def handle_rollwife6(bot: Bot, event: Event, state: T_State):    
    if str(event.message).strip():
        return
    mystr = await get_random_member(bot, event)
    await bot.send(event, f"你的女儿是{mystr}", at_sender=True)

async def get_random_member(bot: Bot, event : Event):
    all = await bot.call_api("get_group_member_list",group_id=event.group_id)
    l = len(all)
    flag = True
    while flag:
        r = random.randint(0, l - 1)
        flag = all[r]['user_id'] == 2720673792
    if all[r]['card']:
        return all[r]['card']
    else:
        return all[r]['nickname']