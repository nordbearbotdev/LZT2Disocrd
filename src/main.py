from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import discord
from discord.ext import commands
from textwrap3 import wrap
import feedparser
from datetime import timedelta, datetime

bot = commands.Bot(command_prefix='?', description="Бот, который перессылает сообщения с вашей темы на лолз на сервер в дсикорд.", help_command=None)
token = "Тут токен"

"""
Функция трансляции сообщений
"""

@bot.command()
async def parse(ctx, link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, "html.parser")
    soup_text = soup.get_text()
    if len(soup_text) > 2000:
        longMsg = wrap(soup_text, 2000)
        for i in longMsg: 
            await ctx.send(i)
    await ctx.send(soup_text)

"""
RSS функция
"""

FEED_URL = ['https://something.com/feeds/rss.xml']

@bot.command()
async def rss_daily(ctx):
    day_ago = datetime.now() - timedelta(days=1)
    for feed in FEED_URL:
        rss_feed = feedparser.parse(feed)
        for entry in rss_feed.entries:
                published_date = entry.published
                published_date = published_date[5:-6]
                published_date_obj = datetime.strptime(published_date, '%d %b %Y %H:%M:%S')
                if published_date_obj > day_ago:
                    await ctx.send(entry.links[0].href)

"""
Другие функции
"""
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def help(ctx):
    await ctx.send("""
    -help -- список команд
    -parse [link] -- печатает текст веб-сайта в чат (печатает все, а не только основной текст) 
    -rss_daily -- выводит в чат ссылки на rss-ленты, включенные в код бота
    """)

bot.run(token)
