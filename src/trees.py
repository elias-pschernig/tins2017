import mesh

class Tree:
    Mesh *mesh
    Land4x4Matrix pos

class Trees:
    LandArray *trees # Tree
    LandHash *kinds_by_name # Mesh

def trees_new -> Trees*:
    Trees *self
    land_alloc(self)
    self.trees = land_array_new()
    land_array_add(self.trees, None)
    self.kinds_by_name = land_hash_new()
    return self

def trees_make(Trees *trees, str name, float x, y):
    Tree *tree
    land_alloc(tree)
    tree.mesh = trees_make_kind(trees, name)
    tree.pos = land_4x4_matrix_translate(x, y, 0)
    land_array_add(trees.trees, tree)

def trees_make_kind(Trees *trees, str name) -> Mesh*:
    Mesh *m = land_hash_get(trees.kinds_by_name, name)
    if m: return m
    m = mesh_make()
    mesh_add(m, "ball", land_4x4_matrix_scale(20, 20, 20))
    mesh_add(m, "cylinder", land_4x4_matrix_mul(
        land_4x4_matrix_translate(0, 0, 20),
        land_4x4_matrix_scale(5, 5, 20)))
    land_hash_insert(trees.kinds_by_name, name, m)
    return m

def trees_draw(Trees *trees):
    for Tree* tree in LandArray* trees.trees:
        if not tree: continue
        mesh_draw(tree.mesh, tree.pos)
