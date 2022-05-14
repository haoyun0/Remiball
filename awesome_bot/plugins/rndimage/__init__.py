from .._gb import *
import nonebot
from nonebot import on_message
from ..control import restart
from .datasource import *
from .hash import *
import os

datax = DataList('image')
data = datax.data

limit_hamming = 12

scheduler = require('nonebot_plugin_apscheduler').scheduler

image_everyday = on_command("每日图", rule=Check_('每日图', 'group'), permission=SUPERUSER, priority=3)
image_random = on_command("随机图", rule=Check_('随机图'), priority=6)
image_add_gallery = on_command("增加图库", aliases={'增添图库', '添加图库', '新建图库'}, rule=Check_('增加图库'), permission=SUPERUSER, priority=3)
image_del_gallery = on_command("删除图库", aliases={'删掉图库', '移除图库'}, rule=Check_('删除图库'), permission=SUPERUSER, priority=3)
image_submit = on_command("提交图片", aliases={'提交图库', '上传图片', '添加图片'}, rule=Check_("提交图片"), priority=5)
image_examine = on_command("图片审核", aliases={"审核图片", '图片检测', '检测图片'}, rule=Check_("图片审核"), permission=SUPERUSER, priority=5)
image_cnt = on_command("图片数量", rule=Check_("图片数量"), priority=5)
image_limit = on_command("图片检测阈值", rule=Check_("图片检测阈值"), permission=SUPERUSER, priority=5)
image_r18 = on_command("随机图r18", rule=Check_("随机图r18"), permission=ADMIN, priority=5)
cmds = [
"每日图",
"随机图",
'增加图库',
'删除图库',
'提交图片',
'图片审核',
'图片数量',
"图片检测阈值",
'随机图r18'
]


st = []
async def all_handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    comd = event.raw_message.replace(str(event.get_message()), "", 1)
    comd = comd[1:]
    if comd in data['gallery']:
        cid = data['gallery'].index(comd)
        handler = st[cid]
        if event.message_type == 'group':
            if event.group_id in data['r18']:
                img = get_image(comd, True)
            else:
                img = get_image(comd)
        else:
            img = get_image(comd, True)
        if img:
            await con.send(bot, event, img)
        else:
            await con.send(bot, event, '图库为空')
        if msg:
            await get_more_image(bot, event, msg)
        await handler.finish()
    else:
        await con.send(bot, event, '图库不存在')

str_help = "蕾米球目前有以下图库："
for g in data['gallery']:
    str_help += "\n" + g
    cmds.append(g)
    st.append(on_command(g, rule=Check_(g), priority=6, handlers=[all_handle]))
con.addcmds('基础功能', cmds)
con.addcmds('随机图', cmds)
str_help += '\n\n支持指令:\n图库名/随机图 图库名 : 可获得一张随机图\n提交图片 图库名 : 可为图库添加图片(需审核\n图片数量 图库名: 查看图片数量'
con.addhelp('随机图', str_help, ['图库', '随机图库'])

path2 = os.path.abspath(os.path.dirname(__file__))
dir = os.path.join(path2, "..", "..", "..", "..","Database","image")


@image_everyday.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    gid = str(event.group_id)
    name = str(event.get_message()).strip()
    if not name in data['gallery']:
        await con.send(bot, event, '不存在该图库')
        await image_everyday.finish()
    if not gid in data['task']:
        data['task'][gid] = []
    if name in data['task'][gid]:
        data['task'][gid].remove(name)
        await con.send(bot, event, '每日图: %s, 已关闭' % name)
    else:
        data['task'][gid].append(name)
        await con.send(bot, event, '每日图: %s, 已开启' % name)
    await datax.output()
    await image_everyday.finish()

@image_random.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    if msg:
        await get_more_image(bot, event, msg)
    else:
        await con.send(bot, event, str_help)
    await image_random.finish()

