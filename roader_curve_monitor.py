# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_roader

from bpy.app.handlers import depsgraph_update_post


class ChangeMonitor:

    callbacks = []    # don't remove any callbacks after adding - objects stores indices on them

    @classmethod
    def add(cls, obj, callback):
        # add object to monitor
        if callback not in cls.callbacks:
            cls.callbacks.append(callback)
        callback_id = cls.callbacks.index(callback)
        if 'on_change_callbacks' not in obj:
            obj['on_change_callbacks'] = []
        if callback_id not in obj['on_change_callbacks']:
            obj_callbacks = list(obj['on_change_callbacks'])
            obj_callbacks.append(callback_id)
            obj['on_change_callbacks'] = obj_callbacks

    @classmethod
    def remove(cls, obj, callback):
        # remove object callback from monitor
        callback_id = cls.callbacks.index(callback)
        if 'on_change_callbacks' in obj and callback_id in obj['on_change_callbacks']:
            obj_callbacks = list(obj['on_change_callbacks'])
            obj_callbacks.remove(callback_id)
            obj['on_change_callbacks'] = obj_callbacks
        # don't remove any callbacks from cls.callbacks

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

    @classmethod
    def on_depsgraph_update(cls, scene, depsgraph):
        # on depsgraph update
        for obj in depsgraph.updates:
            if obj.is_updated_geometry or obj.is_updated_transform:
                # print(obj.id)
                # print(obj.id.location)
                # print(obj.id.original)
                # print(obj.id.original.location)
                if 'on_change_callbacks' in obj.id:
                    for callback_id in obj.id['on_change_callbacks']:
                        cls.callbacks[callback_id](scene, obj.id)
