from prompt_toolkit import Application
from prompt_toolkit.layout import Layout, HSplit, Window, FormattedTextControl
from prompt_toolkit.widgets import TextArea, Frame, RadioList
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style
from prompt_toolkit.filters import Condition
import random, textwrap
from functions import *
from classes import computer_logic
from data_processor import *


def run_settings():
    # Setup Instance Variables for the menu
    config_data = load_data()
    computer = computer_logic()
    computer.name = config_data["name"]
    computer.custom_MOTD = config_data["custom_MOTD_enabled"]
    computer.MOTD_text = config_data["custom_motd"]
    computer.logs_location = config_data["logs_location"]

    if computer.custom_MOTD == False:
        get_motd = motd[random.randrange(len(motd))]
    else: 
        get_motd = computer.MOTD_text

    motd_name = computer.name

    def refresh_logs(app):
        global get_motd, motd_name, config_data, computer
        config_data = load_data()
        computer = computer_logic()
        computer.name = config_data["name"]
        computer.custom_MOTD = config_data["custom_MOTD_enabled"]
        computer.MOTD_text = config_data["custom_motd"]
        computer.logs_location = config_data["logs_location"]

        if computer.custom_MOTD == False:
            get_motd = motd[random.randrange(len(motd))]
        else: 
            get_motd = computer.MOTD_text

        motd_name = computer.name
        app.invalidate()  # Forces a redraw

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
    SETTINGS_ITEMS = [("Set Name", "The Captain's Name! Captain for default,\n  or your own name!", "name"), 
                    ("Set MOTD", "The MOTD! Use a default set or set your own MOTD!\n  Use {captain_name} to use your name!", "custom_motd"), 
                    ("Set Logs Location", "Location to store Captain's Logs! Use the default or\n  your own location!", "logs_location")]

    current_selection = [0]

    scroll_offset = [0]
    max_visible = 15

    editing = [False]
    editing_location = [False]

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
        
        for i, (setting, _, _) in enumerate(visible_entries):
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
        lines.append((f'class:data', 'If you change the Logs location, you will have to\nmanually move your database file from the\ndefault location at /captains_log/storage/logs.\nA new database will be created if none exist!\n\n'))
        lines.append((f'class:data', 'Stay safe among the stars!'))
        return FormattedText(lines)

    def get_setting_details():
        setting = SETTINGS_ITEMS[current_selection[0]]
        lines = [('class:gold', '████')]

        lines.append(('class:gold', '████'))
        lines.append(('', ' '))
        lines.append(('class:header', f' CURRENT VALUES '))
        lines.append(('', ' '))
        lines.append(('class:blue', '██████████████████████'))
        lines.append(('', '\n\n'))
        lines.append(('class:title', f'  Setting: {setting[0]}\n'))
        lines.append(('class:title', f'  {f"Details:\n  {setting[1]}"}\n\n'))
        lines.append(('class:title', '╭───────────────────────────────────────────────╮\n'))
        lines.append(('class:data', f' Current Value:\n\n'))
        lines.append(('class:data', f' "{config_data[setting[2]]}"\n\n'))
        if setting[0] == "Set MOTD":
            lines.append(('class:data', f' "Enabled: {config_data["custom_MOTD_enabled"]}"'))
        return FormattedText(lines)

    def get_footer():
        return FormattedText([
            ('class:title', '╰───────────────────────────────────────────────╯\n'),
            ('class:title', f'  Status: {status_message}\n'),
            ('', '\n'),
            ('class:gold', '███████'),
            ('', ' '),
            ('class:header', ' ↑↓ '),
            ('', ' SELECT  '),
            ('class:header', ' E '),
            ('', ' EDIT  '),
            ('class:orange', ' D '),
            ('', ' DEFAULT '),
            ('class:orange', ' H '),
            ('', ' HOME '),
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
    editor = TextArea(
        text="",
        multiline=False,
        height=1,
    )

    location_editor = TextArea(
        text="",
        multiline=False,
        height=1,
        validator=change_logs_location_question()
    )

    enable_disable = RadioList(
        values=[(True, "Enable"), (False, "Disable")])

    def get_layout():
        if editing[0]:
            if SETTINGS_ITEMS[current_selection[0]][2] == "custom_motd":
                return Layout(HSplit([
                    Window(header_control, height=2),
                    Window(list_control, height=max_visible + 3),
                    Window(content_control, height=5),
                    Frame(editor, title="EDIT SETTING [Ctrl+S save, Esc cancel]"),
                    Frame(enable_disable, title="ENABLE CUSTOM MOTD [Mouse Input]"),
                    Window(footer_control, height=4),
                ]))  
            else:    
                return Layout(HSplit([
                    Window(header_control, height=2),
                    Window(list_control, height=max_visible + 3),
                    Window(content_control, height=5),
                    Frame(editor, title="EDIT SETTING [Ctrl+S save, Esc cancel]"),
                    Window(footer_control, height=4),
                ]))   
        if editing_location[0]:
                return Layout(HSplit([
                    Window(header_control, height=2),
                    Window(list_control, height=max_visible + 3),
                    Window(content_control, height=5),
                    Frame(location_editor, title="EDIT LOG LOCATION [Ctrl+S save, Esc cancel]"),
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
        if editing[0] or editing_location[0]:
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
        if not editing[0] and not editing_location[0]:
            if SETTINGS_ITEMS[current_selection[0]][2] == "logs_location":
                editing_location[0] = True
                location_editor.text = config_data[SETTINGS_ITEMS[current_selection[0]][2]]
                event.app.layout = get_layout()
                event.app.layout.focus(location_editor)
            else:
                editing[0] = True
                editor.text = config_data[SETTINGS_ITEMS[current_selection[0]][2]]
                event.app.layout = get_layout()
                event.app.layout.focus(editor)

    @kb.add('d', filter=editing_active)
    def edit_entry(event):
        if not editing[0] and not editing_title[0] and not creating_log[0] and not deleting_log[0]:
            global status_message
            deleting_log[0] = True
            status_message = f"Default set: {textwrap.shorten(LOG_ENTRIES[current_selection[0]][0], width=23, placeholder="..." )}?"
            event.app.layout = get_layout()

    @kb.add('c-s')
    def save_entry(event):
        global status_message
        if editing[0]:
            if SETTINGS_ITEMS[current_selection[0]][2] == "name":
                computer.name = editor.text
                config_data["name"] = editor.text
                config_json_write(config_data)
                refresh_logs(event.app)
                editing[0] = False
                status_message = f"Name Updated: {textwrap.shorten(editor.text, width=30, placeholder="..." )}"
                event.app.layout = get_layout()
            if SETTINGS_ITEMS[current_selection[0]][2] == "custom_motd":
                computer.MOTD_text = editor.text
                computer.custom_MOTD = enable_disable.current_value
                config_data["custom_motd"] = editor.text
                config_data["custom_MOTD_enabled"] = enable_disable.current_value
                config_json_write(config_data)
                refresh_logs(event.app)
                editing[0] = False
                status_message = f"MOTD Updated: {textwrap.shorten(editor.text, width=30, placeholder="..." )}"
                event.app.layout = get_layout()
        if editing_location[0]:
            buffer = location_editor.buffer
            if buffer.validate():
                computer.logs_location = location_editor.text
                config_data["logs_location"] = location_editor.text
                config_json_write(config_data)
                refresh_logs(event.app)
                create_new_db(location_editor.text, convert_date_to_julian())
                editing_location[0] = False
                status_message = f"Log Location Updated: {textwrap.shorten(location_editor.text, width=30, placeholder="..." )}"
                event.app.layout = get_layout()
            else:
                status_message = buffer.validation_error

    @kb.add('escape')
    def cancel_edit(event):
        if editing[0]:
            editing[0] = False
            event.app.layout = get_layout()
        if editing_location[0]:
            editing_location[0] = False
            event.app.layout = get_layout()

    @kb.add('h', filter=editing_active)
    def quit_app(event):
        event.app.exit()

    @kb.add('H', filter=editing_active)
    def quit_app(event):
        event.app.exit()

    settings_menu = Application(
        layout=get_layout(),
        key_bindings=kb,
        style=LCARS_STYLE,
        full_screen=True,
        mouse_support=True,
    )

    return settings_menu