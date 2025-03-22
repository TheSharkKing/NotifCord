import discord

def setup(bot):
    @bot.tree.command(name="ping", description="Replies with Pong!")
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")
