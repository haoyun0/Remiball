from .._gb import *
import os
datax = Luck.datax
data = Luck.data

luck = on_command('今日运势', aliases={'占卜', '运势'}, rule=Check_('今日运势'), priority=5)

cmds = [
    '今日运势'
]

con.addcmds('基础功能', cmds)
con.addcmds('今日运势', cmds)

luck_list = ['毛茸茸吉', '大吉', '中吉', '小吉', '凶', '大凶']

path2 = os.path.abspath(os.path.dirname(__file__))



@luck.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    uid = str(event.user_id)
    if not uid in data:
        data[uid] = {
            'date': -1,
            'luck': -1
        }
    l = await GetLuck(uid)
    mystr = '今日运势为:\n' + f"[CQ:image,file={os.path.join(path2, 'data', '椛椛', luck_list[l] + '.jpg')}]"
    await con.send(bot, event, mystr, at_sender=True)