import os
from rich.layout import Layout
from rich.console import Console
from rich import inspect
from rich.panel import Panel
from rich import print
import rich
import keyboard
from time import sleep
import shutil

# Instantiate Console obj
con = Console()
con.height = 40



"""
-------------------------Variables------------------------------------
Set Variables for Panels, These will move over to function
calls which will handle logic and conditionally 'build' these strings
----------------------------------------------------------------------
"""

title = ""

hud = f"""
   Cover: 60                                           Actions: O O O
   Health: 100                                         Movement: 2
   Ammo: 6/28                                          Enemies Visible: 2
   Armor: 23                                           Concealed: Y
   Inventory: 'I'  |  Character: 'I'  |  Help: 'H'  |  Line of Sight: 'S'
"""

game_map = """
        A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R  S  T  U
    1  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
    2  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
    3  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
    4  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
    5  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
    6  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
    7  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
    8  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
    9  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
   10  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
"""

sidebar = ""
# -------------------------------------------------------------------#


"""
Create initial Panels, There will be more, including main menu, Options menu, These will be called and then built and returned and the layout will be updated
each time the layout is resized the values will need to be recalculated. 
maybe a special call to the Panels that doesn't resize them if the screen size is the same
"""

MAP = Panel(game_map, title_align="center", title=f"4th St. Library", padding=0)
HUD = Panel(hud, title=f"Buster Scruggs: Level 12", title_align="center")
SIDEBAR = Panel(sidebar)

"""
Create layout, each Menu will have its own unique layout, Inventory, pause menu, main menu
"""
layout = Layout()
# Divide the layout into 3 rows
layout.split_row(
    Layout(SIDEBAR, ratio=1),
    Layout(name="Center", ratio=2),
    Layout(SIDEBAR, ratio=1)
)
# Split the center to a GameMap on top and HUD/UI on the bottom
layout["Center"].split_column(
    Layout(MAP, name="MAP", ratio=2),
    Layout(HUD, name="HUD",size=8)
)
# Draw initial layout
print()
con.print(layout)

# Getting initial console size
twidth, theight = os.get_terminal_size()

while True:
    # If the screen size changes the layout is updated
    current_x, current_y = os.get_terminal_size()
    if (current_x, current_y) != (twidth, theight):
        os.system('clear')
        con.print(layout)
        sleep(0.2)

    # Wait for keyboard input
    key = keyboard.read_key()

    # Check which key has been pressed. Logic processes after this
    # Start of the "Game Loop"
    if key == "i":
        """
        Example: If 'I' is pressed, Create inventory string and panel, jump into the Inventory 'logic' loop and update display
        """
        layout["HUD"].update(Panel(hud, title=f"Buster Scruggs: Level 13", title_align="center"))
        # Clear old console screen and redraw
        os.system('clear')
        print()
        con.print(layout)
        # Slight delay to avoid double presses
        sleep(0.2)

    elif key == "o":
        layout["HUD"].update(Panel(hud, title=f"Buster Scruggs: Level 12", title_align="center"))
        os.system('clear')
        print()
        con.print(layout)
        sleep(0.2)

# update screen()
