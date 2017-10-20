import main
import mesh

class Game:
    Mesh *ball

Game *game

def game_init:
    land_alloc(game)
    game.ball = mesh_make("ball", land_4x4_matrix_scale(20, 20, 20))

def game_tick:
    if land_closebutton(): land_quit()
    if land_key_pressed(LandKeyEscape): land_quit()

def game_draw:
    float w = land_display_width()
    float h = land_display_height()
    land_clear(0.5, 0.5, 0.5, 1)

    Land4x4Matrix m = land_4x4_matrix_orthographic(-1, -1, 100,
           1, 1, -100)
    m = land_4x4_matrix_mul(m, land_4x4_matrix_translate(w / 2, h / 2, 0))
    land_display_transform_4x4(&m)
    mesh_draw(game.ball)

def game_done:
    pass
