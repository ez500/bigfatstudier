import ast
import asyncio.exceptions

import discord
from discord import Intents
from discord.ext import commands
from discord.ext.commands import Bot

intents: Intents = discord.Intents.all()

client: Bot = commands.Bot(command_prefix=';', help_command=None, intents=intents)

with open('subject', 'r') as f:
    subject = ast.literal_eval(f.read())


# TODO: COG AND ORGANIZATION
def get_real_subject(subject_name: str) -> str:
    subject_name = ' '.join(subject_name.split())
    for i in subject:
        if i.lower() == subject_name.lower():
            return i
    raise KeyError('This subject doesn\'t exist!')


def get_subject_homework(subject_name: str) -> str:
    subject_name = ' '.join(subject_name.split())
    for i in subject:
        if i.lower() == subject_name.lower():
            return subject[i]
    raise KeyError('This subject doesn\'t exist!')


def set_subject_homework(subject_name: str, assignment: str) -> None:
    subject_name = ' '.join(subject_name.split())
    for i in subject:
        if i.lower() == subject_name.lower():
            subject[i] = assignment
            return
    raise KeyError('This subject doesn\'t exist!')


def add_subject(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split())
    for i in subject:
        if i.lower() == subject_name.lower():
            raise KeyError('This subject is already added!')
        elif subject_name.lower() == 'all':
            raise NameError('You can\'t add an \'all\' subject!')
    subject[subject_name] = 'None'


def remove_subject(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split())
    for i in subject:
        if i.lower() == subject_name.lower():
            subject.pop(i)
            return
    raise KeyError('This subject never existed!')


def save_all() -> None:
    with open('subject', 'w') as file:
        file.write(repr(subject))


@client.event
async def on_ready():
    print('Bot ready')


@client.event
async def on_member_join(member):
    print(f'{member} just joined')


@client.hybrid_command(brief='List of commands', description='Need help? Call this command!')
async def help(ctx, options=None):
    all_subjects = ''
    for subject_name in subject:
        all_subjects = all_subjects + subject_name + ', '
    all_subjects = all_subjects[0:-2]
    if options is None:
        embed = discord.Embed(color=0x255FAB, title='bigfatstudier Bot Commands',
                              description='Don\'t know commands? Not to worry!')
        for command in client.commands:
            embed.add_field(name=command.name, value=command.description)
        await ctx.send(embed=embed)
    elif options.lower() == 'subjects':
        embed = discord.Embed(color=0xFF9100, title='bigfatstudier \'subjects\' Command',
                              description=subjects.description)
        embed.add_field(name='list', value='List all of the subjects stored on this bot')
        embed.add_field(name='add', value='Add a subject to store on this bot')
        embed.add_field(name='remove', value='Remove a subject from this bot')
        await ctx.send(embed=embed)
    elif options.lower() == 'homework':
        embed = discord.Embed(color=0x00D4FF, title='bigfatstudier \'homework\' Command',
                              description=homework.description)
        embed.add_field(name='all', value='List all of the homework from every subject stored on this bot')
        embed.add_field(name='*Specific Subject*', value=f'Specify a subject to check homework: {all_subjects}')
        await ctx.send(embed=embed)
    elif options.lower() == 'set_homework':
        embed = discord.Embed(color=0xB300FF, title='bigfatstudier \'set_homework\' Command',
                              description=set_homework.description)
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


# TODO: SUBJECT ALIAS
# TODO: MULTIPLE HOMEWORK ASSIGNMENTS
@client.hybrid_command(brief='List of subjects', description='Know what subjects this bot manages homework for')
async def subjects(ctx, options=None, *, subject_name=None):
    if options is None or options.lower() == 'list':
        if repr(subject) == '{}':
            await ctx.send('There are yet to be subjects to be added!')
        else:
            subject_list = ''
            for i in subject:
                subject_list = subject_list + i + ', '
            subject_list = subject_list[0:-2]
            await ctx.send(subject_list)
    elif options.lower() == 'add':
        if subject_name is None:
            await ctx.send('You need to specify what subject you want to add!')
        else:
            try:
                add_subject(subject_name)
                await ctx.send(f'Successfully added {subject_name} to the subject list!')
            except KeyError:
                real_subject = get_real_subject(subject_name)
                await ctx.send(f'{real_subject} already exists!')
            except NameError:
                await ctx.send('You can\'t add an \'all\' subject!')
    elif options.lower() == 'remove':
        if subject_name is None:
            await ctx.send('You need to specify what subject you want to remove!')
        else:
            try:
                real_subject = get_real_subject(subject_name)
                remove_subject(real_subject)
                await ctx.send(f'The subject {real_subject} has been successfully removed')
            except KeyError:
                await ctx.send(f'There is no such subject as {subject_name}!')
    else:
        await ctx.send('Invalid arguments!')
    await client.tree.sync()


