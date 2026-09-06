import os
import random
import time
from io import BytesIO

import discord
from dotenv import load_dotenv
from PIL import Image

from database import add_xp, initialise_database
from settings_panel import (
    OUTPUT_PATH as SETTINGS_PANEL_PATH,
    create_settings_panel,
)
from welcome_card_preview import (
    OUTPUT_PATH as WELCOME_CARD_PATH,
    create_welcome_card,
)


load_dotenv()

token = os.getenv("DISCORD_TOKEN")
login_channel_id = int(os.getenv("LOGIN_CHANNEL_ID"))

user_settings_channel_id = int(
    os.getenv("USER_SETTINGS_CHANNEL_ID")
)

user_settings_message_id = int(
    os.getenv("USER_SETTINGS_MESSAGE_ID")
)

user_role_id = int(os.getenv("USER_ROLE_ID"))

# Colour roles
COLOUR_ROLE_IDS = {
    "pink": int(os.getenv("PINK_ROLE_ID")),
    "red": int(os.getenv("RED_ROLE_ID")),
    "brown": int(os.getenv("BROWN_ROLE_ID")),
    "orange": int(os.getenv("ORANGE_ROLE_ID")),
    "yellow": int(os.getenv("YELLOW_ROLE_ID")),
    "green": int(os.getenv("GREEN_ROLE_ID")),
    "cyan": int(os.getenv("CYAN_ROLE_ID")),
    "blue": int(os.getenv("BLUE_ROLE_ID")),
    "purple": int(os.getenv("PURPLE_ROLE_ID")),
    "grey": int(os.getenv("GREY_ROLE_ID")),
    "white": int(os.getenv("WHITE_ROLE_ID")),
    "black": int(os.getenv("BLACK_ROLE_ID")),
}

# Pronoun roles
PRONOUN_ROLE_IDS = {
    "she_her": int(os.getenv("SHE_HER_ROLE_ID")),
    "he_him": int(os.getenv("HE_HIM_ROLE_ID")),
    "they_them": int(os.getenv("THEY_THEM_ROLE_ID")),
    "any_pronouns": int(os.getenv("ANY_PRONOUNS_ROLE_ID")),
    "ask_me": int(os.getenv("ASK_ME_ROLE_ID")),
}

PRONOUN_LABELS = {
    "she_her": "She / Her",
    "he_him": "He / Him",
    "they_them": "They / Them",
    "any_pronouns": "Any Pronouns",
    "ask_me": "Ask Me",
}

# Region roles
REGION_ROLE_IDS = {
    "act": int(os.getenv("ACT_ROLE_ID")),
    "nsw": int(os.getenv("NSW_ROLE_ID")),
    "wa": int(os.getenv("WA_ROLE_ID")),
    "vic": int(os.getenv("VIC_ROLE_ID")),
    "qld": int(os.getenv("QLD_ROLE_ID")),
    "sa": int(os.getenv("SA_ROLE_ID")),
    "tas": int(os.getenv("TAS_ROLE_ID")),
    "nt": int(os.getenv("NT_ROLE_ID")),
    "new_zealand": int(os.getenv("NEW_ZEALAND_ROLE_ID")),
    "other": int(os.getenv("OTHER_LOCATION_ROLE_ID")),
}

REGION_LABELS = {
    "act": "ACT",
    "nsw": "NSW",
    "wa": "WA",
    "vic": "VIC",
    "qld": "QLD",
    "sa": "SA",
    "tas": "TAS",
    "nt": "NT",
    "new_zealand": "New Zealand",
    "other": "Other",
}

# Platform roles
PLATFORM_ROLE_IDS = {
    "pc": int(os.getenv("PC_ROLE_ID")),
    "xbox": int(os.getenv("XBOX_ROLE_ID")),
    "playstation": int(os.getenv("PLAYSTATION_ROLE_ID")),
    "nintendo_switch": int(
        os.getenv("NINTENDO_SWITCH_ROLE_ID")
    ),
    "mobile": int(os.getenv("MOBILE_ROLE_ID")),
}

PLATFORM_LABELS = {
    "pc": "PC",
    "xbox": "Xbox",
    "playstation": "PlayStation",
    "nintendo_switch": "Nintendo Switch",
    "mobile": "Mobile",
}

