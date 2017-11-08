import sys

import builder
from constants import *
import gui
import grid

class App:
    def __init__(self):
        self.builder = None
        self.grid = None
    
    def click_button(self, button):
        if LOAD_GRID_BUTTON in button:
            self.load_grid()
        elif BUILD_BUTTON in button:
            if self.is_ready_to_build():
                self.run_builder()
            else:
                self.load_menu()
        elif EXIT_BUTTON in button:
            self.exit_program()

    def exit_program(self):
        sys.exit()

    def is_ready_to_build(self):
        if self.grid is None:
            error = gui.Box().message_box(NOT_READY_TO_BUILD_ERROR,
                                          APP['name'])
            return False
        return True
            
    def load_grid(self):
        file_path = gui.Box().open_file(GRID['file_extension'])
        if file_path is not None:
            if file_path.endswith(GRID['file_extension']):
                new_grid = grid.Grid(file_path)
                ws = new_grid.choose_ws()
                if new_grid.can_read_ws(ws) and new_grid.can_parse_ws():
                    self.grid = new_grid
            else:
                error = gui.Box().message_box(INVALID_FILE_ERROR, APP['name'])
        self.load_menu()

    def load_menu(self):
        if not os.path.exists(LOGS_PATH):
            os.mkdir(LOGS_PATH)
        buttons = [LOAD_GRID_BUTTON, BUILD_BUTTON, EXIT_BUTTON]
        if self.grid is not None:
            buttons[0] = buttons[0] + ' (+)'
        button = gui.Box().button_box(APP['name'] + ' v' + APP['version'],
                                      APP['name'],
                                      buttons)
        if button is None:
            button = EXIT_BUTTON
        self.click_button(button)

    def run_builder(self):
        if self.builder is None:
            self.builder = builder.Builder()
        if self.builder.can_open_browser() and self.builder.can_open_url():
            self.builder.build(self.grid)
        self.load_menu()
