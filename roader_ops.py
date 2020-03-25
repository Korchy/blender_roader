# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_roader

from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .roader import Roader
from .roader_curve_monitor import CurveMonitor
from .console_out import printc
from bpy.props import IntProperty


class ROADER_OT_make_road(Operator):
    bl_idname = 'roader.make_road'
    bl_label = 'Roader: make road'
    bl_description = 'Roader: make road'
    bl_options = {'REGISTER', 'UNDO'}

    mode: IntProperty(
        default=0
    )

    def execute(self, context):
        if self.mode == 0:
            printc('start monitor')
            print('start monitor print')
            CurveMonitor.start()
            self.mode = 1
        else:
            printc('stop monitor')
            CurveMonitor.stop()
            self.mode = 0
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return True


def register():
    register_class(ROADER_OT_make_road)


def unregister():
    unregister_class(ROADER_OT_make_road)