@subjects.autocomplete('options')
async def help_autocomplete(interaction, current):
    options = ['list', 'add', 'remove']
    return [discord.app_commands.Choice(name=option, value=option)
            for option in options if current.lower() in option.lower()]


@subjects.autocomplete('subject_name')
async def help_autocomplete(interaction, current):
    options = [subject_name for subject_name in subject]
    return [discord.app_commands.Choice(name=option, value=option)
            for option in options if current.lower() in option.lower()]


@client.hybrid_command(brief='Need homework reminders?',
                       description='Know the homework that you have to do for each class')
async def homework(ctx, *, subject_name=None):
    if subject_name is None:
        await ctx.send('You need to specify what subject you want to check homework for!')
    elif subject_name.lower() == 'all':
        message = 'Homework for all subjects:\n'
        for i in subject:
            message = message + i + ': ' + subject[i] + '\n'
        message = message[0:-1]
        await ctx.send(message)
    else:
        try:
            await ctx.send(get_subject_homework(subject_name))
        except KeyError:
            await ctx.send(f'There is no such subject as {subject_name}!')
    await client.tree.sync()


@homework.autocomplete('subject_name')
async def help_autocomplete(interaction, current):
    options = [subject_name for subject_name in subject]
    options.insert(0, 'all')
    return [discord.app_commands.Choice(name=option, value=option)
            for option in options if current.lower() in option.lower()]


@client.hybrid_command(brief='Set subject homework', description='Set homework for a subject')
async def set_homework(ctx, *, subject_name=None, clear=None):
    if subject_name is None:
        await ctx.send('You need to specify a subject to set the homework to!')
    elif clear is not None:
        if clear.lower() == 'clear':
            try:
                real_subject = get_real_subject(subject_name)
                set_subject_homework(real_subject, 'None')
                await ctx.send(f'Successfully cleared the homework of {real_subject}')
            except KeyError:
                await ctx.send(f'There is no such subject as {subject_name}!')
        else:
            await ctx.send('Invalid clear argument!')
    else:
        if (subject_name[-5:-1] + subject_name[-1]).lower() == 'clear':
            subject_name = subject_name[0:-6]
            try:
                real_subject = get_real_subject(subject_name)
                set_subject_homework(real_subject, 'None')
                await ctx.send(f'Successfully cleared the homework of {real_subject}')
            except KeyError:
                await ctx.send(f'There is no such subject as {subject_name}!')
        else:
            try:
                real_subject = get_real_subject(subject_name)
                await ctx.send('What homework does that subject have?')

                def check(m):
                    return m.channel == ctx.channel and m.author == ctx.author

                msg = await client.wait_for('message', check=check, timeout=40.0)
                if msg.content.lower() == 'clear':
                    set_subject_homework(real_subject, 'None')
                    await ctx.send(f'Successfully cleared the homework of {real_subject}')
                else:
                    set_subject_homework(real_subject, msg.content)
                    await ctx.send(f'Successfully set the homework of {real_subject} to {msg.content}')
            except KeyError:
                await ctx.send(f'There is no such subject as {subject_name}!')
            except asyncio.exceptions.TimeoutError:
                await ctx.send('Timeout! You didn\'t specify homework to set in time')
    await client.tree.sync()


@set_homework.autocomplete('subject_name')
async def help_autocomplete(interaction, current):
    options = [subject_name for subject_name in subject]
    return [discord.app_commands.Choice(name=option, value=option)
            for option in options if current.lower() in option.lower()]


@set_homework.autocomplete('clear')
async def help_autocomplete(interaction, current):
    options = ['clear']
    return [discord.app_commands.Choice(name=option, value=option)
            for option in options if current.lower() in option.lower()]


@client.hybrid_command(brief='Kill the bot', description='Kill the bot, but only for for owner')
async def stop(ctx):
    if ctx.author.id == 434430979075997707:
        save_all()
        await ctx.send('Shutting down')
        await client.tree.sync()
        await client.close()
    else:
        await ctx.send('You think I\'d let anyone close the bot?')
        await client.tree.sync()


with open('token', 'r') as f:
    token = f.read()
save_all()
client.run(token)
