import main
import mesh
import trees
import world
import levels

class Game:
    Trees *trees
    float camera_angle
    World *world
    int tool
    bool paused

    float lx, ly

global Game *game

bool flag
def _set_flag(Trees *trees, Tree *tree, float dx, dy):
    flag = True

def game_init:
    land_display_title("Dr. Forest")
    
    land_alloc(game)
    game.trees = trees_new()
    game.camera_angle = pi / -3.3
    game.world = world_new()

    levels_start(1)

def _draw(float mx, my) -> bool:
    float dx = mx - game.lx
    float dy = my - game.ly
    if dx * dx + dy * dy > 10:
        game.lx = mx
        game.ly = my
        return True
    return False

def place_tree_rising(float x, y, str kind, bool rising) -> Tree*:
    flag = False
    trees_callback(game.trees, x, y, 30, _set_flag)
    if flag: return None
    float z = rising ? -99 : world_get_altitude(game.world, x, y)
    Tree *tree = trees_make(game.trees, kind, x, y, z)
    world_blotch(game.world, x, y, 40, land_color_rgba(0.3, 0.1, 0, 1))
    tree.rising = rising
    return tree

def place_tree(float x, y, str kind) -> Tree*:
    return place_tree_rising(x, y, kind, False)

def game_tick:
    float dw = land_display_width()
    float dh = land_display_height()
    float w, h
    _letterbox(&w, &h)

    if land_closebutton(): land_quit()
    if land_key_pressed(LandKeyEscape): land_quit()

    float mx = (land_mouse_x() - dw / 2) * w / dw
    float my = (dh / 2 - land_mouse_y()) * h / dh

    LandVector t
    if True:
        LandVector v = land_vector(mx, my, 0)
        LandVector p = land_vector(0, 0, 0)
        LandVector x = land_vector(1, 0, 0)
        LandVector y = land_vector(0, 1, 0)
        LandVector z = land_vector(0, 0, 1)
        Land4x4Matrix rot = land_4x4_matrix_rotate(1, 0, 0, game.camera_angle)
        x = land_vector_matmul(x, &rot)
        y = land_vector_matmul(y, &rot)
        z = land_vector_matmul(z, &rot)
        t = land_vector_backtransform(v, p, x, y, z)

        LandFloat e = -t.z / z.z
        t.x += z.x * e
        t.y += z.y * e
        t.z = world_get_altitude(game.world, t.x, t.y)

        LandVector t_ = land_vector_transform(t, p, x, y, z)
        t_.z = 0
        float d = land_vector_norm(land_vector_sub(v, t_))
       
        LandVector t2 = t
        for int i in range(100):
            LandVector t2_ = land_vector_transform(t2, p, x, y, z)
            t2_.z = 0
            float d2 = land_vector_norm(land_vector_sub(v, t2_))
            if d2 > d: break
            d = d2
            t = t2
            t2.y -= 10
            t2.z = -world_get_altitude(game.world, t2.x, t2.y) # why -??

    if land_mouse_button_clicked(0):
        if mx < -420:
            game.tool = (h / 2 - my) / 60
            if game.tool == 7:
                game.paused = not game.paused

    if game.paused:
        trees_dance(game.trees)
        return

    if land_mouse_button(0):
        if mx < -420:
            pass
        elif game.tool == 1:
            if _draw(mx, my):
                world_blotch(game.world, t.x, t.y, 50, land_color_rgba(1, 0.8, 0.6, 1))
                trees_callback(game.trees, t.x, t.y, 60, tree_whirl)
        elif game.tool == 0:
            if _draw(mx, my):
                world_patch(game.world, t.x, t.y, 50, land_color_rgba(0.2, 0.2, 0.8, 1))
                trees_callback(game.trees, t.x, t.y, 50, tree_sink)
        elif game.tool == 2:
            if _draw(mx, my):
                trees_callback(game.trees, t.x, t.y, 60, tree_burn)
                world_blotch(game.world, t.x, t.y, 40, land_color_rgba(0, 0, 0, 1))
        elif game.tool == 3:
            if _draw(mx, my):
                place_tree_rising(t.x, t.y, "oak", True)

    trees_tick(game.trees)

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
        land_4x4_matrix_rotate(1, 0, 0, game.camera_angle)))

    if game.paused:
        float a = land_get_ticks() % 60
        a = a * 2 * pi / 60
        mesh_draw(game.world.mesh, land_4x4_matrix_translate(
            cos(a) * 10, sin(a) * 10, 0))
    else:
        mesh_draw(game.world.mesh, land_4x4_matrix_translate(0, 0, 0))
    trees_draw(game.trees)

    Land4x4Matrix matrix = land_4x4_matrix_identity()
    land_projection(land_4x4_matrix_orthographic(-w / 2, -h / 2, 1000, w / 2, h / 2, -1000))
    land_display_transform_4x4(&matrix)
    land_render_state(LAND_DEPTH_TEST, False)

    for int i in range(8):
        land_color(0.5, 0.5, 0.5, 0.5)
        float x = -480 + 8
        float y = h / 2 - i * 60 - 60
        land_filled_rectangle(x, y, x + 52, y + 52)
        if i == 0:
            land_color(0, 0, 1, 1)
            land_filled_circle(x + 10, y + 10, x + 52 - 10, y + 52 - 10)
        if i == 1:
            land_color(1, 1, 1, 1)
            land_filled_circle(x + 10, y + 10, x + 52 - 10, y + 52 - 10)
        if i == 2:
            land_color(1, 0, 0, 1)
            land_filled_circle(x + 10, y + 10, x + 52 - 10, y + 52 - 10)
        if i == 3:
            land_color(0, 1, 0, 1)
            land_filled_circle(x + 10, y + 10, x + 52 - 10, y + 52 - 10)
        if i == 7:
            land_color(1, 1, 1, 1)
            land_filled_rectangle(x + 10, y + 10, x + 20, y + 52 - 10)
            land_filled_rectangle(x + 52 - 20, y + 10, x + 52 - 10, y + 52 - 10)

def game_done:
    pass
