# [h] print hLibs

from AppKit import NSColor
from vanilla import *

import hTools2.objects
import hTools2.modules.fontinfo

reload(hTools2.objects)
reload(hTools2.modules.fontinfo)

from hTools2.objects import hFont
from hTools2.modules.fontinfo import *


class hLibs_printDialog(object):

    _title = 'hLibs'
    _padding = 13
    _padding_top = 10
    _row_height = 23
    _button_height = 30
    _button_width =  80
    _width = (_button_width * 2) + (_padding * 2) - 1
    _height = _button_height + (_row_height * 11) + (_padding * 3)
    
    _lib_project = True
    _lib_info = True
    _lib_vmetrics = True
    _lib_accents = True
    _lib_composed = True
    _lib_spacing = True
    _lib_interpol = True
    _lib_groups = True

    def __init__(self):
        self.ufo = CurrentFont()
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        #---------
        # buttons
        #---------
        x = self._padding
        y = self._padding_top
        self.w._select_all = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "(de)select all",
                    value=False,
                    sizeStyle='small',
                    #callback=self._select_all_callback
                    )
        y += self._row_height + self._padding_top
        # button : print data
        self.w.button_print = SquareButton(
                    (x, y - 4,
                    self._button_width,
                    self._button_height),
                    "print",
                    callback=self.print_callback,
                    sizeStyle='small')
        x += self._button_width - 1
        # button : clear data
        self.w.button_clear = SquareButton(
                    (x, y - 4,
                    self._button_width,
                    self._button_height),
                    "clear",
                    #callback=self.clear_callback,
                    sizeStyle='small')
        x += self._button_width - 1
        #------------
        # checkboxes
        #------------
        # accents
        x = self._padding
        y += self._button_height + self._padding_top
        self.w._lib_accents = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "accents lib",
                    value=self._lib_accents,
                    sizeStyle='small')
        y += self._row_height
        # info
        self.w._lib_info = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "info lib",
                    value=self._lib_info,
                    sizeStyle='small')
        y += self._row_height
        # groups
        self.w._lib_groups = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "groups lib",
                    value=self._lib_groups,
                    sizeStyle='small')
        y += self._row_height
        # spacing
        self.w._lib_spacing = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "spacing lib",
                    value=self._lib_groups,
                    sizeStyle='small')
        y += self._row_height
        # interpol
        self.w._lib_interpol = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "interpol lib",
                    value=self._lib_interpol,
                    sizeStyle='small')
        y += self._row_height
        # vmetrics
        self.w._lib_vmetrics = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "vmetrics lib",
                    value=self._lib_vmetrics,
                    sizeStyle='small')
        y += self._row_height

        # open window
        self.w.open()

    # callbacks

    def _select_all_callback(self, sender):
        _value = self.w._select_all.get()
        self.set_values(_value)

    def set_values(self, value):
        self.w._lib_accents.set(value)
        self.w._lib_info.set(value)
        self.w._lib_groups.set(value)
        self.w._lib_spacing.set(value)
        self.w._lib_interpol.set(value)
        self.w._lib_vmetrics.set(value)

    def get_values(self):
        self._lib_accents = self.w._lib_accents.get()
        self._lib_info = self.w._lib_info.set()
        self._lib_groups = self.w._lib_groups.set()
        self._lib_spacing = self.w._lib_spacing.set()
        self._lib_interpol = self.w._lib_interpol.set()
        self._lib_vmetrics = self.w._lib_vmetrics.set()

    def clear_callback(self, sender):
        pass

    def print_callback(self, sender):
        font = hFont(self.ufo)
        if self._lib_groups:
            print '-' * 60
            print 'Groups Lib'
            print '-' * 60
            print font.project.libs['groups'].keys()
            print
        if self._lib_accents:
            print '-' * 60
            print 'Accents Lib'
            print '-' * 60
            print '%s entries.' % len(font.project.libs['accents'].keys())
            print
        if self._lib_interpol:
            print '-' * 60
            print 'Interpol Lib'
            print '-' * 60
            print font.project.libs['interpol'].keys()
            print
        if self._lib_spacing:
            print '-' * 60
            print 'Spacing Lib'
            print '-' * 60
            print font.project.libs['spacing'].keys()
            print
        if self._lib_vmetrics:
            print '-' * 60
            print 'vMetrics Lib'
            print '-' * 60
            print font.project.libs['vmetrics'].keys()
            print
        if self._lib_composed:
            print '-' * 60
            print 'Composed Lib'
            print '-' * 60
            print font.project.libs['composed'].keys()
            print

# run

hLibs_printDialog()
