from math import sin, cos
import random

class Vector2D:
    x: float
    y: float

def random_vector(ix: int, iy: int) -> Vector2D:
    seed: int = hash(ix * iy & ix + iy)

    random.seed(seed)

    angle: float = random.randint(0, 6283) / 1000

    # Create the vector from the angle
    v = Vector2D()
    v.x = sin(angle)
    v.y = cos(angle)

    return v

def dot_gradient(ix: int, iy: int, x: float, y: float) -> float:
    gradient = random_vector(ix, iy)

    dx: float = x - float(ix)
    dy: float = y - float(iy)

    return dx * gradient.x + dy * gradient.y

def interpolate(a0: float, a1: float, w: float) -> float:
    return (a1 - a0) * (3.0 - w * 2.0) * w * w + a0

def perlin_noise(x: float, y: float) -> float:
    x0: int = int(x)
    y0: int = int(y)
    x1: int = x0 + 1
    y1: int = y0 + 1

    sx: float = x - float(x0)
    sy: float = y - float(y0)

    n0: float = dot_gradient(x0, y0, x, y)
    n1: float = dot_gradient(x1, y0, x, y)
    ix0: float = interpolate(n0, n1, sx)

    n0: float = dot_gradient(x0, y1, x, y)
    n1: float = dot_gradient(x1, y1, x, y)
    ix1: float = interpolate(n0, n1, sx)

    value: float = interpolate(ix0, ix1, sy)
    
    return value
