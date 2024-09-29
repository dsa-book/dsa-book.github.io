from manim import *
import requests
from IPython.display import HTML, display, clear_output, Image
import logging
import re
import io
import time

def start():
    logging.basicConfig(level=logging.INFO)
    log_capture_string = io.StringIO()
    ch = logging.StreamHandler(log_capture_string)
    ch.setLevel(logging.INFO)
    logger = logging.getLogger('manim')
    logger.addHandler(ch)
    return log_capture_string, ch, logger

def render_scene_with_quality(scene_class, quality_flag):
    log_capture_string, ch, logger = start()
    config.flush_cache = True
    config.pixel_height, config.pixel_width, config.frame_rate = q_dict[quality_flag]
    scene = scene_class()
    show(quality_flag, scene, log_capture_string)

q_dict = {'-ql': (480, 854, 15), '-qm': (720, 1280, 30), '-qh': (1080, 1920, 60), '-qk': (2160, 3840, 60)}

def show(quality_flag, sc, log_capture_string):
    config.flush_cache = True
    scene = sc
    scene.render()

    log_contents = log_capture_string.getvalue()
    file_path_match_video = re.search(r"File ready at '(.+?).mp4'", log_contents)
    file_path_match_image = re.search(r"File ready at '(.+?).png'", log_contents)

    if file_path_match_video:
        file_path = file_path_match_video.group(1) + '.mp4'
        display_video_or_image(file_path, is_video=True)
    elif file_path_match_image:
        file_path = file_path_match_image.group(1) + '.png'
        display_video_or_image(file_path, is_video=False)
    else:
        print("Could not find the file path in Manim's output.")

def display_video_or_image(file_path, is_video):
    clear_output(wait=True)
    if is_video:
        video_url = upload_file(file_path)
        if video_url:
            display(HTML(f"""
            <div style="width: 100%;">
              <video width="100%" controls>
                  <source src="{video_url}" type="video/mp4">
                  Your browser does not support the video tag.
              </video>
            </div>
            """))
    else:
        display(Image(filename=file_path))

def upload_file(file_path):
    with open(file_path, 'rb') as f:
        response = requests.post('https://transfer.adttemp.com.br/', files={'file': f})
        if response.status_code == 200:
            return response.text.strip()
    return None

# def show(quality_flag, sc, log_capture_string):
#     config.flush_cache = True
#     scene = sc
#     scene.render()

#     log_contents = log_capture_string.getvalue()
#     file_path_match = re.search(r"File ready at '(.+?)'", log_contents)

#     if file_path_match:
#         file_path = file_path_match.group(1)
#         print(f"Video saved to {file_path}")

#         def upload_file(file_path):
#             with open(file_path, 'rb') as f:
#                 response = requests.post('https://transfer.sh/', files={'file': f})
#                 if response.status_code == 200:
#                     return response.text.strip()
#             return None

#         video_url = upload_file(file_path)

#         clear_output(wait=True)

#         if video_url:
#             display(HTML(f"""
#             <div style="width: 100%;">
#               <video width="100%" controls>
#                   <source src="{video_url}" type="video/mp4">
#                   Your browser does not support the video tag.
#               </video>
#             </div>
#             """))
#     else:
#         print("Could not find the video file path in Manim's output.")

import os
import shutil
import logging
import io
import re
from IPython.display import HTML

# Assuming the rest of the provided code is unchanged, including the start() function and q_dict

# def render_local(scene_class, quality_flag):
#     log_capture_string, ch, logger = start()
#     config.flush_cache = True
#     config.pixel_height, config.pixel_width, config.frame_rate = q_dict[quality_flag]
#     scene = scene_class()
#     show_local(quality_flag, scene, log_capture_string)

# def show_local(quality_flag, sc, log_capture_string):
#     config.flush_cache = True
#     scene = sc
#     scene.render()

#     log_contents = log_capture_string.getvalue()
#     file_path_match = re.search(r"File ready at '(.+?)'", log_contents)

#     if file_path_match:
#         original_file_path = file_path_match.group(1)
#         videos_folder = '_static/videos'
#         if not os.path.exists(videos_folder):
#             os.makedirs(videos_folder)
#         timestamp = int(time.time())  # Getting current timestamp
#         base_file_name = os.path.basename(original_file_path)
#         # Modifying the filename to include the timestamp for uniqueness
#         unique_file_name = f"{os.path.splitext(base_file_name)[0]}_{timestamp}{os.path.splitext(base_file_name)[1]}"
#         local_file_path = os.path.join(videos_folder, unique_file_name)
#         shutil.copy(original_file_path, local_file_path)
        
#         # Updated to use the unique filename for video display
#         clear_output(wait=True)
#         display(HTML(f"""
#         <div style="width: 100%;">
#           <video width="100%" controls>
#               <source src="{local_file_path}" type="video/mp4">
#               Your browser does not support the video tag.
#           </video>
#         </div>
#         """))
#     else:
#         print("Could not find the video file path in Manim's output.")

def render_local(scene_class, quality_flag):
    log_capture_string, ch, logger = start()
    config.flush_cache = True
    config.pixel_height, config.pixel_width, config.frame_rate = q_dict[quality_flag]
    scene = scene_class()
    show_local(quality_flag, scene, log_capture_string)

def show_local(quality_flag, sc, log_capture_string):
    config.flush_cache = True
    scene = sc
    scene.render()

    log_contents = log_capture_string.getvalue()
    # print(log_contents)
    file_path_match_video = re.search(r"File ready at '(.+?).mp4'", log_contents)
    file_path_match_image = re.search(r"File ready at '(.+?).png'", log_contents)

    # Determine the most recent file type based on the log contents
    if file_path_match_video or file_path_match_image:
        if file_path_match_video and file_path_match_image:
            # If both types are found, determine the latest by their position in the log
            video_pos = log_contents.rfind(file_path_match_video.group(0))
            image_pos = log_contents.rfind(file_path_match_image.group(0))
            if video_pos > image_pos:
                display_file(file_path_match_video.group(1) + '.mp4')
            else:
                display_file(file_path_match_image.group(1) + '.png')
        elif file_path_match_video:
            display_file(file_path_match_video.group(1) + '.mp4')
        elif file_path_match_image:
            display_file(file_path_match_image.group(1) + '.png')
    else:
        print("Could not find the file path in Manim's output.")

def display_file(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    media_folder = '_static/media'
    if not os.path.exists(media_folder):
        os.makedirs(media_folder)
    timestamp = int(time.time())  # Getting current timestamp to avoid file name collision
    base_file_name = os.path.basename(file_path)
    unique_file_name = f"{os.path.splitext(base_file_name)[0]}_{timestamp}{file_extension}"
    local_file_path = os.path.join(media_folder, unique_file_name)
    shutil.copy(file_path, local_file_path)

    clear_output(wait=True)
    if file_extension == '.mp4':
        display(HTML(f"""
        <div style="width: 100%;">
          <video width="100%" controls>
              <source src="{local_file_path}" type="video/mp4">
              Your browser does not support the video tag.
          </video>
        </div>
        """))
    elif file_extension == '.png':
        display(Image(filename=local_file_path))
