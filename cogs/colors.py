# from curses import color_content
import os
import sys
import yaml
from colour import Color
from nextcord.ui import Button, View
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
import random


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class Colors(commands.Cog, name="colors"):
    def __init__(self, bot):
        self.bot = bot

    def luminance(self, color):
        """
        Calculate the luminance of a color.
        """
        red = Color(color).red
        green = Color(color).green
        blue = Color(color).blue

        red = red / 12.92 if red <= 0.04045 else ((red + 0.055) / 1.055)**2.4
        green = green / 12.92 if green <= 0.04045 else ((green + 0.055) / 1.055)**2.4
        blue = blue / 12.92 if blue <= 0.04045 else ((blue + 0.055) / 1.055)**2.4

        return (0.2126 * red) + (0.7152 * green) + (0.0722 * blue)

    def contrast(self, color1, color2):
        """
        Calculate the contrast between two colors.
        """
        lum1 = self.luminance(color1)
        lum2 = self.luminance(color2)

        return (max(lum1, lum2) + 0.05) / (min(lum1, lum2) + 0.05)
    
    def rgb2hex(self, rgb):
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        return "#{:02x}{:02x}{:02x}".format(r,g,b)
    
    def hex2rgb(self, hexcode):
        hexcode = hexcode.lstrip("#")
        return tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4))

    def similarColors(self, color, delta, loop=6):
        rgb = self.hex2rgb(color)

        colors = []
        deltas = [round(delta / u) for u in (1, 1, 1)]
        for _ in range(loop):
            new_rgb = [random.randint(max(0, x - delta), min(x + delta, 255))
                for x, delta in zip(rgb, deltas)]
            colors.append(new_rgb)

        return [self.rgb2hex(color) for color in colors]
    
    def checkContrastOfColorGroup(self, colorGroup):
        for color in colorGroup:
            if self.contrast("#36393f", color) >= 4:
                return [True, color]
        return [False]
    
    async def changeRoleColor(self, color, role):
        await role.edit(colour=nextcord.Colour(int(color.replace("#", ""), 16)))

    def generateRandomColor(self):
        """
        Generate random color value
        """
        limit = 4
        contrast = 0

        while contrast < limit:
            randomColor = hex(random.randint(0, 16777216)) # generate random integer
            randomColor = randomColor[2:]

            if (len(randomColor) < 6):
                randomColor = '0' * (6-len(randomColor)) + randomColor
            randomColor = "#" + randomColor

            contrast = self.contrast("#36393f", randomColor)
            
        return randomColor

    @nextcord.slash_command(name="changecolor", description="change your role color")
    async def changecolor(self, interaction: Interaction, color: str = SlashOption(description="A color hex code, like '#2B5FB3'", required=False)):
        """
        [ColorHexCode] Allows the user to change the color of their nickname. Only usable in some servers.
        """
        try:
            userRoles = interaction.user.roles
            
            if color is None:
                print("color is empty")
                # generate random color
                color = self.generateRandomColor()

            colorButton = Button(label="Another Color", style=nextcord.ButtonStyle.blurple)

            async def color_callback(buttonInteraction):
                if buttonInteraction.user == interaction.user:  # checks that user interacting with button is command sender
                    newColor = self.generateRandomColor()
                    topRole = userRoles[-1]  
                    await self.changeRoleColor(newColor, topRole)
                    await buttonInteraction.message.edit(embed = nextcord.Embed(
                        title="Success!",
                        description=f"Color has been changed to {newColor.upper()}!",
                        color=int(newColor.replace("#", ""), 16)
                    ))

                # await interaction.response.send_message(embed=embed, view=view)
                return

            if len(userRoles) > 1:
                topRole = userRoles[-1]
                await topRole.edit(colour=nextcord.Colour(int(color.replace("#", ""), 16)))
                embed = nextcord.Embed(
                    title="Success!",
                    description="Color has been changed!",
                    color=int(color.replace("#", ""), 16)
                )
                colorButton.callback = color_callback
                view = View(timeout=1000)
                view.add_item(colorButton)

                await interaction.response.send_message(embed = embed, view = view)

        except Exception as e:
            print(e)
            embed = nextcord.Embed(
                title="Error",
                description="Something went wrong, make sure you are using a 6 digit hex code. (ex: !changecolor #FFFFFF)",
                color=config["error"]
            )
            await interaction.response.send_message(embed=embed)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Colors(bot))
