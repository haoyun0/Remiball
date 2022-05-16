from ..._gb import *

shop_all = on_command('抽卡商店', rule=Check_('抽卡商店') ,priority=5)
shop_buy = on_command('抽卡购买', rule=Check_('抽卡购买') ,priority=5)
shop_buy_more = on_command('抽卡批量购买', rule=Check_('抽卡批量购买') ,priority=5)

cmds = [
'抽卡商店',
"抽卡购买",
"抽卡批量购买"
]

con.addcmds('模拟抽卡系统', cmds)
con.addcmds('抽卡系统商店', cmds)

con.addhelp('抽卡系统商店', """
可购买商品有单抽券和十连券
商品会越买越贵,0点刷新
商品每过一小时会有价格浮动
指令如下：
抽卡商店: 查看商店
抽卡购买 x:购买商品x
抽卡批量购买 x y:尝试购买商品x, y次
""".strip())

datax = DataList('card_shop')
data = datax.data

shop_list = ['single', 'ten']
shop_list_name = ['单抽券', '十连券']

@shop_all.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    uid = str(event.user_id)
    await price_reflash(uid)
    mystr = "\n现在商品价格为:"
    mystr += '\n商品1: 单抽券, 价格: %dQ' % data[uid]['single']
    mystr += '\n商品2: 十连券, 价格: %dQ' % data[uid]['ten']
    mystr += '\n\n商品会越买越贵\n商品价格每小时有浮动\n商品价格0点刷新\n指令:抽卡购买,抽卡批量购买'
    await con.send(bot, event, mystr, at_sender=True)
    await shop_all.finish()

@shop_buy.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    uid = str(event.user_id)
    await price_reflash(uid)
    if msg.isnumeric():
        idx = int(msg) - 1
        if 0 <= idx <= len(shop_list):
            op = shop_list[idx]
            name = shop_list_name[idx]
            m = await coin.get(uid)
            if m >= data[uid][op]:
                await coin.modify(uid, -data[uid][op])
                c = await card.get(uid, op)
                if c < 0:
                    await card.new_user(uid)
                await card.modify(uid, op, 1)
                await add_price(uid, op)
                await con.send(bot, event, '成功购买1张%s\n%s价格变为: %d' % (name, name, data[uid][op]))
            else:
                await con.send(bot, event, '你不够Q')
        else:
            await con.send(bot, event, '没有序号为[%s]的商品' % msg)
    else:
        await con.send(bot, event, '没有序号为[%s]的商品' % msg)
    await shop_buy.finish()

@shop_buy_more.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    msgs = str(event.get_message()).strip().split()
    if len(msgs) != 2:
        await con.send(bot, event, '格式错误')
        await shop_buy_more.finish()
    msg = msgs[0]
    cnt_max = msgs[1]
    if not cnt_max.isnumeric():
        await con.send(bot, event, '格式错误')
        await shop_buy_more.finish()
    cnt_max = int(cnt_max)
    if cnt_max <= 0:
        await con.send(bot, event, '格式错误')
        await shop_buy_more.finish()
    uid = str(event.user_id)
    await price_reflash(uid)
    if msg.isnumeric():
        idx = int(msg) - 1
        if 0 <= idx <= len(shop_list):
            cnt = 0
            op = shop_list[idx]
            name = shop_list_name[idx]
            m = await coin.get(uid)
            z = data[uid][op]
            while m >= z and cnt < cnt_max:
                cnt += 1
                await add_price(uid, op, False)
                z += data[uid][op]
            if cnt > 0:
                c = await card.get(uid, op)
                if c < 0:
                    await card.new_user(uid)
                await coin.modify(uid, - z + data[uid][op])
                await card.modify(uid, op, cnt)
                await datax.output()
                await con.send(bot, event, '成功购买%d张%s\n%s价格变为: %d' % (cnt, name, name, data[uid][op]))
            else:
                await con.send(bot, event, '你不够Q')
        else:
            await con.send(bot, event, '没有序号为[%s]的商品' % msg)
    else:
        await con.send(bot, event, '没有序号为[%s]的商品' % msg)
    await shop_buy_more.finish()

async def price_reflash(uid):
    uid = str(uid)
    day = int(time.strftime("%j", time.localtime(time.time())))
    if not uid in data:
        data[uid] = {
            'day': day,
            'single': 1000,
            'ten': 10000,
            'last': time.time()
        }
    if day != data[uid]['day']:
        data[uid]['day'] = day
        data[uid]['single'] = 1000
        data[uid]['ten'] = 10000
        data[uid]['last'] = time.time()
    luck = await GetLuck(uid)
    while time.time() - data[uid]['last'] > 3600:
        data[uid]['last'] += 3600
        ix = random.randint(95 + luck, 105) / 100
        data[uid]['single'] = int(ix * data[uid]['single'])
        ix = random.randint(95 + luck, 105) / 100
        data[uid]['ten'] = int(ix * data[uid]['ten'])
    await datax.output()

async def add_price(uid, op, save=True):
    luck = await GetLuck(uid)
    if op == 'single':
        ix = random.randint(101 + luck, 110) / 100
        data[uid][op] = int(ix * data[uid][op])
    elif op == 'ten':
        ix = random.randint(105 + luck * 2, 125) / 100
        data[uid][op] = int(ix * data[uid][op])
    if save:
        await datax.output()