from ..._gb import *

user_info = on_command('抽卡个人信息', aliases={'抽卡个人查询', '抽卡个人资料'}, rule=Check_('抽卡个人信息') ,priority=5)
card_info = on_command('查看卡牌', rule=Check_('查看卡牌'), priority=6)
card_own = on_command('卡牌仓库', rule=Check_('卡牌仓库'), priority=6)
card_tot = on_command('抽卡生涯统计', rule=Check_('抽卡生涯统计'), priority=6)

name_list = cardpool.data['level_name']
level_num = cardpool.data['level_num']
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
抽卡生涯统计
卡牌仓库
查看卡牌(未完成)
""".strip())

con.addhelp('卡牌仓库', """
指令: 卡牌仓库
可选参数:
[品质] [未拥有] [第几页]
请按顺序，其中品质为必须参数
每页十种球
例：
卡牌仓库 甲球
（默认甲球第一页）
卡牌仓库 丁球 10
（丁球第十页）
卡牌仓库 丙球 未拥有 10
（未拥有的丙球第十页）
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
    msg = str(event.get_message()).strip().split()
    c = await card.get(uid, 'single')
    if c < 0:
        await card.new_user(uid)
    if len(msg) > 0:
        if msg[0] in name_list:
            if len(msg) > 1:
                if msg[1] == '未拥有':
                    flag = False
                    if len(msg) > 2:
                        if msg[2].isnumeric():
                            page = int(msg[2])
                            if page <= 0:
                                await con.send(bot, event, '参数错误，请认真查看帮助')
                                await card_own.finish()
                        else:
                            page = 1
                            await con.send(bot, event, '参数错误，请认真查看帮助')
                            await card_own.finish()
                    else:
                        page = 1
                elif msg[1].isnumeric():
                    page = int(msg[1])
                    flag = True
                    if page <= 0:
                        await con.send(bot, event, '参数错误，请认真查看帮助')
                        await card_own.finish()
                else:
                    flag = True
                    page = 1
                    await con.send(bot, event, '参数错误，请认真查看帮助')
                    await card_own.finish()
            else:
                flag = True
                page = 1
            if flag:
                page -= 1
                if msg[0] in data[uid]['card']:
                    mylist = []
                    for idx in range(level_num[name_list.index(msg[0])]):
                        if str(idx) in data[uid]['card'][msg[0]]:
                            mylist.append('id:%d, %d星, 拥有%d张' % (idx, data[uid]['card'][msg[0]][str(idx)]['star'], data[uid]['card'][msg[0]][str(idx)]['n']))

                    if page*10 >= len(mylist):
                        page = (len(mylist) - 1) // 10
                    st = page * 10
                    mystr = '\n目前为你展示%s第%d页' % (msg[0], page + 1)
                    for idx in range(st, st + 10):
                        if idx >= len(mylist):
                            break
                        mystr += '\n' + mylist[idx]
                    await con.send(bot, event, mystr, at_sender=True)
                else:
                    await con.send(bot, event, '你没有%s' % msg[0])
            else:
                page -= 1
                if msg[0] in data[uid]['card']:
                    mylist = []
                    for idx in range(level_num[name_list.index(msg[0])]):
                        if not str(idx) in data[uid]['card'][msg[0]]:
                            mylist.append('id:%d, 未拥有' % idx)
                    if page*10 >= len(mylist):
                        page = (len(mylist) - 1) // 10
                    st = page * 10
                    mystr = '\n目前为你展示未有%s第%d页' % (msg[0], page + 1)
                    for idx in range(st, st + 10):
                        if idx >= len(mylist):
                            break
                        mystr += '\n' + mylist[idx]
                    await con.send(bot, event, mystr, at_sender=True)
                else:
                    await con.send(bot, event, '你所以%s都没有' % msg[0])
        else:
            await con.send(bot, event, '不存在稀有度[%s]' % msg[0])
    else:
        mystr = '\n你拥有:'
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
        mystr += '\n\n输入帮助 卡牌仓库查看进一步帮助'
        await con.send(bot, event, mystr, at_sender=True)
    await card_own.finish()

@card_tot.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    # for uid in data:
    #     points = 0
    #     times = 0
    #     for level in data[uid]['card']:
    #         for idx in data[uid]['card'][level]:
    #             times += data[uid]['card'][level][idx]['n']
    #             if level == '甲球':
    #                 points += data[uid]['card'][level][idx]['n']*20
    #             if level == '乙球':
    #                 points += data[uid]['card'][level][idx]['n']*5
    #             if level == '丙球':
    #                 points += data[uid]['card'][level][idx]['n']*2
    #             if 's' in data[uid]['card'][level][idx]:
    #                 del data[uid]['card'][level][idx]['s']
    #     data[uid]['points'] = points
    #     data[uid]['times'] = times
    # await datax.output()
    # await con.send(bot, event, '数据修复完成')
    uid = str(event.user_id)
    if data[uid]['times'] < 50:
        await con.send(bot, event, '抽卡次数过少，暂不参与统计')
        await card_tot.finish()
    tot = 1
    now = data[uid]['points'] / data[uid]['times']
    rank = 1
    for uuid in data:
        if data[uuid]['times'] >= 50:
            tot += 1
            if now < data[uuid]['points'] / data[uuid]['times']:
                rank += 1
    mystr = '\n你总共抽过%d次卡' % data[uid]['times']
    mystr += '\n你在%d名玩家中排行第%d' % (tot, rank)
    bit = (rank - 1) / tot
    if bit < 0.05:
        mystr += '\n鉴定为超级欧皇'
    elif bit < 0.1:
        mystr += '\n鉴定为欧皇'
    elif bit < 0.3:
        mystr += '\n鉴定为欧洲人'
    elif bit < 0.7:
        mystr += '\n鉴定为普通人'
    elif bit < 0.9:
        mystr += '\n鉴定为非洲人'
    elif bit < 0.95:
        mystr += '\n鉴定为非酋'
    elif bit < 1:
        mystr += '\n鉴定为超级非酋'
    await con.send(bot, event, mystr, at_sender=True)
    await card_tot.finish()


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


