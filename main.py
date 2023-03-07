import ast
import discord
from discord.ext import commands

intents = discord.Intents.all()

client = commands.Bot(command_prefix=';', help_command=None, intents=intents)

with open('homework_tasks', 'r') as f:
    subject = ast.literal_eval(f.read())


def get_real_subject(subject_name):
    for i in subject:
        if i.lower() == subject_name.lower():
            return i
    raise KeyError('This subject doesn\'t exist!')


def get_subject_homework(subject_name):
    for i in subject:
        if i.lower() == subject_name.lower():
            return subject[i]
    raise KeyError('This subject doesn\'t exist!')


def set_subject_homework(subject_name, assignment):
    for i in subject:
        if i.lower() == subject_name.lower():
            subject[i] = assignment
            return
    raise KeyError('This subject doesn\'t exist!')


def add_subject(subject_name):
    for i in subject:
        if i.lower() == subject_name.lower():
            raise KeyError('This subject is already added!')
        elif subject_name.lower() == 'all':
            raise NameError('You can\'t add an \'all\' subject!')
    subject[subject_name] = 'None'


def remove_subject(subject_name):
    for i in subject:
        if i.lower() == subject_name.lower():
            subject.pop(i)
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
                await ctx.send('That subject never existed!')
    else:
        await ctx.send('Invalid arguments!')
    await client.tree.sync()


@client.hybrid_command(brief='Need homework reminders?')
async def homework(ctx, *, subject_name=None):
    if subject_name is None:
        await ctx.send('You need to specify what subject you want to check homework for!')
    elif subject_name.lower() == 'all':
        message = 'Homework for all subjects: '
        for i in subject:
            message = message + i + ": " + subject[i] + ", "
        message = message[0:-2]
        await ctx.send(message)
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
    try:
        real_subject = get_real_subject(subject_name)
    except KeyError:
        await ctx.send('That is not a valid subject!')
    if clear is not None:
        if clear.lower() == "clear":
            try:
                set_subject_homework(real_subject, 'None')
                await ctx.send(f'Successfully cleared the homework of {real_subject}')
            except KeyError:
                await ctx.send('That is not a valid subject!')
        else:
            await ctx.send('Invalid clear argument!')
    else:
        try:
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
        except TimeoutError:
            await ctx.send('Homework timeout')
    await client.tree.sync()


@client.hybrid_command(brief='Kill the bot')
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
