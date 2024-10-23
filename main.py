import discord
from canvasapi import Canvas
from os import getenv
from dotenv import load_dotenv


CANVAS_API_URL = "https://csufullerton.instructure.com"

def get_canvas_assignments():
    canvas = Canvas(CANVAS_API_URL, getenv("CANVAS_TOKEN"))
    course = canvas.get_course(1)
    assignments = []
    for assignment in course.get_assignments():
        assignments.append(f"{assignment} DUE AT - {assignment.due_at}")
    return "\n".join(assignments)

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
token = getenv("BOT_TOKEN")

if __name__ == "__main__":
    if token:
        client.run(token)
