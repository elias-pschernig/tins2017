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
    Level *level
    LandFont *bigfont
    LandFont *smallfont
    bool resizing
    LandStream *music

    bool won
    int countdown

    LandSound *splash
    int splash_t
    LandSound *frog
    LandSound *fire
    bool fire_p
    LandSound *tree
    int wind_t
    LandSound *wind

global Game *game

bool flag
def _set_flag(Trees *trees, Tree *tree, float dx, dy):
    flag = True

def music(str name):
    land_stream_music_once(game.music, name)

def game_init:
    land_display_title("Dr. Forest")
    land_alloc(game)

    game.music = land_stream_new(2048, 4, 44100, 16, 2)

    game.splash = land_sound_load("data/splash.ogg")
    game.frog = land_sound_load("data/frog.ogg")
    game.fire = land_sound_load("data/fire.ogg")
    game.tree = land_sound_load("data/tree.ogg")
    game.wind = land_sound_load("data/wind.ogg")
    
    game.trees = trees_new()
    game.camera_angle = pi / -3.3

    reload_font(1)

    game_restart_level(1)

def game_restart_level(int number):
    if game.world: world_destroy(game.world)
    trees_clear(game.trees)
    game.world = world_new()
    if number == 0: number = game.level.number
    game.level = levels_start(number)

def _draw(float mx, my) -> bool:
    float dx = mx - game.lx
    float dy = my - game.ly
    if game.level.tools[game.tool] == 0: return False
    if dx * dx + dy * dy > 10:
        game.lx = mx
        game.ly = my
        if game.level.tools[game.tool] > 0:
            game.level.tools[game.tool]--
        return True
    return False

def _draw2(float mx, my) -> bool:
    float dx = mx - game.lx
    float dy = my - game.ly
    if game.level.tools[game.tool] == 0: return False
    if dx * dx + dy * dy > 10:
        game.lx = mx
        game.ly = my
        return True
    return False

def place_tree_rising(float x, y, str kind, bool rising) -> Tree*:
    flag = False
    trees_callback(game.trees, x, y, 30, _set_flag)
    if flag: return None
    return place_tree_rising_nc(x, y, kind, rising, True)

def place_tree_rising_nc(float x, y, str kind, bool rising, bool blotch) -> Tree*:
    float z = rising ? -99 : world_get_altitude(game.world, x, y)
    Tree *tree = trees_make(game.trees, kind, x, y, z)
    if blotch:
        world_blotch(game.world, x, y, 40, land_color_rgba(0.3, 0.1, 0, 1))
    tree.rising = rising
    return tree

def place_tree(float x, y, str kind) -> Tree*:
    return place_tree_rising(x, y, kind, False)

def reload_font(float s):
    if game.bigfont: land_font_destroy(game.bigfont)
    if game.smallfont: land_font_destroy(game.smallfont)
    int si = 32 / s
    game.bigfont = land_font_load("data/JosefinSans-Regular.ttf", si)
    land_font_scale(game.bigfont, 32.0 / si)
    land_font_yscale(game.bigfont, -32.0 / si)
    si = 24 / s
    game.smallfont = land_font_load("data/JosefinSans-Regular.ttf", si)
    land_font_scale(game.smallfont, 24.0 / si)
    land_font_yscale(game.smallfont, -24.0 / si)

