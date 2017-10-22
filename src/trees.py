import mesh
import make

class Tree:
    Mesh *mesh
    Land4x4Matrix pos
    bool whirl
    bool sink
    bool blighted
    LandVector v
    LandVector rot
    bool alive
    int burning
    int frame
    int sick
    bool rising
    bool dancing
    bool beetle
    float angle
    Land4x4Matrix dance
    Tree *target
    int rest
    bool pregnant
    bool infested

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

    Tree *found

macro PC 1000
macro M Land4x4Matrix
macro F LandFloat
macro mul land_4x4_matrix_mul
macro tra land_4x4_matrix_translate

static bool flag

def trees_new -> Trees*:
    Trees *self
    land_alloc(self)
    self.trees = land_array_new()
    self.particles = land_array_new()
    land_array_add(self.trees, None)
    self.kinds_by_name = land_hash_new()

    for int i in range(PC):
        Tree *p
        land_alloc(p)
        land_array_add(self.particles, p)
    return self

def trees_make(Trees *trees, str name, float x, y, z) -> Tree*:
    Tree *tree
    land_alloc(tree)
    tree.mesh = make_kind(trees, name)
    tree.alive = True
    tree.angle = land_rnd(-pi / 4, pi / 4)
    tree.pos = land_4x4_matrix_mul(
        land_4x4_matrix_translate(x, y, z),
        land_4x4_matrix_rotate(0, 0, 1, tree.angle))
    land_array_add(trees.trees, tree)
    return tree

def trees_particle(Trees *trees, str kind, float x, y, z):
    Tree* tree = land_array_get_nth(trees.particles, trees.particle_counter)
    trees.particle_counter++
    trees.particle_counter %= PC
    tree.mesh = make_kind(trees, kind)
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
    if tree.beetle: return
    flag = True
    tree.sick++
    if tree.frame < 18:
        tree.frame++

def tree_blight(Trees *trees, Tree *tree, float dx, dy):
    if land_equals(tree.mesh.name, "eucalypt"):
        return
    if tree.beetle: return
    tree.blighted = True
    tree_sicken(trees, tree, dx, dy)

def tree_infest(Trees *trees, Tree *tree, float dx, dy):
    if tree.sink: return
    if tree.sick: return
    if tree.infested: return
    if land_equals(tree.mesh.name, "oak"):
        trees.found = tree

def tree_flag(Trees *trees, Tree *tree, float dx, dy):
    flag = True

def trees_dance(Trees *trees):
    for Tree* tree in LandArray* trees.trees:
        if not tree:
            continue
        if not tree.dancing:
            tree.dance = tree.pos
            tree.dancing = True
        float x = tree.dance.v[3]
        float y = tree.dance.v[7]
        float z = tree.dance.v[11]
        int t = land_get_ticks()
        int t2 = t % 120
        z += (sin((t % 30)  / 30.0 * pi * 2) + 1) * 10
        tree.pos = land_4x4_matrix_mul(land_4x4_matrix_translate(
            x, y, z), land_4x4_matrix_rotate(
            0, 1, 0, sin(t2 / 120.0 * pi * 2) / 2))

    for Tree* tree in LandArray* trees.particles:
        if not tree.alive: continue
        if not tree.dancing:
            tree.dance = tree.pos
            tree.dancing = True
        int t = land_get_ticks()
        int t2 = t % 120
        tree.pos = land_4x4_matrix_mul(land_4x4_matrix_rotate(
            0, 0, 1, t2 / 120.0 * pi * 2), tree.dance)
        
