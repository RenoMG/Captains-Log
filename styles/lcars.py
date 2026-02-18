from prompt_toolkit.styles import Style

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