def game_tick:
    float dw = land_display_width()
    float dh = land_display_height()
    float w, h
    _letterbox(&w, &h)

    if land_was_resized():
        game.resizing = True

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
            int tool = (h / 2 - my) / 60
            if tool == 6:
                if game.paused:
                    game.won = False
                    pause_toggle()
                game_restart_level(0)
            elif tool == 7:
                pause_toggle()
            else:
                game.tool = tool
                   
    if game.paused:
        if land_mouse_delta_button(0) and not land_mouse_button(0):
            if mx >= -420:
                pause_toggle()
        if land_key_pressed(LandKeyBackspace):
            game.level.number -= 2
            game.won = True
            pause_toggle()
        if land_key_pressed(LandKeyEnter):
            game.won = True
            pause_toggle()
        trees_dance(game.trees)
        funky(False)
        return

    int tick = land_get_ticks()

    levels_tick()

    if land_mouse_button(0):
        if mx < -420:
            pass
        elif game.tool == 1:
            if _draw(mx, my):
                world_blotch(game.world, t.x, t.y, 50, land_color_rgba(1, 0.8, 0.6, 1))
                trees_callback(game.trees, t.x, t.y, 60, tree_whirl)
                if tick > game.wind_t:
                    game.wind_t = tick + 15
                    land_sound_play(game.wind, 1, 0, land_rnd(1, 1.25))
        elif game.tool == 0:
            if _draw(mx, my):
                world_patch(game.world, t.x, t.y, 40, land_color_rgba(0.2, 0.4, 0.4, 1))
                trees_callback_square(game.trees, t.x, t.y, 50, tree_water)
                world_raise(game.world, t.x, t.y, 40, -2)
                trees_callback(game.trees, t.x, t.y, 40, tree_raise)
                if tick > game.splash_t:
                    game.splash_t = tick + 40
                    land_sound_play(game.splash, 1, 0, 1)
        elif game.tool == 2:
            if _draw(mx, my):
                trees_callback(game.trees, t.x, t.y, 60, tree_burn)
                world_blotch(game.world, t.x, t.y, 40, land_color_rgba(0, 0, 0, 1))
        elif game.tool == 5:
            if _draw2(mx, my):
                if place_tree(t.x, t.y, "post"):
                    game.level.tools[game.tool]--
                    world_patch(game.world, t.x, t.y, 40, land_color_rgba(1, 0.8, 0.4, 1))
                    world_raise(game.world, t.x, t.y, 40, 10)
                    trees_callback(game.trees, t.x, t.y, 40, tree_raise)
        elif game.tool == 3:
            if _draw2(mx, my):
                if place_tree_rising(t.x, t.y, "oak", True):
                    game.level.tools[game.tool]--
                    if not land_rand(0, 2):
                        place_tree_rising_nc(t.x, t.y, "beetle", True, False)
        elif game.tool == 4:
            if _draw2(mx, my):
                str kind = "fir"
                if not land_rand(0, 2):
                    kind = "eucalypt"
                if place_tree_rising(t.x, t.y, kind, True):
                    game.level.tools[game.tool]--

    trees_tick(game.trees)

    if game.level.done:
        bool ok = False
        if game.trees.healthy >= game.level.required and\
                game.trees.fires == 0 and\
                game.trees.invasives == 0 and\
                game.trees.beetles == 0 and\
                game.trees.hidden == 0:
            ok = True
        if game.countdown:
            if ok:
                game.countdown--
                if game.countdown == 0:
                    game.won = True
                    pause_toggle()
            else:
                game.countdown = 0
        else:
            if ok:
                game.countdown = 180

def pause_toggle:
    game.paused = not game.paused
    if game.won and not game.paused:
        game.won = False
        game_restart_level(game.level.number + 1)
    if game.paused:
        music("data/funk.ogg")
    else:
        music("data/forest.ogg")
    
    funky(game.paused)

def _letterbox(float *w, *h) -> float:
    float tw = land_display_width()
    float th = land_display_height()
    float hscale = 16 * 60 / tw
    *w = tw * hscale
    *h = th * hscale
    if *w / *h > 16.0 / 9:
        float vscale = 9 * 60 / th
        *w = tw * vscale
        *h = th * vscale
        return vscale
    return hscale

