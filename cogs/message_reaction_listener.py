"""Temporary calculus math role"""

import asyncio
import discord
from discord.ext import commands

from data_config import message_listener, generate_message_listener, remove_message_listener


class SummerMathProgram(commands.Cog, name='summer_math_program'):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.id in message_listener:
            remove_message_listener(message.id)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        guild = user.guild
        msg = reaction.message.id
        emoji = reaction.emoji.id
        if msg in message_listener and emoji in message_listener[msg]['emoji']:
            await user.add_roles(
                message_listener[msg]['role'][guild.get_role(message_listener[msg]['emoji'].index(emoji))])

    @commands.hybrid_command()
    async def reaction_message(self, ctx, *, emojis=None):
        if emojis is None:
            await ctx.send('You need emojis of the reactions to listen to!')
        emojis = emojis.split()
        emoji_listener = []
        role_listener = []
        try:
            await ctx.send('Send the message to be listened to for reactions.')
            msg = await self.client.wait_for('message',
                                             check=lambda m: m.channel == ctx.channel and m.author == ctx.author,
                                             timeout=40.0)
            for emoji in emojis:
                if len(emoji) > 1:
                    if emoji not in [guild_emoji.name for guild_emoji in await ctx.guild.fetch_emojis()]:
                        await ctx.send(f'{emoji} is not a valid emoji name! Sorry, partial emojis are not supported.')
                        return
                    for guild_emoji in await ctx.guild.fetch_emojis():
                        if emoji == guild_emoji.name:
                            emoji_listener.append(guild_emoji.id)
                else:
                    emoji_listener.append(e.demojize(emoji)) # TODO: FIX
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
        msg_listener = await ctx.send(msg.content)
        generate_message_listener(msg_listener.id, emoji_listener, role_listener)


async def setup(client):
    await client.add_cog(SummerMathProgram(client))
