import common
import world

class Mesh:
    LandTriangles *triangles

LandVector light = {-1, -1, 1}

def mesh_make -> Mesh*:
    Mesh *mesh
    land_alloc(mesh)
    mesh.triangles = land_triangles_new()
    return mesh

def _colorize(LandCSG *csg, LandColor rgba):
    for LandCSGPolygon *p in LandArray *csg.polygons:
        for LandCSGVertex *v in LandArray *p.vertices:
            LandFloat d = land_vector_dot(v.normal, light)
            LandFloat b = (1 + d) / 2
            v.rgba = land_color_premul(rgba.r * b, rgba.g * b, rgba.b * b, 1)

def _heightmap(LandCSG *csg):
    for LandCSGPolygon *p in LandArray *csg.polygons:
        for LandCSGVertex *v in LandArray *p.vertices:
            if v.pos.z > 0:
                LandFloat h = world_height(v.pos.x, v.pos.y)
                v.pos.z += h
                LandVector a = land_vector(-0.1, 0, world_height(v.pos.x - 0.1, v.pos.y) - h)
                LandVector b = land_vector(0, -0.1, world_height(v.pos.x, v.pos.y - 0.1) - h)
                LandVector n = land_vector_normalize(land_vector_cross(a, b))
                v.normal = n

def mesh_add(Mesh* mesh, str what, LandColor rgba, Land4x4Matrix matrix):
    LandCSG *csg = None
    if land_equals(what, "ball"):
        csg = csg_sphere(8, 8, None)

    if land_equals(what, "cylinder"):
        csg = csg_cylinder(6, None)

    if land_equals(what, "grid"):
        csg = csg_block(100, 100, 1, True, None)

    land_csg_transform(csg, matrix)

    if land_equals(what, "grid"):
        _heightmap(csg)
    
    _colorize(csg, rgba)
    land_csg_triangles(csg)
    mesh_add_csg(mesh, csg)
    
def mesh_add_csg(Mesh *self, LandCSG* csg):
    for LandCSGPolygon *t in LandArray *csg.polygons:
        for int j in range(3):
            LandCSGVertex *vec = land_array_get_nth(t.vertices, j)
            land_add_vertex(self.triangles,
                vec.pos.x, vec.pos.y, vec.pos.z,
                0, 0, vec.rgba.r, vec.rgba.g, vec.rgba.b, vec.rgba.a)

def mesh_draw(Mesh *mesh, Land4x4Matrix matrix):
    land_display_transform_4x4(&matrix)
    land_triangles_draw(mesh.triangles)
