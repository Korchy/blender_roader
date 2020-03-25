# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_roader

from bpy.types import AddonPreferences
from bpy.props import FloatProperty
from bpy.utils import register_class, unregister_class


class ROADER_preferences(AddonPreferences):
    bl_idname = __package__

    edit_threshold: FloatProperty(
        name='Edit threshold',
        default=0.001
    )

    def draw(self, context):
        self.layout.prop(self, 'edit_threshold')


def register():
    register_class(ROADER_preferences)


def unregister():
    unregister_class(ROADER_preferences)
