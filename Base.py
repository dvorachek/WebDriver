from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, WebDriverException
from errors import ExpectedElementError, WaitForElementError
from Page import Page
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import time

locators = {
        'target': '',
        'todo': [],
        'count': 0,
        'completed': 0
        }

# page_url = "http://portal.axys-aps.com/"
# workspace = "https://portal.axys-aps.com/workspace/#getProjects"
# adv_download = "http://portal.axys-aps.com/downloadadvanced.aspx?id=46185"

class TodoPage(Page):
    
    def new_todo(self, locator):
        locators['todo'].append(locator)
        locators['count'] += 1
    
    '''Properties were added for light assertion'''
    @property
    def todos_completed(self):
        return locators['completed']

    @property
    def todos_remaining(self):
        return locators['count']

    @property
    def todos_listed(self):
        return len(locators['todo'])

    def open(self, page_url):
        self.driver.get(page_url)
        locators['target'] = 'xpath=/html/body'
        locators['todo'] = []
        return self.wait_until_loaded()

    def wait_until_loaded(self):
        self.wait_for_available(locators['target'])
        return self

    def window_resize(self, x, y):
        self.driver.set_window_size(x, y)

    def complete_all_todos(self, delay=0):
        for item in locators['todo']:
            try:
                locators['target'] = item
                self.wait_until_loaded()
                time.sleep(delay)
                self.find_element_by_locator(item).click()
                print item
            except WebDriverException as e:
                if e:
                    print "ucWorkspaceLoadingOverlayText got in the way of the click at {}".format(item)
                    print e 
                else:
                    raise
        locators['completed'] += locators['count']
        locators['count'] = 0
        locators['todo'] = []
        
        
    def elem_offset(self, el, x, y):
        locators['target'] = el
        self.wait_until_loaded()
        e = self.find_element_by_locator(el)
        time.sleep(.5)
        ActionChains(self.driver).move_to_element_with_offset(e, x, y).click().perform()
        locators['completed'] += 1
        
    
    def type_key(self, el, msg):
        self.clear_text(el)
        e = self.find_element_by_locator(el)
        time.sleep(.25)
        e.send_keys(msg)
        time.sleep(.25)
        locators['completed'] += 1
        
    def clear_text(self, el):
        locators['target'] = el
        self.wait_until_loaded()
        self.find_element_by_locator(el).clear()
        
    def browser_name(self):
        return self.driver.capabilities['browserName']
        
    # '''test, for future implementation'''
    # def drag_by_offset_hidden(self, el, x1, y1, x2, y2):
        # locators['target'] = el
        # self.wait_until_loaded()
        # e = self.find_element_by_locator(el)
        # print x1
        # ActionChains(self.driver).move_to_element_with_offset(e, x1, y1).click_and_hold().move_by_offset(x2, y2).release().perform()
        # locators['completed'] += 1    
        
    # def drag_by_offset(self, el, x, y):
        # locators['target'] = el
        # self.wait_until_loaded()
        # e = self.find_element_by_locator(el)
        # time.sleep(.5)
        # ActionChains(self.driver).drag_and_drop_by_offset(e, x, y).perform()
        # locators['completed'] += 1
        
    # def switch_to_new_tab(self):
        # time.sleep(1)
        # self.driver.switch_to.window(self.driver.window_handles[-1])
        # time.sleep(1)
        