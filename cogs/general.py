"""General commands"""

import discord
from discord.ext import commands

import constants
from data_config import subject_data, save_all


class General(commands.Cog, name='general'):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} just joined')

    @commands.hybrid_command(brief='List of commands', description='Need help? Call this command!')
    async def help(self, ctx, options=None):
        all_subjects = ''
        for subject_name in subject_data:
            all_subjects += subject_data[subject_name]['real'] + ', '
        all_subjects = all_subjects[0:-2]
        if options is None:
            embed = discord.Embed(color=0x255FAB, title='bigfatstudier Bot Commands',
                                  description='Don\'t know commands? Not to worry!')
            for command in self.client.commands:
                embed.add_field(name=command.name, value=command.description)
            await ctx.send(embed=embed)
        elif options.lower() == 'subjects':
            embed = discord.Embed(color=0xFF9100, title='bigfatstudier \'subjects\' Command',
                                  description=self.client.get_command('subjects').description)
            embed.add_field(name='list', value='List all of the subjects stored on this bot')
            embed.add_field(name='add', value='Add a subject to store on this bot')
            embed.add_field(name='remove', value='Remove a subject from this bot')
            await ctx.send(embed=embed)
        elif options.lower() == 'homework':
            embed = discord.Embed(color=0x00D4FF, title='bigfatstudier \'homework\' Command',
                                  description=self.client.get_command('homework').description)
            embed.add_field(name='all', value='List all of the homework from every subject stored on this bot')
            embed.add_field(name='*Specific Subject*',
                            value=f'Specify a subject to check homework: {all_subjects}')
            await ctx.send(embed=embed)
        elif options.lower() == 'add_homework':
            embed = discord.Embed(color=0xB300FF, title='bigfatstudier \'add_homework\' Command',
                                  description=self.client.get_command('add_homework').description)
            embed.add_field(name='*Specific Subject*',
                            value=f'Specify a subject to set homework to: {all_subjects}')
            embed.add_field(name='Other Parameters',
                            value='Specify in two follow up messages the assignment name and due date, respectively.')
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'{options} is not a valid command!')

    @help.autocomplete('options')
    async def help_autocomplete(self, _interaction, current):
        options = [command.name for command in self.client.commands if
                   command.name != 'help' and command.name != 'stop']
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    @commands.hybrid_command(brief='Version', description='Get the version of the bot')
    async def version(self, ctx):
        await ctx.send(f'This bot is on version **{constants.VERSION_NAME}**.')

    @commands.hybrid_command(brief='Kill the bot', description='Kill the bot, but only for for owner')
    async def stop(self, ctx):
        if ctx.author.id == 434430979075997707:
            save_all()
            await ctx.send('Shutting down')
            await self.client.tree.sync()
            await self.client.close()
        else:
            await ctx.send('You think I\'d let anyone close the bot?')


async def setup(client):
    await client.add_cog(General(client))
