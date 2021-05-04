# vim: tabstop=4 softtabstop=4 expandtab ai
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
from libqtile.log_utils import logger

mod = "mod4"
myTerm = "termite"
HomePath = os.path.expanduser("~")

# Autostart
@hook.subscribe.startup_once
def autostart():
        autobash = HomePath + "/.config/qtile/autostart.sh"
        logger.warning(f"Executing autostart file {autobash}")
        subprocess.call([autobash])

#Új ablakok létrejöttekor lefutó függvény, ami figyeli a speckó alkalmazások elhelyezését
wintogroup_rules={
                    "Steam": "4",
                    "Lutris": "4",
                    "Edmarketconnector": "4",
                    "discord": "5",
                    "Spotify": "6",
                    "KeePassXC": "7"
                    }

@hook.subscribe.client_new
def WinToGroup(window):
        wClass = window.window.get_wm_class()[1]
        for app in wintogroup_rules.keys():
                if wClass in app:
                        window.togroup(wintogroup_rules[wClass])
                        window.group.cmd_toscreen(toggle=False)


###+ Egér kattintásra válaszoló függvények
def CpuWidgetClicked():
    qtile.cmd_spawn( "$HOME/.config/qtile/bin/displaytopcpu.sh", shell=True )

def MemoryWidgetClicked():
    qtile.cmd_spawn( "$HOME/.config/qtile/bin/displaytopmemory.sh", shell=True )

