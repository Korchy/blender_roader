# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_roader

from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .roader import Roader


class ROADER_OT_add_curve(Operator):
    bl_idname = 'roader.add_curve_to_road_map_base'
    bl_label = 'Add curve to road map base'
    bl_description = 'Roader: add curve to road map base'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # add selected curves to road map basis
        Roader.add(objects=context.selected_objects)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return context.selected_objects


class ROADER_OT_remove_curve(Operator):
    bl_idname = 'roader.remove_curve_from_road_map_base'
    bl_label = 'Remove curve from road map base'
    bl_description = 'Roader: remove curve from road map base'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # remove selected curves from road map basis
        Roader.remove(objects=context.selected_objects)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return context.selected_objects


class ROADER_OT_rebuild_roads(Operator):
    bl_idname = 'roader.rebuild_roads'
    bl_label = 'Rebuild roads'
    bl_description = 'Roader: rebuild roads'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # remove selected curves from road map basis
        Roader.rebuild_road_map()
        return {'FINISHED'}


def register():
    register_class(ROADER_OT_add_curve)
    register_class(ROADER_OT_remove_curve)
    register_class(ROADER_OT_rebuild_roads)


def unregister():
    unregister_class(ROADER_OT_rebuild_roads)
    unregister_class(ROADER_OT_remove_curve)
    unregister_class(ROADER_OT_add_curve)
