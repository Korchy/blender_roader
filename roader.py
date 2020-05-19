# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_roader

import bpy
import bmesh
from .roader_curve_monitor import ChangeMonitor
from .roader_curve_tools import BezierTools


class Roader:

    _curve_tag = 'road_map_basis'
    _default_road_width = 1.0
    _mesh_tag = 'road_map_mesh'
    _object_name = 'road map'
    _collection_name = 'road map'

    @classmethod
    def build_road(cls, road_map_object, curve):
        # make road from curve
        # print(curve)
        bm = bmesh.new()
        bm.from_mesh(road_map_object.data)

        for point in curve.data.splines.active.bezier_points:
            # print(point.co)
            v = bm.verts.new(point.co)
        bm.verts.index_update()
        bm.to_mesh(road_map_object.data)
        # bmesh.update_edit_mesh(road_map_object.data)
        bm.free()

    @classmethod
    def build_road_map(cls, scene):
        # create road map in the scene
        road_map_object = cls._road_map_object()
        if not road_map_object:
            road_map_mesh = cls._road_map_mesh()
            if not road_map_mesh:
                road_map_mesh = bpy.data.meshes.new('road_map')
                road_map_mesh[cls._mesh_tag] = True
            road_map_object = bpy.data.objects.new(cls._object_name, road_map_mesh)
            road_map_object[cls._mesh_tag] = True
            road_map_collection = cls._road_map_collection()
            if not road_map_collection:
                road_map_collection = bpy.data.collections.new(cls._collection_name)
                scene.collection.children.link(road_map_collection)
            road_map_collection.objects.link(road_map_object)
        for curve in cls._road_map_base():
            cls.build_road(road_map_object=road_map_object, curve=curve)

    @classmethod
    def clear_road_map(cls, scene):
        # remove the road map in the scene
        road_map_mesh = cls._road_map_object()
        if road_map_mesh:
            bpy.data.objects.remove(road_map_mesh, do_unlink=True)

    @classmethod
    def rebuild_road_map(cls, scene, curve_changed=None):
        # fully recreate the road map in scene
        if curve_changed:
            # maybe for future optimization - if comes from curve_monitoring rebuild road map only in modified curve part
            pass
        cls.clear_road_map(scene=scene)
        cls.build_road_map(scene=scene)

    @classmethod
    def add_curve_to_map(cls, scene, objects):
        # add curves to road map basis
        curves = (obj for obj in objects if obj.type == 'CURVE')
        for curve in curves:
            curve[cls._curve_tag] = True
            curve.data.width = cls._default_road_width
            ChangeMonitor.add(obj=curve, callback=cls.rebuild_road_map)
        cls.rebuild_road_map(scene=scene)

    @classmethod
    def remove_curve_from_map(cls, scene, objects):
        # remove curves from road map basis
        curves = (obj for obj in objects if obj.type == 'CURVE')
        for curve in curves:
            del curve[cls._curve_tag]
            ChangeMonitor.remove(obj=curve, callback=cls.rebuild_road_map)
        cls.rebuild_road_map(scene=scene)

    @classmethod
    def init_road_map_interactive_change(cls):
        # add all road map curves to interactive change
        for curve in cls._road_map_base():
            ChangeMonitor.add(obj=curve, callback=cls.rebuild_road_map)

    @classmethod
    def stop_road_map_interactive_change(cls):
        # remove all road map curves from interactive change
        for curve in cls._road_map_base():
            ChangeMonitor.remove(obj=curve, callback=cls.rebuild_road_map)

    @classmethod
    def _road_map_base(cls):
        # get road map curves list
        return (obj for obj in bpy.data.objects if obj.type == 'CURVE' and cls._curve_tag in obj)

    @classmethod
    def _road_map_object(cls):
        # get road map object from the scene
        return next((obj for obj in bpy.data.objects if obj.type == 'MESH' and cls._mesh_tag in obj), None)

    @classmethod
    def _road_map_mesh(cls):
        # get road map mesh from the scene
        return next((obj for obj in bpy.data.meshes if cls._mesh_tag in obj), None)

    @classmethod
    def _road_map_collection(cls):
        # get road map collection from the scene
        return next((collection for collection in bpy.data.collections if collection.name == cls._collection_name), None)
