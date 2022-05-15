from .._gb import *
from .datasource import get_dynamic, get_user_info
import json

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
                bot = get_bot()
                dic = item['modules']['module_dynamic']
                msgs = []
                if dic['desc'] is None:
                    msgs.append(segement('text', text=data[uid]['name'] + '发了一条新动态:'))
                else:
                    msgs.append(segement('text', text=data[uid]['name'] + '发了一条新动态:\n' + dic['desc']['text']))
                if dic['major'] is not None:
                    if 'draw' in dic['major']: #图片
                        msgs.append(segement('text', text='\n'))
                        pics = dic['major']['draw']['items']
                        for pic in pics:
                            src = pic['src']
                            msgs.append(segement('image', file=src, cache=0))
                    if 'archive' in dic['major']: #投稿
                        msgs.append(segement('text', text='\n投稿了视频：'))
                        title = dic['major']['archive']['title']
                        desc = dic['major']['archive']['desc']
                        url = await get_valid_url(dic['major']['archive']['jump_url'])
                        cover = await get_valid_cover(bot, dic['major']['archive']['cover'])
                        msgs.append(segement('share', url=url, content=desc, title=title, image=cover))
                    if 'article' in dic['major']: #投稿专栏
                        msgs.append(segement('text', text='\n投稿了文章：'))
                        title = dic['major']['article']['title']
                        url = await get_valid_url(dic['major']['article']['jump_url'])
                        if 'cover' in dic['major']['article']:
                            cover = await get_valid_cover(bot, dic['major']['article']['cover'])
                        elif 'covers' in dic['major']['article']:
                            cover = await get_valid_cover(bot, dic['major']['article']['covers'][0])
                        else:
                            cover = ""
                        desc = dic['major']['article']['desc']
                        msgs.append(segement('share', url=url, content=desc, title=title, image=cover))
                    if 'live_rcmd' in dic['major']:
                        msgs.append(segement('text', text='\n直播了：'))
                        dic2 = json.loads(dic['major']['live_rcmd']['content'])['live_play_info']
                        title = dic2['title']
                        desc = dic2['watched_show']['text_large']
                        cover = await get_valid_cover(bot, dic2['cover'])
                        url = await get_valid_url(dic2['link'])
                        msgs.append(segement('share', url=url, content=desc, title=title, image=cover))
                for gid in data[uid]['group']:
                    time.sleep(0.5)
                    await bot.call_api('send_group_msg', group_id=gid, message=msgs)
    await datax.output()

async def get_valid_cover(bot, org_cover: str) -> str:
    msgid = await bot.call_api('send_private_msg', user_id=847360401,
                               message=[segement('image', file=org_cover)])
    msg = await bot.call_api('get_msg', message_id=msgid['message_id'])
    return msg['message'][0]['data']['url']

async def get_valid_url(org_url: str) -> str:
    if org_url[:6] == 'https:':
        org_url = org_url[6:]
    elif org_url[:5] == 'http:':
        org_url = org_url[5:]
    while org_url[0] == '/':
        org_url = org_url[1:]
    return org_url