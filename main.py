import ast
import discord
from discord.ext import commands

intents = discord.Intents.all()

client = commands.Bot(command_prefix=';', help_command=None, intents=intents)

with open('homework_tasks', 'r') as f:
    subject = ast.literal_eval(f.read())


def check_subject(subject_name):
    for i in subject:
        if i == subject_name:
            return True
    return False


def get_subject_homework(subject_name):
    for i in subject:
        if i == subject_name:
            return subject[subject_name]
    raise KeyError('This subject doesn\'t exist!')


def set_subject_homework(subject_name, assignment):
    for i in subject:
        if i == subject_name:
            subject[subject_name] = assignment
            return
    raise KeyError('This subject doesn\'t exist!')


def add_subject(subject_name):
    for i in subject:
        if i == subject_name:
            raise KeyError('This subject is already added!')
    subject[subject_name] = 'None'


def remove_subject(subject_name):
    for i in subject:
        if i == subject_name:
            subject.pop(subject_name)
            return
    raise KeyError('This subject never existed!')


def save_all():
    with open('homework_tasks', 'w') as file:
        file.write(repr(subject))


@client.event
async def on_ready():
    print('Bot ready')


@client.event
async def on_member_join(member):
    print(f'{member} just joined')


@client.hybrid_command(brief='List of commands')
async def help(ctx):
    embed = discord.Embed(color=0x255FAB, title='bigfatstudier Bot Commands',
                          description='Don\'t know commands? Not to worry!')
    embed.add_field(name='subjects', value='Know what subjects this bot manages homework for!')
    embed.add_field(name='homework', value='Know the homework that you have to do for each class!')
    await ctx.send(embed=embed)
    await client.tree.sync()


@client.hybrid_command(brief='List of subjects')
async def subjects(ctx, options=None, *, subject_name=None):
    if options is None:
        await ctx.send('Options are: *list*, *add*, *remove*')
    elif options.lower() == 'list':
        if repr(subject) == '{}':
            await ctx.send('There are yet to be subjects to be added!')
        else:
            subject_list = ''
            for i in subject:
                subject_list = subject_list + i + ", "
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
                await ctx.send(f'{subject_name} already exists!')
    elif options.lower() == 'remove':
        if subject_name is None:
            await ctx.send('You need to specify what subject you want to remove!')
        else:
            try:
                remove_subject(subject_name)
                await ctx.send(f'The subject {subject_name} has been successfully removed')
            except KeyError:
                await ctx.send('That subject never existed!')
    else:
        await ctx.send('Invalid arguments!')
    await client.tree.sync()


@client.hybrid_command(brief='Need homework reminders?')
async def homework(ctx, *, subject_name=None):
    if subject_name is None:
        await ctx.send('You need to specify what subject you want to check homework for!')
    else:
        try:
            await ctx.send(get_subject_homework(subject_name))
        except KeyError:
            await ctx.send(f'There is no such subject as {subject_name}!')
    await client.tree.sync()


@client.hybrid_command(brief='Set homework reminder')
async def set_homework(ctx, *, subject_name=None, clear=None):
    if subject_name is None:
        await ctx.send('You need to specify a subject to set the homework to!')
    elif not check_subject(subject_name):
        await ctx.send('That is not a valid subject!')
    elif clear is not None:
        if clear.lower() == "clear":
            try:
                set_subject_homework(subject_name, 'None')
                await ctx.send(f'Successfully cleared the homework of {subject_name}')
            except KeyError:
                await ctx.send('That is not a valid subject!')
        else:
            await ctx.send('Invalid clear argument!')
    else:
        await ctx.send('What homework does that subject have?')

        def check(m):
            return m.channel == ctx.channel

        msg = await client.wait_for('message', check=check, timeout=20.0)
        set_subject_homework(subject_name, msg.content)
        await ctx.send(f'Successfully set the homework of {subject_name} to {msg.content}')
    await client.tree.sync()


@client.hybrid_command(brief='Kill the bot')
async def stop(ctx):
    save_all()
    await ctx.send('Shutting down')
    await client.tree.sync()
    await client.close()


with open('token', 'r') as f:
    token = f.read()
save_all()
client.run(token)
