from pokemon.connection import switch, serv
import discord
from discord.ext import commands
from yaml import load
from rich.console import Console
import os
import datetime

# Simple file reader to load advanced settings
with open("advanced/blacklist.yaml", encoding='utf-8') as file:
    data = load(file)
    userblacklist = data["userblacklist"]

with open("advanced/logs.yaml", encoding='utf-8') as file:
    data = load(file)
    log = data["log"]

with open("advanced/priority.yaml", encoding='utf-8') as file:
    data = load(file)
    priority = data["priority"]

with open("advanced/sudo.yaml", encoding='utf-8') as file:
    data = load(file)
    sudo = data["sudo"]

console = Console()

# Queue List by Discord ID
queuelist = []

# Cog 
class request(commands.Cog):
    def __init__(self, client):
        self.client = client

# {-- Request Module --}
    @commands.command()
    @commands.guild_only()
    async def testtradetest(self, ctx):
        if ctx.message.author.id not in userblacklist:
            return
        await ctx.send("User is blacklisted from using the bot.")
        if ctx.message.author.id in queuelist:
            await ctx.send("You are already in queue.")

        else:
            switch(serv, "getTitleID")
            title = serv.recv(689)
            title = title[:-1]
            title = str(title,'utf-8')
            for attachment in ctx.message.attachments:

                if attachment.filename.endswith((".eb8")):

                    # Logs in console
                    os.system('cls||clear')
                    await attachment.save(f"Files/sysbot/requested-{ctx.message.author.id}.eb8")
                    prioritycheck = discord.utils.find(lambda r: r.id == priority, ctx.message.guild.roles)
                    if prioritycheck in ctx.message.author.roles:
                        queuelist.insert(0, ctx.message.author.id)
                    else:
                        queuelist.append(ctx.message.author.id)
                    console.log(f'{ctx.message.author.name} has been added to the queue', style="blue")
                    await ctx.message.delete()
                    await ctx.send(f'{ctx.message.author.name} has been added to the queue. Current queue length: {len(queuelist)}.')
                    with open("logs.txt", "a") as logger:
                        logtime = datetime.datetime.now()
                        logger.write(logtime + " || " + {ctx.message.author.name} + " has requested to trade with the bot" + "\n")
                else:
                    await ctx.channel.send("Unable to trade. Ensure your file ends in `.eb8` and is legal.")
            await ctx.send("SysBot.py is not made for LGPE yet.")
            del queuelist[0]

            await ctx.send("SysBot.py is not made for SWSH yet.")
            del queuelist[0]


def setup(client):
    client.add_cog(request(client))