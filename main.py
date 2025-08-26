import discord
import os
from discord import app_commands
from discord.ext import commands


WEBHOOK_URL = os.environ["WEBHOOK_URL"]
TOKEN = os.environ["DISCORD_BOT_TOKEN"]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

class StandupModal(discord.ui.Modal, title="Daily Standup"):

    yesterday = discord.ui.TextInput(
        label="What did you do yesterday?",
        style=discord.TextStyle.paragraph,
        placeholder="Enter your response...",
        required=True,
    )
    today = discord.ui.TextInput(
        label="What will you do today?",
        style=discord.TextStyle.paragraph,
        placeholder="Enter your response...",
        required=True,
    )
    blockers = discord.ui.TextInput(
        label="Any blockers?",
        style=discord.TextStyle.paragraph,
        placeholder="Enter blockers (if any)...",
        required=False,
    )

    async def on_submit(self, interaction: discord.Interaction):
        webhook = discord.SyncWebhook.from_url(WEBHOOK_URL)

        embed = discord.Embed(
            title=f"Standup Report from {interaction.user.display_name}",
            color=discord.Color.blue(),
        )
        embed.add_field(name="✅ Yesterday", value=self.yesterday.value, inline=False)
        embed.add_field(name="📝 Today", value=self.today.value, inline=False)
        embed.add_field(name="🚧 Blockers", value=self.blockers.value or "None", inline=False)

        webhook.send(embed=embed, username=interaction.user.display_name, avatar_url=interaction.user.display_avatar.url)
        await interaction.response.send_message("✅ Your standup has been submitted!", ephemeral=True)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.tree.command(name="standup", description="Fill out your daily standup")
async def standup(interaction: discord.Interaction):
    await interaction.response.send_modal(StandupModal())


bot.run(TOKEN)

