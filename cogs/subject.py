"""Subject commands"""

import asyncio
import discord
from discord.ext import commands

from util import *


class Subject(commands.Cog, name='subject'):
    def __init__(self, client: commands.Bot):
        self.client = client

    # TODO: ADD REMOVE_HOMEWORK
    # TODO: ALIAS, DESCRIPTION
    # TODO: UPDATE EVERYTHING WITH SUBJECT ALIASES
    @commands.hybrid_command(brief='List of subjects', description='Know what subjects this bot manages homework for')
    async def subjects(self, ctx, options=None, *, subject_name=None):  # lists/add/remove subject, list description
        if options is None or options.lower() == 'list':
            if subject_name is None:
                if repr(subject) == '{}':
                    await ctx.send('There are yet to be subjects to be added!')
                    return
                subject_list = '**Subjects:** '
                for name in subject:
                    subject_list += get_real_subject(name)[1] + ', '
                subject_list = subject_list[0:-2]
                await ctx.send(subject_list)
                return
        elif options.lower() == 'add':
            if subject_name is None:
                try:
                    await ctx.send('What is the name of the subject you want to add?')
                    msg = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                    subject_name = msg.content
                except asyncio.TimeoutError:
                    await ctx.send('Failed to add subject!')
                    return
            try:
                add_subject(subject_name)
                await ctx.send(f'Successfully added {subject_name} to the subject list!')
            except KeyError:
                real_subject = get_real_subject(subject_name)
                await ctx.send(f'{real_subject[1]} already exists!')
            except AttributeError:
                await ctx.send('You can\'t add an \'all\' subject!')
            return
        elif options.lower() == 'remove':
            if subject_name is None:
                try:
                    await ctx.send('What is the name of the subject you want to remove?')
                    msg = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                    subject_name = msg.content
                except asyncio.TimeoutError:
                    await ctx.send('Failed to remove subject!')
                    return
            try:
                real_subject = get_real_subject(subject_name)
                remove_subject(real_subject[0])
                await ctx.send(f'The subject {real_subject[1]} has been successfully removed')
            except KeyError:
                await ctx.send(f'There is no such subject as {subject_name}!')
            return
        subject_name = f'{options} {subject_name}' if options is not None else subject_name
        try:
            subject_name = get_real_subject(subject_name)
            aliases = ', '.join(get_alias(subject_name[0]))
            await ctx.send(f'**{subject_name[1]}**:\n'
                           f'Aliases: '
                           f'''{aliases}\n'''
                           f'Description: '
                           f'{get_subject_description(subject_name[0])}')
        except KeyError:
            await ctx.send(f'There is no such subject as {subject_name}!')
        await self.client.tree.sync()

    @subjects.autocomplete('options')
    async def help_autocomplete(self, _interaction, current):
        options = ['list', 'add', 'remove']
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @subjects.autocomplete('subject_name')
    async def help_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject_name)[1] for subject_name in subject]
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(brief='Need homework reminders?',
                             description='Know the homework that you have to do for each class')
    async def homework(self, ctx, *, subject_name=None):
        if subject_name is None:
            try:
                await ctx.send('What subject to check homework?')
                msg = await self.client.wait_for('message',
                                                 check=lambda m: m.channel == ctx.channel and
                                                 m.author == ctx.author,
                                                 timeout=20.0)
                subject_name = msg.content
            except asyncio.TimeoutError:
                await ctx.send('Failed to retrieve homework!')
                return
        elif subject_name.lower() == 'all':
            if repr(subject) == '{}':
                await ctx.send('No subjects to check homework for!')
                return
            message = '# Homework for all subjects:\n'
            for name in subject:
                if repr(subject[name]['homework']) == '[]':
                    message += f'**{get_real_subject(name)[1]}** has no homework.\n'
                    continue
                message += f'**{get_real_subject(name)[1]}**:\n{get_subject_homework(name)}\n'
            message = message[0:-1]
            if message == 'Homework for all subjects:':
                await ctx.send('There doesn\'t seem to be any homework for any subject.')
                return
            await ctx.send(message)
            return
        try:
            if len(subject[get_real_subject(subject_name)[0]]['homework']) == 0:
                await ctx.send(f'There doesn\'t seem to be any homework for {get_real_subject(subject_name)[1]}.')
                return
            await ctx.send(f'Homework for **{get_real_subject(subject_name)[1]}**:\n'
                           f'{get_subject_homework(subject_name)}')
        except KeyError:
            await ctx.send(f'There is no such subject as {subject_name}!')
        await self.client.tree.sync()

    @homework.autocomplete('subject_name')
    async def help_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject_name)[1] for subject_name in subject]
        options.insert(0, 'all')
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(brief='Set subject homework', description='Set homework for a subject')
    async def add_homework(self, ctx, *, subject_name=None):
        if subject_name is None:
            try:
                await ctx.send('What subject to add homework?')
                msg = await self.client.wait_for('message',
                                                 check=lambda m: m.channel == ctx.channel and
                                                 m.author == ctx.author,
                                                 timeout=20.0)
                subject_name = msg.content
            except asyncio.TimeoutError:
                await ctx.send('Failed to retrieve homework!')
                return
        # elif clear is not None:
        #     if clear.lower() == 'clear':
        #         if subject_name.lower() == 'all':
        #             if ctx.author.id == 434430979075997707:
        #                 try:
        #                     await ctx.send('Are you sure you want to clear the homework for all subjects?')
        #                     msg = await self.client.wait_for(message='message',
        #                                                      check=lambda m: m.channel == ctx.channel and
        #                                                      m.author == ctx.author,
        #                                                      timeout=20.0)
        #                     if msg.content.lower() == 'yes':
        #                         for i in subject:
        #                             add_subject_homework(i, 'None')
        #                         await ctx.send('Cleared homework for all subjects')
        #                     else:
        #                         await ctx.send('Confirmation failed')
        #                 except asyncio.TimeoutError:
        #                     await ctx.send('Timeout! Confirmation failed')
        #             else:
        #                 await ctx.send('Sorry, only certain users are able to clear all the homework.')
        #         else:
        #             try:
        #                 real_subject = get_real_subject(subject_name)
        #                 set_subject_homework(real_subject[0], 'None')
        #                 await ctx.send(f'Successfully cleared the homework of {real_subject[1]}')
        #             except KeyError:
        #                 await ctx.send(f'There is no such subject as {subject_name}!')
        #     else:
        #         await ctx.send('Invalid clear argument!')
        try:
            real_subject = get_real_subject(subject_name)
            await ctx.send(f'What homework does {real_subject[1]} have?')
            msg1 = await self.client.wait_for('message',
                                              check=lambda m: m.channel == ctx.channel and
                                              m.author == ctx.author,
                                              timeout=40.0)
            assignment = msg1.content
            await ctx.send('What is the due date of this homework assignment? (mm/dd/yy)')
            msg2 = await self.client.wait_for('message',
                                              check=lambda m: m.channel == ctx.channel and
                                              m.author == ctx.author,
                                              timeout=40.0)
            due_date = msg2.content
            try:
                add_subject_homework(real_subject[0], assignment, due_date)
                await ctx.send(f'Successfully set the homework of {real_subject[1]} to {assignment} '
                               f'due {due_date}')
            except KeyError:
                await ctx.send(f'There is no such subject as {subject_name}!')
            except AttributeError:
                await ctx.send(f'You can\'t duplicate homework assignments!')
        except asyncio.TimeoutError:
            await ctx.send('Failed to add homework!')
        await self.client.tree.sync()

    @add_homework.autocomplete('subject_name')
    async def help_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject_name)[1] for subject_name in subject]
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    # @add_homework.autocomplete('clear')
    # async def help_autocomplete(self, _interaction, current):
    #     options = ['clear']
    #     return [discord.app_commands.Choice(name=option, value=option)
    #             for option in options if current.lower() in option.lower()]


async def setup(client):
    await client.add_cog(Subject(client))