def game_draw:
    float w, h
    float s = _letterbox(&w, &h)

    if game.resizing:
        game.resizing = False
        reload_font(s)

    land_clear(0.5, 0.5, 0.5, 1)
    land_clear_depth(1)
    land_render_state(LAND_DEPTH_TEST, True)

    land_projection(land_4x4_matrix_mul(
        land_4x4_matrix_orthographic(-w / 2, -h / 2, 1000, w / 2, h / 2, -1000),
        land_4x4_matrix_rotate(1, 0, 0, game.camera_angle)))

    #if game.paused:
    #    float a = land_get_ticks() % 60
    #    a = a * 2 * pi / 60
    #    mesh_draw(game.world.mesh, land_4x4_matrix_translate(
    #        cos(a) * 10, sin(a) * 10, 0))
    #else:
    mesh_draw(game.world.mesh, land_4x4_matrix_translate(0, 0, 0))
    trees_draw(game.trees)

    Land4x4Matrix matrix = land_4x4_matrix_identity()
    land_projection(land_4x4_matrix_orthographic(-w / 2, -h / 2, 1000, w / 2, h / 2, -1000))
    land_display_transform_4x4(&matrix)
    land_render_state(LAND_DEPTH_TEST, False)

    land_color(0.2, 0.2, 0.2, 0.2)
    land_filled_rectangle(-480, -h, -480 + 68, h)

    for int i in range(8):
        float x = -480 + 8
        float y = h / 2 - i * 60 - 60
        if i <= 5 and game.level.tools[i]:
            if i == game.tool:
                land_color(0.9, 0.8, 0.5, 0.8)
                land_filled_rectangle(x - 8, y, x + 60, y + 52)
            else:
                land_color(0.5, 0.5, 0.5, 0.5)
                land_filled_rectangle(x, y, x + 52, y + 52)
        elif i >= 6:
            land_color(0.5, 0.5, 0.5, 0.5)
            land_filled_rectangle(x, y, x + 52, y + 52)

        y += 34
        x += 26
        float r = 16
        
        if i == 0 and game.level.tools[0]:
            land_color(0, 0, 1, 1)
            land_filled_circle(x - r, y - r, x + r, y + r)
        if i == 1 and game.level.tools[1]:
            land_color(1, 1, 1, 1)
            land_filled_circle(x - r, y - r, x + r, y + r)
        if i == 2 and game.level.tools[2]:
            land_color(1, 0, 0, 1)
            land_filled_circle(x - r, y - r, x + r, y + r)
        if i == 3 and game.level.tools[3]:
            land_color(0, 1, 0, 1)
            land_filled_circle(x - r, y - r, x + r, y + r)
        if i == 4 and game.level.tools[4]:
            land_color(0, 0.5, 0, 1)
            land_filled_triangle(x - r, y - r, x, y + r, x + r, y - r)
        if i == 5 and game.level.tools[5]:
            land_color(1, 1, 0, 1)
            land_filled_circle(x - r, y - r, x + r, y + r)

        y -= 34
        x -= 26
        
        if i == 6:
            land_color(1, 1, 1, 1)
            land_text_pos(x + 26, y + 26 - 4)
            land_font_set(game.bigfont)
            land_print_middle("R")
        if i == 7:
            land_color(1, 1, 1, 1)
            land_filled_rectangle(x + 10, y + 10, x + 20, y + 52 - 10)
            land_filled_rectangle(x + 52 - 20, y + 10, x + 52 - 10, y + 52 - 10)

        if i <= 5 and game.level.tools[i] > 0:
            land_color(0, 0, 0, 1)
            land_text_pos(x + 26, y + 20)
            land_font_set(game.smallfont)
            land_print_center("%d", game.level.tools[i])

    land_font_set(game.bigfont)
    land_color(1, 0.8, 0.1, 1)
    land_text_pos(0, h / 2 - 8)
    if game.won:
        if game.trees.lost == 0:
            land_print_center("You lost not a single tree!")
            land_print_center("Awesome! You're Dr. Forest!")
        if game.trees.lost == 1:
            land_print_center("You lost only a single tree!")
            land_print_center("Excellent job!")
        if game.trees.lost > 1:
            land_print_center("You lost %d trees but saved the forest!",
                game.trees.lost)
            land_print_center("Good job!")
        
    else:
        land_print_center("%s", game.level.name)

    if True:
        int hn = game.trees.healthy
        int rn = game.level.required
        if hn >= rn:
            land_color(0.3, 0.6, 0, 1)
        else:
            land_color(1, 0, 0, 1)
        land_text_pos(0, -h / 2 + 32)
        land_print_center("%d / %d trees are healthy", hn, rn)

    if game.trees.fires:
        land_color(1, 0, 0, 1)
        land_text_pos(480, -h / 2 + 32)
        land_print_right("%d fires!", game.trees.fires)

    if game.trees.burning:
        if not game.fire_p:
            land_sound_loop(game.fire, 1, 0, 1)
            game.fire_p = True
    else:
        if game.fire_p:
            land_sound_stop(game.fire)
            game.fire_p = False

    if game.trees.beetles:
        land_color(1, 1, 0, 1)
        land_text_pos(480, -h / 2 + 32 * 2)
        land_print_right("%d beetle%s!", game.trees.beetles,
            game.trees.beetles == 1 ? "" : "s")

    if game.trees.invasives:
        land_color(1, 0.5, 1, 1)
        land_text_pos(480, -h / 2 + 32 * 3)
        land_print_right("%d invasives!", game.trees.invasives)

    if game.paused:
        draw_funk()

def game_done:
    pass

class Funk:
    float x, y, r
    LandColor c
Funk funk[20]
int funkt

def funky(bool start):
    if start:
        funkt = land_get_ticks()
    int b = (land_get_ticks() - funkt) % 60
    if b == 0:
        for int i in range(20):
            Funk *f = funk + i
            f.c = land_color_rgba(0, 0, 0, 0)
    if b == 30:
        for int i in range(20):
            Funk *f = funk + i
            f.x = land_rnd(-400, 400)
            f.y = land_rnd(-400, 400)
            f.r = land_rnd(50, 150)
            f.c = land_color_hsv(land_rnd(0, 360), 1, 1)
            f.c = land_color_premul(f.c.r, f.c.g, f.c.b, 0.1)
    if b > 30:
        for int i in range(20):
            Funk *f = funk + i
            f.x *= 1.005
            f.y *= 1.005

def draw_funk:
    for int i in range(20):
        Funk *f = funk + i
        land_color_set(f.c)
        land_filled_circle(f.x - f.r, f.y - f.r, f.x + f.r, f.y + f.r)
