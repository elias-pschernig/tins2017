import trees

macro G (*global_trees)

Trees *global_trees

def _push: G.stack[G.st++] = G.m
def _pop: G.m = G.stack[--G.st]
def _size(F x, y, z): G.m = land_4x4_matrix_mul(G.m, land_4x4_matrix_scale(x, y, z))
def _turn(F x, y, z, a): G.m = land_4x4_matrix_mul(G.m, land_4x4_matrix_rotate(x, y, z, pi * a))
def _move(F x, y, z): G.m = land_4x4_matrix_mul(G.m, land_4x4_matrix_translate(x, y, z))
def _orient: G.m = land_4x4_matrix_identity()
def _make(str name): mesh_add(G.mesh, name, G.color, G.m)
def _color(F r, g, b, a): G.color = land_color_rgba(r, g, b, a)

def make_kind(Trees *trees, str name) -> Mesh*:
    global_trees = trees
    Mesh *m = land_hash_get(trees.kinds_by_name, name)
    if m: return m

    int anims = 1
    if land_equals(name, "oak") or land_equals(name, "fir") or\
            land_equals(name, "eucalypt"):
        anims = 19
    if land_equals(name, "fire") or land_equals(name, "smoke"):
        anims = 10
    if land_equals(name, "beetle"):
        anims = 8
    
    for int i in range(anims):
        G.mesh = mesh_make(name)
        if not m:
            m = G.mesh
        
        mesh_add_anim(m, G.mesh)
        _orient()

        if land_equals(name, "oak"):
            float fade = 1 - i / 19.0
            for int ir in range(6):
                _push()
                _color(0.5 * fade, 0.7 * fade, 0, 1)
                _move(0, 0, 20 + ir * 3)
                _turn(0, 0, 1, 0.4 * ir)
                if ir < 5:
                    _turn(0, 1, 0, 0.25)
                _size(15 * fade, 15 * fade, 20)
                _move(0, 0, 1)
                _make("ball")
                _pop()

            _push()
            _color(0.4 * fade, 0.2 * fade, 0, 1)
            _size(4, 4, 15)
            _move(0, 0, 1)
            _make("cylinder")
            _pop()

        if land_equals(name, "fir"):
            float fade = 1 - i / 19.0
            for int ir in range(6):
                _push()
                _color(0, 0.6 * fade, 0.3 * fade, 1)
                _move(0, 0, 20 + ir * 5)
                float s = 20 - ir * 2
                _turn(0, 0, 1, ir / 3.0)
                _turn(0, 1, 0, i / 19.0 * 0.5)
                _size(s * fade, s * fade, 10)
                _move(0, 0, 1)
                _make("cone")
                _pop()

            _push()
            _color(0.4 * fade, 0.2 * fade, 0, 1)
            _size(3, 3, 20)
            _move(0, 0, 1)
            _make("cone")
            _pop()

        if land_equals(name, "beetle"):
            _push()
            _color(1, 1, 0, 1)
            _move(0, 0, 1)
            _size(3, 5, 2)
            _move(0, 0, 1)
            _make("ball")
            _pop()

            float la = (i - 2) / 2.0
            if i > 4: la = (8 - i - 2) / 2.0 
            for int lx in range(2):
                for int ly in range(3):
                    _push()
                    _move(-1 + lx * 2, ly, 0)
                    _turn(1, 0, 0, la / 4)
                    _move(0, 0, -1)
                    _make("cylinder")
                    _pop()

        if land_equals(name, "eucalypt"):
            float fade = 1 - i / 19.0
            for int ir in range(3):
                _push()
                _color(0.6 * fade, 0.7 * fade, 0.5 * fade, 1)
                _move(0, 0, 50 + ir * 10)
                _turn(0, 0, 1, ir * 2.0 / 3)
                _size(30, 20 * fade, 2)
                _move(0.7, 0, 1)
                _make("cone")
                _pop()

            _push()
            _color(1 * fade, 0.6 * fade, 0.7 * fade, 1)
            _size(3, 3, 40)
            _move(0, 0, 1)
            _make("cone")
            _pop()

        if land_equals(name, "fire"):
            _push()
            float s = land_rnd(3, 10)
            _color(1, land_rnd(0, 1), land_rnd(0, 0.2), 1)
            _size(s, s, s)
            _make("ball")
            _pop()

        if land_equals(name, "smoke"):
            _push()
            float s = land_rnd(5, 13)
            float a = land_rnd(0.1, 1)
            float b = land_rnd(0, 1)
            _color(a * b, a * b, a * b, a)
            _size(s, s, s)
            _make("ball")
            _pop()
        
    land_hash_insert(trees.kinds_by_name, name, m)
    return m
