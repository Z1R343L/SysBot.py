print("Launching SysBot.py...")

import discord
from discord.ext import commands
import os
import yaml
from yaml import load
yaml.warnings({'YAMLLoadWarning': False})
from discord_slash import SlashCommand
from colorama import Fore
import ctypes
from rich.console import Console
import subprocess
import json

# Loads token and autolauncher from config file
with open("config.yaml") as file:
    data = load(file)
    token = data["token"]
    botprefix = data["defaultprefix"]
    autolauncher = data["autolauncher"]
    twitch = data["twitch"]

# Fetch prefix 
def get_prefix(client, message):
        with open("res/prefix.json", "r") as f:
            prefixes = json.load(f)
        if str(message.guild.id) in prefixes:
            prefix = prefixes[str(message.guild.id)]
            return commands.when_mentioned_or(*prefix)(client, message)
        else:
            prefixes[str(message.guild.id)] = botprefix
            with open("res/prefix.json", "w") as f:
                json.dump(prefixes, f, indent=4)
            return commands.when_mentioned_or(botprefix)(client, message)

##Simple bot settings like mentioning as a prefix, settings all intents to true, deleting built in discord.py help command
client = commands.AutoShardedBot(name="SysBot 2.1.0", command_prefix=get_prefix, intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
pokemon = ["connection"] 
pdiscord = ["advanced", "pokeinput", "queue", "remote", "trader"]

console = Console()

# State if autolauncher is toggled
if autolauncher == 1:
    console.print("Autolauncher set to true.", style="green")
if autolauncher == 2:
    console.print("Autolauncher set to false.", style="green")
    
#Bot Start Up
@client.event
async def on_ready():
    ctypes.windll.kernel32.SetConsoleTitleW('{0.user}'.format(client) + ' ALPHA')
    console.clear()
    print(f'''{Fore.LIGHTBLUE_EX}
           _____           ____        _                 
          / ____|         |  _ \      | |                
         | (___  _   _ ___| |_) | ___ | |_   _ __  _   _ 
          \___ \| | | / __|  _ < / _ \| __| | '_ \| | | |
          ____) | |_| \__ \ |_) | (_) | |_ _| |_) | |_| |
         |_____/ \__, |___/____/ \___/ \__(_)  __/ \__, |
                  __/ |                     | |     __/ |
                 |___/                      |_|    |___/ \x1b[0m{Fore.MAGENTA}By 6A\x1b[0m
{Fore.WHITE}────────────────────────────────────────────────────────────────────────────────                                  
                    {Fore.LIGHTRED_EX}Connected as: {Fore.LIGHTYELLOW_EX}{client.user}
                    {Fore.LIGHTRED_EX}Guild Count: {Fore.LIGHTYELLOW_EX}{len(client.guilds)}    
{Fore.WHITE}──────────────────────────────────────────────────────────────────────────────── 
    ''')

    if autolauncher == 1:
        try:
            client.load_extension("pokemon.connection.wireless")
        except Exception as e:
            console.print(f"Unable to load {e}.", style="red")
        for extension in pdiscord:
            try:
                client.load_extension("pokemon.discord." + extension)
            except Exception as e:
                console.print(f"Unable to load {extension} {e}.", style="red")

    elif autolauncher == 2:
        console.print('The bot will launch without sysbot commands.', style="blue")

    else:
        console.print("Would you like to connect a Nintendo Switch to your bot?\nType Y to load the sysbot module, type N to continue without the sysbot.", style="yellow")
        yes = {'yes', 'y'}
        choice = input().lower()
        if choice in yes:
            try:
                client.load_extension("pokemon.connection.wireless")
            except Exception as e:
                console.print(f"Unable to load {e}.", style="red")
            for extension in pdiscord:
                try:
                    client.load_extension("pokemon.discord." + extension)
                except Exception as e:
                    console.print(f"Unable to load {extension} {e}.", style="red")
        else:
            print('The bot will launch without sysbot commands.')
            
    if twitch == 1:
        subprocess.Popen('python pokemon/twitch.py')
        
    elif autolauncher == 2 or twitch == 2:
        pass

    else:
        console.print("Would you like to launch Sysbot-Twitch.py?", style="blue")
        yes = {'yes', 'y'}
        choice = input().lower()
        if choice in yes:
            subprocess.Popen('python pokemon/twitch.py')
        else:
            print('The bot will launch without sysbot commands.')

# Build Plugins List
plugins = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        plugins.append("cogs." + filename[:-3])
            
# Load plugins
if __name__ == '__main__':
    for x in plugins:
        try:
            client.load_extension(x)
        except Exception as e:
            console.print(f"Unable to load {x}: {e}.", style="red")

#Debugger || {defaultprefix}jsk debug <command>
client.load_extension('jishaku')

try:
    client.run('{}'.format(token))
except Exception as e:
    print(f"Error when logging in: {e}")