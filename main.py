from PIL import Image
import noise
from time import time
from datetime import datetime

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y %H-%M-%S")

# Image Settings
IMAGE_WIDTH = 500
IMAGE_HEIGHT = 500

# Map size
MAP_WIDTH = 100
MAP_HEIGHT = 100

# Perlin noise settings
GRID_SIZE = 40
OCTAVES = 6
SEED = 24

# Height settings NB: Height goes from -1 to 1
MAX_OCEAN_HEIGHT = 0
MAX_BEACH_HEIGHT = 0.025
MAX_MEADOW_HEIGHT = 0.5
MAX_BAREGROUND_HEIGHT = 0.6
MAX_SNOWCAP_HEIGHT = 1

# Colour settings
OCEAN_COLOUR = (68, 97, 227)
MEADOW_COLOUR = (17, 133, 11)
SNOWCAP_COLOUR = (243, 247, 205)
BAREGROUND_COLOUR = (112, 72, 6)
BEACH_COLOUR = (252, 249, 141)

def get_colour(val: int):

  colour = (val + 1) * 150

  if val <= MAX_OCEAN_HEIGHT:
    red = (colour + OCEAN_COLOUR[0]) / 2
    green = (colour + OCEAN_COLOUR[1]) / 2
    blue = (colour + OCEAN_COLOUR[2]) / 2
  elif val <= MAX_BEACH_HEIGHT:
    red = (colour + BEACH_COLOUR[0]) / 2
    green = (colour + BEACH_COLOUR[1]) / 2
    blue = (colour + BEACH_COLOUR[2]) / 2
  elif val <= MAX_MEADOW_HEIGHT:
    red = (colour + MEADOW_COLOUR[0]) / 2
    green = (colour + MEADOW_COLOUR[1]) / 2
    blue = (colour + MEADOW_COLOUR[2]) / 2
  elif val <= MAX_BAREGROUND_HEIGHT:
    red = (colour + BAREGROUND_COLOUR[0]) / 2
    green = (colour + BAREGROUND_COLOUR[1]) / 2
    blue = (colour + BAREGROUND_COLOUR[2]) / 2
  elif val <= MAX_SNOWCAP_HEIGHT:
    red = (colour + SNOWCAP_COLOUR[0]) / 2
    green = (colour + SNOWCAP_COLOUR[1]) / 2
    blue = (colour + SNOWCAP_COLOUR[2]) / 2
    
  return int(red), int(green), int(blue)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def main() -> None:
  image = Image.new(
      "RGB", 
      (int(IMAGE_WIDTH), int(IMAGE_HEIGHT))
    )
  
  for a in range(image.width):
    for b in range(image.height):

      x = translate(a, 0, IMAGE_WIDTH, -MAP_WIDTH, MAP_WIDTH)
      y = translate(b, 0, IMAGE_HEIGHT, -MAP_HEIGHT, MAP_HEIGHT)

      val: float = 0.0
      freq: float = 1.0
      amp: float = 1.0

      for i in range(int(OCTAVES)):
        val += noise.perlin_noise2D((x + 30 * SEED) * freq / GRID_SIZE, (y + 30 * SEED) * freq / GRID_SIZE) * amp
        freq *= 2
        amp /= 2
      
      val *= 1.2

      if val > 1.0:
        val = 1
      elif val < -1.0:
        val = -1.0

      image.putpixel((a, b), get_colour(val))

  image.save(f".\Saves\{dt_string} S{SEED}O{OCTAVES}GS{GRID_SIZE}MW{MAP_WIDTH}MH{MAP_HEIGHT}.png")

if __name__ == "__main__":
  start = time()
  main()
  end = time()

  # Prints info about the image just produced
  print(
    f"{end - start} seconds to process, {(end - start) / 60} minutes",
    "Settings:",
    f"Image Height: {IMAGE_HEIGHT}",
    f"Image Width: {IMAGE_WIDTH}",
    f"Map Height: {MAP_HEIGHT}",
    f"Map Width: {MAP_WIDTH}",
    f"Grid Size: {GRID_SIZE}",
    f"Octaves: {OCTAVES}",
    f"Seed: {SEED}",
    f"Max Ocean Height: {MAX_OCEAN_HEIGHT}",
    f"Max Beach Height: {MAX_BEACH_HEIGHT}",
    f"Max Meadow Height: {MAX_MEADOW_HEIGHT}"
    f"Max Bareground Height: {MAX_BAREGROUND_HEIGHT}",
    f"Max Snowcap Height: {MAX_SNOWCAP_HEIGHT}",
    f"Ocean Colour: {OCEAN_COLOUR}",
    f"Meadow Colour: {MEADOW_COLOUR}",
    f"Bareground Colour: {BAREGROUND_COLOUR}",
    f"Snowcap Colour: {SNOWCAP_COLOUR}"
  )
