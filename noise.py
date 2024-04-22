from dataclasses import dataclass
from math import sin, cos
from sys import getsizeof

@dataclass
class Vector2D:
    x: float
    y: float

'''
 const unsigned w = 8 * sizeof(unsigned);
    const unsigned s = w / 2; 
    unsigned a = ix, b = iy;
    a *= 3284157443;
 
    b ^= a << s | a >> w - s;
    b *= 1911520717;
 
    a ^= b << s | b >> w - s;
    a *= 2048419325;
    float random = a * (3.14159265 / ~(~0u >> 1)); // in [0, 2*Pi]
    
    // Create the vector from the angle
    vector2 v;
    v.x = sin(random);
    v.y = cos(random);
 
    return v;
'''

def random_gradient(ix: int, iy: int) -> Vector2D:
    W: int = 8 * getsizeof(float)
    S: int = W / 2

def dot_grid_gradient(ix: int, iy: int, x: float, y: float) -> float:
    gradient: Vector2D = random_gradient(ix, iy)

def perlin_noise(x, y) -> float:

    # Grid cell co-ordinates
    x0: int = int(x)
    y0: int = int(y)
    y1: int = y0 + 1
    x1: int = x0 + 1

    # Interpolation weights
    sx: float = x - float(x0)
    sy: float = y - float(y0)

    