@image_add_gallery.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    if msg in data['gallery']:
        await con.send(bot, event, "图库已存在")
        await image_add_gallery.finish()
    data['gallery'].append(msg)
    await con.send(bot, event, "创建图库成功")
    add = os.path.join(dir, msg)
    if os.path.exists(add):
        await con.send(bot, event, "图库文件夹已存在")
    else:
        os.makedirs(add)
        await con.send(bot, event, "创建图库文件夹成功")
    await con.send(bot, event, "即将重启程序")
    await datax.output()
    time.sleep(2)
    restart()
    await image_add_gallery.finish()

@image_del_gallery.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    if not msg in data['gallery']:
        await con.send(bot, event, "图库不存在")
        await image_del_gallery.finish()
    data['gallery'].remove(msg)
    await con.send(bot, event, "删除图库成功")
    await con.send(bot, event, "即将重启程序")
    await datax.output()
    time.sleep(2)
    restart()
    await image_del_gallery.finish()

submit_list  : dict[str,]= {"id": 0}
submit_handler = []
submit_valid : list[bool]= []
submit_id : list[str]= []
@image_submit.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    name = str(event.get_message()).strip()
    if not name in data['gallery']:
        await con.send(bot, event, "图库不存在")
        await image_submit.finish()

    await con.send(bot, event, "即将向图库:%s，提交图片\n一直接受你消息中的图片直到接受到非图片信息" % name)
    global submit_list, submit_handler
    idx = str(submit_list['id'])
    submit_list['id'] += 1
    submit_list[idx] = {
        "user": event.user_id
    }
    if event.message_type == 'group':
        submit_list[idx]['group'] = event.group_id
    else:
        submit_list[idx]['group'] = 0
    org_state = submit_list[idx].copy()
    org_state['id'] = idx
    org_state['name'] = name
    for pr in range(6, 8):
        copy_state = org_state.copy()
        copy_state['handler'] = len(submit_handler)
        copy_state['priority'] = pr
        submit_valid.append(True)
        submit_id.append(idx)
        submit_handler.append(on_message(rule=Check_(None, event.message_type), permission=Special_list([str(event.user_id)]), priority=pr, block=True, temp=True, state=copy_state, handlers=[handle_submit]))
    await image_submit.finish()

async def handle_submit(bot: Bot, event: Event, state: T_State):
    global submit_list, submit_handler, submit_valid
    if not state['id'] in submit_list:
        submit_valid[state['handler']] = False
        for x in range(state['handler'] + 1, len(submit_handler)):
            if not submit_id[x] in submit_list and submit_valid[x]:
                submit_valid[x] = False
                await submit_handler[x].finish()
        await submit_handler[state['handler']].finish()
    if state['group'] > 0:
        if event.group_id != state['group']:
            await submit_handler[state['handler']].reject()
    msg = str(event.get_message()).strip()
    cnt = 0
    mystr = "图片提交结果为："
    while '[CQ:image,' in msg:
        cnt += 1
        left = msg.index('[CQ:image,')
        right = msg.index(']', left+5)
        urlid = msg.index(',url=', left+5, right)
        url = msg[urlid+5:right]
        exid = msg.index('.', urlid-7, urlid)
        ex = msg[exid: urlid]
        img = await download_image(url)
        if img:
            idx = str(data['submit']['end'])
            dir0 =os.path.join(dir, 'examine')
            dirr = os.path.join(dir, 'examine', idx + ex)
            with open(dirr, "wb") as f:
                f.write(img)
            new_name = await hash_rename(dirr, dir0, idx, ex)
            if new_name:
                mystr += '\n第%d张图片%s提交成功，目前排队序号为%d' % (cnt, msg[left: right+1], data['submit']['end'] - data['submit']['start'] + 1)
                data['submit']['end'] += 1
                data['submit'][idx] = {
                    'user' : event.user_id,
                    'img_name' : new_name,
                    'gallery': state['name']
                }
                if event.message_type == 'group':
                    data['submit'][idx]['group'] = event.group_id
                else:
                    data['submit'][idx]['group'] = 0
            else:
                mystr += '\n%s已存在，提交失败' % msg[left: right+1]
                os.remove(dirr)
        else:
            mystr += '\n%s提交失败，请重试' % msg[left: right+1]
        msg = msg[right + 1:]
    if cnt > 0:
        await con.send(bot, event, mystr)
        await datax.output()
        copy_state = state.copy()
        copy_state['handler'] = len(submit_handler)
        submit_handler.append(
            on_message(rule=Check_(None, event.message_type), permission=Special_list([str(event.user_id)]), priority=state['priority'],
                       block=True, state=copy_state, handlers=[handle_submit], temp=True))
    else:
        await con.send(bot, event, "未找到图片, 图片提交结束")
        del submit_list[state['id']]
        for x in range(state['handler'] + 1, len(submit_handler)):
            if not submit_id[x] in submit_list and submit_valid[x]:
                submit_valid[x] = False
                await submit_handler[x].finish()
    submit_valid[state['handler']] = False
    await submit_handler[state['handler']].finish()

