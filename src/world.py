import common
import mesh

static macro W 100
static macro H 100

class World:
    Tile *tiles
    Mesh *mesh

class Tile:
    LandColor color
    float height    

static Tile dummy
static LandVector light = {-1, -1, 1}

def world_width -> int: return W
def world_height -> int: return H

def world_tile(World *world, int x, y) -> Tile*:
    if x < 0 or y < 0 or x >= W or y >= H: return &dummy
    return world.tiles + y * W + x

def world_new -> World*:
    World *self
    land_alloc(self)
    self.tiles = land_malloc(W * H * sizeof *self.tiles)

    for int y in range(H):
        for int x in range(W):
            double dx = x - W / 2
            double dy = y - H / 2
            double d = sqrt(dx * dx + dy * dy)
            double h = 80 - d * 2
            h += land_rnd(0, 0.5)
            if h < 0: h = 0
            Tile *t = world_tile(self, x, y)
            t.height = h
            t.color = land_color_rgba(0.4, 0.2, 0, 1)

    for int i in range(40):
        float r = land_rnd(5, 40)
        float rr = land_rnd(0, 0.1)
        float rg = land_rnd(0, 0.1)
        float rb = land_rnd(0, 0.1)
        int rx = land_rand(0, W - 1)
        int ry = land_rand(0, H - 1)
        for int y in range(H):
            for int x in range(W):
                Tile *t = world_tile(self, x, y)
                double dx = x - rx
                double dy = y - ry
                double d = sqrt(dx * dx + dy * dy)
                float c = 1 - d / r
                if c < 0: c = 0
                float cr = t.color.r + c * rr
                float cg = t.color.g + c * rg
                float cb = t.color.b + c * rb
                if cr > 1: cr = 1
                if cg > 1: cg = 1
                if cb > 1: cb = 1
                
                t.color = land_color_rgba(cr, cg, cb, 1)
    
    world_create_mesh(self)

    _update(self, 0, 0, 100, 100)
    
    return self

def world_blotch(World *self, LandFloat px, py, radius, LandColor color):
    double s = 480

    int ax = (px - radius + s) * 50 / s
    int ay = (py - radius + s) * 50 / s
    int bx = (px + radius + s) * 50 / s
    int by = (py + radius + s) * 50 / s
    bx++
    by++

    if ax < 0: ax = 0
    if ay < 0: ay = 0
    if bx > W: bx = W
    if by > H: by = H

    int ix = (px + s) * 50 / s
    int iy = (py + s) * 50 / s
    int ir = radius * 50 / s

    for int y in range(ay, by):
        for int x in range(ax, bx):
           
            float d = sqrt((x - ix) * (x - ix) + (y - iy) * (y - iy))
            if d > ir:
                continue
            Tile *t = world_tile(self, x, y)
            float i = (ir - d) / ir
            float r = t.color.r * (1 - i) + color.r * i
            float g = t.color.g * (1 - i) + color.g * i
            float b = t.color.b * (1 - i) + color.b * i
            t.color = land_color_rgba(r, g, b, 1)

    _update(self, ax, ay, bx, by)

def world_patch(World *self, LandFloat px, py, r, LandColor color):
    double s = 480

    int ax = (px - r + s) * 50 / s
    int ay = (py - r + s) * 50 / s
    int bx = (px + r + s) * 50 / s
    int by = (py + r + s) * 50 / s
    bx++
    by++

    if ax < 0: ax = 0
    if ay < 0: ay = 0
    if bx > W: bx = W
    if by > H: by = H

    for int y in range(ay + 1, by - 1):
        for int x in range(ax + 1, bx - 1):
            Tile *t = world_tile(self, x, y)
            t.color = color

    _update(self, ax, ay, bx, by)

def _update(World *self, int ax, ay, bx, by):
    double s = 480
    for int v in range(ay, by):
        for int u in range(ax, bx):
            int tr1 = 2 * (u + v * 100)
            int tr2 = tr1 + 1

            Tile *t1 = world_tile(self, u, v)
            Tile *t2 = world_tile(self, u + 1, v)
            Tile *t3 = world_tile(self, u + 1, v + 1)
            Tile *t4 = world_tile(self, u, v + 1)
            
            float x1 = -s + u * s * 2 / 100
            float y1 = -s + v * s * 2 / 100
            float x2 = -s + (u + 1) * s * 2 / 100
            float y2 = -s + v * s * 2 / 100
            float x3 = -s + (u + 1) * s * 2 / 100
            float y3 = -s + (v + 1) * s * 2 / 100
            float x4 = -s + u * s * 2 / 100
            float y4 = -s + (v + 1) * s * 2 / 100
            
            _update_vertex(self, tr1 * 3 + 0, x1, y1, t1)
            _update_vertex(self, tr1 * 3 + 1, x2, y2, t2)
            _update_vertex(self, tr1 * 3 + 2, x3, y3, t3)
            _update_vertex(self, tr2 * 3 + 0, x3, y3, t3)
            _update_vertex(self, tr2 * 3 + 1, x4, y4, t4)
            _update_vertex(self, tr2 * 3 + 2, x1, y1, t1)

def _update_vertex(World *self, int tr, float x, y, Tile *t):
    LandVector n = _get_normal(self, x, y)
    LandFloat d = land_vector_dot(n, light)
    d = (1 + d) / 2
    float r = t.color.r * d
    float g = t.color.g * d
    float b = t.color.b * d
    mesh_update_vertex(self.mesh, tr, x, y, t.height, r, g, b, 1)

def _get_normal(World *self, LandFloat x, y) -> LandVector:
    LandFloat s = 9.61
    LandFloat h = world_get_altitude(self, x, y)
    LandFloat ha = world_get_altitude(self, x - s, y)
    LandFloat hb = world_get_altitude(self, x, y - s)
    LandVector a = land_vector(-s, 0, ha - h)
    LandVector b = land_vector(0, -s, hb - h)
    LandVector n = land_vector_normalize(land_vector_cross(a, b))
    return n

def world_get_altitude(World *world, LandFloat x, y) -> LandFloat:
    LandFloat s = 9.61
    Tile *t = world_tile(world, (int)(x + 480) / s, (int)(y + 480) / s)
    return t.height

def world_get_color(World *world, LandFloat x, y) -> LandColor:
    LandFloat s = 9.61 # 9.6 doesn't work?
    Tile *t = world_tile(world, (int)(x + 480) / s, (int)(y + 480) / s)
    return t.color

def world_create_mesh(World *world):
    if not world.mesh:
        world.mesh = mesh_make("world")
    land_triangles_clear(world.mesh.triangles)

    LandCSG *csg = csg_grid(100, 100, None)
    land_csg_transform(csg, land_4x4_matrix_scale(480, 480, 1))
    land_csg_triangles(csg)
    mesh_add_csg(world.mesh, csg)

    land_csg_destroy(csg)
