from ..._gb import *

user_info = on_command('抽卡个人信息', aliases={'抽卡个人查询', '抽卡个人资料'}, rule=Check_('抽卡个人信息') ,priority=5)
card_info = on_command('查看卡牌', rule=Check_('查看卡牌'), priority=6)
card_own = on_command('卡牌仓库', rule=Check_('卡牌仓库'), priority=6)
card_tot = on_command('抽卡生涯统计', rule=Check_('抽卡生涯统计'), priority=6)

name_list = ['甲球', '乙球', '丙球', '丁球', '戊球']
buff_list = [10, 2, 1, 0.2, 0.1]

cmds = [
'抽卡个人信息',
'抽卡生涯统计',
'卡牌仓库',
'查看卡牌'
]

con.addcmds('模拟抽卡系统', cmds)
con.addcmds('抽卡系统统计', cmds)

con.addhelp('抽卡系统统计', """
这里可以查看你的抽卡生涯
以及查看卡牌图鉴
指令:
抽卡个人信息
抽卡生涯统计(未完成)
卡牌仓库
查看卡牌(未完成)
""".strip())

datax = card.datax
data = datax.data

@user_info.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    uid = str(event.user_id)
    c = await card.get(uid, 'single')
    if c < 0:
        await card.new_user(uid)
    mystr = "\n拥有单抽券: %d\n拥有十连券: %d" % (await card.get(uid, 'single'), await card.get(uid, 'ten'))
    await con.send(bot, event, mystr, at_sender=True)
    await user_info.finish()

@card_own.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    uid = str(event.user_id)
    c = await card.get(uid, 'single')
    if c < 0:
        await card.new_user(uid)
    mystr = '你拥有:'
    for i in range(len(name_list)):
        if name_list[i] in data[uid]['card']:
            l = 0
            star = [0] * 5
            for idx in data[uid]['card'][name_list[i]]:
                star[data[uid]['card'][name_list[i]][idx]['star'] - 1] += 1
                l += data[uid]['card'][name_list[i]][idx]['n']
            mystr += '\n' + name_list[i] + "%d张, 其中:" % l
            for j in range(5):
                if star[j] > 0:
                    mystr += '\n\t%d星球%d种' % (j + 1, star[j])
    await con.send(bot, event, mystr)
    await card_own.finish()

async def GetBuff(uid):
    uid = str(uid)
    c = await card.get(uid, 'single')
    if c < 0:
        await card.new_user(uid)
    ans = 0
    for i in range(len(name_list)):
        if name_list[i] in data[uid]['card']:
            cnt = 0
            for idx in data[uid]['card'][name_list[i]]:
                cnt += data[uid]['card'][name_list[i]][idx]['star']
            ans += cnt * buff_list[i]
    return ans

export = export()
export.getBuff = GetBuff


