from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request
import discord
from discord.ext import commands
from itertools import cycle
import emoji
import os

# Client Id : 816671240293974066
# Client Token : 


client = commands.Bot(command_prefix='#')


#오늘 날짜 
def set_today():
    global today

    today_year = str(datetime.today().year)
    today_month = str(datetime.today().month)
    today_day = str(datetime.today().day)


    if len(today_month) == 1:
        today_month = '0' + str(today_month)

    if len(today_day) == 1:
        today_day = '0' + str(today_day)

    today = today_year+today_month+today_day

    print("today is ", end='')
    print(today)
#내일 날짜
def set_tomorrow():
    global tomorrow

    tomorrow = str(int(today) + 1)

    print("tomorrow is ", end='')
    print(tomorrow)
#알레르기 성분 번호 삭제    
def num_remove(food):
    food = str(food).replace("10.", "")
    food = str(food).replace("11.", "")
    food = str(food).replace("12.", "")
    food = str(food).replace("13.", "")
    food = str(food).replace("14.", "")
    food = str(food).replace("15.", "")
    food = str(food).replace("16.", "")
    food = str(food).replace("17.", "")
    food = str(food).replace("18.", "")
    food = str(food).replace("1.", "")
    food = str(food).replace("2.", "")
    food = str(food).replace("3.", "")
    food = str(food).replace("4.", "")
    food = str(food).replace("5.", "")
    food = str(food).replace("6.", "")
    food = str(food).replace("7.", "")
    food = str(food).replace("8.", "")
    food = str(food).replace("9.", "")

    return food
#알레르기 성분 번호 삭제    
def remove_num(meal):
    List = list(meal)
    Real = list()

    for i in List:
        a = num_remove(i)
        Real.append(a)
        
    return Real

#점심 급식 리스트로 받아오기
def get_meal_lunch(day):
    try:
        url = "https://school.jbedu.kr/jeolla-h/M01070403/list?ymd=" + day

        soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')

        meals = soup.select_one('#usm-content-body-id > ul.tch-lnc-list > li:nth-child(2) > dl > dd.tch-lnc > ul').get_text().split()
        meals = remove_num(meals)    

        return meals
    except:
        print("중식 정보가 없습니다.")

        return "Nope"


#저녁 급식 리스트로 받아오기
def get_meal_dinner(day):
    try:
        url = "https://school.jbedu.kr/jeolla-h/M01070403/list?ymd=" + day

        soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')

        meals = soup.select_one('#usm-content-body-id > ul.tch-lnc-list > li:nth-child(3) > dl > dd.tch-lnc > ul').get_text().split()
        meals = remove_num(meals)    

        return meals
    except:
        print("석식 정보가 없습니다.")

        return "Nope"

class makeError(Exception):
    def __init__(self):
        super().__init__('급식 정보가 없습니다.')

#================================================================================================================================================

@client.event
async def on_ready():
    global today_lunch, today_dinner, tomorrow_lunch, tomorrow_dinner

    print(client.user.id)
    print("ready")
    game = discord.Game("전라고 급식 서비스 제공")
    await client.change_presence(status = discord.Status.online, activity = game)
    set_today()
    set_tomorrow()

    # ----------------------------

    today_lunch = get_meal_lunch(today)
    today_dinner = get_meal_dinner(today)

    # ----------------------------

    tomorrow_lunch = get_meal_lunch(tomorrow)
    tomorrow_dinner = get_meal_dinner(tomorrow)



def list_to_str(list):
    k = str()
    for i in list:
        k += i + '\n'
    
    return k

@client.command(name="급식")
async def meal(ctx, *text):

    txt = ''
    for tmp in text:
        txt += tmp
        txt += ' '

    day = "2021" + txt

    day_lunch = get_meal_lunch(day)
    day_dinner = get_meal_dinner(day)

    if day_lunch == "Nope" and day_dinner == "Nope":
        embed = discord.Embed(title = "Error",
        description = "급식 정보가 없습니다.", color = discord.Color.red()
        )
        await ctx.send(embed=embed)
        raise makeError
    elif day_dinner == "Nope":
        embed = discord.Embed(title = "Error",
        description = "저녁 급식 정보가 없습니다.", color = discord.Color.red()
        )
        await ctx.send(embed=embed)
        raise makeError
    elif day_lunch == "Nope":
        embed = discord.Embed(title = "Error",
        description = "점심 급식 정보가 없습니다.", color = discord.Color.red()
        )
        await ctx.send(embed=embed)
        raise makeError

    embed = discord.Embed(title = "전라고등학교 급식",
    description="날짜 : %s년 %s월 %s일" %(day[:4], day[5:6], day[7:]), color=discord.Color.blue())

    embed.add_field(name="중식", value=list_to_str(day_lunch), inline=False)
    embed.add_field(name="석식", value=list_to_str(day_dinner), inline=False)

    await ctx.send(embed=embed)

@client.command(name="오늘")
async def meal(ctx):
    if today_lunch == "Nope" and today_dinner == "Nope":
        embed = discord.Embed(title = "Error",
        description = "급식 정보가 없습니다.", color = discord.Color.red()
        )
        await ctx.send(embed=embed)
        raise makeError
    elif today_dinner == "Nope":
        embed = discord.Embed(title = "Error",
        description = "저녁 급식 정보가 없습니다.", color = discord.Color.red()
        )
        await ctx.send(embed=embed)
        raise makeError
    elif today_lunch == "Nope":
        embed = discord.Embed(title = "Error",
        description = "점심 급식 정보가 없습니다.", color = discord.Color.red()
        )
        await ctx.send(embed=embed)
        raise makeError

    embed = discord.Embed(title = "전라고등학교 급식",
    description="날짜 : %s년 %s월 %s일" %(today[:4], today[5:6], today[7:]), color=discord.Color.blue())

    embed.add_field(name="중식", value=list_to_str(today_lunch), inline=False)
    embed.add_field(name="석식", value=list_to_str(today_dinner), inline=False)

    await ctx.send(embed=embed)

@client.command(name="내일")
async def meal(ctx):
    if tomorrow_lunch == "Nope" and tomorrow_dinner == "Nope":
        embed = discord.Embed(title = "Error",
        description = "급식 정보가 없습니다.", color = discord.Color.red()
        )
        await ctx.send(embed=embed)
        raise makeError
    elif tomorrow_dinner == "Nope":
        embed = discord.Embed(title = "Error",
        description = "저녁 급식 정보가 없습니다.", color = discord.Color.red()
        )
        await ctx.send(embed=embed)
        raise makeError
    elif tomorrow_lunch == "Nope":
        embed = discord.Embed(title = "Error",
        description = "점심 급식 정보가 없습니다.", color = discord.Color.red()
        )
        await ctx.send(embed=embed)
        raise makeError

    embed = discord.Embed(title = "전라고등학교 급식",
    description="날짜 : %s년 %s월 %s일" %(tomorrow[:4], tomorrow[5:6], tomorrow[7:]), color=discord.Color.blue())

    embed.add_field(name="중식", value=list_to_str(tomorrow_lunch), inline=False)
    embed.add_field(name="석식", value=list_to_str(tomorrow_dinner), inline=False)

    await ctx.send(embed=embed)


client.run(os.environ['token'])
