from ..._gb import *
import os
from nonebot import export
tiger = on_command('球球机', rule=Check_('球球机'), aliases={'老虎机', '老球机'}, priority=8)
tiger_tot = on_command('球球机统计', rule=Check_('球球机统计'), aliases={'老虎机统计', '老球机统计'}, priority=8)

cmds = [
'球球机',
'球球机统计'
]

con.addcmds('好感度系统', cmds)
con.addcmds('小游戏', cmds)
con.addcmds('基础功能', cmds)

con.addhelp('老虎机', """
球球机只跟运气有关，扭就完事了
扭到3只相同的球才有奖励
参数为筹码，同样只能为10的正数次方
运气好的话，能稳定赚Q
每天每人天只能抽100次
指令:
""".strip(), ['老球机', '球球机'])

rate = [6666, 1000, 500, 200, 100, 50, 20, 10, 5, 2]
per = [0.0001, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.31, 1]
path2 = os.path.abspath(os.path.dirname(__file__))
image_url = [
"[CQ:image,file=2300b19b4d31baa9f0ee2fa01b71cec93665-100-100.png,url=https://gchat.qpic.cn/gchatpic_new/323690346/963370810-2229752578-2300B19B4D31BAA9F0EE2FA01B71CEC9/0?term=2]",
"[CQ:image,file=cfd7af777d77e4051497e07d83e3e4f33528-100-100.jpg,url=https://gchat.qpic.cn/gchatpic_new/323690346/963370810-2209233301-CFD7AF777D77E4051497E07D83E3E4F3/0?term=2]",
"[CQ:image,file=9a29ce17a5a78d4532ec496eb647f1bf3404-100-100.jpg,url=https://gchat.qpic.cn/gchatpic_new/323690346/963370810-2668381819-9A29CE17A5A78D4532EC496EB647F1BF/0?term=2]",
"[CQ:image,file=d451bbbb344fdb2134d34de2e54ed93e3211-100-100.jpg,url=https://gchat.qpic.cn/gchatpic_new/323690346/963370810-2369587863-D451BBBB344FDB2134D34DE2E54ED93E/0?term=2]",
"[CQ:image,file=c1bde3e64df86a33865bca4c0cbc58103009-100-100.jpg,url=https://gchat.qpic.cn/gchatpic_new/323690346/963370810-3086637182-C1BDE3E64DF86A33865BCA4C0CBC5810/0?term=2]",
"[CQ:image,file=fcf674b2fe3cf03db17e31e55ac293cc2506-100-100.jpg,url=https://gchat.qpic.cn/gchatpic_new/323690346/963370810-2288811735-FCF674B2FE3CF03DB17E31E55AC293CC/0?term=2]",
"[CQ:image,file=8887cee08854324d2b22b2cbe00241f43606-100-100.jpg,url=https://gchat.qpic.cn/gchatpic_new/323690346/963370810-2910859203-8887CEE08854324D2B22B2CBE00241F4/0?term=2]",
"[CQ:image,file=c90bbd8854600a4f50f00537052107373382-100-100.jpg,url=https://gchat.qpic.cn/gchatpic_new/323690346/963370810-2299492410-C90BBD8854600A4F50F0053705210737/0?term=2]",
"[CQ:image,file=f008195c3580d82a9f289a959cdf37ab3155-100-100.jpg,url=https://gchat.qpic.cn/gchatpic_new/323690346/963370810-2220607859-F008195C3580D82A9F289A959CDF37AB/0?term=2]",
"[CQ:image,file=1040079e489967bfe28a09382e8513a43113-100-100.jpg,url=https://gchat.qpic.cn/gchatpic_new/323690346/963370810-2278254535-1040079E489967BFE28A09382E8513A4/0?term=2]"
]

datax = DataList('tiger')
data = datax.data


def GetBall(id):
    return image_url[int(id)]
    #return f"[CQ:image,file={os.path.join(path2, 'data', '球', str(id) + '.png')}]"

limit = {}
times = {}

@tiger.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    z = str(event.get_message()).strip()
    flag = True
    if z.isnumeric():
        if z[0] == '1' and len(z) > 1:
            for i in range(1, len(z)):
                if z[i] != '0':
                    flag = False
                    break
        else:
            flag = False
    else:
        flag = False

    if not flag:
        await con.send(bot, event, "请下注且下正确的金额", at_sender=True)
        await tiger.finish()
    z = int(z)
    m = await coin.get(event.user_id)
    if m < z:
        await con.send(bot, event, "你不够Q")
        await tiger.finish()

    uid = str(event.user_id)
    await user_exmine(uid)
    if data[uid]['day_times'] >= 100:
        await con.send(bot, event, "你今天不能再抽了")
        await tiger.finish()



    data[uid]['Q_in'] += z
    data[uid]['day_in'] += z
    data[uid]['times'] += 1
    data[uid]['day_times'] += 1
    await coin.modify(event.user_id, -z)


    x = random.randint(1, 100000)
    x = x % 1000
    g = await GetLuck(event.user_id)
    mystr = "你扭到了:\n"
    if x <= 200 - g * 20:
        k = random.random()
        s = 0
        ans = 0
        for i in range(10):
            s += per[i]
            if k <= s:
                ans = i
                break
        for _ in range(3):
            mystr += GetBall(ans)
        mystr += '\n获得了%d倍Q，共%d的奖励' % (rate[ans],  rate[ans] * z)
        await coin.modify(event.user_id, rate[ans] * z)
        data[uid]['double'] += rate[ans]
        data[uid]['Q_out'] += rate[ans] * z
        data[uid]['day_double'] += rate[ans]
        data[uid]['day_out'] += rate[ans] * z
    else:
        p = [0, 0, 0]
        for j in range(3):
            p[j] = random.randint(1, 1000) % 10
        while p[0] == p[1] and p[1] == p[2]:
            for j in range(3):
                p[j] = random.randint(1, 1000) % 10
        for j in range(3):
            mystr += GetBall(p[j])
    await datax.output()
    await con.send(bot, event, mystr, at_sender=True)
    await tiger.finish()

@tiger_tot.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    uid = str(event.user_id)
    await user_exmine(uid)
    mystr = ""
    mystr += '\n总共玩了%d次' % data[uid]['times']
    mystr += '\n总共获得了%d倍的Q' % data[uid]['double']
    mystr += '\n总共投入%dQ' % data[uid]['Q_in']
    mystr += '\n总共收入%dQ' % data[uid]['Q_out']
    mystr += '\n今天玩了%d次' % data[uid]['day_times']
    mystr += '\n今天获得了%d倍的Q' % data[uid]['day_double']
    mystr += '\n今天投入%dQ' % data[uid]['day_in']
    mystr += '\n今天收入%dQ' % data[uid]['day_out']
    await con.send(bot, event, mystr, at_sender=True)
    await tiger_tot.finish()

async def user_exmine(uid: str):
    uid = str(uid)
    if not uid in data:
        data[uid] = {
            "double": 0,
            "times": 0,
            "Q_in": 0,
            "Q_out": 0,
            'date': -1,
            'day_times': 0,
            'day_double': 0,
            "day_in": 0,
            "day_out": 0
        }
        await datax.output()
    day = int(time.strftime("%j", time.localtime(time.time())))
    if day != data[uid]['date']:
        data[uid]['date'] = day
        data[uid]['day_double'] = 0
        data[uid]['day_in'] = 0
        data[uid]['day_out'] = 0
        data[uid]['day_times'] = 0
        await datax.output()

def GetBonus(uid):
    return data[uid]['day_out']

export = export()
export.getF = GetBonus