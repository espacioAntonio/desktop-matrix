#!/usr/bin/env python
# -.- encoding: utf-8 -.-

'''
OS Dependences: python-gobject package
'''

import os
import ctypes
import platform
import logging
import signal
import random
import threading

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango
import cairo

COLUMNS = 30
CHARS = 20


def set_name(new_name):
    if platform.system() != 'Linux':
        logging.warning('Rename process:Unsupported platform')
    try:
        libc = ctypes.CDLL('libc.so.6')
        libc.prctl(15, new_name, 0, 0, 0)
        return True
    except:
        logging.warning("Rename process failed :PID: " + repr(os.getpid()))
    return False


class WaterMark(Gtk.Window):

    def __init__(self):
        super(WaterMark, self).__init__()
        self.setup()
        self.init_ui()

    def setup(self):
        self.set_app_paintable(True)
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)
        self.set_keep_below(True)

        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)

    def generate_label(self):
        lbl = Gtk.Label()
        lbl.set_max_width_chars(1)
        lbl.set_line_wrap(True)
        lbl.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        lbl.set_text(" \n" * 20)
        fd = Pango.FontDescription("Serif 20")
        lbl.modify_font(fd)
        lbl.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse("#BBB"))
        lbl.set_yalign(0)
        return lbl

    def init_ui(self):

        self.connect("draw", self.on_draw)

        self.box = Gtk.Box(spacing=6)
        self.add(self.box)

        self.chars_int = range(48, 58) +\
            range(65382, 65438)
#            range(404, 448) +\
#            range(564, 688) +\
#            range(931, 1124) +\
#            range(65382, 65438)

        self.labels = []
        for x in xrange(0, COLUMNS):
            lbl = self.generate_label()
            self.box.pack_start(lbl, True, True, 0)
            self.labels.append(lbl)

        lbtn = Gtk.Label()
        lbtn.set_text("⚪")
        fd = Pango.FontDescription("Serif 20")
        lbtn.modify_font(fd)
        lbtn.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse("gray"))
        lbtn.set_has_window(True)
        lbtn.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        lbtn.connect("button-press-event", self.on_button_clicked)
        self.box.pack_start(lbtn, True, True, 0)

        root_win = Gdk.get_default_root_window()
        root_height = root_win.get_height()
        root_width = root_win.get_width()
        logging.info("Desktop-size: " +
                     repr(root_width) + "x" + repr(root_height))

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        w_width, w_height = self.get_size()
        logging.info("Window-size: " + repr(w_width) + "x" + repr(w_height))
        #self.move(root_width - w_width - 10, root_height - w_height - 10)
        #self.resize(root_width / 4, root_height / 4)
        self.move(100, 100)
        for x in xrange(0, COLUMNS):
            t = random.uniform(1, 5)
            threading.Timer(t, self.update_lbl, [self.labels[x]]).start()

    def on_button_clicked(self, widget, event):
        if widget.get_text() == "⚪":
            self.set_keep_below(False)
            widget.set_text("⚫")
        else:
            self.set_keep_below(True)
            widget.set_text("⚪")

    def on_draw(self, wid, cr):
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

    def update_lbl(self, lbl):
        t = random.uniform(0.8, 1.8)
        threading.Timer(t, self.update_lbl, [lbl]).start()
        text = unichr(random.choice(self.chars_int))
        newtxt = text + lbl.get_text().decode('utf-8')[:CHARS - 1]
        lbl.set_text(newtxt)
        #print lbl.get_allocation().width, lbl.get_allocation().height, len(newtxt), len(self.labels)


def main():
        logging.basicConfig(level=logging.DEBUG)
        set_name("matrix-gtk.py")
        WaterMark()
        Gtk.main()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
