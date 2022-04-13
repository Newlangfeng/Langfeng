import time
import discord
import asyncio
import os
import datetime
import humanfriendly

from asyncio import sleep
from discord.ext import commands 
from discord_slash import SlashCommand, SlashContext


client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True) # Declares slash commands through the client.


@client.event
async def on_ready():
    print("浪烽HelpBot已上線")
    print(client.user.name)
    print(client.user.id)
async def status_task():
    while True:
        await client.change_presence(activity=discord.Game(name="🟡Helpbot beta|浪烽"))
        await asyncio.sleep(8)
        await client.change_presence(activity=discord.Game(name="5️⃣月移植到HelpBot"))
        await asyncio.sleep(8)
        await client.change_presence(activity=discord.Game(name="📟24小時試運轉中"))
        await asyncio.sleep(8)
        

@client.event    
async def on_ready():
    client.loop.create_task(status_task())

@slash.slash(description="查看目前延遲")
async def ping(ctx):
    embed=discord.Embed(title="📡目前延遲",description=f"{round(client.latency*1000)}(ms)", color=0x61d93f)
    await ctx.send(embed=embed)

 
@slash.slash(description="查看伺服IP")
async def IP(ctx: SlashContext):
    embed=discord.Embed(title="風平浪靜伺服", url="https://www.nagiasu.xyz", color=0x0fa8f5)
    embed.set_thumbnail(url="https://www.nagiasu.xyz/logo.png")
    embed.add_field(name="伺服IP (1)", value="nagiasu.xyz", inline=True)
    embed.add_field(name="伺服IP (2)", value="mc.nagiasu.xyz", inline=True)
    await ctx.send(embed=embed)

@slash.slash(description="查看浪烽官網")
async def Langfeng(ctx):
    await ctx.send('https://minecraftlangfeng.blogspot.com')

@slash.slash(description="使用機器人說話")
@commands.has_role(913297450847047680)
async def sayd(ctx,*,說話內容):
    await ctx.send(說話內容)
    

@slash.slash(description="刪除部分信息")
@commands.has_guild_permissions(manage_messages=True, manage_webhooks=True)
async def clear(ctx,數量:int):
    await ctx.channel.purge(limit=數量)
    embed=discord.Embed(title="社區通知",description=f"成功刪除了{數量}條信息", color=0x61d93f)
    await ctx.send(embed=embed)


@slash.slash(description="查看副本任務指南")
async def detask(ctx):
    embed=discord.Embed(title="副本任務指南", url="https://hackmd.io/@drf556923/HJUpKPBLu", color=0x0fa8f5)
    await ctx.send(embed=embed)

@slash.slash(description="查看副本怪物指南")
async def demonster(ctx):
    embed=discord.Embed(title="副本怪物指南", url="https://hackmd.io/@kanoooooooooo/ryiid3rLd", color=0x0fa8f5)
    await ctx.send(embed=embed)

@slash.slash(description="查看伺服官網")
async def nagiasu(ctx):
    await ctx.send('https://www.nagiasu.xyz/')

@slash.slash(description="查看幫助")
@commands.has_role(913297450847047680)
async def help(ctx):
    await ctx.send('開發中')

@slash.slash(description="管理身份組")
@commands.has_permissions(administrator=True)
async def role(ctx, 成員 : discord.Member, *, 身份組 : discord.Role):
  if role.position > ctx.author.top_role.position: #if the role is above users top role it sends error
    return await ctx.send('**:x: | 該身份組高於你的身份組！**') 
  if role in 成員.roles:
      await 成員.remove_roles(身份組) #removes the role if user already has
      await ctx.send(f"已成功移除{成員.mention}的 {role} 身份組")
  else:
      await 成員.add_roles(身份組) #adds role if not already has it
      await ctx.send(f"{成員.mention}成功新增 {role} 身份組") 

@slash.slash(description="進入社區內部聊天室")
async def tl(ctx):
    user = ctx.author
    role = ctx.guild.get_role(913295072865427477)
    if role in user.roles:
      await user.remove_roles(role) #removes the role if user already has
      embed=discord.Embed(title="浪烽社區通知", color=0xcd3232)
      embed.add_field(name=f"{user}", value="你好，你已成功退出社區內部聊天室", inline=False)
      await ctx.author.send(embed=embed)
    else:
      await user.add_roles(role)
      embed=discord.Embed(title="浪烽社區通知", color=0x61d93f)
      embed.add_field(name=f"{user}", value="你好，你已成功進入社區內部聊天室", inline=False)
      await ctx.author.send(embed=embed)
    
@slash.slash(description="用機器人私信")
@commands.has_guild_permissions(manage_messages=True, manage_webhooks=True)
# We are defining member as a discord.Member object, it will convert automatically for us
async def dm(ctx, 成員: discord.Member, *, 私信內容: str):
    try:
        # Send the message by calling the .send method on the member object
        embed=discord.Embed(title=f"浪烽社區通知", color=0x0fa8f5)
        embed.add_field(name=f"{成員}", value=f"{私信內容}", inline=False)
        await 成員.send(embed=embed)
        await ctx.send(f"成功發送私信給 {成員}.")

    # If user is not in guild or has blocked the bot
    except discord.Forbidden:
        await ctx.send(f"發送私信失敗 {成員}.")

@slash.slash(description="倒數器")
async def countdown(ctx, 倒數時間秒: int):
    user = ctx.author    
    embed=discord.Embed(title="社區通知",description=f"倒計時 {倒數時間秒}s" , color=0x61d93f)
    await ctx.send(embed=embed)

    while 倒數時間秒 > 0:
        倒數時間秒 -= 1
        # Sleep for 1 second
        await asyncio.sleep(1)

    await ctx.send(f"{user.mention}")
    embed=discord.Embed(title="社區通知",description="倒計時結束" , color=0xcd3232)
    await ctx.send(embed=embed)

@slash.slash(description="玩家資訊")
async def player(ctx, minecraftid):
    await ctx.send("https://mc-heads.net/avatar/" + minecraftid)
    
@slash.slash(description="踢出成員")
@commands.has_permissions(kick_members=True)
async def kick(ctx, 成員: discord.Member, *, 處分原因=None):
    user = ctx.author 
    if 處分原因==None:
      處分原因=" 沒有原因"
    await ctx.guild.kick(成員)
    embed=discord.Embed(title="🔸已被踢出", color=0xe47f0c)
    embed.set_author(name=f"{成員}", icon_url=成員.avatar_url)
    embed.set_thumbnail(url=成員.avatar_url)
    embed.add_field(name="踢出原因", value=f"{處分原因}", inline=True)
    embed.set_footer(text=f"由{user}處分")
    await ctx.send(embed=embed)
    
@slash.slash(description="封鎖成員")
@commands.has_permissions(ban_members=True)
async def ban(ctx, 成員: discord.Member, *, 處分原因=None):
    user = ctx.author 
    if 處分原因==None:
      處分原因=" 沒有原因"
    await 成員.ban(reason=處分原因)
    embed=discord.Embed(title="⛔已被封鎖", color=0xcd3232)
    embed.set_author(name=f"{成員}", icon_url=成員.avatar_url)
    embed.set_thumbnail(url=成員.avatar_url)
    embed.add_field(name="封鎖原因", value=f"{處分原因}", inline=True)
    embed.set_footer(text=f"由{user}處分")
    await ctx.send(embed=embed)


client.run("Nzg3NTg3NTMzNjM4ODYwODIw.X9XIDA.Lh4FomBzpm8TteY-ag7R-OKOA7g")
