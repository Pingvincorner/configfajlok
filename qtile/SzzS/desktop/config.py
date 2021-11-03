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
myTerm = "alacritty"
guiEditor = "/usr/bin/subl"
guiFileman = "/usr/bin/pcmanfm"
wwwBrowser = "/usr/bin/vivaldi-stable"

HomePath = os.path.expanduser("~")
QtileConfigDir = HomePath + "/.config/qtile"
QtileScriptsDir = QtileConfigDir + "/bin"

# Autostart
@hook.subscribe.startup_once
def autostart():
        autobash = QtileScriptsDir + "/autostart.sh"
#       logger.warning(f"Executing autostart file {autobash}")
        subprocess.call([autobash])

wintogroup_rules={
                    "discord": "8",
                    "KeePassXC": "8",
                    "VirtualBox Machine": "9"
                    }

#Új ablakok létrejöttekor lefutó függvény, ami figyeli a speckó alkalmazások elhelyezését
@hook.subscribe.client_new
def WinToGroup(window):
        try:
            wClass = window.window.get_wm_class()
            if( wClass != None and len(wClass) > 0 ):
                for app in wintogroup_rules.keys():
                    if wClass[1] in app:
                        window.togroup(wintogroup_rules[wClass[1]])
#                        window.group.cmd_toscreen(toggle=False)
        except Exception as e:
                logger.error(f"WinToGroup ERROR: {e}")

#Ablak váltásnál megnézzük, hogy a fókusszal rendelkező ablak lebegő-e.
#Ha igen, akkor az előtérbe hozzuk. Ez alaból nem történik meg sajnos.
@hook.subscribe.client_focus
def FloatWinToFront(window):
    try:
        wInfo = window.info()
        if( wInfo['floating'] == True):
            window.cmd_bring_to_front()
    except Exception as e:
        logger.error(f"FloatWinToFront ERROR: {e}")

###+ Egér kattintásra válaszoló függvények
def CpuWidgetClicked():
    #qtile.cmd_spawn( HomePath + "/.config/qtile/bin/displaytopcpu.sh", shell=True )
    qtile.cmd_spawn( "alacritty -e htop", shell=False )

def MemoryWidgetClicked():
    #qtile.cmd_spawn( HomePath + "/.config/qtile/bin/displaytopmemory.sh", shell=True )
    qtile.cmd_spawn( "alacritty -e htop", shell=False )

def CalendarWidgetClicked():
    qtile.cmd_spawn( ["gsimplecal"] )

def ClockWidgetClicked():
    qtile.cmd_spawn( ["xclock"] )

def ShowWindowsListCallback():
    ShowWindowsList(qtile)

def ShowWindowsList(qtile):
    qtile.cmd_spawn("rofi -modi window -show window")

def GetMusicTitle():
    sTitleText=""
    try:
        sTitleText=subprocess.check_output(HomePath+"/.config/qtile/bin/getmusic.sh").decode("utf-8").strip()
    except subprocess.CalledProcessError:
        sTitleText = "♬"
    return sTitleText
###

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
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),desc="Toggle between split and unsplit sides of stack"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="Aktív ablak lebegő mód be- kikapcsolása"),

    # Volumes
    Key([], "XF86AudioRaiseVolume", lazy.spawn( HomePath+"/.config/qtile/bin/volctl fel" ), desc="Hangerő fel" ),
    Key([], "XF86AudioLowerVolume", lazy.spawn( HomePath+"/.config/qtile/bin/volctl le" ), desc="Hangerő le" ),
    Key([], "XF86AudioMute", lazy.spawn( HomePath + "/.config/qtile/bin/volctl kuss" ), desc="Hangerő némítás" ),
    Key([], "XF86Tools", lazy.spawn("pavucontrol"), desc="Hangkeverő futtatása" ),

    # Spotify Multimedia
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),

    #F9-F12 (F11 nem használható: Kikapcsolja a Super4-et!)
    Key([], "XF86Mail", lazy.spawn("thunderbird")),
    Key([], "XF86HomePage", lazy.spawn(wwwBrowser)),
    Key([], "XF86Calculator", lazy.spawn("speedcrunch")),

    #Programok indítása
    Key([mod, "control"], "k", lazy.spawn("xkill"), desc="XKILL indítása beragadt ablak kilövéséhez"),
    Key([mod], "Return", lazy.spawn(myTerm), desc="Launch terminal"),
    Key([mod], "e", lazy.spawn(guiEditor), desc="Grafikus szövegszerkesztő indítása"),
    Key([mod], "f", lazy.spawn(guiFileman), desc="Grafikus fájlkezelő indítása"),
    #++ROFI
    Key([mod], "Escape", lazy.spawn(HomePath+"/.config/qtile/bin/rofi-power.sh"), desc="Rofi Shutdown Menu"),
    Key([mod], "r", lazy.spawn("rofi -modi drun,run -show drun"), desc="Start ROFI with desktop file list"),
    Key(["mod1"], "Tab", lazy.function(ShowWindowsList), desc="ROFI Alt-Tab Window list"),
    #--ROFI
]


