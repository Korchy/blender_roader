# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_roader

from mathutils import Vector


class BmeshEx:

    @staticmethod
    def row_v(bmesh, point0_co: Vector, point1_co: Vector, number):
        # build row from number of point
        rez = []
        direction = point1_co - point0_co
        for vertex_num in range(number):
            vertex_co = point0_co + (direction * vertex_num / (number - 1))
            vertex = bmesh.verts.new(vertex_co)
            rez.append(vertex)
            # break
        return rez
