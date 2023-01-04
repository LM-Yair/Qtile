import os
import subprocess

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# --- Colors ---

mainColor = "#444444"
highLightColor="#61dafb"
fontType = "Hack Nerd Font"
fontColor = "#f5f5f5"
fontColorInactive = "#888888"
fontSize = 14
heightBar = 25
green = "#0ca611"

# --- layouts --

borderWidth=2
borderActive="#d4d4d4"
borderNormal="#777777"

# --------------

mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    # -------- Mapeos

    Key([mod], "k", lazy.spawn("kitty"), desc="Launch Kitty"),
    Key([mod], "Return", lazy.spawn("alacritty"), desc="Launch terminal Alacritty"),
    Key([mod, "shift"], "f", lazy.spawn("firefox"), desc="Launch Firefox"),
    Key([mod, "shift"], "c", lazy.spawn("chromium"), desc="Launch Chrome"),
    Key([mod, "shift"], "l", lazy.spawn("libreoffice"), desc="Launch LibreOffice"),
    Key([mod, "shift"], "m", lazy.spawn("rofi -show drun"), desc="Launch Rofi"),
    Key([mod], "m", lazy.spawn("kitty -e ranger"), desc="Launch file manager Ranger"),
    Key([mod], "x", lazy.spawn("scrot -s '/home/lazaro/Desktop/screenshots/screenshot_%d-%m-%y_$wx$hpx.png'"), desc="Take Screenshots"),

    # --------

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

# Nerd Fonts Icons
icons = [ 
    " ", # - nf-linux-archlinux
    "",  # - nf-mdi-firefox
    "力", # - nf-mdi-server
    "",  # - nf-cod-debug
    " ", # - nf-cod-github_inverted
    # " ",  # - nf-fa-chrome
    # "",  # - nf-cod-bookmark
    ' ', # nf-linux-docker
]

groups = [Group(i) for i in icons]

for i, group in enumerate(groups):
    numberDesc = str(i + 1)
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                numberDesc,
                lazy.group[group.name].toscreen(),
                desc="Switch to group {}".format(group.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                numberDesc,
                lazy.window.togroup(group.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(group.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(
        margin=2, 
        border_width=borderWidth,
        border_focus=borderActive,
        border_normal=borderNormal,
    ),
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
    font=fontType,
    fontsize=fontSize,
    padding=4,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    foreground="#61dafb",
                    borderwidth=2,
                    active=fontColor,
                    inactive=fontColorInactive,
                    highlight_method='line',
                    highlight_color="#666666",
                    this_current_screen_border=fontColor,
                ),
                # widget.Prompt(),
                widget.TextBox(text="| ", foreground=fontColor), # nf-fa-thermometer_2
                widget.ThermalZone(high=49, crit=55),
                widget.TextBox(text="|", foreground=fontColor),

                widget.Spacer(),
                
                widget.Systray(),
                widget.PulseVolume(),
                widget.TextBox(text="墳", foreground=fontColor), # nf-mdi-volume_high
                widget.TextBox(text="", foreground=green), # nf-mdi-battery_charging
                widget.Battery(format="{percent:2.0%}"),
                widget.Clock(format="  %a %d/%m/%Y   %I:%M "),
                widget.TextBox(text="", foreground=fontColor), # nf-cod-layout
                widget.CurrentLayout(),
                # widget.QuickExit(default_text="|   ", countdown_format="{} ﰸ |"), # nf-mdi-cancel
            ],
            heightBar,
            background=mainColor,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.Popen([home + '/.config/qtile/autostart.sh'])
