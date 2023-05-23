import asyncio
import os

import discord
from discord.ext import commands
from discord.ext import tasks

import data

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


@commands.hybrid_command(brief='List of commands', description='Need help? Call this command!')
async def help(ctx, options=None):
    all_subjects = ''
    for subject_name in data.subject:
        all_subjects += subject_name + ', '
    all_subjects = all_subjects[0:-2]
    if options is None:
        embed = discord.Embed(color=0x255FAB, title='bigfatstudier Bot Commands',
                              description='Don\'t know commands? Not to worry!')
        for command in client.commands:
            embed.add_field(name=command.name, value=command.description)
        await ctx.send(embed=embed)
    elif options.lower() == 'subjects':
        embed = discord.Embed(color=0xFF9100, title='bigfatstudier \'subjects\' Command',
                              description=client.get_command('subjects'))
        embed.add_field(name='list', value='List all of the subjects stored on this bot')
        embed.add_field(name='add', value='Add a subject to store on this bot')
        embed.add_field(name='remove', value='Remove a subject from this bot')
        await ctx.send(embed=embed)
    elif options.lower() == 'homework':
        embed = discord.Embed(color=0x00D4FF, title='bigfatstudier \'homework\' Command',
                              description=client.get_command('homework').description)
        embed.add_field(name='all', value='List all of the homework from every subject stored on this bot')
        embed.add_field(name='*Specific Subject*', value=f'Specify a subject to check homework: {all_subjects}')
        await ctx.send(embed=embed)
    elif options.lower() == 'set_homework':
        embed = discord.Embed(color=0xB300FF, title='bigfatstudier \'set_homework\' Command',
                              description=client.get_command('set_homework').description)
        embed.add_field(name='Param1: *Specific Subject*',
                        value=f'Specify a subject to set homework to: {all_subjects}')
        embed.add_field(name='Param2: [clear]', value='Specify whether you want to clear the homework or not')
        await ctx.send(embed=embed)
    else:
        await ctx.send(f'{options} is not a valid command!')
    await client.tree.sync()


@help.autocomplete('options')
async def help_autocomplete(interaction, current):
    options = [command.name for command in client.commands if command.name != 'help' and command.name != 'stop']
    return [discord.app_commands.Choice(name=option, value=option)
            for option in options if current.lower() in option.lower()]


@client.hybrid_command(brief='Kill the bot', description='Kill the bot, but only for for owner')
async def stop(ctx):
    if ctx.author.id == 434430979075997707:
        data.save_all()
        await ctx.send('Shutting down')
        await client.tree.sync()
        await client.close()
    else:
        await ctx.send('You think I\'d let anyone close the bot?')
        await client.tree.sync()


@tasks.loop(minutes=10)
async def save_task():
    data.save_all()


async def load_cogs():
    for file in os.listdir('cogs'):
        if os.fsdecode(file).endswith('.py'):
            await client.load_extension(f'cogs.{file[0:-3]}')


async def main():
    save_task.start()
    await load_cogs()
    await client.start(token)


if __name__ == '__main__':
    asyncio.run(main())