common_layoutconfig = dict( border_focus_stack='#EB3E19',
                            border_focus='#EB3E19',
                            border_normal='#151a2b',
                            border_normal_stack='#151a2b',
                            border_on_single=True,
                            border_width=3,
                            margin=8
                        )

layouts = [
    layout.Columns( **common_layoutconfig ),
    layout.Max()
]
groups = [
            Group(name="1",label="1",layout="columns"),
            Group(name="2",label="2",layout="columns"),
            Group(name="3",label="3",layout="columns"),
            Group(name="4",label="4",layout="columns"),
            Group(name="5",label="5",layout="columns"),
            Group(name="6",label="6",layout="columns"),
            Group(name="7",label="7",layout="columns"),
            Group(name="8",label="8",layout="columns"),
            Group(name="9",label="9",layout="columns")
        ]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(toggle=False), desc="Switch to group {}".format(i.name)),

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
                margin=[10,20,5,20],
                opacity=1.0
                )

widget_defaults = dict(
    font='JetBrainsMono Nerd Font Mono',
    fontsize=16,
    padding=2,
    foreground="#ffffff",
    background="#000000"
)

extension_defaults = widget_defaults.copy()
separator_default = dict(padding=10,linewidth=2,size_percent=80,foreground=["#000000","#136ccb"])
textbox_forecolor = "#5a7cd3"

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer( length=15 ),
### Widget Virtual Desktops
                widget.GroupBox(
                    spacing=4,
                    disable_drag=True,
                    use_mouse_wheel=False,
                    highlight_method="block",
                    active="#ffffff",
                    inactive="#545454",
                    block_highlight_text_color="#ffffff",
                    this_current_screen_border="#136ccb",
                    urgent_alert_method="block",
                    urgent_border="#ff0000",
                    urgent_text="#ffffff"
                ),
                widget.Sep( **separator_default ),
### Widget WindowName 
                widget.WindowName(
                    format="{name}",
                    empty_group_string="--nincs aktív ablak--",
                    mouse_callbacks={ 'Button1': ShowWindowsListCallback }
                    ),
                widget.Sep( **separator_default ),
### Windget Media Player
                widget.GenPollText(
                    update_interval=0.5,
                    func=GetMusicTitle,
                    max_chars=80
                    ),
                widget.Sep( **separator_default ),
### Widget Layout Display
                widget.CurrentLayout( foreground=textbox_forecolor ),
                widget.Sep( **separator_default ),
### Widget Date & Clock
                widget.Clock(
                                format="%Y.%m.%d, %A",
                                mouse_callbacks = { 'Button1': CalendarWidgetClicked } 
                            ),
                widget.Clock(
                                format=" %H:%M",
                                mouse_callbacks = { 'Button1': ClockWidgetClicked } 
                            ),
                widget.Sep( **separator_default ),
### Widget CPU Sensor
                widget.ThermalSensor(
                                foreground_alert="ff0000",
                                treshold=80,
                                update_interval=10,
                                show_tag=False,
                                tag_sensor="AMD TSI Addr 98h",
                                mouse_callbacks = { 'Button1': CpuWidgetClicked } 
                            ),
                widget.Sep( **separator_default ),
### Widget.Memory
                widget.Memory(
                                format="{MemUsed: .0f} MB",
                                update_interval=5,
                                mouse_callbacks = { 'Button1': MemoryWidgetClicked }
                            ),
                widget.Sep( **separator_default ),
### Widget Systray
                widget.Spacer( length=6 ),
                widget.Systray( padding=4 ),
                widget.Spacer( length=6 ),
### Widget Quit
                widget.Spacer( background="5E0A00", length=3 ),
                widget.QuickExit(
                                    background="5E0A00",
                                    foreground="FFAEA4",
                                    default_text=" 🗝 ",
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
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    #Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = False
bring_front_click = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
floating_layout = layout.Floating( border_focus='#6B4EDD', border_width=3,
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
                                Match(wm_class='MEGAsync'),
                                Match(wm_class='XClock'),
                                Match(wm_class='Edmarketconnector'),
                                ]
                    )

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
#wmname = "LG3D"

wmname = "QTile"
