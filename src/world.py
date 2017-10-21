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
        
    world_update_mesh(self)
    return self

def world_blotch(World *self, LandFloat px, py, radius, LandColor color):
    int ix = (px + 480) / 10
    int iy = (py + 480) / 10
    int ir = radius / 10
    for int y in range(iy - ir, iy + 1 + ir):
        if y < 0: continue
        if y >= H: break
        for int x in range(ix - ir, ix + 1 + ir):
            if x < 0: continue
            if x >= W: break
            float d = sqrt((x - ix) * (x - ix) + (y - iy) * (y - iy))
            if d > ir:
                continue
            Tile *t = world_tile(self, x, y)
            float i = (ir - d) / ir
            float r = t.color.r * (1 - i) + color.r * i
            float g = t.color.g * (1 - i) + color.g * i
            float b = t.color.b * (1 - i) + color.b * i
            t.color = land_color_rgba(r, g, b, 1)
    world_update_mesh(self)

def world_patch(World *self, LandFloat px, py, r, LandColor color):
    int ix = (px + 480) / 10
    int iy = (py + 480) / 10
    int ir = r / 10
    for int y in range(iy - ir, iy + 1 + ir):
        if y < 0: continue
        if y >= H: break
        for int x in range(ix - ir, ix + 1 + ir):
            if x < 0: continue
            if x >= W: break
            Tile *t = world_tile(self, x, y)
            t.color = color
    world_update_mesh(self)

def world_get_altitude(World *world, LandFloat x, y) -> LandFloat:
    Tile *t = world_tile(world, (int)(x + 480) / 10, (int)(y + 480) / 10)
    return t.height

def world_get_color(World *world, LandFloat x, y) -> LandColor:
    Tile *t = world_tile(world, (int)(x + 480) / 10, (int)(y + 480) / 10)
    return t.color

def _heightmap(World *world, LandCSG *csg):
    LandVector light = {-1, -1, 1}
    for LandCSGPolygon *p in LandArray *csg.polygons:
        for LandCSGVertex *v in LandArray *p.vertices:
            if True:
                LandFloat h = world_get_altitude(world, v.pos.x, v.pos.y)
                v.pos.z += h
                LandVector a = land_vector(-10, 0, world_get_altitude(
                    world, v.pos.x - 10, v.pos.y) - h)
                LandVector b = land_vector(0, -10, world_get_altitude(
                    world, v.pos.x, v.pos.y - 10) - h)
                LandVector n = land_vector_normalize(land_vector_cross(a, b))
                v.normal = n

                LandFloat d = land_vector_dot(v.normal, light)
                d = (1 + d) / 2
                LandColor c = world_get_color(world, v.pos.x, v.pos.y)
                v.rgba = land_color_premul(c.r * d, c.g * d, c.b * d, 1)

def world_update_mesh(World *world):
    if not world.mesh:
        world.mesh = mesh_make()
    land_triangles_clear(world.mesh.triangles)

    LandCSG *csg = csg_grid(100, 100, None)
    land_csg_transform(csg, land_4x4_matrix_scale(480, 480, 1))
    _heightmap(world, csg)
    land_csg_triangles(csg)
    mesh_add_csg(world.mesh, csg)

    land_csg_destroy(csg)
