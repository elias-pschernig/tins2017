import main

def game_init:
    pass

def game_tick:
    if land_closebutton(): land_quit()
    if land_key_pressed(LandKeyEscape): land_quit()

def game_draw:
    land_clear(0.5, 0.5, 0.5, 1)

def game_done:
    pass
