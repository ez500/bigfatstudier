import asyncio

import discord
from discord.ext import commands

from data import subject, get_real_subject, get_subject_homework, set_subject_homework, add_subject, remove_subject


class Subjects(commands.Cog, name='subjects'):
    def __init__(self, client):
        self.client = client

    # TODO: SUBJECT ALIAS
    # TODO: MULTIPLE HOMEWORK ASSIGNMENTS
    @commands.hybrid_command(brief='List of subjects', description='Know what subjects this bot manages homework for')
    async def subjects(self, ctx, options=None, *, subject_name=None):
        if options is None or options.lower() == 'list':
            if repr(subject) == '{}':
                await ctx.send('There are yet to be subjects to be added!')
            else:
                subject_list = ''
                for i in subject:
                    subject_list += i + ', '
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
        await self.client.tree.sync()

    @subjects.autocomplete('options')
    async def help_autocomplete(self, interaction, current):
        options = ['list', 'add', 'remove']
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @subjects.autocomplete('subject_name')
    async def help_autocomplete(self, interaction, current):
        options = [subject_name for subject_name in subject]
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(brief='Need homework reminders?',
                             description='Know the homework that you have to do for each class')
    async def homework(self, ctx, *, subject_name=None):
        if subject_name is None:
            await ctx.send('You need to specify what subject you want to check homework for!')
        elif subject_name.lower() == 'all':
            message = 'Homework for all subjects:\n'
            for i in subject:
                message += i + ': ' + subject[i] + '\n'
            message = message[0:-1]
            await ctx.send(message)
        else:
            try:
                await ctx.send(get_subject_homework(subject_name))
            except KeyError:
                await ctx.send(f'There is no such subject as {subject_name}!')
        await self.client.tree.sync()

    @homework.autocomplete('subject_name')
    async def help_autocomplete(self, interaction, current):
        options = [subject_name for subject_name in subject]
        options.insert(0, 'all')
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(brief='Set subject homework', description='Set homework for a subject')
    async def set_homework(self, ctx, *, subject_name=None, clear=None):
        if subject_name is None:
            await ctx.send('You need to specify a subject to set the homework to!')
        elif clear is not None:
            if clear.lower() == 'clear':
                if subject_name.lower() == 'all':
                    if ctx.author.id == 434430979075997707:
                        try:
                            await ctx.send('Are you sure you want to clear the homework for all subjects?')
                            msg = await self.client.wait_for('message',
                                                             check=lambda m: m.channel == ctx.channel and
                                                                             m.author == ctx.author,
                                                             timeout=20.0)
                            if msg.content.lower() == 'yes':
                                for i in subject:
                                    set_subject_homework(i, 'None')
                                await ctx.send('Cleared homework for all subjects')
                            else:
                                await ctx.send('Confirmation failed')
                        except asyncio.exceptions.TimeoutError:
                            await ctx.send('Timeout! Confirmation failed')
                    else:
                        await ctx.send('Sorry, only certain users are able to clear all of the homework.')
                else:
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
                if subject_name == 'all':
                    await ctx.send('You can\'t set a homework for all subjects.')
                else:
                    try:
                        real_subject = get_real_subject(subject_name)
                        await ctx.send('What homework does that subject have?')
                        msg = await self.client.wait_for('message',
                                                         check=lambda m: m.channel == ctx.channel and
                                                                         m.author == ctx.author,
                                                         timeout=40.0)
                        if msg.content.lower() == 'clear':
                            set_subject_homework(real_subject, 'None')
                            await ctx.send(f'Successfully cleared the homework of {real_subject}')
                        else:
                            set_subject_homework(real_subject, msg.content)
                            await ctx.send(f'Successfully set the homework of {real_subject} to {msg.content}')
                    except KeyError:
                        await ctx.send(f'There is no such subject as {subject_name}!')
                    except asyncio.exceptions.TimeoutError:
                        await ctx.send('Timeout! No homework specified in time')
        await self.client.tree.sync()

    @set_homework.autocomplete('subject_name')
    async def help_autocomplete(self, interaction, current):
        options = [subject_name for subject_name in subject]
        options.insert(0, 'all')
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @set_homework.autocomplete('clear')
    async def help_autocomplete(self, interaction, current):
        options = ['clear']
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]


async def setup(client):
    await client.add_cog(Subjects(client))
