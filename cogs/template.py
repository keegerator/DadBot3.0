# import os
# import sys
# import yaml
# import nextcord
# from typing import Optional
# from nextcord.ext import commands
# from nextcord import Interaction, SlashOption, ChannelType
# from nextcord.abc import GuildChannel


# with open("config.yaml") as file:
#     config = yaml.load(file, Loader=yaml.FullLoader)

# # Here we name the cog and create a new class for the cog.
# class Template(commands.Cog, name="template"):
#     def __init__(self, bot):
#         self.bot = bot

    # # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    # @nextcord.slash_command(name="template", description="This is a testing command that does nothing.")
    # async def testcommand(self, context):
    #     """
    #     [No Arguments] This is a testing command that does nothing.
    #     """
    #     await context.send("I'll tell you when you're older. Move along now, child.")

# # And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
# def setup(bot):
#     bot.add_cog(Template(bot))
