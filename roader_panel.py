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
        layout = self.layout
        if context.preferences.addons[__package__].preferences.interactive_update:
            layout.prop(context.preferences.addons[__package__].preferences, 'interactive_update', icon='CANCEL', toggle=True)
        else:
            layout.prop(context.preferences.addons[__package__].preferences, 'interactive_update', icon='PLAY', toggle=True)
        layout.operator('roader.add_curve_to_road_map_base', icon='PLUS')
        layout.operator('roader.remove_curve_from_road_map_base', icon='PANEL_CLOSE')
        layout.separator()
        layout.operator('roader.rebuild_roads', icon='FILE_REFRESH')


def register():
    register_class(ROADER_PT_panel)


def unregister():
    unregister_class(ROADER_PT_panel)
