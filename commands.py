from typing import Final
import os
from dotenv import load_dotenv
from discord import Interaction, Object, app_commands, ButtonStyle, Interaction, ui
from responses import get_response  
import obs_actions
from obs_list import streamer_links, streamer_promos

#Determines server on which bot will run
load_dotenv()
GUILD: Final[Object] = Object(id=int(os.getenv('GUILD')))

#Create Button Menu for confirmation of action
async def create_button_menu(interaction: Interaction, message: str, confirm_action, cancel_action) -> None:
    # Create buttons
    green_button = ui.Button(label="Confirm", style=ButtonStyle.green)
    red_button = ui.Button(label="Cancel", style=ButtonStyle.red)

    # Create a view to hold the buttons
    view = ui.View()
    view.add_item(green_button)
    view.add_item(red_button)

    # Send a message with the buttons
    await interaction.response.send_message(message, view=view, ephemeral=True)

    # Enable confirmation and cancelation
    async def confirm_callback(interaction: Interaction):
        await confirm_action(interaction)
    async def cancel_callback(interaction: Interaction):
        await cancel_action(interaction)

    # Assign the callbacks to the buttons
    green_button.callback = confirm_callback
    red_button.callback = cancel_callback

async def slash_commands(tree) -> None:
    @tree.command(name="about", description="Get more info on the bot", guild=GUILD)
    async def about(interaction: Interaction):
        resp = get_response('help')
        await interaction.response.send_message(resp) 

    #Stream adjustments
    @tree.command(name="switch_scene", description="Switch the Preview Scene to Live", guild=GUILD)
    async def switchscene(interaction: Interaction):
        async def confirm_action(interaction: Interaction):
            old_scene, new_scene = obs_actions.switch_scene()
            await interaction.response.send_message(f"Live scene switched from {old_scene} to {new_scene}")
        async def cancel_action(interaction: Interaction):
            await interaction.response.send_message("Command canceled.", ephemeral=True)

        program, preview = obs_actions.status()[:2]
        await create_button_menu(interaction, f'Do you want to replace {program} with {preview} on the stream?', confirm_action, cancel_action)
    
    @tree.command(name="start_stream", description="Start the Stream", guild=GUILD)
    async def startstream(interaction: Interaction):
        async def confirm_action(interaction: Interaction):
            obs_resp = obs_actions.start_stream()
            await interaction.response.send_message(obs_resp)
        async def cancel_action(interaction: Interaction):
            await interaction.response.send_message("Command canceled.", ephemeral=True)
            
        await create_button_menu(interaction, "Do you want to start the stream?", confirm_action, cancel_action)
    
    @tree.command(name="stop_stream", description="Stop the Stream", guild=GUILD)
    async def stopstream(interaction: Interaction):
        async def confirm_action(interaction: Interaction):
            obs_resp = obs_actions.stop_stream()
            await interaction.response.send_message(obs_resp)
        async def cancel_action(interaction: Interaction):
            await interaction.response.send_message("Command canceled.", ephemeral=True)

        await create_button_menu(interaction, "Do you want to stop the stream?", confirm_action, cancel_action)

    #OBS Source Customization    
    @tree.command(name="set_stream_a", description="Choose Streamer of Upcoming Slot", guild=GUILD)
    @app_commands.choices(stream_links = streamer_links)
    @app_commands.describe(stream_links ='Choose a Streamer')
    async def setstreama(interaction: Interaction, stream_links: app_commands.Choice[str]):
        success = obs_actions.set_stream_a(stream_links.value)
        if success:
            await interaction.response.send_message(f"You setup {stream_links.value} for Stream A")
        elif not success:
            await interaction.response.send_message(f"You can't change Stream A, as it is Active!")
       
    @tree.command(name="set_stream_b", description="Choose Streamer of Upcoming Slot", guild=GUILD)
    @app_commands.choices(stream_links = streamer_links)
    @app_commands.describe(stream_links ='Choose a Streamer')
    async def setstreamb(interaction: Interaction, stream_links: app_commands.Choice[str]):
        success = obs_actions.set_stream_b(stream_links.value)
        if success:
            await interaction.response.send_message(f"You setup {stream_links.value} for Stream B")
        elif not success:
            await interaction.response.send_message(f"You can't change Stream B, as it is Active!")
    
    @tree.command(name="set_manual_a", description="Enter YouTube URL for Stream A", guild=GUILD)
    async def setmanuala(interaction: Interaction, user_message: str):
        async def confirm_action(interaction: Interaction):
            obs_actions.set_stream_a(user_message)
            await interaction.response.send_message(f"You setup {user_message} for Stream A")
        async def cancel_action(interaction: Interaction):
            await interaction.response.send_message("Command canceled.", ephemeral=True)

        await create_button_menu(interaction, f'Do you want to load {user_message} to Stream A?', confirm_action, cancel_action)
    
    @tree.command(name="set_manual_b", description="Enter YouTube URL for Stream B", guild=GUILD)
    async def setmanualb(interaction: Interaction, user_message: str):
        async def confirm_action(interaction: Interaction):
            obs_actions.set_stream_b(user_message)
            await interaction.response.send_message(f"You setup {user_message} for Stream B")
        async def cancel_action(interaction: Interaction):
            await interaction.response.send_message("Command canceled.", ephemeral=True)

        await create_button_menu(interaction, f'Do you want to load {user_message} to Stream B?', confirm_action, cancel_action)
    
    @tree.command(name="set_promo_streamer", description="Choose Streamer Promo Video", guild=GUILD)
    @app_commands.choices(stream_promos = streamer_promos)
    @app_commands.describe(stream_promos ='Choose a Streamer')
    async def setpromostreamer(interaction: Interaction, stream_promos: app_commands.Choice[str]):
        obs_actions.set_promo(stream_promos.value)
        await interaction.response.send_message(f"You setup {stream_promos.value} for the Streamer Promo")

    #Preview adjustments
    @tree.command(name="stream_a", description="Switch to Stream Feed A", guild=GUILD)
    async def streama(interaction: Interaction):
        old_scene, new_scene = obs_actions.feed_a()
        await interaction.response.send_message(f'OBS Switched from {old_scene} to {new_scene}')  

    @tree.command(name="stream_b", description="Switch to Stream Feed B", guild=GUILD)
    async def streamb(interaction: Interaction):
        old_scene, new_scene = obs_actions.feed_b()
        await interaction.response.send_message(f'OBS Switched from {old_scene} to {new_scene}')  

    @tree.command(name="promo_charity", description="Switch to Charity Promo Scene", guild=GUILD)
    async def promocharity(interaction: Interaction):
        old_scene, new_scene = obs_actions.promo_charity()
        await interaction.response.send_message(f'OBS Switched from {old_scene} to {new_scene}')  

    @tree.command(name="promo_aoe2", description="Switch to AoE2 Promo Scene", guild=GUILD)
    async def promoaoe2(interaction: Interaction):
        old_scene, new_scene = obs_actions.promo_aoe2()
        await interaction.response.send_message(f'OBS Switched from {old_scene} to {new_scene}')  

    @tree.command(name="promo_rocket_league", description="Switch to Rocket League Promo Scene", guild=GUILD)
    async def promorl(interaction: Interaction):
        old_scene, new_scene = obs_actions.promo_rl()
        await interaction.response.send_message(f'OBS Switched from {old_scene} to {new_scene}')  

    @tree.command(name="promo_finals", description="Switch to Finals Promo Scene", guild=GUILD)
    async def promofinals(interaction: Interaction):
        old_scene, new_scene = obs_actions.promo_finals()
        await interaction.response.send_message(f'OBS Switched from {old_scene} to {new_scene}')  

    @tree.command(name="promo_streamer", description="Switch to Streamer Promo Scene", guild=GUILD)
    async def promostreamer(interaction: Interaction):
        old_scene, new_scene = obs_actions.promo_streamer()
        await interaction.response.send_message(f'OBS Switched from {old_scene} to {new_scene}')    

    #Sync the commands to the Server
    try:
        synced_commands: list = await tree.sync(guild=GUILD)
        print(f'Synced {len(synced_commands)} commands')
    except Exception as e:
        print(f'Syncing commands error: {e}')

    
