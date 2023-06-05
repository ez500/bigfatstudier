"""Subject commands"""

import asyncio
import datetime

import discord
from discord.ext import commands

from util import *


class Subject(commands.Cog, name='subject'):
    def __init__(self, client: commands.Bot):
        self.client = client

    # TODO: ADD DAILY REMINDERS
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
                    await ctx.send('Timeout! Failed to add subject!')
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
                    await ctx.send('Timeout! Failed to remove subject!')
                    return
            try:
                real_subject = get_real_subject(subject_name)
                remove_subject(real_subject[0])
                await ctx.send(f'The subject {real_subject[1]} has been successfully removed')
            except KeyError:
                await ctx.send(f'There is no such subject as {subject_name}!')
            return
        else:
            subject_name = f'{options} {subject_name}'
        try:
            real_subject = get_real_subject(subject_name)
            aliases = ', '.join(get_subject_alias(real_subject[0]))
            await ctx.send(f'**{real_subject[1]}**:\n'
                           f'''Aliases: {aliases if len(aliases) > 0 else 'No aliases'}\n'''
                           f'Description: {get_subject_description(real_subject[0])}')
        except KeyError:
            await ctx.send(f'There is no such subject as {subject_name}!')

    @subjects.autocomplete('options')
    async def subject_options_autocomplete(self, _interaction, current):
        options = ['list', 'add', 'remove']
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @subjects.autocomplete('subject_name')
    async def subject_name_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject_name)[1] for subject_name in subject]
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(brief='Manage alias',
                             description='List, add, or remove aliases to subjects to make them more accessible')
    async def alias(self, ctx, options=None, *, subject_name=None):
        if options is None or options.lower() == 'list':
            if subject_name is None:
                try:
                    await ctx.send('What subject to view aliases?')
                    msg = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                    subject_name = msg.content
                except asyncio.TimeoutError:
                    await ctx.send('Timeout! Failed to retrieve aliases!')
                    return
        elif options.lower() == 'add':
            if subject_name is None:
                try:
                    await ctx.send('What subject to add alias to?')
                    msg = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                    subject_name = msg.content
                except asyncio.TimeoutError:
                    await ctx.send('Timeout! Failed to add alias!')
                    return
            try:
                real_subject = get_real_subject(subject_name)
                await ctx.send(f'What is the alias to add to {real_subject[1]}?')
                msg = await self.client.wait_for('message',
                                                 check=lambda m: m.channel == ctx.channel and
                                                 m.author == ctx.author,
                                                 timeout=20.0)
                subject_alias = msg.content
            except KeyError:
                await ctx.send(f'There is no such subject as {subject_name}!')
                return
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Failed to add alias!')
                return
            try:
                add_subject_alias(real_subject[0], subject_alias)
                await ctx.send(f'Added {subject_alias} to the list of aliases of {real_subject[1]}!')
            except AttributeError:
                await ctx.send(f'{subject_alias} already exists as an alias to {real_subject[1]}!')
            return
        elif options.lower() == 'remove':
            if subject_name is None:
                try:
                    await ctx.send('What subject to remove alias from?')
                    msg = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                    subject_name = msg.content
                except asyncio.TimeoutError:
                    await ctx.send('Timeout! Failed to remove alias!')
                    return
            try:
                real_subject = get_real_subject(subject_name)
                await ctx.send(f'What is the alias to remove from {real_subject[1]}?')
                msg = await self.client.wait_for('message',
                                                 check=lambda m: m.channel == ctx.channel and
                                                 m.author == ctx.author,
                                                 timeout=20.0)
                subject_alias = msg.content
            except KeyError:
                await ctx.send(f'There is no such subject as {subject_name}!')
                return
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Failed to add alias!')
                return
            try:
                remove_subject_alias(real_subject[0], subject_alias)
                await ctx.send(f'Removed {subject_alias} from the list of aliases of {real_subject[1]}!')
            except AttributeError:
                await ctx.send(f'There is no such alias as {subject_alias} in {real_subject[1]}!')
            return
        else:
            subject_name = f'{options} {subject_name}'
        try:
            real_subject = get_real_subject(subject_name)
            aliases = ', '.join(get_subject_alias(real_subject[0]))
            await ctx.send(f'''Aliases of {real_subject[1]}: {aliases if len(aliases) > 0 else 'No aliases'}''')
            return
        except KeyError:
            await ctx.send(f'There is no such subject as {subject_name}!')

    @alias.autocomplete('options')
    async def alias_options_autocomplete(self, _interaction, current):
        options = ['list', 'add', 'remove']
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @alias.autocomplete('subject_name')
    async def subject_name_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject_name)[1] for subject_name in subject]
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(brief='Manage description',
                             description='List, set, or clear description of subjects')
    async def description(self, ctx, options=None, *, subject_name=None):
        if options is None or options.lower() == 'list':
            if subject_name is None:
                try:
                    await ctx.send('What subject to view description?')
                    msg = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                    subject_name = msg.content
                except asyncio.TimeoutError:
                    await ctx.send('Timeout! Failed to retrieve aliases!')
                    return
        elif options.lower() == 'set':
            if subject_name is None:
                try:
                    await ctx.send('What subject to set description?')
                    msg = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                    subject_name = msg.content
                except asyncio.TimeoutError:
                    await ctx.send('Timeout! Failed to set description!')
                    return
            try:
                real_subject = get_real_subject(subject_name)
                await ctx.send(f'What is the description for {real_subject[1]}?')
                msg = await self.client.wait_for('message',
                                                 check=lambda m: m.channel == ctx.channel and
                                                 m.author == ctx.author,
                                                 timeout=20.0)
                subject_description = msg.content
            except KeyError:
                await ctx.send(f'There is no such subject as {subject_name}!')
                return
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Failed to set description!')
                return
            try:
                set_subject_description(real_subject[0], subject_description)
                await ctx.send(f'Set description of {real_subject[1]} to *{subject_description}*!')
            except AttributeError:
                await ctx.send(f'{subject_description} is already the description of {real_subject[1]}!')
            return
        elif options.lower() == 'clear':
            if subject_name is None:
                try:
                    await ctx.send('What subject to clear description?')
                    msg = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                    subject_name = msg.content
                except asyncio.TimeoutError:
                    await ctx.send('Timeout! Failed to clear description!')
                    return
            try:
                real_subject = get_real_subject(subject_name)
            except KeyError:
                await ctx.send(f'There is no such subject as {subject_name}!')
                return
            try:
                set_subject_description(real_subject[0], 'No description')
                await ctx.send(f'Cleared description of {real_subject[1]}!')
            except AttributeError:
                await ctx.send(f'{real_subject[1]} has no description to clear!')
            return
        else:
            subject_name = f'{options} {subject_name}'
        try:
            real_subject = get_real_subject(subject_name)
            await ctx.send(f'**{real_subject[1]} description:** {get_subject_description(real_subject[0])}')
            return
        except KeyError:
            await ctx.send(f'There is no such subject as {subject_name}!')

    @description.autocomplete('options')
    async def description_options_autocomplete(self, _interaction, current):
        options = ['list', 'set', 'clear']
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @description.autocomplete('subject_name')
    async def subject_name_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject_name)[1] for subject_name in subject]
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(brief='Need homework reminders?',
                             description='Know the homework that you have to do for each class')
    async def homework(self, ctx, *, subject_name=None, _clear=None):
        if subject_name is None:
            if _clear is None:
                try:
                    await ctx.send('What subject to check homework?')
                    msg = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                    subject_name = msg.content
                except asyncio.TimeoutError:
                    await ctx.send('Timeout! Failed to retrieve homework!')
                    return
            elif _clear.lower() == 'clear':
                try:
                    await ctx.send('What subject to clear homework?')
                    msg = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                    subject_name = msg.content + ' clear'
                    _clear = None
                except asyncio.TimeoutError:
                    await ctx.send('Timeout! Failed to clear homework!')
                    return
        elif subject_name.lower() == 'all':
            if _clear is None:
                if repr(subject) == '{}':
                    await ctx.send('No subjects to check homework for!')
                    return
                message = '# Homework for all subjects:\n'
                for name in subject:
                    if repr(subject[name]['homework']) == '[]':
                        message += f'**{get_real_subject(name)[1]}** has no homework.\n'
                        continue
                    message += f'''**{get_real_subject(name)[1]}**:\n''' + '\n'.join(get_subject_homework(name)) + '\n'
                message = message[0:-1]
                if message == 'Homework for all subjects:':
                    await ctx.send('There doesn\'t seem to be any homework for any subject.')
                    return
                await ctx.send(message)
                return
            if _clear.lower() == 'clear':
                await ctx.send('Sorry, but you cannot clear homework for all subjects.')
                return
            else:
                await ctx.send(f'Invalid clear argument ({_clear})')
                return
        if subject_name.lower() == 'clear':
            try:
                await ctx.send('What subject to clear homework?')
                msg = await self.client.wait_for('message',
                                                 check=lambda m: m.channel == ctx.channel and
                                                 m.author == ctx.author,
                                                 timeout=20.0)
                subject_name = msg.content + ' clear'
                _clear = None
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Failed to clear homework!')
                return
        if _clear is None:
            if subject_name.split()[-1] == 'clear':
                subject_name = ' '.join(subject_name.split()[:-1])
                if subject_name.lower() == 'all':
                    await ctx.send('Sorry, but you cannot clear homework for all subjects.')
                    return
                try:
                    real_subject = get_real_subject(subject_name)
                    await ctx.send(f'Are you sure you want to clear the homework for '
                                   f'{real_subject[1]}?')
                    confirm = await self.client.wait_for('message',
                                                         check=lambda m: m.channel == ctx.channel and
                                                         m.author == ctx.author,
                                                         timeout=20.0)
                    if confirm.content.lower() == 'yes':
                        clear_subject_homework(real_subject[0])
                        await ctx.send(f'Cleared homework for {real_subject[1]}')
                    else:
                        await ctx.send('Confirmation failed')
                except asyncio.TimeoutError:
                    await ctx.send('Timeout! Confirmation failed')
                except KeyError:
                    await ctx.send(f'There is no such subject as {subject_name}!')
                return
            try:
                real_subject = get_real_subject(subject_name)
                if len(subject[real_subject[0]]['homework']) == 0:
                    await ctx.send(f'There doesn\'t seem to be any homework for {real_subject[1]}.')
                    return
                await ctx.send(f'Homework for **{real_subject[1]}**:\n' +
                               '\n'.join(get_subject_homework(real_subject[0])))
            except KeyError:
                await ctx.send(f'There is no such subject as {subject_name}!')
        if _clear.lower() == 'clear':
            try:
                real_subject = get_real_subject(subject_name)
                await ctx.send(f'Are you sure you want to clear the homework for {real_subject[1]}?')
                confirm = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                if confirm.content.lower() == 'yes':
                    clear_subject_homework(real_subject[0])
                    await ctx.send(f'Cleared homework for {real_subject[1]}')
                else:
                    await ctx.send('Confirmation failed')
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Confirmation failed')
            except KeyError:
                await ctx.send(f'There is no such subject as {subject_name}!')
            return
        else:
            await ctx.send(f'Invalid clear argument ({_clear})')
            return

    @homework.autocomplete('subject_name')
    async def subject_name_with_all_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject_name)[1] for subject_name in subject]
        options.insert(0, 'all')
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @homework.autocomplete('_clear')
    async def homework_clear_autocomplete(self, _interaction, current):
        options = ['clear']
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
                await ctx.send('Timeout! Failed to add homework!')
                return
        try:
            real_subject = get_real_subject(subject_name)
            await ctx.send(f'What homework does {real_subject[1]} have?')
            msg1 = await self.client.wait_for('message',
                                              check=lambda m: m.channel == ctx.channel and
                                              m.author == ctx.author,
                                              timeout=40.0)
            assignment = msg1.content
            await ctx.send('What is the due date of this homework assignment? (mm/dd/yyyy)')  # TODO: CHECK IF PAST
            msg2 = await self.client.wait_for('message',
                                              check=lambda m: m.channel == ctx.channel and
                                              m.author == ctx.author,
                                              timeout=40.0)
            due_date = msg2.content
        except asyncio.TimeoutError:
            await ctx.send('Timeout! Failed to add homework!')
            return
        try:
            date = datetime.datetime.strptime(due_date, '%m/%d/%Y')
            if date < datetime.datetime.now():
                await ctx.send('This due date is before today. Add the assignment anyway?')
                confirm = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                if confirm.content.lower() != 'yes':
                    await ctx.send('Confirmation failed! Failed to add homework!')
                    return
        except ValueError:
            await ctx.send('Not a valid date in the specified format!')
            return
        except asyncio.TimeoutError:
            await ctx.send('Timeout! Failed to add homework!')
            return
        try:
            add_subject_homework(real_subject[0], assignment, due_date)
            await ctx.send(f'Successfully set the homework of {real_subject[1]} to {assignment} '
                           f'due {due_date}')
        except KeyError:
            await ctx.send(f'There is no such subject as {subject_name}!')
        except AttributeError:
            await ctx.send(f'You can\'t duplicate homework assignments!')

    @add_homework.autocomplete('subject_name')
    async def subject_name_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject_name)[1] for subject_name in subject]
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(brief='Remove subject homework', description='Remove homework from a subject')
    async def remove_homework(self, ctx, *, subject_name=None):
        if subject_name is None:
            try:
                await ctx.send('What subject to remove homework?')
                msg = await self.client.wait_for('message',
                                                 check=lambda m: m.channel == ctx.channel and
                                                 m.author == ctx.author,
                                                 timeout=20.0)
                subject_name = msg.content
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Failed to remove homework!')
                return
        try:
            real_subject = get_real_subject(subject_name)
            if len(get_subject_homework(real_subject[0])) == 0:
                await ctx.send(f'{real_subject[1]} has no homework to remove!')
                return
            await ctx.send(f'What homework in {real_subject[1]} to remove? '
                           f'''Current assignments: {', '.join(get_subject_homework_name(real_subject[0]))}''')
            msg1 = await self.client.wait_for('message',
                                              check=lambda m: m.channel == ctx.channel and
                                              m.author == ctx.author,
                                              timeout=40.0)
            assignment = msg1.content
        except asyncio.TimeoutError:
            await ctx.send('Timeout! Failed to remove homework!')
            return
        try:
            remove_subject_homework(real_subject[0], assignment)
            await ctx.send(f'''Successfully removed homework '{assignment}' from {real_subject[1]}''')
        except KeyError:
            await ctx.send(f'There is no such subject as {subject_name}!')
        except AttributeError:
            await ctx.send(f'{assignment} doesn\'t exist!')

    @remove_homework.autocomplete('subject_name')
    async def subject_name_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject_name)[1] for subject_name in subject]
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]


async def setup(client):
    await client.add_cog(Subject(client))
