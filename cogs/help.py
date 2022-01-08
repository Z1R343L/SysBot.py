import discord
from discord.ext import commands
from yaml import load
import datetime
import itertools
import psutil
from discord_components import DiscordComponents, SelectOption, Select, Button, ButtonStyle
import asyncio

with open("config.yaml") as file:
    data = load(file)
    botprefix = data["botprefix"]
    support2 = data["support-server-invite"]

ttr = str(f"""
```yaml
Prefix: {botprefix} - Required Parameter: <> - Optional Parameter: ()
```
""")

sysbotval = str(
    '\x1f ⋅ testtradetest `<eb8>`: Request a pokemon from the bot.\x1f ⋅ guide: Shows a video on how to use SysBot.\x1f ⋅ languide: Shows instructions on how to download LAN play.\x1f ⋅ lgpe: Shows a video on how to use the LGPE SysBot.\x1f ⋅ queue: Sends you current queue position.\x1f ⋅ queue list: Displays the total queue list.\x1f ⋅ queue leave: Requests to leave the queue.\x1f'
)


filesval = str(
    '\x1f ⋅ pk8 `<pokemon>`: Sends a `pk8` file.\x1f ⋅ ek8 `<pokemon>`: Sends a `ek8` file.\x1f ⋅ pk7 `<pokemon>`: Sends a `pk7` file.\x1f ⋅ pk6 `<pokemon>`: Sends a `pk6` file.\x1f ⋅ pb8 `<pokemon>`: Sends a `eb8` file.\x1f ⋅ eb8 `<pokemon>`: Sends a `eb8` file.\x1f ⋅ pb7 `<pokemon>`: Sends a `pb7` file.\x1f'
)


miscellaneousval = str(
    "\x1f ⋅ prefix: Fetches the bot's prefix.\x1f ⋅ latency: Reports latency.\x1f ⋅ invite: Sends invite link to bot's home server.\x1f ⋅ support: Sends bot's donation link.\x1f ⋅ vote: Vote for a SysBot mode.\x1f ⋅ votelock: 3 votes will lock the channel the command is used in.\x1f ⋅ addcode: Saves your friend code.\x1f ⋅ fcode: Shows saved your friend code.\x1f ⋅ changecode: Changes your friend code.\x1f ⋅ removecode: Deletes your friend code.\x1f"
)


chanval = str(
    "\x1f ⋅ lock: Prevents members from type in used channel.\x1f ⋅ unlock: Allows members from type in used channel.\x1f ⋅ say <message>: Sends invite link to bot's home server.\x1f ⋅ purge <amount>: Bot repeats message.\x1f ⋅ slowmode <amount>: Changes the slowmode of used channel.\x1f ⋅ add: Adds channel to bot's announcement notification list.\x1f ⋅ remove: Removes channel from bot's announcement notification list.\x1f"
)


modval = str(
    "\x1f ⋅ kick  <member> (reason): Kicks mentioned member.\x1f ⋅ ban  <member> (reason): Bans mentioned member.\x1f ⋅ shareban <member> (reason): Bans mentioned member and announces in all linked channels.\x1f ⋅ unban <member>: Unbans mentioned member.\x1f ⋅ userinfo <member>: Displays mentioned member's info.\x1f ⋅ warn <member> <reason>: Warns mentioned member.\x1f ⋅ addrole <member> <role>: Gives mentioned member a role.\x1f ⋅ removerole <member> <role>: Removes mentioned member a role.\x1f ⋅ mute <member> <duration> (reason): Mutes mentioned member for said duration.\x1f ⋅ unmute <member>: Unmutes member.\x1f ⋅ category <channel> <category>: Moves the channels category location.\x1f ⋅ addban: Adds channel to bot's shareban notification list.\x1f ⋅ removeban: Removes channel from bot's shareban notification list.\x1f"
)


remoteval = str(
    '\x1f ⋅ click (x, a, b, or y): Tells switch to click selected button.\x1f ⋅ spamb: Tells switch to spam press the b button.\x1f ⋅ click (up, right, down, left): Tells switch which direction to move.\x1f ⋅ click (plus. minus, home): Clicks selected hotkey on switch.\x1f ⋅ pokemon (inject, dump): Dumps or injects pokemon into box 1 slot 1.\x1f ⋅ screen (on, off, shot, capture, percent): Controls the switch screen.\x1f ⋅ reconnect: Attempts to reconnect to your switch.\x1f'
)


ownerval = str(
    '\x1f ⋅ boton <message>: Sends a bot online message.\x1f ⋅ announcment <message>: Sends an announcement message.\x1f ⋅ botdown <message>: Sends a bot offline message.\x1f ⋅ redact <amount>: Redacts desired amount of announcement messages.\x1f ⋅ addsudo <member>: Adds member to sudo list.\x1f ⋅ removesudo <member>: Removes member from sudo list.\x1f ⋅ blacklist <member>: Saves your friend code.\x1f ⋅ unblacklist <member>: Shows saved your friend code.\x1f ⋅ loghere: Adds channel to logging output.\x1f ⋅ dontlog: Removes channel from logging output.\x1f'
)


