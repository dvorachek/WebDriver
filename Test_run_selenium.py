
'''         The main file where commands are given. 

Selenium must be installed
http://www.seleniumhq.org/projects/webdriver/

This script uses pytest to organize and run the tests. 
Easy to use once installed 
https://docs.pytest.org/en/latest/getting-started.html
CD into folder then run either pytest Test_run_selenium.py or 
python Test_run_selenium for email/sms notification.

pytest will not create a log so if one is desired, easily redirect stdout into
a file.
Windows(cmd) Example: pytest Test_run_selenium.py > log.txt

Each browser requires a different web driver, hence there are three different 
web drivers in the folder.

In order to switch which browser runs the tests, go to driver.py and change 
line 7 to the name of the desired browser (Chrome, Edge, Firefox).

Base.py, Page.py, WebElement.py were created to reduce redundancy in the code,
as well as avoid implicit waits.


                    ..HOW IT WORKS..

Each test starts with initalizing an TodoPage object with the open method.
A parameter may be passed into open() to set the url the webdriver opens from.

By calling new_todo(location) an element is entered into a list that acts as a
queue.

Once complete_all_todos() is called then the elements that haven been entered
into the queue will be clicked on as they are located. There is an explicit
wait that has been set to search for an object every .25s and then click if it
appears. There is an timeout period which can be set in Page.py line 7.

send_keys(location, string) is used to type into a text field, specified by
the location.
complete_all_todos() must be executed before send_keys() is called.

window_resize() is used to set the browser window to a specific resolution.
The idea is to set the window to a specific size so that performing a click by
an offset from an element will result in a click at a specific location.
An update to Chromedirver.exe now places a banner at the top of the driver
window. This means that the resolution of the window needs to be altered for
Chrome to work properly. The browser_name() method is used to get the name of
the browser that is being used.

elem_offset(location, xoffset, yoffset) clicks in a location that uses
'location' as a starting point and then performs a click with an offset
specified in the parameters. Firefox requires a slightly different offset
(higher and to the right).
complete_all_todos() must be executed before elem_offset() is called.
'''

import sys
import os
import glob
import time

from driver import WebDriver
import pytest

from Base import TodoPage

'''
Dictionary containing elements that are searched for. Need to fill out
'''
location = {
    "github": ['xpath=/html/body/div[1]/div[2]/div/div/div[1]/div/div/form/label/input[1]',
               'xpath=//*[@id="tsf"]/div[2]/div[3]/center/input[1]',
               'xpath=//*[@id="rso"]/div[1]/div/div/div/div/h3/a'
    ]
}

class TestTodos(object):
    def setup_method(self, method):
        self.driver = WebDriver()
        self.current_method_name = method.__name__

    def teardown_method(self, method):
        try:
            self.driver.close()
            self.driver.quit()
        except:
            pass  # need to add exception

    def test_google_search(self):
        todos = TodoPage(self.driver).open("https://github.com/")

        todos.type_key(location['github'][0], 'Dvorachek')
        # todos.new_todo(location['github'][1])
        # todos.new_todo(location['github'][2])
        todos.complete_all_todos()
        time.sleep(1)


if __name__=="__main__":
    result = pytest.main()

