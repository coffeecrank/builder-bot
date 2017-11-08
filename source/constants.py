import collections
import os

# Paths. -------------------------------------------------------------------
DRIVERS_PATH = os.path.join(os.getcwd(), 'drivers')
LOGS_PATH = os.path.join(os.getcwd(), 'logs')
CHROME_DRIVER_PATH = os.path.join(DRIVERS_PATH, 'chromedriver.exe')
CHROME_LOG_PATH = os.path.join(LOGS_PATH, 'chrome.log')
FIREFOX_DRIVER_PATH = os.path.join(DRIVERS_PATH, 'geckodriver.exe')
FIREFOX_LOG_PATH = os.path.join(LOGS_PATH, 'firefox.log')
# General. --------------------------------------------------------------------
APP = {'name': 'BuilderBot',
       'version': '1.0'}
APP_IDS = {'mindtap-ab': 'ActivityBuilder'}
BROWSERS = {'Chrome': {'driver_path': CHROME_DRIVER_PATH,
                       'log_path': CHROME_LOG_PATH},
            'Firefox': {'driver_path': FIREFOX_DRIVER_PATH,
                        'log_path': FIREFOX_LOG_PATH}}
GRID = {'file_extension': '.xlsx',
        'required_columns': ['file type', 'cgi'],
        'optional_columns': ['description'],
        'level_columns': ['level ']}
DELAY = 10
LONG_DELAY = 30
SHORT_DELAY = 1
FOLDER = 'Folder'
UNIT = 'Unit'
# App UI. ---------------------------------------------------------------------
BUILD_BUTTON = 'Build'
EXIT_BUTTON = 'Exit'
LOAD_GRID_BUTTON = 'Load grid'
# ----------
LOGIN_FIELD = 'Login'
PASSWORD_FIELD = 'Password'
# ----------
CHOOSE_BROWSER_MESSAGE = 'Please choose your browser.'
CHOOSE_STARTING_CONTAINER_TYPE_MESSAGE = 'Please choose your top level.'
CHOOSE_WS_MESSAGE = 'Please choose a worksheet.'
ENTER_URL_MESSAGE = 'Please copy and paste the master URL.'
LOG_IN_MESSAGE = 'Please enter your login information.'
# ----------
BAD_ROWS_ERROR = 'Please fix these rows before proceeding: '
EXCEPTION_ERROR = ('An error occured. Please follow README instructions. If'
                   ' the error still occurs, please report it to'
                   ' lana.ovcharenko@contractor.cengage.com.\n\n')
INVALID_CHOICE_ERROR = 'This is not a valid choice. Please try again.'
INVALID_LOGIN_INFO_ERROR = ('This is not valid login information. Please try'
                            ' again.')
INVALID_FILE_ERROR = 'This is not a valid file. Please try again.'
INVALID_URL_ERROR = 'The browser cannot open this URL. Please try again.'
INVALID_WS_ERROR = 'This is not a valid worksheet. Please try again.'
MISSING_APPS_ERROR = 'Please provision these apps before proceeding: '
NOT_READY_TO_BUILD_ERROR = ('Please make sure to upload a grid before'
                            ' proceeding.')
SERVER_ERROR = 'There is a server issue. Please try again later.'