@image_examine.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    l = data['submit']['end'] - data['submit']['start']
    if l:
        state['dir'] = os.path.join(dir, 'examine')
        state['again'] = []
        state['r18'] = False
        await con.send(bot, event, '还有%d张图片需要检测\n输入y(yes)/n(no)/e(exit)' % l)
        idx = str(data['submit']['start'])
        state['name'] = data['submit'][idx]['gallery']
        mystr = "提交者: %d\n群组: %d\n图库: %s" % (data['submit'][idx]['user'], data['submit'][idx]['group'], data['submit'][idx]['gallery'])
        mystr += f"[CQ:image,file={os.path.join(state['dir'], data['submit'][idx]['img_name'])}]"
        await con.send(bot, event, mystr)
    else:
        await con.send(bot, event, "没有新的图片需要检测")
        await image_examine.finish()

@image_examine.receive()
async def handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip().split()
    if msg[0] == 'e':
        await con.send(bot, event, "已结束")
        await image_examine.finish()
    next_flag = False
    idx = str(data['submit']['start'])
    if msg[0] == 'y':
        next_flag = True
        if len(msg) > 1:
            if msg[1] == 'r18':
                state['r18'] = True
        if len(state['again']) > 0:
            del state['again'][0]
        else:
            #检测是否重复
            add = os.path.join(dir, state['name'])
            im = get_all(add, True, only_name=True)
            for img in im:
                dis = Hamming_distance(data['submit'][idx]['img_name'], img)
                if limit_hamming >= dis >= 0:
                    state['again'].append(img)
        if len(state['again']) == 0:
            #保存
            add = os.path.join(dir, state['name'])
            if state['r18']:
                add = os.path.join(add, 'r18')
                if not os.path.exists(add):
                    os.makedirs(add)
            with open(os.path.join(state['dir'], data['submit'][idx]['img_name']), "rb") as f1:
                f = f1.read()
                with open(os.path.join(add, data['submit'][idx]['img_name']), "wb") as f2:
                    f2.write(f)
            os.remove(os.path.join(state['dir'], data['submit'][idx]['img_name']))
            if state['r18']:
                await con.send(bot, event, "R18图片已保存")
            else:
                await con.send(bot, event, "图片已保存")
            del data['submit'][idx]
            data['submit']['start'] += 1
            await datax.output()
    elif msg[0] == 'n':
        next_flag = True
        if len(state['again']) > 0:
            state['again'] = []
        os.remove(os.path.join(state['dir'], data['submit'][idx]['img_name']))
        del data['submit'][idx]
        data['submit']['start'] += 1
        await datax.output()
        await con.send(bot, event, "图片已拒绝")
    if next_flag:
        if len(state['again']) > 0:
            mystr = "检测到相似图片，相似度:%.2f%%\n" % (100/64 * (64 - Hamming_distance(data['submit'][idx]['img_name'], state['again'][0])))
            mystr += f"[CQ:image,file={os.path.join(dir, state['name'], state['again'][0])}]"
            mystr += '\n是否继续保存？y/n'
            await con.send(bot, event, mystr)
        else:
            if data['submit']['start'] >= data['submit']['end']:
                await con.send(bot, event, "所有图片检测完毕")
                await image_examine.finish()
            idx = str(data['submit']['start'])
            mystr = "提交者: %d\n群组: %d\n图库: %s" % (
            data['submit'][idx]['user'], data['submit'][idx]['group'], data['submit'][idx]['gallery'])
            state['r18'] = False
            state['name'] = data['submit'][idx]['gallery']
            mystr += f"[CQ:image,file={os.path.join(state['dir'], data['submit'][idx]['img_name'])}]"
            await con.send(bot, event, mystr)
    await image_examine.reject()

