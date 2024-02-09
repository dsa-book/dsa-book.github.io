from manim import *
import requests
from IPython.display import HTML, display, clear_output
import logging
import re
import io

def start():
  # Setup logging to capture Manim's output
  logging.basicConfig(level=logging.INFO)
  log_capture_string = io.StringIO()
  ch = logging.StreamHandler(log_capture_string)
  ch.setLevel(logging.INFO)

  # Get Manim's logger and add the custom handler
  logger = logging.getLogger('manim')
  logger.addHandler(ch)
  return log_capture_string, ch, logger

def set_res(quality_flag):
  if quality_flag == "-ql":
    config.pixel_height = 480
    config.pixel_width = 854
    config.frame_rate = 15
  elif quality_flag == "-qm":
    config.pixel_height = 720
    config.pixel_width = 1280
    config.frame_rate = 30
  elif quality_flag == "-qh":
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 60
  elif quality_flag == "-qk":
    config.pixel_height = 2160
    config.pixel_width = 3840
    config.frame_rate = 60

def show(quality_flag, sc):
  # Set quality based on the flag

  # Render the scene
  config.flush_cache = True
  scene = sc
  scene.render()

  # Extract the log contents and find the file path
  log_contents = log_capture_string.getvalue()
  file_path_match = re.search(r"File ready at '(.+?)'", log_contents)

  if file_path_match:
      file_path = file_path_match.group(1)
      print(f"Video saved to {file_path}")

      def upload_file(file_path):
          with open(file_path, 'rb') as f:
              response = requests.post('https://transfer.sh/', files={'file': f})
              if response.status_code == 200:
                  return response.text.strip()
          return None

      video_url = upload_file(file_path)

      clear_output(wait=True)

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
      print("Could not find the video file path in Manim's output.")

