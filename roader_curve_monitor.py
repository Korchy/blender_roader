# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_roader

from bpy.app.handlers import depsgraph_update_post


class CurveMonitor:

    @classmethod
    def start(cls):
        # start monitor changes
        if cls.on_depsgraph_update not in depsgraph_update_post:
            depsgraph_update_post.append(cls.on_depsgraph_update)

    @classmethod
    def stop(cls):
        # stop monitor changes
        if cls.on_depsgraph_update in depsgraph_update_post:
            depsgraph_update_post.remove(cls.on_depsgraph_update)

    @staticmethod
    def on_depsgraph_update(cls):
        # on depsgraph update
        print('update')