def CalendarWidgetClicked():
    bashScript = HomePath + "/.config/qtile/bin/showcalendar.sh"
    qtile.cmd_spawn( [myTerm,"-e",bashScript] )
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
    Key(["mod1"], "Tab", lazy.spawn("rofi -show window"), desc="Start ROFI"),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="Aktív ablak lebegő mód be- kikapcsolása"),

    # Volumes
    Key([], "XF86AudioRaiseVolume", lazy.spawn( HomePath + "/.config/qtile/bin/volctl fel" ), desc="Hangerő fel" ),
    Key([], "XF86AudioLowerVolume", lazy.spawn( HomePath + "/.config/qtile/bin/volctl le" ), desc="Hangerő le" ),
    Key([], "XF86AudioMute", lazy.spawn( HomePath + "/.config/qtile/bin/volctl kuss" ), desc="Hangerő némítás" ),
    Key([], "XF86Tools", lazy.spawn("pavucontrol"), desc="Hangkeverő futtatása" ),

    # Spotify Multimedia
    Key([], "XF86AudioStop", lazy.spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Pause")),
    Key([], "XF86AudioPrev", lazy.spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous")),
    Key([], "XF86AudioPlay", lazy.spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause")),
    Key([], "XF86AudioNext", lazy.spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next")),
#
    #F9-F12 (F11 nem használható: Kikapcsolja a Super4-et!)
    Key([], "XF86Mail", lazy.spawn("thunderbird")),
    Key([], "XF86HomePage", lazy.spawn("firefox")),
    Key([], "XF86Calculator", lazy.spawn("speedcrunch")),
]


common_layoutconfig = dict( border_focus_stack='#4e82dd',
                            border_focus='#4e82dd',
                            border_width=3,
                            margin=8
                        )

layouts = [
    layout.Columns( **common_layoutconfig ),
    layout.Max(),
    layout.Floating( border_focus='#6B4EDD', border_width=3,
                    float_rules=[
                                # Run the utility of `xprop` to see the wm class and name of an X client.
                                *layout.Floating.default_float_rules,
                                Match(wm_class='confirmreset'),  # gitk
                                Match(wm_class='makebranch'),  # gitk
                                Match(wm_class='maketag'),  # gitk
                                Match(title='branchdialog'),  # gitk
                                Match(wm_class='ssh-askpass'),  # ssh-askpass
                                Match(title='pinentry'),  # GPG key password entry
                                Match(wm_class='Gpick'),  # Gtk Color picker
                                Match(wm_class='Gcolor3'),  # Gtk Color picker
                                Match(wm_class='MEGAsync'),  # Megasync windows
                                Match(wm_class='Doublecmd', title='Opciók'), #DoubleCommander
                                Match(wm_class='Doublecmd', title='Fájl(ok) másolása'), #DoubleCommander
                                Match(wm_class='Doublecmd', title='Fájl(ok) mozgatása') #DoubleCommander
                                ]
                    )
]
groups = [
            Group(name="1",label="\uf80b\uf17c",layout="columns"),
            Group(name="2",label="\uf80c\uf17c",layout="columns"),
            Group(name="3",label="\uf80d\uf17c",layout="columns"),
            Group(name="4",label="\uf80e\uf1b6", layout="floating"), #GAMES
            Group(name="5",label="\uf80f\uf392",layout="columns"), #Discord
            Group(name="6",label="\uf810\uf1bc",layout="columns"), #Spotify
            Group(name="7",label="\uf811\ue60a",layout="columns"), #KeepassXC
        ]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

bar_parameters=dict(
                background="#000000",
                margin=[10,20,0,20],
                opacity=1
                )

widget_defaults = dict(
    font='Ubuntu',
    fontsize=16,
    padding=2,
    foreground="#ffffff",
    background="#000000"
)
extension_defaults = widget_defaults.copy()

separator_default = dict(padding=10,linewidth=2,size_percent=60,foreground=["#000000","#136ccb"])

textbox_forecolor = "#b3d2e4"

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer( length=6 ),
### Widget Virtual Desktops
                widget.GroupBox(
                    block_highlight_text_color="#8bd6ff",
                    disable_drag=True,
                    highlight_method="border",
                    borderwidth=2,
                    this_current_screen_border="#136ccb",
                    inactive="#545454"
                ),
                widget.Sep( **separator_default ),
### Widget Task List 
                widget.TextBox( text="\uf2d2", foreground=textbox_forecolor),
                widget.TaskList(
                        fontsize=14,
                        margin_y=4,
                        padding=4,
                        spacing=4,
                        highlight_method="block",
                        border="#136ccb",
                        unfocused_border="#2b2b2b",
                        txt_floating="\uf069 ",
                        txt_maximized="\uf077 ",
                        txt_minimized="\uf078 "
                        ),
                widget.Sep( **separator_default ),
### Widget Layout Display
                widget.CurrentLayoutIcon( scale= 0.5, foreground=textbox_forecolor ),
                widget.CurrentLayout( ),
                widget.Sep( **separator_default ),
### Widget Clock
                widget.TextBox(
                                text="\uf073", foreground=textbox_forecolor,
                                mouse_callbacks = { 'Button1': CalendarWidgetClicked }
                            ),
                widget.Clock(
                                format="%Y.%m.%d %H:%M",
                                mouse_callbacks = { 'Button1': CalendarWidgetClicked } 
                            ),
                widget.Sep( **separator_default ),
### Widget CPU Sensor
                widget.TextBox( text="\ue350", foreground=textbox_forecolor ),
                widget.ThermalSensor(
                                foreground_alert="ff0000",
                                treshold=80,
                                show_tag=False,
                                tag_sensor="AMD TSI Addr 98h",
                                mouse_callbacks = { 'Button1': CpuWidgetClicked } 
                            ),
                widget.Sep( **separator_default ),
### Widget.Memory
                widget.TextBox(
                                text="\uf145", foreground=textbox_forecolor,
                                mouse_callbacks = { 'Button1': MemoryWidgetClicked }
                            ),
                widget.Memory(
                                format="{MemUsed} MB",
                                update_interval=2,
                                mouse_callbacks = { 'Button1': MemoryWidgetClicked }
                            ),
                widget.Sep( **separator_default ),
### Widget Systray
                widget.Spacer( length=6 ),
                widget.Systray( padding=3 ),
                widget.Spacer( length=6 ),
### Widget Quit
                widget.Spacer( background="5E0A00", length=3 ),
                widget.QuickExit(
                                    background="5E0A00",
                                    foreground="FFAEA4",
                                    default_text=" \uf011 ",
                                    countdown_format=" {} "
                                ),
                widget.Spacer( background="5E0A00", length=3 ),
            ],
            size=32,
            **bar_parameters
        )
    )
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
follow_mouse_focus = False
bring_front_click = True
cursor_warp = False
floating_layout = layouts[2]
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
