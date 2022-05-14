from .._gb import *
import aiohttp
import json

music_163 = on_command('点歌', rule=Check_('点歌'), priority=8)

cmds = [
'点歌'
]
con.addhelp('点歌', """
蕾米球目前仅支持网易云点歌
指令：
点歌 关键词
只会发送默认匹配度第一的歌曲
""".strip())
con.addcmds('基础功能', cmds)
con.addcmds('点歌', cmds)


async def fetch(session, url, params = None, proxy = None):
    async with session.get(url,params=params, proxy=proxy) as response:
        return await response.text()

async def Get_Music_163(name: str):
    url = r'http://music.cyrilstudio.top/search?keywords=' + name +'&limit=1'
    async with aiohttp.ClientSession() as session:
        # params = {'type':'json'}
        html = await fetch(session, url)
        data = json.loads(html)
        if data['result']['songCount'] > 0:
            song = data['result']['songs'][0]
            return f'[CQ:music,type=163,id=%d]' % song['id']
        else:
            return None
@music_163.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    m = await Get_Music_163(str(event.get_message()).strip())
    if m:
        await con.send(bot, event, m)
    else:
        await con.send(bot, event, '找不到对应歌曲')
    await music_163.finish()

