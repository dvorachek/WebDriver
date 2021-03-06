import time
from selenium.common.exceptions import NoAlertPresentException
from errors import WaitForElementError
  
class Page(object):
    timeout_attempts = 100
    sleep_interval = .1

    def __init__(self, driver):
        self.driver = driver
        
    @property
    def referrer(self):
        return self.driver.execute_script('return document.referrer')
    
    def sleep(self, seconds=None):
        if seconds:
            time.sleep(seconds)
        else:
            time.sleep(self.sleep_interval)
            
    def find_element_by_locator(self, locator):
        return self.driver.find_element_by_locator(locator)
    
    def find_elements_by_locator(self, locator):
        return self.driver.find_elements_by_locator(locator)
    
    def wait_for_available(self, locator):
        for i in range(self.timeout_attempts):
            if self.driver.is_element_available(locator):
                break
            self.sleep()
        else:
            raise WaitForElementError('Wait for available timed out')
        return True
    
    def wait_for_visible(self, locator):
        for i in range(self.timeout_attempts):
            if self.driver.is_visible(locator):
                break
            self.sleep()
        else:
            raise WaitForElementError('Wait for hidden timed out')
        return True
    
    def wait_for_alert(self):
        for i in range(self.timeout_attempts):
            try:
                alert = self.driver.switch_to_alert()
                if alert.test:
                    break
            except NoAlertPresentException as Nape:
                pass
            self.sleep()
        else:
            raise NoAlertPresentException(msg='Wait for alert timed out')
        return True
    
    def _dispatch(self, l_call, l_args, d_call, d_args):
        pass