import easygui

class Box:  
    def open_file(self, extension):
        mask = '*' + extension
        return easygui.fileopenbox(filetypes=[mask])
    
    def button_box(self, message, title, buttons):
        return easygui.buttonbox(message, title, buttons)

    def message_box(self, message, title):
        return easygui.msgbox(message, title)

    def choice_box(self, message, title, choices):
        return easygui.choicebox(message, title, choices)

    def text_box(self, message, title):
        return easygui.enterbox(message, title)

    def password_box(self, message, title, fields):
        return easygui.multpasswordbox(message, title, fields)

    def exception_box(self, message, title):
        return easygui.exceptionbox(message, title)

    def yes_no_box(self, message, title):
        return easygui.ynbox(message, title)
