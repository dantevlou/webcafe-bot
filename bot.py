import os

import discord
from dotenv import load_dotenv


load_dotenv()

token = os.getenv("DISCORD_TOKEN")
login_channel_id = int(os.getenv("LOGIN_CHANNEL_ID"))

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_member_join(member):
    login_channel = client.get_channel(login_channel_id)

    if login_channel is None:
        print("Login channel could not be found.")
        return

    embed = discord.Embed(
        title="webcafe.exe // NEW CONNECTION",
        description=(
            f"```text\n"
            f"> user detected\n"
            f"> connection status: ONLINE\n"
            f"```\n"
            f"Welcome, {member.mention}.\n\n"
            f"Configure your account in **#ᴜsᴇʀ-sᴇᴛᴛɪɴɢs** "
            f"to unlock the rest of the café."
        ),
        color=0x67DDE0
    )

    embed.set_footer(text="webcafe.exe • connection established")

    await login_channel.send(embed=embed)


client.run(token)