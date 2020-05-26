# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_roader

from bpy.props import FloatProperty
from bpy.types import Curve
from .roader import Roader


def register():
    Curve.width = FloatProperty(
        default=1.0,
        min=0.1,
        update=lambda self, context: Roader.rebuild_road_map(
            scene=context.scene
        )
    )


def unregister():
    del Curve.width
