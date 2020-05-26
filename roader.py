# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_roader

import bpy
import bmesh
from mathutils import Vector
from .roader_curve_monitor import ChangeMonitor
from .roader_curve_tools import BezierTools
from .roader_bmesh_ex import BmeshEx as BmEx


class Roader:

    _curve_tag = 'road_map_basis'
    _default_road_width = 1.0
    _mesh_tag = 'road_map_mesh'
    _object_name = 'road map'
    _collection_name = 'road map'

    @classmethod
    def build_road(cls, road_map_object, curve):
        # make road from curve
        bm = bmesh.new()
        bm.from_mesh(road_map_object.data)
        for spline in curve.data.splines:
            for first_point, next_point in zip(spline.bezier_points, spline.bezier_points[1:]):
                print(first_point.co, next_point.co)
                cls._build_segment(
                    bm=bm,
                    curve=curve,
                    bezier_point0=first_point,
                    bezier_point1=next_point
                )
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
        road_map_object = cls._road_map_object()
        if road_map_object:
            bpy.data.objects.remove(road_map_object, do_unlink=True)
        road_map_mesh = cls._road_map_mesh()
        if road_map_mesh:
            bpy.data.meshes.remove(road_map_mesh)

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
    def _build_segment(cls, bm, curve, bezier_point0, bezier_point1, verts0=None, verts1=None):
        # built grid segment from bezier point0 to point1
        z_normal = Vector((0.0, 0.0, 1.0))
        point0_co = (bezier_point0.handle_right - bezier_point0.co).cross(z_normal)
        point0_co.normalize()
        point0_co *= curve.data.width
        point0_co += bezier_point0.co
        point0_co = curve.matrix_world @ point0_co
        point1_co = (bezier_point0.handle_left - bezier_point0.co).cross(z_normal)
        point1_co.normalize()
        point1_co *= curve.data.width
        point1_co += bezier_point0.co
        point1_co = curve.matrix_world @ point1_co
        # print('p0,p1', point0_co, point1_co)
        row = BmEx.row_v(bmesh=bm, point0_co=point0_co, point1_co=point1_co, number=curve.data.resolution_u+1)
        # print(row)

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
