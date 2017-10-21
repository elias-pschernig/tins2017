import main
import mesh
import trees
import world

class Game:
    Trees *trees
    float camera_angle
    World *world
    int tool

global Game *game

def game_init:
    land_display_title("Dr. Forest")
    
    land_alloc(game)
    game.trees = trees_new()
    game.camera_angle = pi / -3.3
    game.world = world_new()

    for int i in range(5):
        float x = land_rnd(-300, 300)
        float y = land_rnd(-300, 300)
        trees_make(game.trees, "oak", x, y, world_get_altitude(
            game.world, x, y))

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
            game.tool = (dh / 2 - my) / 60
            print("%d", game.tool)
        elif game.tool == 0:
            trees_make(game.trees, "oak", t.x, t.y, world_get_altitude(
                game.world, t.x, t.y))
        elif game.tool == 1:
            world_blotch(game.world, t.x, t.y, 50, land_color_rgba(1, 0.8, 0.6, 1))
        elif game.tool == 2:
             world_patch(game.world, t.x, t.y, 50, land_color_rgba(0, 0, 1, 1))

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

def game_done:
    pass
