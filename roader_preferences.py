# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_roader

from bpy.types import AddonPreferences
from bpy.props import FloatProperty, BoolProperty
from bpy.utils import register_class, unregister_class
from .roader import Roader
from .roader_curve_monitor import ChangeMonitor


class ROADER_preferences(AddonPreferences):
    bl_idname = __package__

    edit_threshold: FloatProperty(
        name='Edit threshold',
        default=0.1
    )

    interactive_update: BoolProperty(
        name='Interactive update',
        default=False,
        update=lambda self, context: self._on_interactive_update_change(
            self=self,
            context=context
        )
    )

    def draw(self, context):
        self.layout.prop(self, 'edit_threshold')

    @staticmethod
    def _on_interactive_update_change(self, context):
        # on interactive update change
        if self.interactive_update:
            print('start interactive update')
            Roader.init_road_map_interactive_change()
            ChangeMonitor.start()
        else:
            print('stop interactive update')
            ChangeMonitor.stop()
            Roader.stop_road_map_interactive_change()


def register():
    register_class(ROADER_preferences)


def unregister():
    unregister_class(ROADER_preferences)
