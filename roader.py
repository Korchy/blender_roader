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
            source_loop = None
            source_loop_first = None
            dest_loop = None
            # all spline points
            spline_points = spline.bezier_points[:]
            # if spline is closed
            if spline.use_cyclic_u:
                spline_points.append(spline.bezier_points[0])
            # for every point of the spline
            for first_point, next_point in zip(spline_points, spline_points[1:]):
                # get list of all points by resolution
                all_points = [[None, first_point.handle_left, first_point.co, first_point.handle_right, None], ]     # add first point data
                for point_index in range(spline.resolution_u - 1):
                    point_data = BezierTools.count_new_point_data(
                        point0_co=first_point.co,
                        point0_handle_right=first_point.handle_right,
                        point1_handle_left=next_point.handle_left,
                        point1_co=next_point.co,
                        t=(point_index + 1) * (1 / spline.resolution_u)
                    )
                    all_points.append(point_data)
                all_points.append([None, next_point.handle_left, next_point.co, next_point.handle_right, None])     # add last point data
                # make bridge for all segments of all points
                for f_point, n_point in zip(all_points, all_points[1:]):
                    source_loop, dest_loop = cls._build_segment(
                        bm=bm,
                        curve=curve,
                        point0_hl=f_point[1],
                        point0_co=f_point[2],
                        point0_hr=f_point[3],
                        point1_hl=n_point[1],
                        point1_co=n_point[2],
                        point1_hr=n_point[3],
                        source_loop=dest_loop,
                        dest_loop=(source_loop_first if spline.use_cyclic_u and n_point == all_points[-1] and next_point == spline_points[-1] else None)
                    )
                    if spline.use_cyclic_u and source_loop_first is None:
                        source_loop_first = source_loop
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
            # todo: for future optimization - if comes from curve_monitoring rebuild road map only in modified curve part
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
    def _build_segment(cls, bm, curve, point0_hl, point0_co, point0_hr, point1_hl, point1_co, point1_hr, source_loop=None, dest_loop=None):
        # built grid segment from bezier point0 to point1
        # if source_loop of dest_loop != None - use this vertices loops to build segment
        z_normal = Vector((0.0, 0.0, 1.0))
        # start loop
        if source_loop is None:
            source_loop_point0_co = (point0_hr - point0_co).cross(z_normal)
            source_loop_point0_co.normalize()
            source_loop_point0_co *= curve.data.width
            source_loop_point0_co += point0_co
            source_loop_point0_co = curve.matrix_world @ source_loop_point0_co
            source_loop_point1_co = (point0_hl - point0_co).cross(z_normal)
            source_loop_point1_co.normalize()
            source_loop_point1_co *= curve.data.width
            source_loop_point1_co += point0_co
            source_loop_point1_co = curve.matrix_world @ source_loop_point1_co
            source_loop = BmEx.row_v(
                bmesh=bm,
                point0_co=source_loop_point0_co,
                point1_co=source_loop_point1_co,
                resolution=curve.data.resolution_u+1
            )
        # dest loop
        if dest_loop is None:
            source_loop_point0_co = (point1_hr - point1_co).cross(z_normal)
            source_loop_point0_co.normalize()
            source_loop_point0_co *= curve.data.width
            source_loop_point0_co += point1_co
            source_loop_point0_co = curve.matrix_world @ source_loop_point0_co
            source_loop_point1_co = (point1_hl - point1_co).cross(z_normal)
            source_loop_point1_co.normalize()
            source_loop_point1_co *= curve.data.width
            source_loop_point1_co += point1_co
            source_loop_point1_co = curve.matrix_world @ source_loop_point1_co

            # todo: try to find external dest loop to connect the rad
            dest_loop = cls._get_dest_loop_from_existed_vertices(
                bm=bm,
                point0_co=source_loop_point0_co,
                point1_co=source_loop_point1_co
            )

            if dest_loop is None:
                dest_loop = BmEx.row_v(
                    bmesh=bm,
                    point0_co=source_loop_point0_co,
                    point1_co=source_loop_point1_co,
                    resolution=curve.data.resolution_u+1
                )
        BmEx.bridge(bmesh=bm, source_loop=source_loop, dest_loop=dest_loop)
        return source_loop, dest_loop

    @classmethod
    def _get_dest_loop_from_existed_vertices(cls, bm, point0_co, point1_co):
        # get dest loop from existing vertices
        dest_loop = None

        # todo: try to find external dest loop to connect the rad

        # road_map_mesh = cls._road_map_mesh()
        # # check for point 0
        # closest = (None, None)
        # for vertex in bm.verts:
        #     if (vertex.co - point0_co).length < bpy.context.preferences.addons[__package__].preferences.edit_threshold:
        #
        #         print(len(vertex.link_edges))
        #
        #         if closest[0] is None or (vertex.co - point0_co).length < closest[1]:
        #             closest = (vertex, (vertex.co - point0_co).length)
        #
        return dest_loop

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
