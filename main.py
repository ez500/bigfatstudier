"""Initialize the bot"""

import asyncio
import os
import discord
from discord.ext import commands
from discord.ext import tasks

import data_config

intents = discord.Intents.all()

with open('client.token', 'r') as f:
    token = f.readline().strip()

client = commands.Bot(command_prefix=';', help_command=None, intents=intents)


@client.event
async def on_ready():
    print('Bot ready')


@client.event
async def on_member_join(member):
    await client.change_presence(status=discord.Status.do_not_disturb)
    print(f'{member} just joined')


@tasks.loop(minutes=10)
async def save_task():
    data_config.save_all()


async def load_cogs():
    for file in os.listdir('./cogs'):
        if os.fsdecode(file).endswith('.py'):
            await client.load_extension(f'cogs.{file[0:-3]}')


async def main():
    save_task.start()
    await load_cogs()
    await client.start(token)


if __name__ == '__main__':
    asyncio.run(main())
