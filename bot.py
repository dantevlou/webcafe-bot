import os
from io import BytesIO

import discord
from dotenv import load_dotenv
from PIL import Image

from welcome_card_preview import OUTPUT_PATH, create_welcome_card


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

    avatar_bytes = await member.display_avatar.read()

    with Image.open(BytesIO(avatar_bytes)) as avatar_image:
        create_welcome_card(
            member.name,
            avatar_image,
        )

        await login_channel.send(
            file=discord.File(OUTPUT_PATH),
        )


client.run(token)