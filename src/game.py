import main
import mesh
import trees
import world

class Game:
    Trees *trees
    float camera_angle
    World *world
    int tool

    float lx, ly

global Game *game

def game_init:
    land_display_title("Dr. Forest")
    
    land_alloc(game)
    game.trees = trees_new()
    game.camera_angle = pi / -3.3
    game.world = world_new()

    for int i in range(25):
        float x = land_rnd(-300, 300)
        float y = land_rnd(-300, 300)
        trees_make(game.trees, "oak", x, y, world_get_altitude(
            game.world, x, y))

def _draw(float mx, my) -> bool:
    float dx = mx - game.lx
    float dy = my - game.ly
    if dx * dx + dy * dy > 10:
        game.lx = mx
        game.ly = my
        return True
    return False

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

    if land_mouse_button(0):
        if mx < -420:
            pass
        elif game.tool == 1:
            if _draw(mx, my):
                world_blotch(game.world, t.x, t.y, 50, land_color_rgba(1, 0.8, 0.6, 1))
        elif game.tool == 0:
            if _draw(mx, my):
                world_patch(game.world, t.x, t.y, 50, land_color_rgba(0.2, 0.2, 0.8, 1))

    if land_mouse_button_clicked(0):

        if mx < -420:
            game.tool = (h / 2 - my) / 60
        elif game.tool == 2:
            trees_make(game.trees, "oak", t.x, t.y, world_get_altitude(
                game.world, t.x, t.y))
            world_blotch(game.world, t.x, t.y, 20, land_color_rgba(0.3, 0.1, 0, 1))
        elif game.tool == 3:
            trees_callback(game.trees, t.x, t.y, 40, tree_whirl)
        elif game.tool == 4:
            trees_callback(game.trees, t.x, t.y, 40, tree_burn)

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

    mesh_draw(game.world.mesh, land_4x4_matrix_translate(0, 0, 0))
    trees_draw(game.trees)

    Land4x4Matrix matrix = land_4x4_matrix_identity()
    land_projection(land_4x4_matrix_orthographic(-w / 2, -h / 2, 1000, w / 2, h / 2, -1000))
    land_display_transform_4x4(&matrix)
    land_render_state(LAND_DEPTH_TEST, False)

    for int i in range(5):
        land_color(0.5, 0.5, 0.5, 0.5)
        float y = h / 2 - i * 60
        land_filled_rectangle(-480 + 8, y - 8, -480 + 60, y - 60)

def game_done:
    pass
