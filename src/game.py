import main
import mesh
import trees

class Game:
    Trees *trees

Game *game

def game_init:
    land_display_title("Dr. Forest")
    
    land_alloc(game)
    game.trees = trees_new()

    for int i in range(50):
        trees_make(game.trees, "oak", land_rnd(-300, 300), land_rnd(-200, 200))

def game_tick:
    if land_closebutton(): land_quit()
    if land_key_pressed(LandKeyEscape): land_quit()

def game_draw:
    float w = land_display_width()
    float h = land_display_height()
    land_clear(0.5, 0.5, 0.5, 1)

    land_projection(land_4x4_matrix_mul(
        land_4x4_matrix_orthographic(-w / 2, -h / 2, 1000, w / 2, h / 2, -1000),
        land_4x4_matrix_rotate(1, 0, 0, pi / 4)))

    trees_draw(game.trees)

def game_done:
    pass
