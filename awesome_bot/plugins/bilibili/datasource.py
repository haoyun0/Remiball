import aiohttp
import json

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def get_dynamic(uid) -> list:
    api = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?host_mid=' + str(uid)
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, api)
        datax = json.loads(html)
        data = datax['data']
        items = data['items']
        return items

async def get_user_info(uid) -> dict:
    api = 'https://api.bilibili.com/x/space/acc/info?mid=%s&jsonp=jsonp' % str(uid)
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, api)
        datax = json.loads(html)
        data = datax['data']
        return data
