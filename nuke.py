from discord.ext import commands
from colorama import init, Fore, Style
from time import sleep

import os
import re
init(convert=True)

def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def get_all_tokens():
    roaming = os.getenv('APPDATA')

    paths = {
        'Discord': roaming + '\\Discord',
    }

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue
 
        tokens = find_tokens(path)

        if len(tokens) == 0:
            print(f"{Fore.RED}TOKEN NOT FOUND!{Style.RESET_ALL}")
            return
        else:
            print(f"{Fore.GREEN}[!]{Style.RESET_ALL} {len(tokens)} Token(s) Found!")
            return tokens

def auto_fill_token(tokens):
    print(f"{Fore.BLUE}[-]{Style.RESET_ALL} Attempting to connect")
    for token in tokens:
        try:
            client.run(token, bot=False)
        except RuntimeError:
            pass
    os.system("cls")

prefix = "!" 

client = commands.Bot(command_prefix=prefix, self_bot=True)
client.remove_command("help")

@client.event
async def on_ready():
    print(f"{Fore.GREEN}[!]{Style.RESET_ALL} Ready!")
    print(f"\nName: {Fore.BLUE}{client.user.name}{Style.RESET_ALL}\n" + 
          f"ID: {Fore.BLUE}{client.user.id}{Style.RESET_ALL}")
    print(f"Type {Fore.YELLOW}!clear{Style.RESET_ALL} in a Channel or DM to remove messages")

@client.listen()
async def on_command_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        print(f"{Fore.RED}[x] Error{Style.RESET_ALL}: Ensure your limit is a number.", end="\n\n")

@client.command()
async def clear_id(ctx, id : int=None, skipx : int=0,  limit : int=None):
    channel = client.get_channel(id)
    print(f"{Fore.BLUE}[-]{Style.RESET_ALL} Purging {Fore.BLUE}{channel}{Style.RESET_ALL}")
    count = 0
    async for msg in channel.history(limit=limit):
        if client.user.id == msg.author.id:
            count += 1

    iter = 0
    async for msg in channel.history(limit=limit):
        if client.user.id == msg.author.id:
            iter += 1
            sleep(0.3)
            if iter < skipx:
                print(f"{Fore.BLUE}[{iter}/{count}]{Style.RESET_ALL} {Fore.MAGENTA}SKIPPED{Style.RESET_ALL} message: {Fore.CYAN}{msg.content}{Style.RESET_ALL}")
                continue

            print (f"{Fore.BLUE}[{iter}/{count}]{Style.RESET_ALL} {Fore.RED}DELETED{Style.RESET_ALL} message: {Fore.CYAN}{msg.content}{Style.RESET_ALL}")
            await msg.delete()

    print(count)



@client.command()
async def clear(ctx, limit: int=None):
    count = 0
    try:
        nukee = str(ctx.message.channel).split(' ')[3]
        print (f"\n{Fore.BLUE}[-]{Style.RESET_ALL} Purging DM's with: {Fore.BLUE}{nukee}{Style.RESET_ALL}")
     
    except IndexError:
        channel_str = ctx.message.channel
        print (f"{Fore.BLUE}[-]{Style.RESET_ALL} Purging Messages in: {Fore.BLUE}#{channel_str}{Style.RESET_ALL}")


    async for msg in ctx.message.channel.history(limit=limit):
        
        if client.user.id == msg.author.id:
            try:
                await msg.delete()
                count += 1
            except:
                pass

    print(f"{Fore.GREEN}[!]{Style.RESET_ALL} Purge Complete!\n" +
          f"{Fore.BLUE}[-]{Style.RESET_ALL} Removed {Fore.RED}{count}{Style.RESET_ALL} messages.", end="\n\n")

def main():
    while(True):
        print(f"Token Mode:\n" +
            f"{Fore.BLUE}[1]{Style.RESET_ALL} - Get Token Automatically\n" +
            f"{Fore.BLUE}[2]{Style.RESET_ALL} - Input Token Manually")

        choice = input("Input choice : ")

        if choice == "1":
            os.system('cls')
            auto_fill_token(get_all_tokens())
            break  

        elif choice == "2":
            print(f"\n{Fore.BLUE}[-]{Style.RESET_ALL} Manual mode selected!")
            token = input("Input Token : ")
            
            if token[0] and token[-1] == '"':
                token = str(token[1:-1])

            os.system('cls')
            try:
                client.run(token, bot=False)
            except:
                print(f"{Fore.RED}Invalid Token! Please restart program{Style.RESET_ALL}")
                break

        else:
            print(f"{Fore.RED}Invalid choice! Please try again!{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
