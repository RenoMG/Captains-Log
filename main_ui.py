from prompt_toolkit import Application
from prompt_toolkit.layout import Layout, HSplit, Window, FormattedTextControl
from prompt_toolkit.widgets import TextArea, Frame
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style
from prompt_toolkit.filters import Condition
import random, textwrap
from functions import convert_date_to_julian
from classes import computer_logic
from database.db import list_log_names, list_all_log_data, edit_log, edit_log_title, create_log, delete_log
from config.config import load_data, motd
from settings_ui import run_settings as settings_app

def run_main():
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

    def check_motd_captain_name():
        if "{captain_name}" in get_motd:
            return get_motd.format(captain_name=motd_name)
        else:
            return get_motd

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
    LOG_ENTRIES = list_all_log_data()

    current_selection = [0]

    scroll_offset = [0]
    max_visible = 15

    editing = [False]
    editing_title = [False]
    creating_log = [False]
    deleting_log = [False]

    status_message = "Boot Success!"

    def get_header():
        return FormattedText([
            ('class:gold', '█████████'),
            ('', ' '),
            ('class:header', f'  FILE = CAPTAIN\'S LOG  '),
            ('', ' '),
            ('class:gold', '███'),
            ('', ' '),
            ('class:orange', '██'),
            ('', ' '),
            ('class:stardate', f'JULIANDATE {convert_date_to_julian()}'),
            ('', ' '),
            ('class:orange', '█'),
            ('', '\n'),
            ('class:title', f'MOTD: {textwrap.shorten(check_motd_captain_name(), width=60, placeholder="..." )}\n\n'),
            ('', '\n'),
        ])

    def get_log_list():
        lines = [('class:title', '╭─── ACCESS FILE = CAPTAIN\'S LOG ───────────────╮\n')]

        visible_entries = LOG_ENTRIES[scroll_offset[0]:scroll_offset[0] + max_visible]
        
        for i, (title, jd, _) in enumerate(visible_entries):
            actual_index = i + scroll_offset[0]
            if actual_index == current_selection[0]:
                marker = ('class:status-on', ' ● ')
                style = 'class:text bold'
            else:
                marker = ('class:status-off', ' ○ ')
                style = 'class:data'
            
            lines.append(marker)
            lines.append((style, f'{f"{textwrap.shorten('Enterprise NX-01', width=17, placeholder="..." )}"} DATE {jd}  {f"{textwrap.shorten(computer.name, width=12, placeholder=f"{computer.name[:9]}..." )}"}\n'))
        
        total = len(LOG_ENTRIES)
        lines.append(('class:title', f' ○ Showing {scroll_offset[0]+1}-{min(scroll_offset[0]+max_visible, total)} of {total} LOGS\n'))
        lines.append(('class:title', f'╰───────────────────────────────────────────────╯'))
        return FormattedText(lines)

    def get_log_content():
        try: 
            title, jd, body = LOG_ENTRIES[current_selection[0]]
            return FormattedText([
                ('class:gold', '████'),
                ('', ' '),
                ('class:header', f' {textwrap.shorten(computer.name, width=25, placeholder=f"{computer.name[:20]}..." )} '),
                ('', ' '),
                ('class:blue', '██████████████████████'),
                ('', '\n\n'),
                ('class:title', f'  Title: {textwrap.shorten(title, width=40, placeholder="..." )}\n'),
                ('class:title', f'  Juliandate: {jd}\n'),
                ('class:title', f'  {f"Ship: {textwrap.shorten('Enterprise NX-01', width=40, placeholder="..." )}"}\n\n'),
                ('class:title', f'  {"Log Excerpt:"}\n\n'),
                ('class:title', '╭───────────────────────────────────────────────╮\n'),
                ('class:data', f'{textwrap.indent(textwrap.fill(body, width=45, placeholder=" ...", replace_whitespace=False), "  ")}\n')
            ])
        except Exception as e:
            current_selection[0] = max(0, current_selection[0] - 1)
            if current_selection[0] < scroll_offset[0]:
                scroll_offset[0] = current_selection[0]
            refresh_logs(main_app)
            return FormattedText([
                ('class:gold', '████'),
                ('', ' '),
                ('class:header', f' {textwrap.shorten(computer.name, width=25, placeholder=f"{computer.name[:20]}..." )} '),
                ('', ' '),
                ('class:blue', '██████████████████████'),
                ('', '\n\n'),
                ('class:title', f'  Title: A log in the void\n'),
                ('class:title', f'  Juliandate: {convert_date_to_julian()}\n'),
                ('class:title', f'  {f"Ship: {textwrap.shorten('Enterprise NX-01', width=40, placeholder="..." )}"}\n\n'),
                ('class:title', f'  {"Log Excerpt:"}\n\n'),
                ('class:title', '╭───────────────────────────────────────────────╮\n'),
                ('class:data', f'{textwrap.indent(textwrap.fill("""Well, seems like you either just deleted your last log or have no logs at all? Hmm, better get to typing! You dont want me calling the Romulans, right?
                                                                Does this count as an Easter Egg, or just bad programming?""", width=45, placeholder=" ...", replace_whitespace=False), "  ")}\n')
            ])

    def get_footer():
        return FormattedText([
            ('class:title', '╰───────────────────────────────────────────────╯\n'),
            ('class:title', f'  Status: {status_message}\n'),
            ('', '\n'),
            ('class:gold', '█'),
            ('', ' '),
            ('class:header', ' ↑↓ '),
            ('', ' SELECT  '),
            ('class:header', ' E / R '),
            ('', ' EDIT  '),
            ('class:header', ' C '),
            ('', ' NEW  '),
            ('class:orange', ' D '),
            ('', ' DEL '),
            ('class:orange', ' S '),
            ('', ' SETTINGS  '),
            ('class:orange', ' Q '),
            ('', ' QUIT  '),
            ('class:gold', '█'),
        ])

    # Controls
    list_control = FormattedTextControl(get_log_list)
    content_control = FormattedTextControl(get_log_content)
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

    def refresh_config_data():
        nonlocal get_motd, motd_name, config_data, computer
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

    def refresh_logs(main_app):
        nonlocal LOG_ENTRIES
        LOG_ENTRIES = list_all_log_data()
        main_app.invalidate()  # Forces a redraw

    def get_layout():
        if editing[0]:
            return Layout(HSplit([
                Window(header_control, height=2),
                Window(list_control, height=max_visible + 3),
                Window(content_control, height=5),
                Frame(editor, title="EDIT LOG ENTRY [Ctrl+S save, Esc cancel]"),
                Window(footer_control, height=4),
            ]))
        elif editing_title[0]:
            return Layout(HSplit([
                Window(header_control, height=2),
                Window(list_control, height=max_visible + 3),
                Window(content_control, height=6),
                Frame(editor_title, title="EDIT TITLE [Ctrl+S save, Esc cancel]"),
                Window(footer_control, height=4),
            ]))      
        elif creating_log[0]:
            return Layout(HSplit([
                Window(header_control, height=2),
                Window(list_control, height=max_visible + 3),
                Window(content_control, height=6),
                Frame(editor_title, title="CREATE LOG - TITLE [Ctrl+S save, Esc cancel]"),
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
        if editing[0] or editing_title[0] or creating_log[0]:
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
        current_selection[0] = min(len(LOG_ENTRIES) - 1, current_selection[0] + 1)
        if current_selection[0] >= scroll_offset[0] + max_visible:
            scroll_offset[0] = current_selection[0] - max_visible + 1

    @kb.add('e', filter=editing_active)
    def edit_log_content(event):
        if not editing[0] and not editing_title[0] and not creating_log[0] and not deleting_log[0]:
            editing[0] = True
            editor.text = LOG_ENTRIES[current_selection[0]][2]
            event.app.layout = get_layout()
            event.app.layout.focus(editor)

    @kb.add('r', filter=editing_active)
    def rename_log(event):
        if not editing[0] and not editing_title[0] and not creating_log[0] and not deleting_log[0]:
            editing_title[0] = True
            editor_title.text = LOG_ENTRIES[current_selection[0]][0]
            editor.text = LOG_ENTRIES[current_selection[0]][2]
            event.app.layout = get_layout()
            event.app.layout.focus(editor_title)

    @kb.add('d', filter=editing_active)
    def default_value(event):
        if not editing[0] and not editing_title[0] and not creating_log[0] and not deleting_log[0]:
            nonlocal status_message
            deleting_log[0] = True
            status_message = f"Delete Log: {textwrap.shorten(LOG_ENTRIES[current_selection[0]][0], width=23, placeholder="..." )}?"
            event.app.layout = get_layout()

    @kb.add('y', filter=delete_confirm)
    def confirm_yes(event):
        if not editing[0] and not editing_title[0] and not creating_log[0]:
            nonlocal status_message
            status_message = f"Deleted Log: {textwrap.shorten(LOG_ENTRIES[current_selection[0]][0], width=23, placeholder="..." )}"
            delete_log(LOG_ENTRIES[current_selection[0]][0])
            refresh_logs(event.app)
            deleting_log[0] = False

    @kb.add('n', filter=delete_confirm)
    def confirm_no(event):
        if not editing[0] and not editing_title[0] and not creating_log[0]:
            nonlocal status_message
            deleting_log[0] = False
            status_message = "Log Deletion Aborted!"

    @kb.add('c-s')
    def save_entry(event):
        nonlocal status_message
        if editing[0]:
            editor.title = LOG_ENTRIES[current_selection[0]][0]
            edit_log(editor.title, editor.text)
            refresh_logs(event.app)
            editing[0] = False
            status_message = f"Edited Log: {textwrap.shorten(editor.title, width=23, placeholder="..." )}"
            event.app.layout = get_layout()

        if editing_title[0]:
            editor.title = LOG_ENTRIES[current_selection[0]][0]
            if editor_title.text in list_log_names():
                status_message = f"Error: Title already exists!"
            else:
                edit_log_title(editor.title, editor_title.text)
                refresh_logs(event.app)
                editing_title[0] = False
                status_message = f"Edited Title: Old: {textwrap.shorten(editor.title, width=14, placeholder="..." )} / New: {textwrap.shorten(editor_title.text, width=14, placeholder="..." )}"
                event.app.layout = get_layout()

        if creating_log[0]:
            create_log(editor_title.text, convert_date_to_julian())
            refresh_logs(event.app)
            creating_log[0] = False
            status_message = f"Created Log: {textwrap.shorten(editor_title.text, width=23, placeholder="..." )}"
            event.app.layout = get_layout()

    @kb.add('escape')
    def cancel_edit(event):
        if editing[0]:
            editing[0] = False
            event.app.layout = get_layout()

        if editing_title[0]:
            editing_title[0] = False
            event.app.layout = get_layout()

        if creating_log[0]:
            creating_log[0] = False
            event.app.layout = get_layout()

    @kb.add('c', filter=editing_active)
    def new_entry(event):
        if not editing[0] and not editing_title[0] and not creating_log[0] and not deleting_log[0]:
            creating_log[0] = True
            editor_title.text = "Set a Title"
            event.app.layout = get_layout()
            refresh_logs(event.app)
            event.app.layout.focus(editor_title)

    @kb.add('s', filter=editing_active)
    async def open_settings(event):
        event.app.exit(result="settings")


    @kb.add('q', filter=editing_active)
    def quit_app(event):
        event.app.exit()

    @kb.add('Q', filter=editing_active)
    def quit_app(event):
        event.app.exit()

    main_app = Application(
        layout=get_layout(),
        key_bindings=kb,
        style=LCARS_STYLE,
        full_screen=True,
        mouse_support=True,
    )

    # Navigation loop
    current = "main"
    while True:
        if current == "main":
            result = main_app.run()
            current = result if result else "quit"
        elif current == "settings":
            settings = settings_app()  # calls run_settings(), returns Application
            result = settings.run()
            current = result if result else "main"  # default back to main
            refresh_config_data()
        elif current == "quit":
            break
