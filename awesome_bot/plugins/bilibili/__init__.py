from .._gb import *
from .datasource import get_dynamic, get_user_info

dynamic_on = on_command('b站动态订阅', aliases={'bilibili动态订阅'}, rule=Check_('b站动态订阅', 'group'), priority=5, permission=ADMIN)

datax = DataList('bilibili_dynamic')
data = datax.data


cmds = [
'b站动态订阅'
]

con.addcmds('基础功能', cmds)
con.addcmds('bilibili', cmds)

con.addhelp('bilibili', """
指令:
b站动态订阅 uid :该指令仅群管理员可用
(取消订阅也是这条指令)

""".strip(), ['b站'])

scheduler = require('nonebot_plugin_apscheduler').scheduler

@dynamic_on.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    uid = str(event.get_message()).strip()
    try:
        udata = await get_user_info(uid)
        name = udata['name']
        if not uid in data:
            data[uid] = {
                'group': [],
                'ids': [],
                'name': name
            }
        items = await get_dynamic(uid)
        for item in items:
            id_str = item['id_str']
            if not id_str in data[uid]['ids']:
                data[uid]['ids'].append(id_str)
        gid = event.group_id
        if not gid in data[uid]['group']:
            data[uid]['group'].append(gid)
            await con.send(bot, event, "订阅[%s]的动态成功" % name)
        else:
            data[uid]['group'].remove(gid)
            await con.send(bot, event, "已取消[%s]的动态订阅" % name)
        await datax.output()
    except:
        await con.send(bot, event, "找不到uid为%s的用户" % uid)


@scheduler.scheduled_job('interval', minutes=5)
async def handle():
    for uid in data:
        if len(data[uid]['group']) > 0:
            items = await get_dynamic(uid)
            for item in items:
                id_str = item['id_str']
                if id_str in data[uid]['ids']:
                    continue
                else:
                    data[uid]['ids'].append(id_str)
                    if len(data[uid]['ids']) > 100:
                        del data[uid]['ids'][0]
                dic = item['modules']['module_dynamic']
                if dic['desc'] is None:
                    mystr = data[uid]['name'] + '发了一条新动态:'
                else:
                    mystr = data[uid]['name'] + '发了一条新动态:\n' + dic['desc']['text']
                mystrs = []
                if dic['major'] is not None:
                    if 'draw' in dic['major']: #图片
                        pics = dic['major']['draw']['items']
                        if mystr != "":
                            mystr += '\n'
                        for pic in pics:
                            src = pic['src']
                            mystr += '[CQ:image,file=%s,cache=0]' % src
                    if 'archive' in dic['major']: #投稿
                        if mystr != "":
                            mystr += '\n'
                        else:
                            mystr += '视频投稿：\n'
                        title = dic['major']['archive']['title']
                        url = dic['major']['archive']['jump_url']
                        cover = dic['major']['archive']['cover']
                        desc = dic['major']['archive']['desc']
                        mystr += '[CQ:share,url=%s,title=%s,content=%s,image=%s]' % (url, title, desc, cover)
                        # mystrs.append('[CQ:share,url="%s",title="%s",content="%s",image="%s"]' % (url, title, desc, cover))
                    if 'article' in dic['major']: #投稿专栏
                        if mystr != "":
                            mystr += '\n'
                        else:
                            mystr += '专栏投稿：\n'
                        title = dic['major']['article']['title']
                        url = dic['major']['article']['jump_url']
                        if 'cover' in dic['major']['article']:
                            cover = dic['major']['article']['cover']
                        elif 'covers' in dic['major']['article']:
                            cover = dic['major']['article']['covers'][0]
                        else:
                            cover = ""
                        desc = dic['major']['article']['desc']
                        mystr += '[CQ:share,url=%s,title=%s,content=%s,image=%s]' % (url, title, desc, cover)
                        # mystrs.append('[CQ:share,url="%s",title="%s",content="%s",image="%s"]' % (url, title, desc, cover))
                bot = get_bot()
                for gid in data[uid]['group']:
                    time.sleep(0.5)
                    await bot.call_api('send_group_msg', group_id=gid, message=mystr, auto_escape=False)
                    # for mstr in mystrs:
                    #     time.sleep(0.5)
                    #     await bot.call_api('send_group_msg', group_id=gid, message=mstr, auto_escape=False)
    await datax.output()