def trees_tick(Trees *trees):
    for Tree* tree in LandArray* trees.trees:
        if not tree:
            continue
        if tree.dancing:
            tree.pos = tree.dance
            tree.dancing = False
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
            z += 0.5
            float az = world_get_altitude(game.world, x, y)
            float s = 1 - (az - z) / 100
            if s < 0.1: s = 0.1
            tree.pos = land_4x4_matrix_mul(land_4x4_matrix_translate(x, y, z),
                land_4x4_matrix_mul(
                    land_4x4_matrix_scale(s, s, s),
                    land_4x4_matrix_rotate(0, 0, 1, tree.angle)))
            if z >= az:
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

        if tree.beetle and not tree.sink:
            if tree.rest:
                tree.rest--
                continue
            tree.frame = (land_get_ticks() / 4) % 8
            LandVector p = land_4x4_matrix_get_position(&tree.pos)
            LandVector b = land_4x4_matrix_get_up(&tree.pos)
            if tree.target:
                Tree *tt = tree.target
                if not tt.alive or tt.sink or tt.sick > 18:
                    tree.target = None
                    tree.pregnant = True
                    continue
                LandVector tp = land_4x4_matrix_get_position(&tt.pos)
                LandVector towards = land_vector_sub(tp, p)
                if land_vector_norm(towards) < 20:
                    tree_sicken(trees, tt, 0, 0)
                    tree.rest = 30
                towards = land_vector_normalize(towards)
                LandFloat di = land_vector_dot(b, towards)
                LandFloat ci = land_vector_cross(b, towards).z
                if di > 0.01:
                        di = 0
                        if ci > 0.01: di = 0.02
                        if ci < -0.01: di = -0.02
                elif di < -0.01:
                    di = (land_rnd(0, 1) - 1) * 2 * 0.02
                else: di = 0
                tree.pos.v[3] = 0
                tree.pos.v[7] = 0
                tree.pos.v[11] = 0
                tree.pos = mul(land_4x4_matrix_rotate(0, 0, 1, di), tree.pos)
                tree.pos.v[3] = p.x
                tree.pos.v[7] = p.y
                tree.pos.v[11] = p.z
            else:
                if p.x < -440 or p.y < -440 or p.x > 440 or p.y > 440:
                    float tx = p.x - land_rnd(-100, 100)
                    float ty = p.y - land_rnd(-100, 100)
                    tree.pos = mul(tra(p.x, p.y, p.z),
                        land_4x4_matrix_rotate(0, 0, 1, atan2(tx, -ty)))
            tree.pos = mul(tra(b.x, b.y, world_get_altitude(
                game.world, p.x, p.y) - p.z), tree.pos)

    int n = land_array_count(trees.trees)
    int per_second = 1 + n / 60
    for int ri in range(per_second):
        int r = land_rand(1, n - 1)
        Tree* rtree = land_array_get_nth(trees.trees, r)
        float x = rtree.pos.v[3]
        float y = rtree.pos.v[7]

        if rtree.sink:
            continue
        if rtree.rising:
            continue
            
        if rtree.sick:
            if rtree.sick > 18:
                if not rtree.sink and rtree.blighted:
                    tree_sink(trees, rtree, 0, 0)
                    Tree *t = trees_make(trees, "eucalypt", x, y, -99)
                    t.rising = True
            else:
                if land_rand(0, 4) == 0:
                    rtree.sick--
                    rtree.frame--
        elif land_equals(rtree.mesh.name, "eucalypt"):
            flag = False
            trees_callback(trees, x, y, 70, tree_blight)
            if not flag:
                x += land_rnd(-60, 60)
                y += land_rnd(-60, 60)
                if x < -480 or y < -480 or x > 480 or y > 480:
                    pass
                else:
                    flag = False
                    trees_callback(trees, x, y, 50, tree_flag)
                    if not flag:
                        Tree *t = trees_make(trees, "eucalypt", x, y, -99)
                        t.rising = True
        elif land_equals(rtree.mesh.name, "beetle"):
            if not rtree.target:
                if rtree.pregnant:
                    rtree.pregnant = False
                    LandVector p = land_4x4_matrix_get_position(&rtree.pos)
                    Tree* clone = trees_make(trees, "beetle", p.x, p.y, p.z)
                    clone.beetle = True
                trees.found = None
                trees_callback(trees, x, y, 200, tree_infest)
                if trees.found:
                    rtree.target = trees.found
                    trees.found.infested = True

    # prune dead trees (actually, only the first one)
    for int i in range(1, n):
        Tree* dtree = land_array_get_nth(trees.trees, i)
        if not dtree.alive:
            land_array_remove(trees.trees, i)
            break

    for Tree* tree in LandArray* trees.particles:
        if not tree.alive: continue
        if tree.dancing:
            tree.pos = tree.dance
            tree.dancing = False
        tree.pos.v[3] += tree.v.x
        tree.pos.v[7] += tree.v.y
        tree.pos.v[11] += tree.v.z
        if tree.pos.v[11] > 200: tree.alive = False
