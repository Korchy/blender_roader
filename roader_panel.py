# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_roader

from bpy.types import Panel
from bpy.utils import register_class, unregister_class


class ROADER_PT_panel(Panel):
    bl_idname = 'ROADER_PT_panel'
    bl_label = 'Roader'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Roader'

    def draw(self, context):
        operator = self.layout.operator('roader.make_road', icon='BLENDER', text='roader execute')


def register():
    register_class(ROADER_PT_panel)


def unregister():
    unregister_class(ROADER_PT_panel)