botmanval = str(
    "\x1f ⋅ directmessage <userid> <content>: Sends message to directed user.\x1f ⋅ send <channelid> <content>: Sends message to directed channel.\x1f ⋅ list: List all servers the bot is in, including name, guild ID, owner, and invite.\x1f ⋅ leave <guildid>: Leaves server from directed guild.\x1f ⋅ createguild <name>: Creates a guild.\x1f ⋅ deleteguild <guildid>: Deletes an owned guild.\x1f ⋅ rename <name>: Renames the bot's name.\x1f ⋅ repfp <image>: Change the bot's pfp.\x1f ⋅ botinvite: Generates a bot invite.\x1f ⋅ load <cog>: Loads a cog.\x1f ⋅ reload <cog>: Reloads a cog.\x1f ⋅ unload <cog>: Unloads a cog.\x1f ⋅ restart: Restarts the bot.\x1f ⋅ shutdown: Turns off the bot.\x1f"
)

class help(commands.Cog):
    def __init__(self, client):
        self.client = client
        DiscordComponents(self.client)

    @commands.command()
    async def help(self, ctx):

        # Embeds
        embed=discord.Embed(title=f'{self.client.user.name} Commands', description=f"Utilize the dropdown menu to select help pages.{ttr}", color= ctx.author.color)
        embed.add_field(name="💁 **Help Modules:**", value="Page 1 | SysBot Commands\nPage 2 | Pokemon Files Commands\nPage 3 | Miscellaneous Commands\nPage 4 | Management Commands\nPage 5 | Moderation Commands\nPage 6 | Switch Commands\nPage 7 | Owner Commands\nPage 8 | Bot Management Commands", inline=True)
        embed.add_field(name="ℹ️ **Bot Info:**", value=f"Servers: {len(self.client.guilds)}\nUsers: {len(self.client.users)}\nCommands: {len(self.client.commands)}\nCPU: {psutil.cpu_percent()}%\nMemory: {psutil.virtual_memory().percent}%", inline=True)
        sysbot = discord.Embed(
            title='SysBot Module', description=ttr, color=ctx.author.color
        )

        sysbot.add_field(name="SysBot Commands", value=sysbotval, inline=True)
        files = discord.Embed(
            title='Files Module', description=ttr, color=ctx.author.color
        )

        files.add_field(name="Pkx and Ekx Search Commands", value=filesval, inline=True)
        general = discord.Embed(
            title='Miscellaneous Module', description=ttr, color=ctx.author.color
        )

        general.add_field(name="General Commands", value=miscellaneousval, inline=True)
        amanagement = discord.Embed(
            title='Channel Management Module',
            description=ttr,
            color=ctx.author.color,
        )

        amanagement.add_field(name="Channel Commands", value=chanval, inline=True)
        moderation = discord.Embed(
            title='Moderation Module', description=ttr, color=ctx.author.color
        )

        moderation.add_field(name="Server Moderation Commands", value=modval, inline=True)
        sremote = discord.Embed(
            title='Switch Module', description=ttr, color=ctx.author.color
        )

        sremote.add_field(name="Switch Remote Control Commands", value=remoteval, inline=True)
        owner = discord.Embed(
            title='Owner Module', description=ttr, color=ctx.author.color
        )

        owner.add_field(name="Owner Only Commands", value=ownerval, inline=True)
        omanagement = discord.Embed(
            title='Bot Management Module', description=ttr, color=ctx.author.color
        )

        omanagement.add_field(name="Bot Management Commands", value=botmanval, inline=True)

        components=[
            [
                Select(
                    placeholder="Select a help menu",
                    options=[
                        SelectOption(label="Page 1 | SysBot Module", value="sysbot"),
                        SelectOption(label="Page 2 | Files Module", value="files"),
                        SelectOption(label="Page 3 | Miscellaneous Module", value="general"),
                        SelectOption(label="Page 4 | Channel Management Module", value="amanagement"),
                        SelectOption(label="Page 5 | Moderation Module", value="moderation"),
                        SelectOption(label="Page 6 | Switch Remote Module", value="sremote"),
                        SelectOption(label="Page 7 | Owner Module", value="owner"),
                        SelectOption(label="Page 8 | Bot Management Module", value="omanagement")
                        ],
                    )
            ],
            [
                Button(label='Support Server', style=ButtonStyle.URL, url=support2)
            ]
        ]

        message = await ctx.reply(embed=embed, components=components)

        while(True):
            try:
                interaction = await self.client.wait_for("select_option", check=None, timeout=30)
                if interaction.values[0] == "sysbot":
                    await interaction.respond(type=7, ephemeral=False, embed=sysbot)
                if interaction.values[0] == "files":
                    await interaction.respond(type=7, ephemeral=False, embed=files)
                if interaction.values[0] == "general":
                    await interaction.respond(type=7, ephemeral=False, embed=general)
                if interaction.values[0] == "amanagement":
                    await interaction.respond(type=7, ephemeral=False, embed=amanagement)
                if interaction.values[0] == "moderation":
                    await interaction.respond(type=7, ephemeral=False, embed=moderation)
                if interaction.values[0] == "sremote":
                    await interaction.respond(type=7, ephemeral=False, embed=sremote)
                if interaction.values[0] == "owner":
                    await interaction.respond(type=7, ephemeral=False, embed=owner)
                if interaction.values[0] == "omanagement":
                    await interaction.respond(type=7, ephemeral=False, embed=omanagement)
            except asyncio.TimeoutError:
                await message.disable_components()
                return


def setup(client):
    client.add_cog(help(client))