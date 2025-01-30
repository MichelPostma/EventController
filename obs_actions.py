from typing import Final
import os
from dotenv import load_dotenv
import obsws_python as obs

#Load connection info for OBS Websockets
load_dotenv()
OBS_IP: Final[str] = str(os.getenv('SERVER_IP'))
OBS_PORT: Final[int] = int(os.getenv('SERVER_PORT'))
OBS_PASS: Final[str] = str(os.getenv('SERVER_PASS')) 

#Connect to OBS
try:
        obsstudio = obs.ReqClient(host=OBS_IP, port=4455, password=OBS_PASS)
        print('Connected to OBS Websocket')
except Exception as e:
        print(f'OBS Websocket Connection failed: {e}')

#Stream adjustments
def switch_scene() -> tuple[str,str]:
    old_scene = obsstudio.get_current_preview_scene().scene_name
    obsstudio.trigger_studio_mode_transition()
    new_scene = obsstudio.get_current_preview_scene().scene_name
    return old_scene,new_scene

def start_stream() -> str:
    if obsstudio.get_stream_status().output_active:
        obsstudio.start_stream()
        return('Stream has started')
    else:
        return('Stream is already running')

def stop_stream() -> str:
    if obsstudio.get_stream_status().output_active:
        obsstudio.stop_stream()
        return('Stream has stopped')
    else:
        return('Stream is already stopped')
    
#OBS Source Customization 
def set_stream_a(url) -> bytes:
    if status()[0] != ('Stream Feed A'):
        source_settings = obsstudio.get_input_settings('Stream A').input_settings
        source_settings['playlist'][0]['value'] = url
        obsstudio.set_input_settings('Stream A', source_settings, True)
        return True
    else:
        return False

def set_stream_b(url) -> bytes:
    if status()[0] != ('Stream Feed B'):
        source_settings = obsstudio.get_input_settings('Stream B').input_settings
        source_settings['playlist'][0]['value'] = url
        obsstudio.set_input_settings('Stream B', source_settings, True)
        return True
    else:
        return False

def set_promo(path) -> None:
    source_settings = obsstudio.get_input_settings('Streamer Promo Video').input_settings
    source_settings['playlist'][0]['value'] = path
    obsstudio.set_input_settings('Streamer Promo Video', source_settings, True)
    return

#Preview adjustments
def feed_a() -> tuple[str,str]:
    old_scene = obsstudio.get_current_preview_scene().scene_name
    obsstudio.set_current_preview_scene('Stream Feed A')
    new_scene = obsstudio.get_current_preview_scene().scene_name
    return old_scene, new_scene

def feed_b() -> tuple[str,str]:
    old_scene = obsstudio.get_current_preview_scene().scene_name
    obsstudio.set_current_preview_scene('Stream Feed B')
    new_scene = obsstudio.get_current_preview_scene().scene_name
    return old_scene, new_scene

def promo_charity() -> tuple[str,str]:
    old_scene = obsstudio.get_current_preview_scene().scene_name
    obsstudio.set_current_preview_scene('Promo Charity')
    new_scene = obsstudio.get_current_preview_scene().scene_name
    return old_scene, new_scene

def promo_aoe2() -> tuple[str,str]:
    old_scene = obsstudio.get_current_preview_scene().scene_name
    obsstudio.set_current_preview_scene('Promo Game AoE2')
    new_scene = obsstudio.get_current_preview_scene().scene_name
    return old_scene, new_scene

def promo_rl() -> tuple[str,str]:
    old_scene = obsstudio.get_current_preview_scene().scene_name
    obsstudio.set_current_preview_scene('Promo Game Rocket League')
    new_scene = obsstudio.get_current_preview_scene().scene_name
    return old_scene, new_scene

def promo_finals() -> tuple[str,str]:
    old_scene = obsstudio.get_current_preview_scene().scene_name
    obsstudio.set_current_preview_scene('Promo Game The Finals')
    new_scene = obsstudio.get_current_preview_scene().scene_name
    return old_scene, new_scene

def promo_streamer() -> tuple[str,str]:
    old_scene = obsstudio.get_current_preview_scene().scene_name
    obsstudio.set_current_preview_scene('Promo Streamer')
    new_scene = obsstudio.get_current_preview_scene().scene_name
    return old_scene, new_scene

#OBS Status Request
def status() -> tuple[str, str, bytes, float, int, int]:
    current_program_scene = obsstudio.get_current_program_scene().scene_name
    current_preview_scene = obsstudio.get_current_preview_scene().scene_name
    stats = obsstudio.get_stream_status()
    active = stats.output_active
    congestion = stats.output_congestion
    skip_frame = stats.output_skipped_frames
    tot_frame = stats.output_total_frames
    return current_program_scene, current_preview_scene, active, congestion, skip_frame, tot_frame

