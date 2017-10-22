import common
import world
import game

class Mesh:
    char *name
    LandTriangles *triangles
    LandArray *frames # Mesh

LandVector light = {-1, -1, 1}

def mesh_make(str name) -> Mesh*:
    Mesh *mesh
    land_alloc(mesh)
    mesh.name = land_strdup(name)
    mesh.triangles = land_triangles_new()
    return mesh

def mesh_destroy(Mesh* self):
    if self.frames:
        for Mesh *m in LandArray *self.frames:
            if m != self:
                mesh_destroy(m)
        land_array_destroy(self.frames)
    land_triangles_destroy(self.triangles)
    land_free(self.name)
    land_free(self)

def _colorize(LandCSG *csg, LandColor rgba):
    for LandCSGPolygon *p in LandArray *csg.polygons:
        for LandCSGVertex *v in LandArray *p.vertices:
            LandFloat d = land_vector_dot(v.normal, light)
            LandFloat b = (1 + d) / 2
            v.rgba = land_color_premul(rgba.r * b, rgba.g * b, rgba.b * b, 1)

def mesh_add_anim(Mesh *mesh, Mesh *anim):
    if not mesh.frames:
        mesh.frames = land_array_new()
    land_array_add(mesh.frames, anim)

def mesh_add(Mesh* mesh, str what, LandColor rgba, Land4x4Matrix matrix):
    LandCSG *csg = None
    if land_equals(what, "ball"):
        csg = csg_sphere(8, 8, None)

    if land_equals(what, "cylinder"):
        csg = csg_cylinder(6, None)

    if land_equals(what, "cone"):
        csg = csg_cone(6, None)

    land_csg_transform(csg, matrix)

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

def mesh_update_vertex(Mesh *self, int i, float x, y, z, r, g, b, a):
    
    land_update_vertex(self.triangles, i, x, y, z, 0, 0, r, g, b, a)

def mesh_draw(Mesh *mesh, Land4x4Matrix matrix):
    land_display_transform_4x4(&matrix)
    land_triangles_draw(mesh.triangles)