# Game roles
GAME_ROLE_IDS = {
    "valorant": int(os.getenv("VALORANT_ROLE_ID")),
    "minecraft": int(os.getenv("MINECRAFT_ROLE_ID")),
    "league": int(os.getenv("LEAGUE_ROLE_ID")),
    "roblox": int(os.getenv("ROBLOX_ROLE_ID")),
}

GAME_LABELS = {
    "valorant": "Valorant",
    "minecraft": "Minecraft",
    "league": "League",
    "roblox": "Roblox",
}

# Level roles
LEVEL_ROLE_IDS = {
    1: int(os.getenv("NEWCOMER_ROLE_ID")),
    10: int(os.getenv("CAFE_REGULAR_ROLE_ID")),
    20: int(os.getenv("CAFE_MEMBER_ROLE_ID")),
    30: int(os.getenv("CAFE_ENTHUSIAST_ROLE_ID")),
    40: int(os.getenv("CAFE_KEEPER_ROLE_ID")),
    50: int(os.getenv("CAFE_CONNOISSEUR_ROLE_ID")),
    60: int(os.getenv("CAFE_INSIDER_ROLE_ID")),
    70: int(os.getenv("CAFE_STAR_ROLE_ID")),
    80: int(os.getenv("CAFE_CELEBRITY_ROLE_ID")),
    90: int(os.getenv("CAFE_ICON_ROLE_ID")),
    100: int(os.getenv("CAFE_LEGEND_ROLE_ID")),
}

XP_MIN = 10
XP_MAX = 15
XP_COOLDOWN_SECONDS = 60

xp_cooldowns = {}

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)


async def sync_level_roles(
    member: discord.Member,
    level: int,
):
    """Give a member the correct milestone role for their level."""
    eligible_levels = [
        milestone
        for milestone in LEVEL_ROLE_IDS
        if milestone <= level
    ]

    if not eligible_levels:
        return

    current_milestone = max(eligible_levels)
    selected_role_id = LEVEL_ROLE_IDS[current_milestone]

    selected_role = member.guild.get_role(
        selected_role_id
    )

    current_level_roles = [
        role
        for role in member.roles
        if role.id in LEVEL_ROLE_IDS.values()
    ]

    roles_to_remove = [
        role
        for role in current_level_roles
        if role.id != selected_role_id
    ]

    if roles_to_remove:
        await member.remove_roles(
            *roles_to_remove
        )

    if (
        selected_role is not None
        and selected_role not in member.roles
    ):
        await member.add_roles(
            selected_role
        )


