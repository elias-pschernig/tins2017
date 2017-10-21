import mesh

class Tree:
    Mesh *mesh
    Land4x4Matrix pos
    bool whirl
    LandVector v
    LandVector rot
    bool alive
    int burning

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

def trees_make(Trees *trees, str name, float x, y, z):
    Tree *tree
    land_alloc(tree)
    tree.mesh = trees_make_kind(trees, name)
    tree.pos = land_4x4_matrix_translate(x, y, z)
    land_array_add(trees.trees, tree)

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
    G.mesh = mesh_make()
    _orient()

    if land_equals(name, "oak"):

        _push()
        _color(0, 0.7, 0, 1)
        _move(0, 0, 20)
        _size(20, 20, 20)
        _move(0, 0, 1)
        _make("ball")
        _pop()

        _push()
        _color(0.4, 0.2, 0, 1)
        _size(3, 3, 10)
        _move(0, 0, 1)
        _make("cylinder")
        _pop()

    if land_starts_with(name, "fire"):
        _push()
        float s = land_rnd(5, 10)
        _color(1, land_rnd(0, 1), land_rnd(0, 0.2), 1)
        _size(s, s, s)
        _make("ball")
        _pop()
        
    land_hash_insert(trees.kinds_by_name, name, G.mesh)
    return G.mesh

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
    
    if land_starts_with(kind, "fire"):
        tree.v.z = 0.7

def trees_draw(Trees *trees):
    for Tree* tree in LandArray* trees.trees:
        if not tree: continue
        mesh_draw(tree.mesh, tree.pos)
    for Tree* tree in LandArray* trees.particles:
        if not tree.alive: continue
        mesh_draw(tree.mesh, tree.pos)

def trees_callback(Trees *trees, float x, y, radius,
        void (*cb)(Trees *trees, Tree*, float , float)):
    for Tree* tree in LandArray* trees.trees:
        if not tree: continue
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
    tree.burning = 140
  
def trees_tick(Trees *trees):
    for Tree* tree in LandArray* trees.trees:
        if not tree:
            continue
        if tree.burning:
            tree.burning--
            if tree.burning == 0:
                tree.alive = False
            str fires[] = {"fire1", "fire2", "fire3", "fire4", "fire5",
                "fire6", "fire7", "fire8", "fire9", "fire10"}
            float x = tree.pos.v[3]
            float y = tree.pos.v[7]
            float z = tree.pos.v[11]
            tree.pos.v[11] -= 0.5
           
            int f = land_rand(0, 20)
            if f < 10:
                trees_particle(trees, fires[f], x + land_rnd(-20, 20),
                    y + land_rnd(-20, 20), z + land_rnd(0, 20))
        if tree.whirl:
            float x = tree.pos.v[3] + tree.v.x
            float y = tree.pos.v[7] + tree.v.y
            float z = tree.pos.v[11] + tree.v.z
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
            if tree.pos.v[11] < -100: tree.whirl = False

    for Tree* tree in LandArray* trees.particles:
        if not tree.alive: continue
        tree.pos.v[11] += tree.v.z
        if tree.pos.v[11] > 200: tree.alive = False
