import mesh

class Tree:
    Mesh *mesh
    Land4x4Matrix pos

class Trees:
    LandArray *trees # Tree
    LandHash *kinds_by_name # Mesh

    LandColor color
    Land4x4Matrix m
    int st
    Land4x4Matrix stack[16]
    Mesh *mesh

macro M Land4x4Matrix
macro F LandFloat
macro G (*global_trees)

Trees *global_trees

def trees_new -> Trees*:
    Trees *self
    land_alloc(self)
    self.trees = land_array_new()
    land_array_add(self.trees, None)
    self.kinds_by_name = land_hash_new()
    global_trees = self
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

    if land_equals(name, "hill"):
        _color(0.3, 0.5, 0.2, 1)
        _size(480, 480, 1)
        _make("grid")
        
    land_hash_insert(trees.kinds_by_name, name, G.mesh)
    return G.mesh

def trees_draw(Trees *trees):
    for Tree* tree in LandArray* trees.trees:
        if not tree: continue
        mesh_draw(tree.mesh, tree.pos)
