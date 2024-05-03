from functools import wraps
from PIL import Image
from time import time
from datetime import datetime
import os
import noise
import threading

# Image Settings
IMAGE_WIDTH = 1000
IMAGE_HEIGHT = 1000

# Map size
MAP_WIDTH = 100
MAP_HEIGHT = 100

# Perlin noise settings
GRID_SIZE = 40
OCTAVES = 3
SEED = 801

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

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
os.mkdir(f".\saves\{dt_string}")

settings = [
    "Settings:\n",
    f"Image Height: {IMAGE_HEIGHT}\n",
    f"Image Width: {IMAGE_WIDTH}\n",
    f"Map Height: {MAP_HEIGHT}\n",
    f"Map Width: {MAP_WIDTH}\n",
    f"Grid Size: {GRID_SIZE}\n",
    f"Octaves: {OCTAVES}\n",
    f"Seed: {SEED}\n",
    f"Max Ocean Height: {MAX_OCEAN_HEIGHT}\n",
    f"Max Beach Height: {MAX_BEACH_HEIGHT}\n",
    f"Max Meadow Height: {MAX_MEADOW_HEIGHT}\n"
    f"Max Bareground Height: {MAX_BAREGROUND_HEIGHT}\n",
    f"Max Snowcap Height: {MAX_SNOWCAP_HEIGHT}\n",
    f"Ocean Colour: {OCEAN_COLOUR}\n",
    f"Meadow Colour: {MEADOW_COLOUR}\n",
    f"Bareground Colour: {BAREGROUND_COLOUR}\n",
    f"Snowcap Colour: {SNOWCAP_COLOUR}\n"
]

# Creation of files
image = Image.new(
    "RGB", 
    (int(IMAGE_WIDTH), int(IMAGE_HEIGHT))
  )

heightmap = Image.new(
  "RGB",
  (int(IMAGE_WIDTH), int(IMAGE_HEIGHT))
)

with open(f".\saves\{dt_string}\Settings.txt", "x") as f:
  for setting in settings:
    f.write(setting)
  f.close()

def memoize(func):
  cache = {}

  @wraps(func)
  def wrapper(*args, **kwargs):
    key = str(args) + str(kwargs)
    if key not in cache:
      cache[key] = func(*args, **kwargs)
    return cache[key]
  return wrapper

@memoize
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

@memoize
def cal(a):
        return int((IMAGE_WIDTH / 20) * a)

@memoize
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

@memoize
def main(xs, xe, ys, ye) -> None:
  for a in range(xs, xe):
    for b in range(ys, ye):

      x = translate(a, 0, IMAGE_WIDTH, -MAP_WIDTH, MAP_WIDTH)
      y = translate(b, 0, IMAGE_HEIGHT, -MAP_HEIGHT, MAP_HEIGHT)

      val: float = 0.0
      freq: float = 1.0
      amp: float = 1.0

      for i in range(int(OCTAVES)):
        val += noise.perlin_noise(
          (x + 30 * SEED) * freq / GRID_SIZE, (y + 30 * SEED) * freq / GRID_SIZE
          ) * amp
        
        freq *= 2
        amp /= 2
      
      val *= 1.2

      if val > 1.0:
        val = 1
      elif val < -1.0:
        val = -1.0

      heightmap_val = int((val + 1) * 125)
      image.putpixel((a, b), get_colour(val))
      heightmap.putpixel((a, b), (heightmap_val, heightmap_val, heightmap_val))

  image.save(f".\saves\{dt_string}\ Map.png")
  heightmap.save(f".\saves\{dt_string}\ Heightmap.png")

if __name__ == "__main__":
  start = time()
  t1 = threading.Thread(target=main, args=(0, image.height, cal(0), cal(1)))
  t2 = threading.Thread(target=main, args=(0, image.height, cal(1), cal(2)))
  t3 = threading.Thread(target=main, args=(0, image.height, cal(2), cal(3)))
  t4 = threading.Thread(target=main, args=(0, image.height, cal(3), cal(4)))
  t5 = threading.Thread(target=main, args=(0, image.height, cal(4), cal(5)))
  t6 = threading.Thread(target=main, args=(0, image.height, cal(5), cal(6)))
  t7 = threading.Thread(target=main, args=(0, image.height, cal(6), cal(7)))
  t8 = threading.Thread(target=main, args=(0, image.height, cal(7), cal(8)))
  t9 = threading.Thread(target=main, args=(0, image.height, cal(8), cal(9)))
  t10 = threading.Thread(target=main, args=(0, image.height, cal(9), cal(10)))
  t11 = threading.Thread(target=main, args=(0, image.height, cal(10), cal(11)))
  t12 = threading.Thread(target=main, args=(0, image.height, cal(11), cal(12)))
  t13 = threading.Thread(target=main, args=(0, image.height, cal(12), cal(13)))
  t14 = threading.Thread(target=main, args=(0, image.height, cal(13), cal(14)))
  t15 = threading.Thread(target=main, args=(0, image.height, cal(14), cal(15)))
  t16 = threading.Thread(target=main, args=(0, image.height, cal(15), cal(16)))
  t17 = threading.Thread(target=main, args=(0, image.height, cal(16), cal(17)))
  t18 = threading.Thread(target=main, args=(0, image.height, cal(17), cal(18)))
  t19 = threading.Thread(target=main, args=(0, image.height, cal(18), cal(19)))
  t20 = threading.Thread(target=main, args=(0, image.height, cal(19), cal(20)))
  t1.start()
  t2.start()
  t3.start()
  t4.start()
  t5.start()
  t6.start()
  t7.start()
  t8.start()
  t9.start()
  t10.start()
  t11.start()
  t12.start()
  t13.start()
  t14.start()
  t15.start()
  t16.start()
  t17.start()
  t18.start()
  t19.start()
  t20.start()
  t1.join()
  t2.join()
  t3.join()
  t4.join()
  t5.join()
  t6.join()
  t7.join()
  t8.join()
  t9.join()
  t10.join()
  t11.join()
  t12.join()
  t13.join()
  t14.join()
  t15.join()
  t16.join()
  t17.join()
  t18.join()
  t19.join()
  t20.join()
  end = time()
  print(
      f"{round(end - start, 2)} seconds to process, {round((end - start) / 60, 2)} minutes"
  )
