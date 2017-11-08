import collections
import xlrd

from constants import *
import gui

class Grid:
    def __init__(self, path):
        self.wb_name = os.path.basename(path)
        self.wb = xlrd.open_workbook(path)
        self.ws = None
        self.required_columns = None
        self.optional_columns = None
        self.level_columns = None
        self.starting_row = None
        self.starting_container_type = None
        self.rows = None

    def can_parse_ws(self):
        rows = []
        bad_rows = []
        for r in range(self.starting_row, self.ws.nrows):
            file_type = self.format_value(
                self.ws.cell(r, self.required_columns['file type']).value)
            if file_type == '':
                bad_rows.append(r)
            elif file_type == 'multi-page sequence':
                rows.append(r)
        if len(rows) > 0 and rows[0] != self.starting_row:
            for r in range(self.starting_row, rows[0]):
                if r not in bad_rows:
                    bad_rows.append(r)
        good_rows = []
        for r in range(len(rows)):
            beginning = rows[r]
            if r == len(rows) - 1:
                end = self.ws.nrows
            else:
                end = rows[r + 1]
            row = self.parse_sequence(beginning, end)
            if row is None:
                for i in range(beginning, end):
                    if i not in bad_rows:
                        bad_rows.append(i)
            else:
                good_rows.append(row)
        if len(bad_rows) == 0:
            self.rows = good_rows
            if (len(self.level_columns) > 0
                    and self.starting_container_type is None):
                buttons = [FOLDER, UNIT]
                starting_container_type = None
                while starting_container_type is None:
                    starting_container_type = gui.Box().button_box(
                        CHOOSE_STARTING_CONTAINER_TYPE_MESSAGE,
                        APP['name'],
                        buttons)
                self.starting_container_type = starting_container_type
            return True
        error = gui.Box().message_box(
            BAD_ROWS_ERROR + (', '.join([str(r) for r in bad_rows])) + '.',
            APP['name'])
        return False

    def can_read_ws(self, ws_name):
        ws = self.wb.sheet_by_name(ws_name)
        for r in range(ws.nrows):
            row = [self.format_value(ws.cell(r, c).value)
                   for c in range(ws.ncols)]
            required_columns = {}
            optional_columns = {}
            level_columns = collections.OrderedDict()
            for c in range(len(row)):
                column_to_lower = row[c].lower()
                if (column_to_lower in GRID['required_columns']
                        and column_to_lower not in required_columns):
                    required_columns[column_to_lower] = c
                elif (any(column_to_lower.startswith(column)
                          for column in GRID['level_columns'])
                          and column_to_lower not in level_columns):
                    level_columns[column_to_lower] = c
                elif (column_to_lower in GRID['optional_columns']
                          and column_to_lower not in optional_columns):
                    optional_columns[column_to_lower] = c
            if len(required_columns) == len(GRID['required_columns']):
                self.ws = ws
                self.starting_row = r + 1
                self.required_columns = required_columns
                self.optional_columns = optional_columns
                self.level_columns = level_columns
                return True
        error = gui.Box().message_box(INVALID_WS_ERROR, APP['name'])
        return False

    def choose_ws(self):
        ws_choices = [ws_name for ws_name in self.wb.sheet_names()]
        while True:
            ws = gui.Box().choice_box(CHOOSE_WS_MESSAGE,
                                      APP['name'],
                                      ws_choices)
            if ws not in ws_choices:
                message = gui.Box().message_box(INVALID_CHOICE_ERROR,
                                                APP['name'])
            else:
                return ws

    def format_value(self, value):
        if value is None:
            return ''
        return ' '.join(str(value).split())

    def parse_row(self, r):
        required_columns = {}
        for key in self.required_columns:
            cell = self.format_value(self.ws.cell(
                r, self.required_columns[key]).value)
            required_columns[key] = cell
        optional_columns = {}
        for key in self.optional_columns:
            cell = self.format_value(self.ws.cell(
                r, self.optional_columns[key]).value)
            optional_columns[key] = cell
        level_columns = []
        for key in self.level_columns:
            cell = self.format_value(self.ws.cell(
                r, self.level_columns[key]).value)
            level_columns.append(cell)
        return [required_columns, optional_columns, level_columns]

    def parse_sequence(self, beginning, end):
        sequence = [i for i in range(beginning, end)]
        r = None
        for i in sequence:
            file_type = self.format_value(self.ws.cell(
                i, self.required_columns['file type']).value)
            if file_type == '':
                continue
            cgi = self.format_value(self.ws.cell(
                i, self.required_columns['cgi']).value)
            if cgi != '':
                r = i
                break
        if r is None:
            return None
        return self.parse_row(r)
