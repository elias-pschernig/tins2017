import mesh

class Tree:
    Mesh *mesh
    Land4x4Matrix pos
    bool whirl
    bool sink
    LandVector v
    LandVector rot
    bool alive
    int burning
    int frame
    int sick
    bool rising

class Trees:
    LandArray *trees # Tree
    LandHash *kinds_by_name # Mesh

    LandArray *particles
    int particle_counter

    LandColor color
    Land4x4Matrix m
    int st
    Land4x4Matrix stack[16]
    Mesh *mesh

macro PC 1000
macro M Land4x4Matrix
macro F LandFloat
macro G (*global_trees)

Trees *global_trees

def trees_new -> Trees*:
    Trees *self
    land_alloc(self)
    self.trees = land_array_new()
    self.particles = land_array_new()
    land_array_add(self.trees, None)
    self.kinds_by_name = land_hash_new()
    global_trees = self

    for int i in range(PC):
        Tree *p
        land_alloc(p)
        land_array_add(self.particles, p)
    return self

def trees_make(Trees *trees, str name, float x, y, z) -> Tree*:
    Tree *tree
    land_alloc(tree)
    tree.mesh = trees_make_kind(trees, name)
    tree.alive = True
    tree.pos = land_4x4_matrix_mul(
        land_4x4_matrix_translate(x, y, z),
        land_4x4_matrix_rotate(0, 0, 1, land_rnd(-pi / 4, pi / 4)))
    land_array_add(trees.trees, tree)
    return tree

def _push: G.stack[G.st++] = G.m
def _pop: G.m = G.stack[--G.st]
def _size(F x, y, z): G.m = land_4x4_matrix_mul(G.m, land_4x4_matrix_scale(x, y, z))
def _turn(F x, y, z, a): G.m = land_4x4_matrix_mul(G.m, land_4x4_matrix_rotate(x, y, z, pi * a))
def _move(F x, y, z): G.m = land_4x4_matrix_mul(G.m, land_4x4_matrix_translate(x, y, z))
def _orient: G.m = land_4x4_matrix_identity()
def _make(str name): mesh_add(G.mesh, name, G.color, G.m)
def _color(F r, g, b, a): G.color = land_color_rgba(r, g, b, a)

def trees_make_kind(Trees *trees, str name) -> Mesh*:
    Mesh *m = land_hash_get(trees.kinds_by_name, name)
    if m: return m

    int anims = 1
    if land_equals(name, "oak") or land_equals(name, "fir") or\
            land_equals(name, "eucalypt"):
        anims = 19
    if land_equals(name, "fire") or land_equals(name, "smoke"):
        anims = 10
    
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

def trees_particle(Trees *trees, str kind, float x, y, z):
    Tree* tree = land_array_get_nth(trees.particles, trees.particle_counter)
    trees.particle_counter++
    trees.particle_counter %= PC
    tree.mesh = trees_make_kind(trees, kind)
    tree.pos = land_4x4_matrix_translate(x, y, z)
    tree.v = land_vector(0, 0, 0)
    tree.whirl = False
    tree.burning = 0
    tree.alive = True
    tree.frame = land_rand(0, land_array_count(tree.mesh.frames) - 1)
    
    if land_starts_with(kind, "fire"):
        tree.v.z = 0.7
    if land_starts_with(kind, "smoke"):
        tree.v.x = land_rnd(-0.2, 0.2)
        tree.v.y = land_rnd(-0.2, 0.2)
        tree.v.z = 0.5

def trees_draw(Trees *trees):
    for Tree* tree in LandArray* trees.trees:
        if not tree: continue
        Mesh *mesh = land_array_get_nth(tree.mesh.frames, tree.frame)
        mesh_draw(mesh, tree.pos)
    for Tree* tree in LandArray* trees.particles:
        if not tree.alive: continue
        Mesh *mesh = land_array_get_nth(tree.mesh.frames, tree.frame)
        mesh_draw(mesh, tree.pos)

def trees_callback(Trees *trees, float x, y, radius,
        void (*cb)(Trees *trees, Tree*, float , float)):
    for Tree* tree in LandArray* trees.trees:
        if not tree: continue
        if not tree.alive: continue
        float dx = tree.pos.v[3] - x
        float dy = tree.pos.v[7] - y
        if dx * dx + dy * dy < radius * radius:
            cb(trees, tree, dx, dy)

