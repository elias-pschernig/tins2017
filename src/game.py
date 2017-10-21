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

    trees_make(game.trees, "hill", 0, 0, 0)

    for int i in range(50):
        float x = land_rnd(-300, 300)
        float y = land_rnd(-200, 200)
        trees_make(game.trees, "oak", x, y, world_height(x, y))

def game_tick:
    if land_closebutton(): land_quit()
    if land_key_pressed(LandKeyEscape): land_quit()

def _letterbox(float *w, *h):
    float tw = land_display_width()
    float th = land_display_height()
    float hscale = 16 * 60 / tw
    *w = tw * hscale
    *h = th * hscale
    if *w / *h > 16.0 / 9:
        float vscale = 9 * 60 / th
        *w = tw * vscale
        *h = th * vscale

def game_draw:
    float w, h
    _letterbox(&w, &h)

    land_clear(0.5, 0.5, 0.5, 1)
    land_clear_depth(1)
    land_render_state(LAND_DEPTH_TEST, True)

    land_projection(land_4x4_matrix_mul(
        land_4x4_matrix_orthographic(-w / 2, -h / 2, 1000, w / 2, h / 2, -1000),
        land_4x4_matrix_rotate(1, 0, 0, pi / -3.3)))

    trees_draw(game.trees)

def game_done:
    pass
