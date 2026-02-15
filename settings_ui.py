from prompt_toolkit import Application
from prompt_toolkit.layout import Layout, HSplit, Window, FormattedTextControl
from prompt_toolkit.widgets import TextArea, Frame
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style
from prompt_toolkit.filters import Condition
import random, textwrap
from functions import *
from classes import computer_logic
from data_processor import *

# Setup Instance Variables for the menu
config_data = load_data()
computer = computer_logic()
computer.name = config_data["name"]
computer.custom_MOTD = config_data["custom_MOTD_enabled"]
computer.MOTD_text = config_data["custom_motd"]
computer.editor = config_data["editor"]
computer.logs_location = config_data["logs_location"]

if computer.custom_MOTD == False:
    get_motd = motd[random.randrange(len(motd))]
else: 
    get_motd = computer.MOTD_text

motd_name = computer.name

# LCARS color scheme
LCARS_STYLE = Style.from_dict({
    'header': 'bg:#cc99ff #000000 bold',      # Lavender bar
    'gold': 'bg:#ffcc66 #000000',              # Gold/tan bar
    'orange': 'bg:#ff7700 #000000',            # Orange accent
    'blue': 'bg:#99ccff #000000',              # Blue bar
    'text': '#ff9944',                          # Orange text
    'title': '#cc99ff bold',                    # Lavender titles
    'data': '#99ccff',                          # Cyan data
    'stardate': '#ffcc66',                      # Gold text
    'status-on': '#00ff00',                     # Green dot
    'status-off': '#666666',                    # Dim dot
    'border': '#cc99ff',                        # Border color
})

#TUI Variables
SETTINGS_ITEMS = [("Set Name", "The Captain's Name! Captain for default,\n  or your own name!"), 
                  ("Set MOTD", "The MOTD! Use a default set or set your own MOTD!\n  Use {captain_name} to use your name!"), 
                  ("Set Logs Location", "Location to store Captain's Logs! Use the default or\n  your own location!")]

current_selection = [0]

scroll_offset = [0]
max_visible = 15

editing = [False]
editing_title = [False]
creating_log = [False]
deleting_log = [False]

status_message = "Settings Loaded!"

def get_header():
    return FormattedText([
        ('class:gold', '█████████'),
        ('', ' '),
        ('class:header', f'  FILE = SETTINGS  '),
        ('', ' '),
        ('class:gold', '███'),
        ('', ' '),
        ('class:orange', '██'),
        ('', ' '),
        ('class:stardate', f'JULIANDATE {convert_date_to_julian()}'),
        ('', ' '),
        ('class:orange', '█'),
        ('', '\n'),
        ('class:title', f'MOTD: {textwrap.shorten(get_motd.format(captain_name=motd_name), width=60, placeholder="..." )}\n\n'),
        ('', '\n'),
    ])

def get_settings_list():
    lines = [('class:title', '╭─── ACCESS FILE = SETTINGS ────────────────────╮\n')]

    visible_entries = SETTINGS_ITEMS[scroll_offset[0]:scroll_offset[0] + max_visible]
    
    for i, (setting, _) in enumerate(visible_entries):
        actual_index = i + scroll_offset[0]
        if actual_index == current_selection[0]:
            marker = ('class:status-on', ' ● ')
            style = 'class:text bold'
        else:
            marker = ('class:status-off', ' ○ ')
            style = 'class:data'
        
        lines.append(marker)
        lines.append((style, f'{setting}\n'))
    
    total = len(SETTINGS_ITEMS)
    lines.append(('class:title', f' ○ Showing {scroll_offset[0]+1}-{min(scroll_offset[0]+max_visible, total)} of {total} SETTINGS\n'))
    lines.append(('class:title', f'╰───────────────────────────────────────────────╯\n'))
    lines.append((f'class:data', 'Some helpful information:\n\n'))
    lines.append((f'class:data', 'Use {captain_name} to insert your name into a\ncustom MOTD!\n\n'))
    lines.append((f'class:data', 'If you change the Logs location, you will have to\nmanually move your database file from the\ndefault location at /captains_log/storage/logs.\n\n'))
    lines.append((f'class:data', 'Stay safe among the stars!'))
    return FormattedText(lines)

def get_setting_details():
    setting = SETTINGS_ITEMS[current_selection[0]]
    return FormattedText([
        ('class:gold', '████'),
        ('', ' '),
        ('class:header', f' CURRENT VALUES '),
        ('', ' '),
        ('class:blue', '██████████████████████'),
        ('', '\n\n'),
        ('class:title', f'  Setting: {setting[0]}\n'),
        ('class:title', f'  {f"Details:\n  {setting[1]}"}\n\n'),
        ('class:title', '╭───────────────────────────────────────────────╮\n'),
        ('class:data', f'{textwrap.indent(textwrap.fill(setting[1], width=45, placeholder=" ...", replace_whitespace=False), "  ")}\n')
    ])

