import common

class Mesh:
    LandTriangles *triangles

def mesh_make -> Mesh*:
    Mesh *mesh
    land_alloc(mesh)
    mesh.triangles = land_triangles_new()
    return mesh

def mesh_add(Mesh* mesh, str what, Land4x4Matrix matrix):
    if land_equals(what, "ball"):
        LandCSG* csg = csg_sphere(4, 4, None)
        land_csg_transform(csg, matrix)
        land_csg_triangles(csg)
        mesh_add_csg(mesh, csg)

    if land_equals(what, "cylinder"):
        LandCSG* csg = csg_cylinder(4, None)
        land_csg_transform(csg, matrix)
        land_csg_triangles(csg)
        mesh_add_csg(mesh, csg)
    
def mesh_add_csg(Mesh *self, LandCSG* csg):
    for LandCSGPolygon *t in LandArray *csg.polygons:
        for int j in range(3):
            LandCSGVertex *vec = land_array_get_nth(t.vertices, j)
            land_add_vertex(self.triangles, vec.pos.x, vec.pos.y, vec.pos.z,
                0, 0, 1, 1, 1, 1)

def mesh_draw(Mesh *mesh, Land4x4Matrix matrix):
    land_display_transform_4x4(&matrix)
    land_triangles_draw(mesh.triangles)
