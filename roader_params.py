# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_roader

from bpy.props import FloatProperty
from bpy.types import Curve


def register():
    Curve.width = FloatProperty(
        default=0.0
    )


def unregister():
    del Curve.width