def get_footer():
    return FormattedText([
        ('class:title', '╰───────────────────────────────────────────────╯\n'),
        ('class:title', f'  Status: {status_message}\n'),
        ('', '\n'),
        ('class:gold', '███████'),
        ('', ' '),
        ('class:header', ' ↑↓ '),
        ('', ' SELECT  '),
        ('class:header', ' E / R '),
        ('', ' EDIT  '),
        ('class:header', ' C '),
        ('', ' NEW  '),
        ('class:orange', ' D '),
        ('', ' DEL '),
        ('class:orange', ' Q '),
        ('', ' QUIT  '),
        ('class:gold', '███'),
    ])

# Controls
list_control = FormattedTextControl(get_settings_list)
content_control = FormattedTextControl(get_setting_details)
header_control = FormattedTextControl(get_header)
footer_control = FormattedTextControl(get_footer)

# Editor (hidden initially)
editor_title = TextArea(
    text="",
    multiline=False,
    height=1,
)

editor = TextArea(
    text="",
    multiline=True,
    wrap_lines=True,
    height=16,
)

def refresh_logs(app):
    app.invalidate()  # Forces a redraw

def get_layout():
    if editing[0]:
        return Layout(HSplit([
            Window(header_control, height=2),
            Window(list_control, height=max_visible + 3),
            Window(content_control, height=5),
            Frame(editor, title="EDIT LOG ENTRY [Ctrl+S save, Esc cancel]"),
            Window(footer_control, height=4),
        ]))   
    else:
        return Layout(HSplit([
            Window(header_control, height=2),
            Window(list_control, height=max_visible + 3),
            Window(content_control, height=23),
            Window(footer_control, height=4),
        ]))

kb = KeyBindings()

@Condition
def editing_active():
    if editing[0]:
        return False
    else:
        return True
    
@Condition
def delete_confirm():
    if deleting_log[0] == False:
        return False
    else:
        return True

@kb.add('up', filter=editing_active)
def nav_up(event):
    current_selection[0] = max(0, current_selection[0] - 1)
    if current_selection[0] < scroll_offset[0]:
        scroll_offset[0] = current_selection[0]

@kb.add('down', filter=editing_active)
def nav_down(event):
    current_selection[0] = min(len(SETTINGS_ITEMS) - 1, current_selection[0] + 1)
    if current_selection[0] >= scroll_offset[0] + max_visible:
        scroll_offset[0] = current_selection[0] - max_visible + 1

@kb.add('e', filter=editing_active)
def edit_entry(event):
    if not editing[0] and not editing_title[0] and not creating_log[0] and not deleting_log[0]:
        editing[0] = True
        editor.text = SETTINGS_ITEMS[current_selection[0]][2]
        event.app.layout = get_layout()
        event.app.layout.focus(editor)

@kb.add('d', filter=editing_active)
def edit_entry(event):
    if not editing[0] and not editing_title[0] and not creating_log[0] and not deleting_log[0]:
        global status_message
        deleting_log[0] = True
        status_message = f"Delete Log: {textwrap.shorten(LOG_ENTRIES[current_selection[0]][0], width=23, placeholder="..." )}?"
        event.app.layout = get_layout()

@kb.add('y', filter=delete_confirm)
def confirm_yes(event):
    if not editing[0] and not editing_title[0] and not creating_log[0]:
        global status_message
        status_message = f"Deleted Log: {textwrap.shorten(LOG_ENTRIES[current_selection[0]][0], width=23, placeholder="..." )}"
        delete_log(LOG_ENTRIES[current_selection[0]][0])
        refresh_logs(event.app)
        deleting_log[0] = False

@kb.add('n', filter=delete_confirm)
def confirm_no(event):
    if not editing[0] and not editing_title[0] and not creating_log[0]:
        global status_message
        deleting_log[0] = False
        status_message = "Log Deletion Aborted!"

@kb.add('c-s')
def save_entry(event):
    global status_message
    if editing[0]:
        editor.title = LOG_ENTRIES[current_selection[0]][0]
        edit_log(editor.title, editor.text)
        refresh_logs(event.app)
        editing[0] = False
        status_message = f"Edited Log: {textwrap.shorten(editor.title, width=23, placeholder="..." )}"
        event.app.layout = get_layout()

@kb.add('escape')
def cancel_edit(event):
    if editing[0]:
        editing[0] = False
        event.app.layout = get_layout()

@kb.add('q', filter=editing_active)
def quit_app(event):
    event.app.exit()

@kb.add('Q', filter=editing_active)
def quit_app(event):
    event.app.exit()

app = Application(
    layout=get_layout(),
    key_bindings=kb,
    style=LCARS_STYLE,
    full_screen=True,
    mouse_support=True,
)

app.run()
