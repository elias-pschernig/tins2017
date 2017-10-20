import land.land

macro pi LAND_PI

def print(char const *s, ...):
    va_list args
    va_start(args, s)
    vprintf(s, args)
    va_end(args)
    printf("\n")
