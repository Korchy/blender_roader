# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_roader

import builtins
import sys
import bpy


def printc(*args, clear=False):
    # output to console
    for area in bpy.context.screen.areas:
        if area.type == 'CONSOLE':
            context = dict()
            context['area'] = area
            context['space_data'] = area.spaces.active
            context['region'] = area.regions[-1]
            context['window'] = bpy.context.window
            context['screen'] = bpy.context.screen
            output = ' '.join([str(arg) for arg in args])
            if clear:
                bpy.ops.console.clear(context)
            for line in output.split('\n'):
                bpy.ops.console.scrollback_append(context, text=line)


def exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # Let the system handle things like CTRL+C
        sys.__excepthook__(*args)
    printc('Exception: ', exc_type, exc_value, exc_traceback)


sys.excepthook = exception_handler

class printc_class(object):
    # def __init__(self, f):
    #     self.f = open(f, 'w')

    # def __enter__(self):
    #     return self   # return instance of A which is assign to `f`.

    def write(self, text):
        sys.__stdout__.write(text)  # print to the shell
        print('write')
        printc(text)

class stdoutOverride:
    def write(self, text):
        printc(text)
        sys.__stdout__.write(repr(text))

sys.stdout = stdoutOverride()
