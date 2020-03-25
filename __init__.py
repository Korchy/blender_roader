# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_roader

from . import roader_ops
from . import roader_panel
from . import roader_preferences
from .addon import Addon


bl_info = {
    'name': 'Roader',
    'category': 'All',
    'author': 'Nikita Akimov',
    'version': (1, 0, 0),
    'blender': (2, 82, 0),
    'location': 'N-Panel > Roader',
    'wiki_url': 'https://b3d.interplanety.org/en/blender-add-on-roader/',
    'tracker_url': 'https://b3d.interplanety.org/en/blender-add-on-roader',
    'description': 'Easy making roads'
}


def register():
    if not Addon.dev_mode():
        roader_ops.register()
        roader_panel.register()
        roader_preferences.register()
    else:
        print('It seems you are trying to use the dev version of the ' + bl_info['name'] + ' add-on. It may work not properly. Please download and use the release version!')


def unregister():
    if not Addon.dev_mode():
        roader_preferences.unregister()
        roader_panel.unregister()
        roader_ops.unregister()


if __name__ == '__main__':
    register()
