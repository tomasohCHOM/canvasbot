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

CANVAS_API_URL = "https://canvas.instructure.com"


# Embed generator to format embed message outpt
def createMessageEmbed(title: str, description: str):
    embed = discord.Embed(
        title=title, description=description, color=discord.Color.blue()
    )
    return embed


# Function to get all Canvas courses associated with this user
def get_canvas_courses():
    canvas = Canvas(CANVAS_API_URL, CANVAS_TOKEN)
    user = canvas.get_current_user()
    course_list = []
    for course in user.get_courses(enrollment_state="active"):
        course_list.append(f"{course.name} ({course.id})")
    return "\n".join(course_list)


# Function to get all Canvas assignments given the course_id
def get_canvas_assignments(course_id):
    canvas = Canvas(CANVAS_API_URL, CANVAS_TOKEN)
    course = canvas.get_course(course_id)
    assignments = []
    for assignment in course.get_assignments():
        assignments.append(f"{assignment} DUE AT - {assignment.due_at}")
    return "\n".join(assignments)


# Register the canvas-courses slash command
@bot.tree.command(
    name="canvas-courses", description="Get Canvas courses from this user."
)
async def canvas_courses(interaction: discord.Interaction):
    try:
        courses = get_canvas_courses()
        await interaction.response.send_message(
            embed=createMessageEmbed(
                title="Available Canvas Courses", description=courses
            ),
        )
    except Exception as e:
        await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)


# Register the canvas-assignments slash command
@bot.tree.command(
    name="canvas-assignments", description="Get Canvas assignments for a course."
)
async def canvas_assignments(interaction: discord.Interaction, course_id: int):
    try:
        assignments = get_canvas_assignments(course_id)
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