def tree_whirl(Trees *trees, Tree *tree, float dx, dy):
    tree.whirl = True
    tree.v = land_vector_normalize(land_vector(dx, dy, 1))
    tree.v.x *= 5
    tree.v.y *= 5
    tree.v.z = 20
    tree.rot = land_vector_normalize(land_vector_cross(
        land_vector(0, 0, 1), land_vector(dx, dy, 0)))

def tree_burn(Trees *trees, Tree *tree, float dx, dy):
    if tree.sink or tree.rising: return
    if tree.frame == 18 or tree.burning or tree.sick > 18: return
    tree.burning = 140

def tree_sink(Trees *trees, Tree *tree, float dx, dy):
    tree.sink = True
    tree.burning = 0

def tree_sicken(Trees *trees, Tree *tree, float dx, dy):
    if land_equals(tree.mesh.name, "eucalypt"):
        return
    tree.sick++
    if tree.frame < 18:
        tree.frame++
  
def trees_tick(Trees *trees):
    for Tree* tree in LandArray* trees.trees:
        if not tree:
            continue
        float x = tree.pos.v[3]
        float y = tree.pos.v[7]
        float z = tree.pos.v[11]
        if tree.burning:
            tree.burning--
            if tree.burning == 0:
                tree.sick = 19
                trees_callback(trees, tree.pos.v[3], tree.pos.v[7],
                    100, tree_burn)
            
            int wf = 18 * (140 - tree.burning) / 140
            if wf > tree.frame:
                tree.frame = wf
            
            int f = land_rand(0, 20)
            if f < 10:
                trees_particle(trees, f * 10 < tree.burning ? "fire" : "smoke",
                    x + land_rnd(-20, 20),
                    y + land_rnd(-20, 20), z + land_rnd(0, 20))
        if tree.sink:
            tree.pos.v[11] -= 0.5
            if tree.pos.v[11] < -100:
                tree.alive = False
        if tree.rising:
            tree.pos.v[11] += 0.5
            if tree.pos.v[11] >= world_get_altitude(game.world, x, y):
                tree.rising = False
        if tree.whirl:
            x += tree.v.x
            y += tree.v.y
            z += tree.v.z
            tree.pos.v[3] = 0
            tree.pos.v[7] = 0
            tree.pos.v[11] = 0
            tree.v.x *= 0.99
            tree.v.y *= 0.99
            tree.v.z -= 1
            tree.pos = land_4x4_matrix_mul(land_4x4_matrix_rotate(
                tree.rot.x, tree.rot.y, tree.rot.z, 0.1), tree.pos)
            tree.pos.v[3] = x
            tree.pos.v[7] = y
            tree.pos.v[11] = z
            if tree.pos.v[11] < -100:
                tree.whirl = False
                tree.alive = False

    # prune dead trees (actually, only the first one)
    int n = land_array_count(trees.trees)

    int r = land_rand(1, n - 1)
    Tree* rtree = land_array_get_nth(trees.trees, r)
    float x = rtree.pos.v[3]
    float y = rtree.pos.v[7]
    if land_equals(rtree.mesh.name, "eucalypt"):
        trees_callback(trees, x, y, 70, tree_sicken)
    elif rtree.sick:
        if rtree.sick > 18:
            if not rtree.sink:
                tree_sink(trees, rtree, 0, 0)
                Tree *t = trees_make(trees, "eucalypt", x, y, -99)
                t.rising = True
        else:
            if land_rand(0, 4) == 0:
                rtree.sick--
                rtree.frame--
    
    for int i in range(1, n):
        Tree* dtree = land_array_get_nth(trees.trees, i)
        if not dtree.alive:
            land_array_remove(trees.trees, i)
            break

    for Tree* tree in LandArray* trees.particles:
        if not tree.alive: continue
        tree.pos.v[3] += tree.v.x
        tree.pos.v[7] += tree.v.y
        tree.pos.v[11] += tree.v.z
        if tree.pos.v[11] > 200: tree.alive = False