class ColourSelect(discord.ui.Select):
    """Handle single-choice colour role selection."""

    def __init__(self):
        options = [
            discord.SelectOption(label="Pink", value="pink"),
            discord.SelectOption(label="Red", value="red"),
            discord.SelectOption(label="Brown", value="brown"),
            discord.SelectOption(label="Orange", value="orange"),
            discord.SelectOption(label="Yellow", value="yellow"),
            discord.SelectOption(label="Green", value="green"),
            discord.SelectOption(label="Cyan", value="cyan"),
            discord.SelectOption(label="Blue", value="blue"),
            discord.SelectOption(label="Purple", value="purple"),
            discord.SelectOption(label="Grey", value="grey"),
            discord.SelectOption(label="White", value="white"),
            discord.SelectOption(label="Black", value="black"),
        ]

        super().__init__(
            placeholder="choose your colour",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        """Update the member's colour role and grant server access."""
        await interaction.response.defer(ephemeral=True)

        selected_colour = self.values[0]
        selected_role_id = COLOUR_ROLE_IDS[selected_colour]

        selected_role = interaction.guild.get_role(
            selected_role_id
        )

        user_role = interaction.guild.get_role(
            user_role_id
        )

        current_colour_roles = [
            role
            for role in interaction.user.roles
            if role.id in COLOUR_ROLE_IDS.values()
        ]

        if current_colour_roles:
            await interaction.user.remove_roles(
                *current_colour_roles
            )

        await interaction.user.add_roles(
            selected_role
        )

        if user_role not in interaction.user.roles:
            await interaction.user.add_roles(
                user_role
            )

        await interaction.followup.send(
            (
                "SETTINGS SAVED // "
                f"{selected_colour.title()} selected"
            ),
            ephemeral=True,
        )


class PronounButton(discord.ui.Button):
    """Handle single-choice pronoun role selection."""

    def __init__(
        self,
        label: str,
        pronoun_key: str,
    ):
        super().__init__(
            label=label,
            style=discord.ButtonStyle.secondary,
        )
        self.pronoun_key = pronoun_key

    async def callback(self, interaction: discord.Interaction):
        """Update the member's selected pronoun role."""
        await interaction.response.defer(ephemeral=True)

        selected_role_id = PRONOUN_ROLE_IDS[
            self.pronoun_key
        ]
        selected_role = interaction.guild.get_role(
            selected_role_id
        )
        selected_label = PRONOUN_LABELS[
            self.pronoun_key
        ]

        current_pronoun_roles = [
            role
            for role in interaction.user.roles
            if role.id in PRONOUN_ROLE_IDS.values()
        ]

        already_selected = any(
            role.id == selected_role_id
            for role in current_pronoun_roles
        )

        if already_selected:
            await interaction.followup.send(
                (
                    "SETTINGS SAVED // "
                    f"**{selected_label}** already selected"
                ),
                ephemeral=True,
            )
            return

        previous_role = (
            current_pronoun_roles[0]
            if current_pronoun_roles
            else None
        )

        if current_pronoun_roles:
            await interaction.user.remove_roles(
                *current_pronoun_roles
            )

        await interaction.user.add_roles(
            selected_role
        )

        if previous_role is not None:
            previous_key = next(
                key
                for key, role_id in PRONOUN_ROLE_IDS.items()
                if role_id == previous_role.id
            )

            previous_label = PRONOUN_LABELS[
                previous_key
            ]

            message = (
                "SETTINGS SAVED // pronouns switched from "
                f"**{previous_label}** to **{selected_label}**"
            )
        else:
            message = (
                "SETTINGS SAVED // pronouns set to "
                f"**{selected_label}**"
            )

        await interaction.followup.send(
            message,
            ephemeral=True,
        )


class RegionButton(discord.ui.Button):
    """Handle single-choice region role selection."""

    def __init__(
        self,
        label: str,
        region_key: str,
    ):
        super().__init__(
            label=label,
            style=discord.ButtonStyle.secondary,
        )
        self.region_key = region_key

    async def callback(self, interaction: discord.Interaction):
        """Update the member's selected region role."""
        await interaction.response.defer(ephemeral=True)

        selected_role_id = REGION_ROLE_IDS[
            self.region_key
        ]
        selected_role = interaction.guild.get_role(
            selected_role_id
        )
        selected_label = REGION_LABELS[
            self.region_key
        ]

        current_region_roles = [
            role
            for role in interaction.user.roles
            if role.id in REGION_ROLE_IDS.values()
        ]

        already_selected = any(
            role.id == selected_role_id
            for role in current_region_roles
        )

        if already_selected:
            await interaction.followup.send(
                (
                    "SETTINGS SAVED // "
                    f"**{selected_label}** already selected"
                ),
                ephemeral=True,
            )
            return

        previous_role = (
            current_region_roles[0]
            if current_region_roles
            else None
        )

        if current_region_roles:
            await interaction.user.remove_roles(
                *current_region_roles
            )

        await interaction.user.add_roles(
            selected_role
        )

        if previous_role is not None:
            previous_key = next(
                key
                for key, role_id in REGION_ROLE_IDS.items()
                if role_id == previous_role.id
            )

            previous_label = REGION_LABELS[
                previous_key
            ]

            message = (
                "SETTINGS SAVED // location switched from "
                f"**{previous_label}** to **{selected_label}**"
            )
        else:
            message = (
                "SETTINGS SAVED // location set to "
                f"**{selected_label}**"
            )

        await interaction.followup.send(
            message,
            ephemeral=True,
        )


class PlatformSelect(discord.ui.Select):
    """Handle multi-select gaming platform roles."""

    def __init__(self):
        options = [
            discord.SelectOption(
                label="PC",
                value="pc",
            ),
            discord.SelectOption(
                label="Xbox",
                value="xbox",
            ),
            discord.SelectOption(
                label="PlayStation",
                value="playstation",
            ),
            discord.SelectOption(
                label="Nintendo Switch",
                value="nintendo_switch",
            ),
            discord.SelectOption(
                label="Mobile",
                value="mobile",
            ),
        ]

        super().__init__(
            placeholder="choose your platforms",
            min_values=0,
            max_values=len(options),
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        """Synchronise the member's selected platform roles."""
        await interaction.response.defer(ephemeral=True)

        selected_platforms = set(self.values)

        selected_role_ids = {
            PLATFORM_ROLE_IDS[platform_key]
            for platform_key in selected_platforms
        }

        current_platform_roles = [
            role
            for role in interaction.user.roles
            if role.id in PLATFORM_ROLE_IDS.values()
        ]

        roles_to_remove = [
            role
            for role in current_platform_roles
            if role.id not in selected_role_ids
        ]

        current_role_ids = {
            role.id
            for role in current_platform_roles
        }

        roles_to_add = [
            interaction.guild.get_role(
                PLATFORM_ROLE_IDS[platform_key]
            )
            for platform_key in selected_platforms
            if (
                PLATFORM_ROLE_IDS[platform_key]
                not in current_role_ids
            )
        ]

        roles_to_add = [
            role
            for role in roles_to_add
            if role is not None
        ]

        if roles_to_remove:
            await interaction.user.remove_roles(
                *roles_to_remove
            )

        if roles_to_add:
            await interaction.user.add_roles(
                *roles_to_add
            )

        if selected_platforms:
            selected_labels = [
                PLATFORM_LABELS[platform_key]
                for platform_key in PLATFORM_ROLE_IDS
                if platform_key in selected_platforms
            ]

            formatted_platforms = ", ".join(
                f"**{label}**"
                for label in selected_labels
            )

            message = (
                "SETTINGS SAVED // platforms set to "
                f"{formatted_platforms}"
            )
        else:
            message = (
                "SETTINGS SAVED // platforms cleared"
            )

        await interaction.followup.send(
            message,
            ephemeral=True,
        )


class GameSelect(discord.ui.Select):
    """Handle multi-select game roles."""

    def __init__(self):
        options = [
            discord.SelectOption(
                label="Valorant",
                value="valorant",
            ),
            discord.SelectOption(
                label="Minecraft",
                value="minecraft",
            ),
            discord.SelectOption(
                label="League",
                value="league",
            ),
            discord.SelectOption(
                label="Roblox",
                value="roblox",
            ),
        ]

        super().__init__(
            placeholder="choose your games",
            min_values=0,
            max_values=len(options),
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        """Synchronise the member's selected game roles."""
        await interaction.response.defer(ephemeral=True)

        selected_games = set(self.values)

        selected_role_ids = {
            GAME_ROLE_IDS[game_key]
            for game_key in selected_games
        }

        current_game_roles = [
            role
            for role in interaction.user.roles
            if role.id in GAME_ROLE_IDS.values()
        ]

        roles_to_remove = [
            role
            for role in current_game_roles
            if role.id not in selected_role_ids
        ]

        current_role_ids = {
            role.id
            for role in current_game_roles
        }

        roles_to_add = [
            interaction.guild.get_role(
                GAME_ROLE_IDS[game_key]
            )
            for game_key in selected_games
            if (
                GAME_ROLE_IDS[game_key]
                not in current_role_ids
            )
        ]

        roles_to_add = [
            role
            for role in roles_to_add
            if role is not None
        ]

        if roles_to_remove:
            await interaction.user.remove_roles(
                *roles_to_remove
            )

        if roles_to_add:
            await interaction.user.add_roles(
                *roles_to_add
            )

        if selected_games:
            selected_labels = [
                GAME_LABELS[game_key]
                for game_key in GAME_ROLE_IDS
                if game_key in selected_games
            ]

            formatted_games = ", ".join(
                f"**{label}**"
                for label in selected_labels
            )

            message = (
                "SETTINGS SAVED // games set to "
                f"{formatted_games}"
            )
        else:
            message = "SETTINGS SAVED // games cleared"

        await interaction.followup.send(
            message,
            ephemeral=True,
        )


class ProfileSettingsLayout(discord.ui.LayoutView):
    """Build the interactive user settings panel."""

    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(
            discord.ui.MediaGallery(
                discord.MediaGalleryItem(
                    "attachment://settings_panel.png"
                )
            )
        )

        self.add_item(
            discord.ui.Separator()
        )

        self.add_item(
            discord.ui.TextDisplay(
                "**01 // choose your colour**"
            )
        )

        self.add_item(
            discord.ui.ActionRow(
                ColourSelect()
            )
        )

        self.add_item(
            discord.ui.Separator()
        )

        self.add_item(
            discord.ui.TextDisplay(
                "**02 // choose your pronouns**"
            )
        )

        self.add_item(
            discord.ui.ActionRow(
                PronounButton("She / Her", "she_her"),
                PronounButton("He / Him", "he_him"),
                PronounButton("They / Them", "they_them"),
                PronounButton(
                    "Any Pronouns",
                    "any_pronouns",
                ),
                PronounButton("Ask Me", "ask_me"),
            )
        )

        self.add_item(
            discord.ui.Separator()
        )

        self.add_item(
            discord.ui.TextDisplay(
                "**03 // choose your location**"
            )
        )

        self.add_item(
            discord.ui.ActionRow(
                RegionButton("ACT", "act"),
                RegionButton("NSW", "nsw"),
                RegionButton("WA", "wa"),
                RegionButton("VIC", "vic"),
                RegionButton("QLD", "qld"),
            )
        )

        self.add_item(
            discord.ui.ActionRow(
                RegionButton("SA", "sa"),
                RegionButton("TAS", "tas"),
                RegionButton("NT", "nt"),
                RegionButton(
                    "New Zealand",
                    "new_zealand",
                ),
                RegionButton("Other", "other"),
            )
        )

        self.add_item(
            discord.ui.Separator()
        )

        self.add_item(
            discord.ui.TextDisplay(
                "**04 // select your gaming platforms**"
            )
        )

        self.add_item(
            discord.ui.ActionRow(
                PlatformSelect()
            )
        )

        self.add_item(
            discord.ui.Separator()
        )

        self.add_item(
            discord.ui.TextDisplay(
                "**05 // select the games you play**"
            )
        )

        self.add_item(
            discord.ui.ActionRow(
                GameSelect()
            )
        )


@client.event
async def on_ready():
    """Prepare the settings panel when Miso connects to Discord."""
    print(f"Logged in as {client.user}")

    user_settings_channel = client.get_channel(
        user_settings_channel_id
    )

    if user_settings_channel is None:
        print("User settings channel could not be found.")
        return

    print("User settings channel ready.")

    create_settings_panel()

    settings_message = await user_settings_channel.fetch_message(
        user_settings_message_id
    )

    await settings_message.edit(
        content=None,
        embed=None,
        attachments=[
            discord.File(
                SETTINGS_PANEL_PATH,
                filename="settings_panel.png",
            )
        ],
        view=ProfileSettingsLayout(),
    )


@client.event
async def on_message(message):
    """Award eligible members XP and update their level role."""
    if message.author.bot:
        return

    if message.guild is None:
        return

    cooldown_key = (
        message.guild.id,
        message.author.id,
    )

    current_time = time.monotonic()
    last_xp_time = xp_cooldowns.get(cooldown_key)

    if (
        last_xp_time is not None
        and current_time - last_xp_time
        < XP_COOLDOWN_SECONDS
    ):
        return

    xp_cooldowns[cooldown_key] = current_time

    xp_amount = random.randint(
        XP_MIN,
        XP_MAX,
    )

    total_xp, old_level, new_level = add_xp(
        message.author.id,
        xp_amount,
    )

    await sync_level_roles(
        message.author,
        new_level,
    )

    print(
        f"{message.author} earned {xp_amount} XP "
        f"and now has {total_xp} at level {new_level}."
    )

    if new_level > old_level:
        print(
            f"{message.author} reached level "
            f"{new_level} with {total_xp} XP."
        )


@client.event
async def on_member_join(member):
    """Generate and send a welcome card for a new member."""
    login_channel = client.get_channel(
        login_channel_id
    )

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
            file=discord.File(WELCOME_CARD_PATH),
        )


initialise_database()
client.run(token) 