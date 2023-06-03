"""Initialize the bot"""

import asyncio
import os
import signal
import sys
import discord
from discord.ext import commands
from discord.ext import tasks

from constants import *
from data_config import *


def termination_handler(_signal, _frame):
    print('Termination signal detected!')
    save_all()
    sys.exit(0)


signal.signal(signal.SIGINT, termination_handler)

intents = discord.Intents.all()

with open('client.token', 'r') as f:
    token = f.readline().strip()

client = commands.Bot(command_prefix=';', help_command=None, intents=intents)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.do_not_disturb)
    await client.tree.sync()
    print(f'Bot ready. {VERSION}')


@tasks.loop(minutes=10)
async def save_task():
    save_all()
    await client.tree.sync()


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
