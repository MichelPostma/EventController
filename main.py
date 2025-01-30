from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, app_commands
from responses import get_response
from commands import slash_commands

# Load Token from env file
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Setup bot with intents
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)
tree = app_commands.CommandTree(client)

# Report when bot is ready
@client.event
async def on_ready() -> None:
    print(f'{client.user} is running!')
    await slash_commands(tree)

# Message functionality with Coroutine expression, returns None as it only executes code
async def send_message(message: Message, user_message: str) -> None: 
    if not user_message:
        print('Message was empty')
    try:
        response: str = get_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        print(e)

# Handling incoming messages
@client.event
async def on_message(message: Message) -> None:
    # Prevent bot from responding to itself
    if message.author == client.user:
        return
    
    # Get user credentials
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel} {username}: {user_message}]')
    print(message.author)
    await send_message(message, user_message)

# Run the bot if it's being executed directly
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
