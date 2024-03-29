"""Role giving listener based on messages"""

import asyncio
import traceback
from emoji import EMOJI_DATA

import discord
from discord.ext import commands

from data_config import message_listener
from util import generate_message_listener, remove_message_listener, MessageAttributeError, MessageError


class MessageReactionListener(commands.Cog, name='message_reaction_listener'):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        print(f'listened message delete detected {payload.message_id}')
        if payload.message_id in message_listener:
            remove_message_listener(payload.message_id)

    @commands.Cog.listener('on_raw_reaction_add')
    async def message_reaction_add_listener(self, payload):
        guild = await self.client.fetch_guild(payload.guild_id)
        channel = await guild.fetch_channel(payload.channel_id)
        member = await guild.fetch_member(payload.user_id)
        msg_id = payload.message_id
        emoji_name = payload.emoji.name
        if payload.user_id == 970868539022008330:
            return
        if msg_id not in message_listener:
            return
        elif msg_id in message_listener and emoji_name in message_listener[msg_id]['emoji']:
            print(f'reaction add detected {guild} {channel} {member} {msg_id} {emoji_name}')
            role_id = message_listener[msg_id]['role'][message_listener[msg_id]['emoji'].index(emoji_name)]
            role_name = guild.get_role(role_id).name
            try:
                await member.add_roles(guild.get_role(role_id))
            except discord.Forbidden:
                await channel.send(
                    f'I do not have permission to give the \'{role_name}\' role to {member.display_name}.')
        else:
            msg = await channel.fetch_message(msg_id)
            await msg.remove_reaction(payload.emoji, member)
            return

    @commands.Cog.listener('on_raw_reaction_remove')
    async def message_reaction_remove_listener(self, payload):
        guild = await self.client.fetch_guild(payload.guild_id)
        channel = await guild.fetch_channel(payload.channel_id)
        member = await guild.fetch_member(payload.user_id)
        msg_id = payload.message_id
        emoji_name = payload.emoji.name
        role_name = None
        print(f'reaction remove detected {guild} {channel} {member} {msg_id} {emoji_name}')
        if msg_id in message_listener and emoji_name in message_listener[msg_id]['emoji']:
            role_id = message_listener[msg_id]['role'][message_listener[msg_id]['emoji'].index(emoji_name)]
            role_name = guild.get_role(role_id).name
            await member.remove_roles(guild.get_role(role_id))
        if msg_id in message_listener and role_name is None:
            await channel.send(f'This reaction message does not work anymore. Delete the'
                               f' reaction message and rerun the reaction_message command.')
            return

    @commands.hybrid_command()
    async def reaction_message(self, ctx, *, emojis=None):
        emoji_listener = []
        role_listener = []
        if ctx.author.id != 434430979075997707:
            await ctx.send("You are not authorized to use this command!")
            return
        if emojis is None:
            try:
                await ctx.send('What emojis will be listened to?')
                emojis = await self.client.wait_for('message',
                                                    check=lambda m: m.channel == ctx.channel and m.author == ctx.author,
                                                    timeout=40.0)
                emojis = emojis.content
            except asyncio.TimeoutError:
                await ctx.send('Failed to add message to listen to!')
        emojis = emojis.split()
        for emoji in emojis:
            if emoji not in EMOJI_DATA and (emoji[2:emoji.find(':', 2, -1)] not in
                                            [guild_emoji.name for guild_emoji in
                                             await ctx.guild.fetch_emojis()]):
                await ctx.send('Invalid emoji! Please enter emoji icons, not the names.' if len(emojis) == 1 else
                               'Invalid emojis! Please enter emoji icons, not the names.')
                return
            emoji_listener.append(emoji)
        try:
            await ctx.send('What is the message to be listened to for reactions?')
            msg = await self.client.wait_for('message',
                                             check=lambda m: m.channel == ctx.channel and m.author == ctx.author,
                                             timeout=40.0)
            msg = msg.content
            for emoji in emojis:
                await ctx.send(f'What is the name of the role associated with {emoji}?')
                role = await self.client.wait_for('message',
                                                  check=lambda m: m.channel == ctx.channel and m.author == ctx.author,
                                                  timeout=20.0)
                role = role.content
                if role not in [guild_role.name for guild_role in await ctx.guild.fetch_roles()]:
                    await ctx.send(f'{role} is not a valid role name to assign {emoji} to!')
                    return
                for guild_role in await ctx.guild.fetch_roles():
                    if role == guild_role.name:
                        role_listener.append(guild_role.id)
        except asyncio.TimeoutError:
            await ctx.send('Failed to add message to listen to!')
            return
        try:
            await ctx.send('Mention everyone? (y/N)')
            everyone = await self.client.wait_for('message',
                                                  check=lambda m: m.channel == ctx.channel and m.author == ctx.author,
                                                  timeout=3.0)
            everyone = everyone.content
        except asyncio.TimeoutError:
            everyone = 'n'
        if everyone.lower() == 'y':
            msg = '@everyone ' + msg
        try:
            await ctx.send('Which channel to send?')
            channel_id = await self.client.wait_for('message',
                                                 check=lambda m: m.channel == ctx.channel and m.author == ctx.author,
                                                 timeout=40.0)
            channel_id = channel_id.content[2:-1] if (channel_id.content.startswith('<#') and
                                                      channel_id.content.endswith('>')) else channel_id.content
            try:
                channel = await ctx.guild.fetch_channel(channel_id)
            except discord.NotFound:
                await ctx.send('Channel not found!')
                return
        except asyncio.TimeoutError:
            channel = ctx.channel.id
        msg_listener = await channel.send(msg)
        for emoji in emoji_listener:
            if emoji not in EMOJI_DATA:
                for e in await msg_listener.guild.fetch_emojis():
                    if emoji == e.name:
                        await msg_listener.add_reaction(e)
                continue
            await msg_listener.add_reaction(emoji)
        try:
            generate_message_listener(msg_listener.id, emoji_listener, role_listener)
            print(f'Added {msg_listener.id}, {emoji_listener} with {role_listener}, respectively, to message_listener')
        except MessageAttributeError as e:
            await ctx.send(str(e))


async def setup(client):
    await client.add_cog(MessageReactionListener(client))
