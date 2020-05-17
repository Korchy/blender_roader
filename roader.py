# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_roader

import bpy
from .roader_curve_monitor import ChangeMonitor


class Roader:

    _curve_tag = 'road_map_basis'
    _mesh_tag = 'road_map_mesh'

    @staticmethod
    def build_road(curve):
        # make road from curve
        # for point in curve.data.splines.active.bezier_points:
        #     print(point.co)
        print(curve)

    @classmethod
    def build_road_map(cls):
        # create road map in the scene
        for curve in cls.road_map_base():
            cls.build_road(curve=curve)

    @classmethod
    def clear_road_map(cls):
        # remove the road map in the scene
        road_map_mesh = cls.road_map_mesh()
        if road_map_mesh:
            bpy.data.objects.remove(road_map_mesh, do_unlink=True)

    @classmethod
    def rebuild_road_map(cls, curve_changed=None):
        # fully recreate the road map in scene
        if curve_changed:
            # maybe for future optimization - if comes from curve_monitoring rebuild road map only in modified curve part
            pass
        cls.clear_road_map()
        cls.build_road_map()

    @classmethod
    def add(cls, objects):
        # add curves to road map basis
        curves = (obj for obj in objects if obj.type == 'CURVE')
        for curve in curves:
            curve[cls._curve_tag] = True
            ChangeMonitor.add(obj=curve, callback=cls.rebuild_road_map)
        cls.rebuild_road_map()

    @classmethod
    def remove(cls, objects):
        # remove curves from road map basis
        curves = (obj for obj in objects if obj.type == 'CURVE')
        for curve in curves:
            del curve[cls._curve_tag]
            ChangeMonitor.remove(obj=curve, callback=cls.rebuild_road_map)
        cls.rebuild_road_map()

    @classmethod
    def road_map_base(cls):
        # get road map curves list
        return (obj for obj in bpy.data.objects if obj.type == 'CURVE' and cls._curve_tag in obj)

    @classmethod
    def road_map_mesh(cls):
        # get road map mesh from the scene
        return next((obj for obj in bpy.data.objects if obj.type == 'MESH' and cls._mesh_tag in obj), None)
