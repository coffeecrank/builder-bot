from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import traceback

from constants import *
import gui

class Builder:
    def __init__(self):
        self.browser = None
        self.driver = None
        self.login = None
        self.password = None
        self.statistics = {'activities_added': 0,
                           'bad_cgis': [],
                           'total_time': 0,
                           'resets': 0}

    def add_activity(self, row, container_types):
        i = 0
        is_added = False
        while i < 3:
            if i < 2:
                delay = SHORT_DELAY
            else:
                delay = LONG_DELAY
            is_added = self.can_add_activity(row, container_types, delay)
            if not is_added:
                i += 1
            else:
                break
        if not is_added:
            self.statistics['bad_cgis'].append(row[0]['cgi'])
        else:
            self.statistics['activities_added'] += 1

    def add_container(self, container_sequence, container_types):
        if container_types[len(container_sequence) - 1] == UNIT:
            back_button = self.find_visible_element(By.LINK_TEXT,
                                                    'Back',
                                                    SHORT_DELAY)
            if back_button is not None:
                back_button.click()
                time.sleep(SHORT_DELAY)
        add_button = self.find_visible_element(By.ID, 'menu_addContent')
        add_button.click()
        time.sleep(SHORT_DELAY)
        container_type = container_types[len(container_sequence) - 1]
        if container_type == FOLDER:
            add_folder_button = self.find_visible_element(By.ID,
                                                          'menu_addFolder')
            add_folder_button.click()
        else:
            add_unit_button = self.find_visible_element(By.ID, 'menu_addUnit')
            add_unit_button.click()
        time.sleep(SHORT_DELAY)
        name_field = self.find_visible_element(By.ID, 'name')
        name_field.send_keys(container_sequence[-1])
        self.set_location(container_sequence[:-1], container_types)
        save_button = self.find_visible_element(By.LINK_TEXT, 'Save')
        save_button.click()
        time.sleep(SHORT_DELAY)

    def build(self, grid):
        learning_path_tree = self.find_learning_path_tree()
        if learning_path_tree is None:
            error = gui.Box().message_box(INVALID_URL_ERROR, APP['name'])
        elif self.can_find_apps():
            container_types = self.find_container_types(
                grid.rows[0][2], grid.starting_container_type)
            starting_time = time.time()
            is_error = False
            previous_row = None
            r = 0
            while r < len(grid.rows):
                try:
                    row = grid.rows[r]
                    containers = [level for level in row[2] if level != '']
                    for i in range(len(containers)):
                        container_sequence = [containers[i]
                                              for i in range(i + 1)]
                        if container_sequence not in learning_path_tree:
                            self.add_container(container_sequence,
                                               container_types)
                            learning_path_tree.append(container_sequence)
                    self.add_activity(row, container_types)
                    previous_row = row
                    r += 1
                except:
                    traceback.print_exc()
                    self.statistics['resets'] += 1
                    self.driver.refresh()
                    time.sleep(SHORT_DELAY)
                self.statistics['total_time'] = time.time() - starting_time
            statistics = self.get_statistics()
            message = gui.Box().message_box(statistics, APP['name'])
        self.close()

    def can_add_activity(self, row, container_types, delay):
        add_button = self.find_visible_element(By.ID, 'menu_addContent')
        add_button.click()
        time.sleep(SHORT_DELAY)
        add_activity_button = self.find_visible_element(By.ID,
                                                        'menu_addActivity')
        add_activity_button.click()
        time.sleep(SHORT_DELAY)
        app = self.find_visible_element(By.ID, APP_IDS['mindtap-ab'])
        app.click()
        time.sleep(SHORT_DELAY)
        if not self.can_add_cgi(row[0]['cgi'], delay):
            return False
        if ('description' in row[1] and row[1]['description'] != ''):
            description_field = self.find_visible_element(By.ID, 'description')
            description_field.send_keys(row[1]['description'])
        self.set_location(row[2], container_types)
        save_button = self.find_visible_element(By.LINK_TEXT, 'Save')
        save_button.click()
        time.sleep(SHORT_DELAY)
        return True

    def can_add_cgi(self, cgi, delay):
        frame = self.find_visible_element(By.TAG_NAME, 'iframe')
        self.driver.switch_to.frame(frame)
        open_button = self.find_visible_element(By.CLASS_NAME, 'open-button')
        open_button.click()
        time.sleep(SHORT_DELAY)
        search_field = self.find_visible_element(By.ID, 'searchBoxInput')
        search_field.send_keys(cgi)
        search_button = self.find_visible_element(By.CLASS_NAME,
                                                  'rc--searchBar--inputButton')
        search_button.click()
        time.sleep(SHORT_DELAY)
        assign_button = self.find_visible_element(By.XPATH,
                                                  '//*[text()=" Assign"]')
        assign_button.click()
        time.sleep(SHORT_DELAY)
        save_and_assign_button = self.find_visible_element(
            By.XPATH, '//*[text()="Save and Assign to Course"]')
        save_and_assign_button.click()
        time.sleep(SHORT_DELAY)
        self.driver.switch_to.default_content()
        starting_time = time.time()
        can_add = False
        while time.time() - starting_time < delay:
            location_button = self.find_visible_element(By.ID,
                                                        'parentId-button')
            if location_button is not None:
                can_add = True
                break
        return can_add

    def can_find_apps(self):
        add_button = self.find_visible_element(By.ID, 'menu_addContent')
        add_button.click()
        time.sleep(SHORT_DELAY)
        add_activity_button = self.find_visible_element(By.ID,
                                                        'menu_addActivity')
        add_activity_button.click()
        time.sleep(SHORT_DELAY)
        apps = sorted([app for app in APP_IDS])
        missing_apps = []
        for app_name in apps:
            app = self.find_visible_element(By.ID, APP_IDS[app_name])
            if app is None:
                missing_apps.append(app_name)
        cancel_button = self.find_visible_element(By.ID, 'cancelbtnId')
        cancel_button.click()
        if len(missing_apps) > 0:
            message = MISSING_APPS_ERROR + ', '.join(missing_apps) + '.'
            error = gui.Box().message_box(message, APP['name'])
            return False
        return True

    def can_open_browser(self):
        if self.browser is None:
            browsers = sorted([browser for browser in BROWSERS])
            browser = None
            while browser is None:
                browser = gui.Box().button_box(CHOOSE_BROWSER_MESSAGE,
                                               APP['name'],
                                               browsers)
            self.browser = browser
        driver_path = BROWSERS[self.browser]['driver_path']
        log_path = BROWSERS[self.browser]['log_path']
        try:
            if self.browser == 'Chrome':
                self.driver = webdriver.Chrome(executable_path=driver_path,
                                               service_log_path=log_path)
            elif self.browser == 'Firefox':
                self.driver = webdriver.Firefox(executable_path=driver_path,
                                                log_path=log_path)
            return True
        except Exception:
            exception = gui.Box().exception_box(
                EXCEPTION_ERROR + str(Exception), APP['name'])
            self.close()
            return False

    def can_open_url(self):
        url = gui.Box().text_box(ENTER_URL_MESSAGE, APP['name'])
        self.driver.get(url)
        self.driver.maximize_window()
        login_field = self.find_visible_element(By.ID, '_username_id')
        password_field = self.find_visible_element(By.ID, '_password_id')
        go_button = self.find_visible_element(By.CLASS_NAME, 'goButton')
        if login_field is None or password_field is None or go_button is None:
            error = gui.Box().message_box(INVALID_URL_ERROR, APP['name'])
            self.close()
            return False
        self.log_in()
        login_field.send_keys(self.login)
        password_field.send_keys(self.password)
        url = self.driver.current_url
        go_button.click()
        new_url = self.find_new_url(url)
        if new_url == url:
            error = gui.Box().message_box(SERVER_ERROR, APP['name'])
            self.close()
            return False
        elif '?error=true' in new_url:
            error = gui.Box().message_box(INVALID_LOGIN_INFO_ERROR,
                                          APP['name'])
            self.login = None
            self.password = None
            self.close()
            return False
        return True

    def close(self):
        self.driver.quit()

    def find_child_element(self, parent, attribute, name):
        wait = WebDriverWait(parent, SHORT_DELAY)
        presence = EC.presence_of_element_located((attribute, name))
        try:
            element = wait.until(presence)
            return element
        except TimeoutException:
            return None

    def find_child_elements(self, parent, attribute, name):
        wait = WebDriverWait(parent, SHORT_DELAY)
        presence = EC.presence_of_all_elements_located((attribute, name))
        try:
            elements = wait.until(presence)
            return elements
        except TimeoutException:
            return []

    def find_container_location(self, container_sequence, container_types):
        menu = self.find_visible_element(By.ID, 'parentId-menu')
        learning_path = self.find_child_element(menu, By.XPATH, 'child::li')
        locations = self.find_child_elements(learning_path,
                                              By.XPATH,
                                              'following-sibling::li')
        location = learning_path
        for loc in locations:
            loc_name = self.find_location_name(loc).replace(' (Current)',
                                                            '')
            loc_level = self.find_location_level(loc)
            loc_type = self.find_location_type(loc)
            for i in range(len(container_sequence)):
                if (loc_name == container_sequence[i]
                        and loc_level == i + 2
                        and loc_type == container_types[i]):
                    location = loc
                    break
        return location

    def find_container_types(self,
                             container_sequence,
                             starting_container_type):
        container_types = []
        for r in range(len(container_sequence)):
            if r % 2 == 0:
                container_type = starting_container_type
            else:
                if starting_container_type == FOLDER:
                    container_type = UNIT
                else:
                    container_type = FOLDER
            container_types.append(container_type)
        return container_types

    def find_current_location(self, location_button):
        span = self.find_child_element(location_button,
                                       By.XPATH,
                                       'child::span')
        location = span.text.replace(' (Current)', '')
        return location

    def find_learning_path_tree(self):
        add_button = self.find_visible_element(By.ID, 'menu_addContent')
        if add_button is None:
            return None
        add_button.click()
        time.sleep(SHORT_DELAY)
        add_folder_button = self.find_visible_element(By.ID, 'menu_addFolder')
        add_folder_button.click()
        time.sleep(SHORT_DELAY)
        location_button = self.find_visible_element(By.ID, 'parentId-button')
        location_button.click()
        time.sleep(SHORT_DELAY)
        menu = self.find_visible_element(By.ID, 'parentId-menu')
        learning_path = self.find_child_element(menu, By.XPATH, 'child::li')
        locations = self.find_child_elements(learning_path,
                                             By.XPATH,
                                             'following-sibling::li')
        tree = []
        location_sequence = []
        previous_location_level = None
        for location in locations:
            location_level = self.find_location_level(location)
            location_name = self.find_location_name(location).replace(
                ' (Current)', '')
            if (previous_location_level is None
                    or location_level > previous_location_level):
                location_sequence.append(location_name)
            else:
                location_sequence_copy = location_sequence[:]
                tree.append(location_sequence_copy)
                location_sequence[location_level - 2] = location_name
                for i in range(location_level - previous_location_level):
                    location_sequence = location_sequence[:-1]
            previous_location_level = location_level
        if len(location_sequence) > 0:
            tree.append(location_sequence)
        location_button.click()
        time.sleep(SHORT_DELAY)
        cancel_button = self.find_visible_element(By.LINK_TEXT, 'Cancel')
        cancel_button.click()
        time.sleep(SHORT_DELAY)
        return tree

    def find_location_level(self, location):
        location_class = location.get_attribute('class')
        cutoff_string = location_class[
            location_class.find('level_')+len('level_'):]
        space_idx = cutoff_string.find(' ')
        if space_idx != -1:
            location_level = int(cutoff_string[:space_idx])
        else:
            location_level = int(cutoff_string)
        return location_level

    def find_location_name(self, location):
        link = self.find_child_element(location, By.XPATH, 'child::a')
        return link.text

    def find_location_type(self, location):
        location_class = location.get_attribute('class')
        if 'group_icon' in location_class:
            return FOLDER
        else:
            return UNIT

    def find_new_url(self, url):
        wait = WebDriverWait(self.driver, DELAY)
        event = EC.url_changes(url)
        try:
            wait.until(event)
            return self.driver.current_url
        except TimeoutException:
            return url

    def format_time(self, time):
        hours = round(time) // 3600
        hours_leftover = round(time - (hours * 3600))
        minutes = hours_leftover // 60
        seconds = round(hours_leftover - (minutes * 60))
        formatted_time = ''
        if hours != 0:
            formatted_time += str(hours) + ' hours '
        if minutes != 0:
            formatted_time += str(minutes) + ' minutes '
        formatted_time += str(seconds) + ' seconds'
        return formatted_time

    def find_visible_element(self, attribute, name, delay=DELAY):
        wait = WebDriverWait(self.driver, delay)
        visibility = EC.visibility_of_element_located((attribute, name))
        try:
            element = wait.until(visibility)
            return element
        except TimeoutException:
            return None

    def get_statistics(self):
        statistics = ('The program finished with '
                      + str(self.statistics['resets'])
                      + ' resets. ')
        if len(self.statistics['bad_cgis']) == 0:
            statistics += 'No bad CGI\'s were found. '
        else:
            statistics += ('These CGI\'s could not be added: '
                           + ', '.join(self.statistics['bad_cgis'])
                           + '. ')
        formatted_time = self.format_time(self.statistics['total_time'])
        if self.statistics['activities_added'] != 0:
            time_per_activity = self.format_time(
                self.statistics['total_time']
                / self.statistics['activities_added'])
        else:
            time_per_activity = self.format_time(0)
        statistics += ('Total time: '
                       + formatted_time
                       + '. Number of activities added: '
                       + str(self.statistics['activities_added'])
                       + '. Time per activity: '
                       + time_per_activity
                       + '.')
        return statistics

    def log_in(self):
        if self.login is None and self.password is None:  
            fields = [LOGIN_FIELD, PASSWORD_FIELD]
            login_info = None
            while login_info is None:
                login_info = gui.Box().password_box(LOG_IN_MESSAGE,
                                                    APP['name'],
                                                    fields)
            self.login, self.password = login_info

    def set_location(self, container_sequence, container_types):
        location_button = self.find_visible_element(By.ID, 'parentId-button')
        current_location = self.find_current_location(location_button)
        if (len(container_sequence) > 0
                and current_location != container_sequence[-1]
                and any(container != '' for container in container_sequence)):
            location_button.click()
            time.sleep(SHORT_DELAY)
            location = self.find_container_location(container_sequence,
                                                    container_types)
            location.click()
            time.sleep(SHORT_DELAY)
