import os

from dotenv import load_dotenv

load_dotenv()

token = os.getenv("DISCORD_TOKEN")

if token:
    print("Discord token loaded successfully.")
else:
    print("Discord token was not found.")