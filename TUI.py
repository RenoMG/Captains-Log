from prompt_toolkit import Application
from prompt_toolkit.layout import Layout, HSplit, VSplit, Window, FormattedTextControl
from prompt_toolkit.widgets import TextArea, Frame
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML, FormattedText
from prompt_toolkit.styles import Style
from datetime import datetime
import os, random, subprocess, webbrowser
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

# Sample log entries (à la USS Yamato)
LOG_ENTRIES = [
    ("45236.4", "J.L. PICARD", "USS ENTERPRISE", "Arrived at Neutral Zone..."),
    ("45234.1", "J.L. PICARD", "USS ENTERPRISE", "Diplomatic mission to Romulus..."),
    ("45231.8", "J.L. PICARD", "USS ENTERPRISE", "Encountered anomaly near..."),
    ("42591.4", "D. VARLEY", "USS YAMATO", "Discovered Iconian gateway..."),
    ("42587.2", "D. VARLEY", "USS YAMATO", "System malfunctions continue..."),
]

print(list_log_data())

current_selection = [0]

def get_header():
    stardate = f"{45000 + (datetime.now().timetuple().tm_yday / 10):.1f}"
    return FormattedText([
        ('class:gold', '█████████'),
        ('', ' '),
        ('class:header', f'  FILE = CAPTAIN\'S LOG  '),
        ('', ' '),
        ('class:gold', '███'),
        ('', ' '),
        ('class:orange', '██'),
        ('', '  '),
        ('class:stardate', f'STARDATE {stardate}'),
        ('', '\n'),
    ])

def get_log_list():
    lines = [('class:title', '╭─── ACCESS FILE = CAPTAIN\'S LOG ───────────────╮\n')]
    
    for i, (sd, captain, ship, _) in enumerate(LOG_ENTRIES):
        if i == current_selection[0]:
            marker = ('class:status-on', ' ● ')
            style = 'class:text bold'
        else:
            marker = ('class:status-off', ' ○ ')
            style = 'class:data'
        
        lines.append(marker)
        lines.append((style, f'{ship:<16} STARDATE {sd}  {captain}\n'))
    
    lines.append(('class:title', '╰────────────────────────────────────────────────╯'))
    return FormattedText(lines)

def get_log_content():
    sd, captain, ship, content = LOG_ENTRIES[current_selection[0]]
    return FormattedText([
        ('class:gold', '████'),
        ('', ' '),
        ('class:header', f' {captain} '),
        ('', ' '),
        ('class:blue', '██████████████████████'),
        ('', '\n\n'),
        ('class:title', f'  Captain\'s Log - Stardate {sd}\n'),
        ('class:title', f'  {ship}\n\n'),
        ('class:data', f'  {content}\n'),
        ('', '\n'),
        ('class:gold', '██'),
        ('', ' '),
        ('class:orange', '██'),
        ('', ' '),
        ('class:blue', '███'),
        ('', ' '),
        ('class:status-on', '● REC'),
        ('', '  '),
        ('class:status-off', '○ ENCRYPT'),
        ('', '  '),
        ('class:status-on', '● ARCHIVE'),
    ])

def get_footer():
    return FormattedText([
        ('', '\n'),
        ('class:gold', '███████'),
        ('', ' '),
        ('class:header', ' ↑↓ '),
        ('', ' SELECT  '),
        ('class:header', ' E '),
        ('', ' EDIT  '),
        ('class:header', ' N '),
        ('', ' NEW  '),
        ('class:orange', ' Q '),
        ('', ' QUIT  '),
        ('class:gold', '████████████████'),
    ])

# Controls
list_control = FormattedTextControl(get_log_list)
content_control = FormattedTextControl(get_log_content)
header_control = FormattedTextControl(get_header)
footer_control = FormattedTextControl(get_footer)

# Editor (hidden initially)
editor = TextArea(
    text="",
    multiline=True,
    wrap_lines=True,
    height=6,
)

editing = [False]

def get_layout():
    if editing[0]:
        return Layout(HSplit([
            Window(header_control, height=2),
            Window(list_control, height=len(LOG_ENTRIES) + 2),
            Window(content_control, height=8),
            Frame(editor, title="EDIT LOG ENTRY [Ctrl+S save, Esc cancel]"),
            Window(footer_control, height=2),
        ]))
    else:
        return Layout(HSplit([
            Window(header_control, height=2),
            Window(list_control, height=len(LOG_ENTRIES) + 2),
            Window(content_control, height=10),
            Window(footer_control, height=2),
        ]))

kb = KeyBindings()

@kb.add('up')
def nav_up(event):
    if not editing[0]:
        current_selection[0] = max(0, current_selection[0] - 1)

@kb.add('down')
def nav_down(event):
    if not editing[0]:
        current_selection[0] = min(len(LOG_ENTRIES) - 1, current_selection[0] + 1)

@kb.add('e')
def edit_entry(event):
    if not editing[0]:
        editing[0] = True
        editor.text = LOG_ENTRIES[current_selection[0]][3]
        event.app.layout = get_layout()
        event.app.layout.focus(editor)

@kb.add('c-s')
def save_entry(event):
    if editing[0]:
        sd, captain, ship, _ = LOG_ENTRIES[current_selection[0]]
        LOG_ENTRIES[current_selection[0]] = (sd, captain, ship, editor.text)
        editing[0] = False
        event.app.layout = get_layout()

@kb.add('escape')
def cancel_edit(event):
    if editing[0]:
        editing[0] = False
        event.app.layout = get_layout()

@kb.add('n')
def new_entry(event):
    if not editing[0]:
        stardate = f"{45000 + (datetime.now().timetuple().tm_yday / 10):.1f}"
        LOG_ENTRIES.insert(0, (stardate, "J.L. PICARD", "USS ENTERPRISE", "New log entry..."))
        current_selection[0] = 0
        editing[0] = True
        editor.text = "New log entry..."
        event.app.layout = get_layout()
        event.app.layout.focus(editor)

@kb.add('q')
def quit_app(event):
    if not editing[0]:
        event.app.exit()

app = Application(
    layout=get_layout(),
    key_bindings=kb,
    style=LCARS_STYLE,
    full_screen=True,
    mouse_support=True,
)

if __name__ == '__main__':
    app.run()