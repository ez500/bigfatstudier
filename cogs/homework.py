"""Homework commands"""

import asyncio
import datetime

import discord
from discord.ext import commands

from util import *


class Homework(commands.Cog, name='homework'):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.hybrid_command(brief='View homework assignments',
                             description='View or clear homework for each class')
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
                if len(subject_data) == 0:
                    await ctx.send('No subjects to check homework for!')
                    return
                message = '# Homework for all subjects:\n'
                for name in subject_data:
                    if repr(subject_data[name]['homework']) == '[]':
                        message += f'**{get_real_subject(name)[1]}** has no homework.\n'
                        continue
                    message += f'''**{get_real_subject(name)[1]}**:\n''' + '\n'.join(get_subject_homework(name)) + '\n'
                message = message[0:-1]
                await ctx.send(message)
                return
            if _clear.lower() == 'clear':
                await ctx.send('Sorry, but you cannot clear homework for all subjects.')
                return
            else:
                await ctx.send(f'Invalid clear argument ({_clear})')
                return
        elif subject_name.lower() == 'subscribed':
            if _clear is None:
                if len(get_user_subjects(ctx.author.id)) == 0:
                    await ctx.send('You are not subscribed to any subjects!')
                    return
                message = '# Homework for your subscribed subjects:\n'
                for name in get_user_subjects(ctx.author.id):
                    if repr(subject_data[name]['homework']) == '[]':
                        message += f'**{get_real_subject(name)[1]}** has no homework.\n'
                        continue
                    message += f'''**{get_real_subject(name)[1]}**:\n''' + '\n'.join(get_subject_homework(name)) + '\n'
                message = message[0:-1]
                await ctx.send(message)
                return
            if _clear.lower() == 'clear':
                await ctx.send('Sorry, but you cannot clear homework for your subscribed subjects.')
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
                if subject_name.lower() == 'subscribed':
                    await ctx.send('Sorry, but you cannot clear homework for your subscribed subjects.')
                    return
                _clear = 'clear'
            else:
                try:
                    real_subject = get_real_subject(subject_name)
                    if len(subject_data[real_subject[0]]['homework']) == 0:
                        await ctx.send(f'There doesn\'t seem to be any homework for {real_subject[1]}.')
                        return
                    await ctx.send(f'Homework for **{real_subject[1]}**:\n' +
                                   '\n'.join(get_subject_homework(real_subject[0])))
                except SubjectError as e:
                    await ctx.send(str(e))
        if _clear.lower() == 'clear':
            try:
                real_subject = get_real_subject(subject_name)
                if not is_subscribed(ctx.author.id, real_subject[0]):
                    await ctx.send(f'You need to be subscribed to {real_subject[1]} to clear homework!')
                    return
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
            except SubjectError as e:
                await ctx.send(str(e))
            return
        else:
            await ctx.send(f'Invalid clear argument ({_clear})')
            return

    @homework.autocomplete('subject_name')
    async def subject_name_with_all_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject_name)[1] for subject_name in subject_data]
        options[0:0] = ['all', 'subscribed']
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @homework.autocomplete('_clear')
    async def homework_clear_autocomplete(self, _interaction, current):
        options = ['clear']
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(brief='Add subject homework', description='Add an assignment to a subject')
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
            if not is_subscribed(ctx.author.id, real_subject[0]):
                await ctx.send(f'You need to be subscribed to {real_subject[1]} to add homework!')
                return
            await ctx.send(f'What homework does {real_subject[1]} have?')
            msg1 = await self.client.wait_for('message',
                                              check=lambda m: m.channel == ctx.channel and
                                              m.author == ctx.author,
                                              timeout=40.0)
            assignment = msg1.content
            await ctx.send('What is the due date of this homework assignment? (mm/dd/yyyy)')
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
            await ctx.send(f'Successfully added {assignment} to {real_subject[1]} '
                           f'due {due_date}')
        except SubjectError as e:
            await ctx.send(str(e))
        except SubjectAttributeError as e:
            await ctx.send(str(e))

    @add_homework.autocomplete('subject_name')
    async def subject_name_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject_name)[1] for subject_name in subject_data]
        for subject in subject_data:
            options.extend(alias for alias in get_subject_alias(subject))
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(brief='Remove subject homework', description='Remove an assignment from a subject')
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
            if not is_subscribed(ctx.author.id, real_subject[0]):
                await ctx.send(f'You need to be subscribed to {real_subject[1]} to remove homework!')
                return
            if len(get_subject_homework(real_subject[0])) == 0:
                await ctx.send(f'{real_subject[1]} has no homework to remove!')
                return
            await ctx.send(f'What homework in {real_subject[1]} to remove? '
                           f'''Current assignments: {', '.join(get_subject_homework_names(real_subject[0]))}''')
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
        except SubjectError as e:
            await ctx.send(str(e))
        except SubjectAttributeError as e:
            await ctx.send(str(e))

    @remove_homework.autocomplete('subject_name')
    async def subject_name_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject_name)[1] for subject_name in subject_data]
        for subject in subject_data:
            options.extend(alias for alias in get_subject_alias(subject))
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(brief='View projects',
                             description='View or clear projects for each class')
    async def project(self, ctx, *, subject_name=None, _clear=None):
        if subject_name is None:
            if _clear is None:
                try:
                    await ctx.send('What subject to check projects?')
                    msg = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                    subject_name = msg.content
                except asyncio.TimeoutError:
                    await ctx.send('Timeout! Failed to retrieve projects!')
                    return
            elif _clear.lower() == 'clear':
                try:
                    await ctx.send('What subject to clear projects?')
                    msg = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                    subject_name = msg.content + ' clear'
                    _clear = None
                except asyncio.TimeoutError:
                    await ctx.send('Timeout! Failed to clear projects!')
                    return
        elif subject_name.lower() == 'all':
            if _clear is None:
                if len(subject_data) == 0:
                    await ctx.send('No subjects to check projects for!')
                    return
                message = '# Projects for all subjects:\n'
                for name in subject_data:
                    if repr(subject_data[name]['project']) == '[]':
                        message += f'**{get_real_subject(name)[1]}** has no projects.\n'
                        continue
                    message += f'''**{get_real_subject(name)[1]}**:\n''' + '\n'.join(get_subject_projects(name)) + '\n'
                message = message[0:-1]
                await ctx.send(message)
                return
            if _clear.lower() == 'clear':
                await ctx.send('Sorry, but you cannot clear projects for all subjects.')
                return
            else:
                await ctx.send(f'Invalid clear argument ({_clear})')
                return
        elif subject_name.lower() == 'subscribed':
            if _clear is None:
                if len(get_user_subjects(ctx.author.id)) == 0:
                    await ctx.send('You are not subscribed to any subjects!')
                    return
                message = '# Projects for your subscribed subjects:\n'
                for name in get_user_subjects(ctx.author.id):
                    if repr(subject_data[name]['project']) == '[]':
                        message += f'**{get_real_subject(name)[1]}** has no projects.\n'
                        continue
                    message += f'''**{get_real_subject(name)[1]}**:\n''' + '\n'.join(get_subject_projects(name)) + '\n'
                message = message[0:-1]
                await ctx.send(message)
                return
            if _clear.lower() == 'clear':
                await ctx.send('Sorry, but you cannot clear projects for your subscribed subjects.')
                return
            else:
                await ctx.send(f'Invalid clear argument ({_clear})')
                return
        if subject_name.lower() == 'clear':
            try:
                await ctx.send('What subject to clear projects?')
                msg = await self.client.wait_for('message',
                                                 check=lambda m: m.channel == ctx.channel and
                                                 m.author == ctx.author,
                                                 timeout=20.0)
                subject_name = msg.content + ' clear'
                _clear = None
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Failed to clear projects!')
                return
        if _clear is None:
            if subject_name.split()[-1] == 'clear':
                subject_name = ' '.join(subject_name.split()[:-1])
                if subject_name.lower() == 'all':
                    await ctx.send('Sorry, but you cannot clear projects for all subjects.')
                    return
                if subject_name.lower() == 'subscribed':
                    await ctx.send('Sorry, but you cannot clear projects for your subscribed subjects.')
                    return
                _clear = 'clear'
            else:
                try:
                    real_subject = get_real_subject(subject_name)
                    if len(subject_data[real_subject[0]]['project']) == 0:
                        await ctx.send(f'There doesn\'t seem to be any projects for {real_subject[1]}.')
                        return
                    await ctx.send(f'Projects for **{real_subject[1]}**:\n' +
                                   '\n'.join(get_subject_projects(real_subject[0])))
                except SubjectError as e:
                    await ctx.send(str(e))
        if _clear.lower() == 'clear':
            try:
                real_subject = get_real_subject(subject_name)
                if not is_subscribed(ctx.author.id, real_subject[0]):
                    await ctx.send(f'You need to be subscribed to {real_subject[1]} to clear projects!')
                    return
                await ctx.send(f'Are you sure you want to clear the projects for {real_subject[1]}?')
                confirm = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                if confirm.content.lower() == 'yes':
                    clear_subject_projects(real_subject[0])
                    await ctx.send(f'Cleared projects for {real_subject[1]}')
                else:
                    await ctx.send('Confirmation failed')
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Confirmation failed')
            except SubjectError as e:
                await ctx.send(str(e))
            return
        else:
            await ctx.send(f'Invalid clear argument ({_clear})')
            return

    @project.autocomplete('subject_name')
    async def subject_name_with_all_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject_name)[1] for subject_name in subject_data]
        options[0:0] = ['all', 'subscribed']
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @project.autocomplete('_clear')
    async def project_clear_autocomplete(self, _interaction, current):
        options = ['clear']
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(brief='Add subject projects', description='Add a project to a subject')
    async def add_project(self, ctx, *, subject_name=None):
        if subject_name is None:
            try:
                await ctx.send('What subject to add project?')
                msg = await self.client.wait_for('message',
                                                 check=lambda m: m.channel == ctx.channel and
                                                 m.author == ctx.author,
                                                 timeout=20.0)
                subject_name = msg.content
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Failed to add project!')
                return
        try:
            real_subject = get_real_subject(subject_name)
            if not is_subscribed(ctx.author.id, real_subject[0]):
                await ctx.send(f'You need to be subscribed to {real_subject[1]} to add a project!')
                return
            await ctx.send(f'What project does {real_subject[1]} have?')
            msg1 = await self.client.wait_for('message',
                                              check=lambda m: m.channel == ctx.channel and
                                              m.author == ctx.author,
                                              timeout=40.0)
            project = msg1.content
            await ctx.send('What is the due date of this project? (mm/dd/yyyy)')
            msg2 = await self.client.wait_for('message',
                                              check=lambda m: m.channel == ctx.channel and
                                              m.author == ctx.author,
                                              timeout=40.0)
            due_date = msg2.content
        except asyncio.TimeoutError:
            await ctx.send('Timeout! Failed to add project!')
            return
        try:
            date = datetime.datetime.strptime(due_date, '%m/%d/%Y')
            if date < datetime.datetime.now():
                await ctx.send('This due date is before today. Add the project anyway?')
                confirm = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                if confirm.content.lower() != 'yes':
                    await ctx.send('Confirmation failed! Failed to add project!')
                    return
        except ValueError:
            await ctx.send('Not a valid date in the specified format!')
            return
        except asyncio.TimeoutError:
            await ctx.send('Timeout! Failed to add project!')
            return
        try:
            add_subject_project(real_subject[0], project, due_date)
            await ctx.send(f'Successfully added {project} to {real_subject[1]} '
                           f'due {due_date}')
        except SubjectError as e:
            await ctx.send(str(e))
        except SubjectAttributeError as e:
            await ctx.send(str(e))

    @add_project.autocomplete('subject_name')
    async def subject_name_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject_name)[1] for subject_name in subject_data]
        for subject in subject_data:
            options.extend(alias for alias in get_subject_alias(subject))
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(brief='Remove subject projects', description='Remove a project from a subject')
    async def remove_project(self, ctx, *, subject_name=None):
        if subject_name is None:
            try:
                await ctx.send('What subject to remove project?')
                msg = await self.client.wait_for('message',
                                                 check=lambda m: m.channel == ctx.channel and
                                                 m.author == ctx.author,
                                                 timeout=20.0)
                subject_name = msg.content
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Failed to remove project!')
                return
        try:
            real_subject = get_real_subject(subject_name)
            if not is_subscribed(ctx.author.id, real_subject[0]):
                await ctx.send(f'You need to be subscribed to {real_subject[1]} to remove projects!')
                return
            if len(get_subject_projects(real_subject[0])) == 0:
                await ctx.send(f'{real_subject[1]} has no project to remove!')
                return
            await ctx.send(f'What project in {real_subject[1]} to remove? '
                           f'''Current projects: {', '.join(get_subject_project_names(real_subject[0]))}''')
            msg1 = await self.client.wait_for('message',
                                              check=lambda m: m.channel == ctx.channel and
                                              m.author == ctx.author,
                                              timeout=40.0)
            project = msg1.content
        except asyncio.TimeoutError:
            await ctx.send('Timeout! Failed to remove project!')
            return
        try:
            remove_subject_project(real_subject[0], project)
            await ctx.send(f'''Successfully removed project '{project}' from {real_subject[1]}''')
        except SubjectError as e:
            await ctx.send(str(e))
        except SubjectAttributeError as e:
            await ctx.send(str(e))

    @remove_project.autocomplete('subject_name')
    async def subject_name_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject_name)[1] for subject_name in subject_data]
        for subject in subject_data:
            options.extend(alias for alias in get_subject_alias(subject))
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(brief='View tests',
                             description='View or clear tests for each class')
    async def test(self, ctx, *, subject_name=None, _clear=None):
        if subject_name is None:
            if _clear is None:
                try:
                    await ctx.send('What subject to check for tests?')
                    msg = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                    subject_name = msg.content
                except asyncio.TimeoutError:
                    await ctx.send('Timeout! Failed to retrieve tests!')
                    return
            elif _clear.lower() == 'clear':
                try:
                    await ctx.send('What subject to clear tests?')
                    msg = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                    subject_name = msg.content + ' clear'
                    _clear = None
                except asyncio.TimeoutError:
                    await ctx.send('Timeout! Failed to clear tests!')
                    return
        elif subject_name.lower() == 'all':
            if _clear is None:
                if len(subject_data) == 0:
                    await ctx.send('No subjects to check for tests for!')
                    return
                message = '# Tests for all subjects:\n'
                for name in subject_data:
                    if repr(subject_data[name]['test']) == '[]':
                        message += f'**{get_real_subject(name)[1]}** has no upcoming tests.\n'
                        continue
                    message += f'''**{get_real_subject(name)[1]}**:\n''' + '\n'.join(get_subject_tests(name)) + '\n'
                message = message[0:-1]
                await ctx.send(message)
                return
            if _clear.lower() == 'clear':
                await ctx.send('Sorry, but you cannot clear tests for all subjects.')
                return
            else:
                await ctx.send(f'Invalid clear argument ({_clear})')
                return
        elif subject_name.lower() == 'subscribed':
            if _clear is None:
                if len(get_user_subjects(ctx.author.id)) == 0:
                    await ctx.send('You are not subscribed to any subjects!')
                    return
                message = '# Tests for your subscribed subjects:\n'
                for name in get_user_subjects(ctx.author.id):
                    if repr(subject_data[name]['test']) == '[]':
                        message += f'**{get_real_subject(name)[1]}** has no upcoming tests.\n'
                        continue
                    message += f'''**{get_real_subject(name)[1]}**:\n''' + '\n'.join(get_subject_tests(name)) + '\n'
                message = message[0:-1]
                await ctx.send(message)
                return
            if _clear.lower() == 'clear':
                await ctx.send('Sorry, but you cannot clear tests for your subscribed subjects.')
                return
            else:
                await ctx.send(f'Invalid clear argument ({_clear})')
                return
        if subject_name.lower() == 'clear':
            try:
                await ctx.send('What subject to clear tests?')
                msg = await self.client.wait_for('message',
                                                 check=lambda m: m.channel == ctx.channel and
                                                 m.author == ctx.author,
                                                 timeout=20.0)
                subject_name = msg.content + ' clear'
                _clear = None
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Failed to clear tests!')
                return
        if _clear is None:
            if subject_name.split()[-1] == 'clear':
                subject_name = ' '.join(subject_name.split()[:-1])
                if subject_name.lower() == 'all':
                    await ctx.send('Sorry, but you cannot clear tests for all subjects.')
                    return
                if subject_name.lower() == 'subscribed':
                    await ctx.send('Sorry, but you cannot clear tests for your subscribed subjects.')
                    return
                _clear = 'clear'
            else:
                try:
                    real_subject = get_real_subject(subject_name)
                    if len(subject_data[real_subject[0]]['test']) == 0:
                        await ctx.send(f'There doesn\'t seem to be any upcoming tests for {real_subject[1]}.')
                        return
                    await ctx.send(f'Tests for **{real_subject[1]}**:\n' +
                                   '\n'.join(get_subject_tests(real_subject[0])))
                except SubjectError as e:
                    await ctx.send(str(e))
        if _clear.lower() == 'clear':
            try:
                real_subject = get_real_subject(subject_name)
                if not is_subscribed(ctx.author.id, real_subject[0]):
                    await ctx.send(f'You need to be subscribed to {real_subject[1]} to clear tests!')
                    return
                await ctx.send(f'Are you sure you want to clear the tests for {real_subject[1]}?')
                confirm = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                if confirm.content.lower() == 'yes':
                    clear_subject_tests(real_subject[0])
                    await ctx.send(f'Cleared tests for {real_subject[1]}')
                else:
                    await ctx.send('Confirmation failed')
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Confirmation failed')
            except SubjectError as e:
                await ctx.send(str(e))
            return
        else:
            await ctx.send(f'Invalid clear argument ({_clear})')
            return

    @test.autocomplete('subject_name')
    async def subject_name_with_all_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject_name)[1] for subject_name in subject_data]
        options[0:0] = ['all', 'subscribed']
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @test.autocomplete('_clear')
    async def test_clear_autocomplete(self, _interaction, current):
        options = ['clear']
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(brief='Add subject tests', description='Add an upcoming test to a subject')
    async def add_test(self, ctx, *, subject_name=None):
        if subject_name is None:
            try:
                await ctx.send('What subject to add an upcoming test?')
                msg = await self.client.wait_for('message',
                                                 check=lambda m: m.channel == ctx.channel and
                                                 m.author == ctx.author,
                                                 timeout=20.0)
                subject_name = msg.content
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Failed to add upcoming test!')
                return
        try:
            real_subject = get_real_subject(subject_name)
            if not is_subscribed(ctx.author.id, real_subject[0]):
                await ctx.send(f'You need to be subscribed to {real_subject[1]} to add upcoming tests!')
                return
            await ctx.send(f'What test will {real_subject[1]} have?')
            msg1 = await self.client.wait_for('message',
                                              check=lambda m: m.channel == ctx.channel and
                                              m.author == ctx.author,
                                              timeout=40.0)
            test = msg1.content
            await ctx.send('When will this test be? (mm/dd/yyyy)')
            msg2 = await self.client.wait_for('message',
                                              check=lambda m: m.channel == ctx.channel and
                                              m.author == ctx.author,
                                              timeout=40.0)
            due_date = msg2.content
        except asyncio.TimeoutError:
            await ctx.send('Timeout! Failed to add test!')
            return
        try:
            date = datetime.datetime.strptime(due_date, '%m/%d/%Y')
            if date < datetime.datetime.now():
                await ctx.send('This test date is before today. Add test anyway?')
                confirm = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                if confirm.content.lower() != 'yes':
                    await ctx.send('Confirmation failed! Failed to add test!')
                    return
        except ValueError:
            await ctx.send('Not a valid date in the specified format!')
            return
        except asyncio.TimeoutError:
            await ctx.send('Timeout! Failed to add test!')
            return
        try:
            add_subject_test(real_subject[0], test, due_date)
            await ctx.send(f'Successfully added {test} to {real_subject[1]} '
                           f'due {due_date}')
        except SubjectError as e:
            await ctx.send(str(e))
        except SubjectAttributeError as e:
            await ctx.send(str(e))

    @add_test.autocomplete('subject_name')
    async def subject_name_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject_name)[1] for subject_name in subject_data]
        for subject in subject_data:
            options.extend(alias for alias in get_subject_alias(subject))
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(brief='Remove subject tests', description='Remove a test from a subject')
    async def remove_test(self, ctx, *, subject_name=None):
        if subject_name is None:
            try:
                await ctx.send('What subject to remove a test?')
                msg = await self.client.wait_for('message',
                                                 check=lambda m: m.channel == ctx.channel and
                                                 m.author == ctx.author,
                                                 timeout=20.0)
                subject_name = msg.content
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Failed to remove test!')
                return
        try:
            real_subject = get_real_subject(subject_name)
            if not is_subscribed(ctx.author.id, real_subject[0]):
                await ctx.send(f'You need to be subscribed to {real_subject[1]} to remove tests!')
                return
            if len(get_subject_tests(real_subject[0])) == 0:
                await ctx.send(f'{real_subject[1]} has no test to remove!')
                return
            await ctx.send(f'What test in {real_subject[1]} to remove? '
                           f'''Upcoming tests: {', '.join(get_subject_test_names(real_subject[0]))}''')
            msg1 = await self.client.wait_for('message',
                                              check=lambda m: m.channel == ctx.channel and
                                              m.author == ctx.author,
                                              timeout=40.0)
            test = msg1.content
        except asyncio.TimeoutError:
            await ctx.send('Timeout! Failed to remove test!')
            return
        try:
            remove_subject_test(real_subject[0], test)
            await ctx.send(f'''Successfully removed test '{test}' from {real_subject[1]}''')
        except SubjectError as e:
            await ctx.send(str(e))
        except SubjectAttributeError as e:
            await ctx.send(str(e))

    @remove_test.autocomplete('subject_name')
    async def subject_name_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject_name)[1] for subject_name in subject_data]
        for subject in subject_data:
            options.extend(alias for alias in get_subject_alias(subject))
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]


async def setup(client):
    await client.add_cog(Homework(client))
