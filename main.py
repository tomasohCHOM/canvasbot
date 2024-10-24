import os
# IMPORT DISCORD
# IMPORT DISCORD.EXT COMMANDS
import asyncio
from canvasapi import Canvas
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CANVAS_TOKEN = os.getenv("CANVAS_TOKEN")

assert BOT_TOKEN is not None
assert CANVAS_TOKEN is not None

CANVAS_API_URL = "https://csufullerton.instructure.com/"

canvas = Canvas(CANVAS_API_URL, CANVAS_TOKEN)

# INTENTS DEAFULT

# COMMANDS.BOT command_prefix, intents, help_command


# Embed generator to format embed message outpt
def createMessageEmbed(title: str, description: str):
    embed = discord.Embed(
        title=title, description=description, color=discord.Color.blue()
    )
    return embed


# Function to get all Canvas courses associated with this user
def get_canvas_courses():
    global canvas
    user = canvas.get_current_user()
    course_list = []
    for course in user.get_courses(enrollment_state="active"):
        course_list.append(f"{course.name} ({course.id})")
    return "\n".join(course_list)


# Function to get all Canvas assignments given the course_id
def get_canvas_assignments(course_id):
    global canvas
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
            ephemeral=True,
        )
    except Exception as e:
        await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)


# Register the canvas-assignments slash command
@bot.tree.command(
    name="canvas-assignments", description="Get Canvas assignments for a course."
)
async def canvas_assignments():
    pass

# Set up bot statup event
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        # Sync the command tree to ensure slash commands are registered
        commandtree = await bot.tree.sync()
        print(f"Synced {len(commandtree)} application command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

async def main() -> None:
    # Run other async tasks
    # USE ASYNC TASK GROUPS TO DO MULTIPLE TASKS AT A SINGLE TIME FOR EASY PARALLEL PROCESSING
    # https://docs.python.org/3/library/asyncio-task.html#task-groups

    # Start the bot
    try:
        async with bot:
            await bot.start(BOT_TOKEN)
    except:
        print('Invalid Token')
        exit(1)

asyncio.run(main())
