# vim: tabstop=4 softtabstop=4 expandtab
# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
import socket
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from typing import List  # noqa: F401

mod = "mod4"
myTerm = "lxterminal"
HomePath = os.path.expanduser("~")

# Autostart
@hook.subscribe.startup_once
def autostart():
    autobash = HomePath + "/bin/autostart.sh"
    subprocess.call([autobash])


###+ Alkalmazásindító függvények
def ShowRofi_Editors(qtile):
    qtile.cmd_spawn("python " + HomePath + "/bin/rofi-scripts/rofi-editconfigs.py") )

def ShowNetworkConnectionEditor(qtile):
    qtile.cmd_spawn(myTerm + " -t 'Edit Network Connections' -e 'sleep 0.5; nmtui-edit'")

def ShowNetworkConnectionConnect(qtile):
    qtile.cmd_spawn(myTerm + " -t 'Select Network Connection' -e 'sleep 0.5; nmtui-connect'")

def MemoryWidgetClicked():
    #Egér klikk a Memory widget-en
    qtile.cmd_spawn(myTerm+ " -e 'sleep 0.5; htop'",shell=True)

def CalendarWidgetClicked():
    #Egér klikk a Calendar widget-en
    qtile.cmd_spawn(myTerm + " -e 'sleep 0.5; cal -wmn2; read'",shell=True)
###-

keys = [
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(myTerm), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Start ROFI"),
    Key([mod], "e", lazy.function(ShowRofi_Editors)),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="Aktív ablak lebegő mód be- kikapcsolása"),

    # == volumes
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pulseaudio-ctl up")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pulseaudio-ctl down")),
    Key([], "XF86AudioMute", lazy.spawn("pulseaudio-ctl mute")),
    Key([mod], "XF86AudioRaiseVolume", lazy.spawn("pavucontrol")),
    Key([mod], "XF86AudioLowerVolume", lazy.spawn("pavucontrol")),
    Key([mod], "XF86AudioMute", lazy.spawn("pavucontrol")),

    #Networks
    Key([mod], "c", lazy.function(ShowNetworkConnectionConnect)),
    Key([mod, "shift"], "c", lazy.function(ShowNetworkConnectionEditor))
]

groups = [Group(i) for i in "1234"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(toggle=False),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layouts = [
    layout.Columns(border_focus_stack='#ff0000',
                    border_focus='#ff0000',
                    border_width=2,
                    margin=2),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Terminus',
    fontsize=14,
    padding=3,
)
extension_defaults = widget_defaults.copy()


screens = [
    Screen(
        top=bar.Bar(
            [
### Widget Layout Display
                widget.Sep(padding=1,linewidth=0),
                widget.CurrentLayout( background="#0D112C" ),
### Widget Virtual Desktops
                widget.TextBox(
                                padding=0,
                                fontsize=24,
                                font="Font Awesome 5 Free",
                                text="\u25e2",
                                foreground="000000",
                                background="0d112c"
                                ),
                widget.GroupBox(),
### Widget Active Window
                widget.TextBox(
                                padding=0,
                                fontsize=24,
                                font="Font Awesome 5 Free",
                                text="\u25e2",
                                foreground="26445a",
                                background="000000"
                                ),
                widget.TextBox(
                                background="26445a",
                                foreground="99b5c9",
                                font="Font Awesome 5 Free",
                                text="\uf2d0",
                            ),
                widget.WindowName(
                                    background="26445a",
                                    foreground="99b5c9"
                                ),
### Widget Systray
                widget.TextBox(
                                padding=0,
                                fontsize=24,
                                font="Font Awesome 5 Free",
                                text="\u25e2",
                                foreground="000000",
                                background="26445a"
                                ),
                widget.Systray(),
### Widget Clock
               widget.TextBox(
                                padding=0,
                                fontsize=24,
                                font="Font Awesome 5 Free",
                                text="\u25e2",
                                foreground="571800",
                                background="000000"
                                ),
                widget.TextBox(
                                background="571800",
                                foreground="ff7700",
                                font="Font Awesome 5 Free",
                                text="\uf073",
                                mouse_callbacks = { 'Button1': CalendarWidgetClicked }
                            ),
                widget.Clock(
                                background="571800",
                                foreground="ff7700",
                                format="%Y.%m.%d %H:%M",
                                mouse_callbacks = { 'Button1': CalendarWidgetClicked } 
                            ),
### Widget CPU Sensor
                widget.TextBox(
                                padding=0,
                                fontsize=24,
                                font="Font Awesome 5 Free",
                                text="\u25e2",
                                foreground="304630",
                                background="571800"
                                ),
                widget.TextBox(
                                background="304630",
                                foreground="ffffff",
                                text="\uf2c9",
                                font="Font Awesome 5 Free",
                            ),
                widget.ThermalSensor(
                                background="304630",
                                foreground="ffffff",
                                foreground_alert="ff0000",
                                treshold=80,
                                show_tag="CPU",
                            ),
### Widget.Memory
                widget.TextBox(
                                padding=0,
                                fontsize=24,
                                font="Font Awesome 5 Free",
                                text="\u25e2",
                                foreground="000d4e",
                                background="304630"
                                ),
                widget.TextBox(
                                background="000d4e",
                                foreground="ffffff",
                                text="\uf538",
                                font="Font Awesome 5 Free",
                                mouse_callbacks = { 'Button1': MemoryWidgetClicked }
                            ),
                widget.Memory(
                                background="000d4e",
                                foreground="ffffff",
                                format="{MemUsed: 0.f} MB",
                                mouse_callbacks = { 'Button1': MemoryWidgetClicked }
                            ),
### Widget Battery
                widget.TextBox(
                                padding=0,
                                fontsize=24,
                                text="\u25e2",
                                font="Font Awesome 5 Free",
                                foreground="3a0069",
                                background="000d4e"
                                ),
                widget.TextBox(
                                text="\uf242",
                                font="Font Awesome 5 Free",
                                foreground="e000ef",
                                background="3a0069"
                                ),
                widget.Battery(
                                background="3A0069",
                                foreground="E000EF",
                                full_char="\u2295",
                                empty_char="\u2296",
                                charge_char="\u21AF",
                                discharge_char="\u21A7",
                                format="{char}:{percent:2.0%} ~{hour:d}:{min:02d}"
                                ),
### Widget Quit
                widget.TextBox(
                                padding=0,
                                fontsize=24,
                                font="Font Awesome 5 Free",
                                text="\u25e2",
                                foreground="#5E0A00",
                                background="#3A0069"
                                ),
                widget.QuickExit(
                                    background="#5E0A00",
                                    foreground="#FFAEA4",
                                    default_text="\u23FB Kilépés",
                                    countdown_format="{} Kilépés"
                                ),
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='doublecmd', title='Opciók') #DoubleCommander settings window
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