@image_cnt.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    name = str(event.get_message()).strip()
    if not name in data['gallery']:
        await con.send(bot, event, "图库不存在")
        await image_submit.finish()
    if event.message_type == 'group':
        if event.group_id in data['r18']:
            im = get_all(os.path.join(dir, name), True)
        else:
            im = get_all(os.path.join(dir, name))
    else:
        im = get_all(os.path.join(dir, name), True)
    await con.send(bot, event, "图库: %s, 共有%d张图片" % (name, len(im)))
    await image_cnt.finish()


@image_limit.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    global limit_hamming
    msg = str(event.get_message()).strip()
    if msg.isnumeric():
        li = int(msg)
        if 0 <= li <= 64:
            limit_hamming = li
            await con.send(bot, event, "当前图片检测阈值为%.2f%%" % (100/64 * (64 -li)))
        else:
            await con.send(bot, event, "参数非法")
    else:
        await con.send(bot, event, "参数非法")
    await image_limit.finish()

@image_r18.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    if event.group_id in data['r18']:
        data['r18'].remove(event.group_id)
        await con.send(bot, event, "不可以色色！")
    else:
        data['r18'].append(event.group_id)
        await con.send(bot, event, "可以色色！")
    await datax.output()
    await image_r18.finish()
@scheduler.scheduled_job("cron" , hour=0, minute=0)
async def ceg():
    bots = nonebot.get_bots()
    for i in bots:
        bot = bots[i]
        break
    for gid in data['task']:
        if len(data['task'][gid]):
            await bot.sendGroupMsg(group_id=gid, message=time.strftime("新的一天！今天是%m月%d日, %A", time.localtime()))
    for gid in data['task']:
        if len(data['task'][gid]):
            for name in data['task'][gid]:
                await bot.sendGroupMsg(group_id=gid, message='今天的%s图是：\n' % name + get_image(name))

def get_image(address: str, r18 = False):
    add = os.path.join(dir, address)
    im = get_all(add, r18)
    if len(im) > 0:
        img = random.choice(im)
        return f"[CQ:image,file={os.path.join(add, img)}]"
    else:
        return None

def get_all(cwd, ex = False, add = False, only_name = False) -> list:
    result = []
    get_dir = os.listdir(cwd)
    if add:
        now_dir = cwd.split("\\")[-1]
    for i in get_dir:
        sub_dir = os.path.join(cwd,i)
        if os.path.isdir(sub_dir):
            if ex:
                result += get_all(sub_dir, False, True)
        else:
            if add and not only_name:
                result.append(os.path.join(now_dir, i))
            else:
                result.append(i)

    return result

async def get_more_image(bot: Bot, event: Event, msg: str):
    while len(msg) > 0:
        flag = True
        for name in data['gallery']:
            if name in msg:
                if msg.index(name) == 0:
                    flag = False
                    await con.send(bot, event, get_image(name))
                    if random.random() >= 0.75:
                        return
                    msg = msg[len(name):]
                    break
        if flag:
            break

