import os
import discord
from discord.ext import commands
from canvasapi import Canvas
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CANVAS_TOKEN = os.getenv("CANVAS_TOKEN")


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="^", intents=intents, help_command=None)

CANVAS_API_URL = "https://csufullerton.instructure.com"


def get_canvas_assignments(class_id):
    canvas = Canvas(CANVAS_API_URL, CANVAS_TOKEN)
    course = canvas.get_course(class_id)
    assignments = []
    for assignment in course.get_assignments():
        assignments.append(f"{assignment} DUE AT - {assignment.due_at}")
    return "\n".join(assignments)


# Embed generator to format embed message outpt
def createMessageEmbed(title: str, description: str):
    embed = discord.Embed(
        title=title, description=description, color=discord.Color.blue()
    )
    return embed


# Register the canvas-assignments slash command
@bot.tree.command(
    name="canvas-assignments", description="Get Canvas assignments for a course."
)
async def canvas_assignments(interaction: discord.Interaction, class_id: int):
    try:
        assignments = get_canvas_assignments(class_id)
        await interaction.response.send_message(
            embed=createMessageEmbed(
                title="Canvas Assignments", description=assignments
            )
        )
    except Exception as e:
        await interaction.response.send_message(f"Error: str({e})", ephemeral=True)


# Set up bot statup event
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        # Sync the command tree to ensure slash commands are registered
        await bot.tree.sync()
        print("Slash commands synced.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


if __name__ == "__main__":
    if not BOT_TOKEN:
        print("No Token Found")
        exit(1)
    bot.run(BOT_TOKEN)
