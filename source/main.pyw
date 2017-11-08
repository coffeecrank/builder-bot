import os
import sys

sys.dont_write_bytecode = True
sys.path.append(os.getcwd())

import app

def main():
    application = app.App()
    application.load_menu()

if __name__ == '__main__':
    main()
