import discord
from discord.ext import commands
from colorama import Fore, Style

token = "" # Put Token Here
prefix = "!" 

client = commands.Bot(command_prefix=prefix, self_bot=True)
client.remove_command("help")

@client.event
async def on_ready():
    print(f"Name: {Fore.RED}{client.user.name}{Style.RESET_ALL}\n" + 
          f"ID: {Fore.RED}{client.user.id}{Style.RESET_ALL}\n")

@client.command()
async def clr(ctx, limit: int=None):
    try:
        nukee = str(ctx.message.channel).split(' ')[3]
        print (f"{Fore.BLUE}[!]{Style.RESET_ALL} Nuking DM's with: {Fore.BLUE}{nukee}{Style.RESET_ALL}")
    
    except IndexError:
        channel_str = ctx.message.channel
        print (f"{Fore.BLUE}[!]{Style.RESET_ALL} Nuking messages in : {Fore.BLUE}#{channel_str}{Style.RESET_ALL}")


    async for msg in ctx.message.channel.history(limit=limit):
        if msg.author.id == client.user.id:
            try:
                await msg.delete()
            except:
                pass

    print(f"{Fore.GREEN}[!] Nuke Complete{Style.RESET_ALL}")

client.run(token, bot=False)
