import common
static import game

def init:
    game_init()

def tick:
    game_tick()

def draw:
    game_draw()

def done:
    game_done()

def realmain():
    land_init()
    land_set_display_parameters(16 * 60, 9 * 60, LAND_WINDOWED | LAND_OPENGL)
    land_callbacks(init, tick, draw, done)
    land_mainloop()

land_use_main(realmain)
