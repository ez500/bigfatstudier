"""Subject commands"""

import asyncio
import traceback

import discord
from discord.ext import commands

from util import *


class Subject(commands.Cog, name='subject'):
    def __init__(self, client: commands.Bot):
        self.client = client

    # TODO: UPCOMING COMMAND
    # TODO: IMPLEMENT ASSIGNMENT + PERSONALIZED REMINDERS
    # TODO: REMOVE ASSIGNMENTS/PROJECTS/TESTS ON DUE DATE
    # TODO: MANUAL API CALLS TO ASSIGNMENTS THRU COMMAND? (WL.INSTRUCTURE.COM)
    @commands.hybrid_command(brief='Manage subjects', description='List, add, or remove subjects')
    async def subjects(self, ctx, options=None, *, subject_name=None):
        if options is None or options.lower() == 'list':
            if subject_name is None:
                if repr(subject_data) == '{}':
                    await ctx.send('There are yet to be subjects to be added!')
                    return
                subject_list = '**Subjects:** '
                for name in subject_data:
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
                real_subject = add_subject(subject_name, ctx.author.id)
                await ctx.send(f'Successfully added {real_subject[1]} to the subject list!')
            except SubjectError as e:
                await ctx.send(str(e))
            except SubjectNameError as e:
                await ctx.send(str(e))
            except SubjectAttributeError as e:
                await ctx.send(str(e))
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
                if is_owner(ctx.author.id, real_subject[0]):
                    remove_subject(real_subject[0])
                    await ctx.send(f'The subject {real_subject[1]} has been successfully removed')
                    return
                await ctx.send(f'You must be the owner of {real_subject[1]} to delete it!')
            except SubjectError as e:
                await ctx.send(str(e))
            return
        else:
            subject_name = f'{options} {subject_name}'
        try:
            real_subject = get_real_subject(subject_name)
            aliases = ', '.join(get_subject_alias(real_subject[0]))
            await ctx.send(f'**{real_subject[1]}**:\n'
                           f'''Aliases: {aliases if len(aliases) > 0 else 'No aliases'}\n'''
                           f'Description: {get_subject_description(real_subject[0])}\n'
                           f'''{'You are subscribed to this class!'
                           if is_subscribed(ctx.author.it, real_subject[0])
                           else 'You are not subscribed to this class!'}''')
        except SubjectError as e:
            await ctx.send(str(e))

    @subjects.autocomplete('options')
    async def subject_options_autocomplete(self, _interaction, current):
        options = ['list', 'add', 'remove']
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @subjects.autocomplete('subject_name')
    async def subject_name_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject_name)[1] for subject_name in subject_data]
        for subject in subject_data:
            options.extend(alias for alias in get_subject_alias(subject))
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(brief='Manage alias',
                             description='List, add, or remove aliases to subjects for more accessibility')
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
                if not is_subscribed(ctx.author.id, real_subject[0]):
                    await ctx.send(f'You must be subscribed to {real_subject[1]} to add aliases to it!')
                    return
                await ctx.send(f'What is the alias to add to {real_subject[1]}?')
                msg = await self.client.wait_for('message',
                                                 check=lambda m: m.channel == ctx.channel and
                                                 m.author == ctx.author,
                                                 timeout=20.0)
                subject_alias = msg.content
            except SubjectError as e:
                await ctx.send(str(e))
                return
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Failed to add alias!')
                return
            try:
                add_subject_alias(real_subject[0], subject_alias)
                await ctx.send(f'Added {subject_alias} to the list of aliases of {real_subject[1]}!')
            except SubjectAttributeError as e:
                await ctx.send(str(e))
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
                if not is_subscribed(ctx.author.id, real_subject[0]):
                    await ctx.send(f'You must be subscribed to {real_subject[1]} to remove aliases from it!')
                    return
                await ctx.send(f'What is the alias to remove from {real_subject[1]}?')
                msg = await self.client.wait_for('message',
                                                 check=lambda m: m.channel == ctx.channel and
                                                 m.author == ctx.author,
                                                 timeout=20.0)
                subject_alias = msg.content
            except SubjectError as e:
                await ctx.send(str(e))
                return
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Failed to add alias!')
                return
            try:
                remove_subject_alias(real_subject[0], subject_alias)
                await ctx.send(f'Removed {subject_alias} from the list of aliases of {real_subject[1]}!')
            except SubjectAttributeError as e:
                await ctx.send(str(e))
            return
        else:
            subject_name = f'{options} {subject_name}'
        try:
            real_subject = get_real_subject(subject_name)
            aliases = ', '.join(get_subject_alias(real_subject[0]))
            await ctx.send(f'''Aliases of {real_subject[1]}: {aliases if len(aliases) > 0 else 'No aliases'}''')
            return
        except SubjectError as e:
            await ctx.send(str(e))

    @alias.autocomplete('options')
    async def alias_options_autocomplete(self, _interaction, current):
        options = ['list', 'add', 'remove']
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @alias.autocomplete('subject_name')
    async def subject_name_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject_name)[1] for subject_name in subject_data]
        for subject in subject_data:
            options.extend(alias for alias in get_subject_alias(subject))
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
                    await ctx.send('Timeout! Failed to retrieve description!')
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
                if not is_subscribed(ctx.author.id, real_subject[0]):
                    await ctx.send(f'You must be subscribed to {real_subject[1]} to add a description to it!')
                    return
                await ctx.send(f'What is the description for {real_subject[1]}?')
                msg = await self.client.wait_for('message',
                                                 check=lambda m: m.channel == ctx.channel and
                                                 m.author == ctx.author,
                                                 timeout=20.0)
                subject_description = msg.content
            except SubjectError as e:
                await ctx.send(str(e))
                return
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Failed to set description!')
                return
            try:
                set_subject_description(real_subject[0], subject_description)
                await ctx.send(f'Set description of {real_subject[1]} to *{subject_description}*!')
            except SubjectAttributeError as e:
                await ctx.send(str(e))
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
                if not is_subscribed(ctx.author.id, real_subject[0]):
                    await ctx.send(f'You must be subscribed to {real_subject[1]} to clear its description!')
                    return
            except SubjectError as e:
                await ctx.send(str(e))
                return
            try:
                set_subject_description(real_subject[0], 'No description')
                await ctx.send(f'Cleared description of {real_subject[1]}!')
            except SubjectAttributeError as e:
                await ctx.send(str(e))
            return
        else:
            subject_name = f'{options} {subject_name}'
        try:
            real_subject = get_real_subject(subject_name)
            await ctx.send(f'**{real_subject[1]} description:** {get_subject_description(real_subject[0])}')
            return
        except SubjectError as e:
            await ctx.send(str(e))

    @description.autocomplete('options')
    async def description_options_autocomplete(self, _interaction, current):
        options = ['list', 'set', 'clear']
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @description.autocomplete('subject_name')
    async def subject_name_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject_name)[1] for subject_name in subject_data]
        for subject in subject_data:
            options.extend(alias for alias in get_subject_alias(subject))
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(brief='Subscribe to subjects',
                             description='Subscribe to subjects to receive their reminders')
    async def subscribe(self, ctx, *, subject_name=None):
        if subject_name is None:
            try:
                await ctx.send('What subject to subscribe to?')
                msg = await self.client.wait_for('message',
                                                 check=lambda m: m.channel == ctx.channel and
                                                 m.author == ctx.author,
                                                 timeout=20.0)
                subject_name = msg.content
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Failed to subscribe!')
                return
        try:
            real_subject = get_real_subject(subject_name)
        except SubjectError as e:
            await ctx.send(str(e))
            return
        try:
            add_user_subject(ctx.author.id, real_subject[0])
        except UserError as e:
            await ctx.send(str(e))
            return
        await ctx.send(f'Subscribed to {real_subject[1]}!')

    @subscribe.autocomplete('subject_name')
    async def subscription_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject)[1] for subject in subject_data]
        for subject in subject_data:
            options.extend(alias for alias in get_subject_alias(subject))
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(brief='Unsubscribe to subjects',
                             description='Unsubscribe to subjects to stop receiving their reminders')
    async def unsubscribe(self, ctx, *, subject_name=None):
        if subject_name is None:
            try:
                await ctx.send('What subject to unsubscribe from?')
                msg = await self.client.wait_for('message',
                                                 check=lambda m: m.channel == ctx.channel and
                                                 m.author == ctx.author,
                                                 timeout=20.0)
                subject_name = msg.content
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Failed to unsubscribe!')
                return
        try:
            real_subject = get_real_subject(subject_name)
        except SubjectError as e:
            await ctx.send(str(e))
            return
        try:
            remove_user_subject(ctx.author.id, real_subject[0])
            await ctx.send(f'Unsubscribed from {real_subject[1]}!')
        except UserOwnerError as e:
            await ctx.send(str(e))
            return
        except UserError as e:
            await ctx.send(str(e))
            return

    @unsubscribe.autocomplete('subject_name')
    async def unsubscription_autocomplete(self, interaction, current):
        options = [get_real_subject(subject)[1] for subject in subject_data
                   if subject in get_user_subjects(interaction.user.id)]
        for subject in subject_data:
            if subject in get_user_subjects(interaction.user.id):
                options.extend(alias for alias in get_subject_alias(subject))
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(brief='Manage admin',
                             description='View, add, or remove admins of the subject you created/own')
    async def admin(self, ctx, options=None, *, subject_name=None):
        if options is None or options.lower() == 'list':
            if subject_name is None:
                try:
                    await ctx.send('What subject to check admins?')
                    msg = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                    subject_name = msg.content
                except asyncio.TimeoutError:
                    await ctx.send('Timeout! Failed to retrieve admins!')
                    return
        elif options.lower() == 'add':
            if subject_name is None:
                try:
                    await ctx.send('What subject to add admin?')
                    msg = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                    subject_name = msg.content
                except asyncio.TimeoutError:
                    await ctx.send('Timeout! Failed to add admin!')
                    return
            try:
                real_subject = get_real_subject(subject_name)
            except SubjectError as e:
                await ctx.send(str(e))
                return
            if not is_owner(ctx.author.id, real_subject[0]):
                await ctx.send(f'Only the owner of {real_subject[1]} can add admins to it!')
                return
            if len(subject_data[real_subject[0]]['admins']) == 10:
                await ctx.send(f'Subjects can only have up to 10 admins!')
                return
            try:
                await ctx.send('Who to add as admin? (Use their ping tag)')
                msg = await self.client.wait_for('message',
                                                 check=lambda m: m.channel == ctx.channel and m.author == ctx.author,
                                                 timeout=20.0)
                user_mention = msg.content
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Failed to add admin!')
                return
            try:
                add_admin_subject(user_mention, real_subject[0])
                await ctx.send(f'Added {user_mention} as admin of {real_subject[1]}!')
            except UserError as e:
                await ctx.send(str(e), allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False))
            return
        elif options.lower() == 'remove':
            if subject_name is None:
                try:
                    await ctx.send('What subject to remove admin?')
                    msg = await self.client.wait_for('message',
                                                     check=lambda m: m.channel == ctx.channel and
                                                     m.author == ctx.author,
                                                     timeout=20.0)
                    subject_name = msg.content
                except asyncio.TimeoutError:
                    await ctx.send('Timeout! Failed to remove admin!')
                    return
            try:
                real_subject = get_real_subject(subject_name)
            except SubjectError as e:
                await ctx.send(str(e))
                return
            if not is_owner(ctx.author.id, real_subject[0]):
                await ctx.send(f'Only the owner of {real_subject[1]} can remove admins from it!')
                return
            try:
                await ctx.send('Who to remove as admin? (Use their ping tag)')
                msg = await self.client.wait_for('message',
                                                 check=lambda m: m.channel == ctx.channel and m.author == ctx.author,
                                                 timeout=20.0)
                user_mention = msg.content
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Failed to remove admin!')
                return
            try:
                remove_admin_subject(user_mention, real_subject[0])
                await ctx.send(f'Removed {user_mention} as admin of {real_subject[1]}!')
            except UserError as e:
                await ctx.send(str(e))
            except UserOwnerError as e:
                await ctx.send(str(e))
            return
        else:
            subject_name = f'{options} {subject_name}'
        try:
            real_subject = get_real_subject(subject_name)
        except SubjectError as e:
            await ctx.send(str(e))
            return
        message = f'Admins of {real_subject[1]}: '
        for admin in subject_data[real_subject[0]]['admins']:
            message += f'{await self.client.fetch_user(admin)}, '
        message = message[:-2]
        await ctx.send(message)
        return

    @admin.autocomplete('options')
    async def admin_options_autocomplete(self, _interaction, current):
        options = ['list', 'add', 'remove']
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @admin.autocomplete('subject_name')
    async def subject_name_autocomplete(self, _interaction, current):
        options = [get_real_subject(subject)[1] for subject in subject_data]
        for subject in subject_data:
            options.extend(alias for alias in get_subject_alias(subject))
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]


async def setup(client):
    await client.add_cog(Subject(client))
