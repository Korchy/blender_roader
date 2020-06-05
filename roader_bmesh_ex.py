# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_roader

from mathutils import Vector


class BmeshEx:

    @staticmethod
    def row_v(bmesh, point0_co: Vector, point1_co: Vector, resolution):
        # build row from number of point
        rez = []
        direction = point1_co - point0_co
        for vertex_num in range(resolution):
            vertex_co = point0_co + (direction * vertex_num / (resolution - 1))
            vertex = bmesh.verts.new(vertex_co)
            vertex.select = True
            rez.append(vertex)
        bmesh.verts.index_update()
        return rez

    @staticmethod
    def bridge(bmesh, source_loop, dest_loop):
        # build simple quad bridge from vertices source_loop to vertices dest_loop
        if source_loop and dest_loop:
            for source_loop_vertex_pair, dest_loop_vertex_pair in zip(zip(source_loop, source_loop[1:]), zip(dest_loop, dest_loop[1:])):
                face = bmesh.faces.new([source_loop_vertex_pair[1], source_loop_vertex_pair[0], dest_loop_vertex_pair[0], dest_loop_vertex_pair[1]])
                face.select = True
        bmesh.faces.index_update()
