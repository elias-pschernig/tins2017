import common

def world_height(LandFloat x, y) -> LandFloat:
    double dx = x - 0
    double dy = y - 0
    double d = sqrt(dx * dx + dy * dy)
    double h = 80 - d / 5
    if h < 0: h = 0
    return h
