#!/usr/bin/env python
import functools

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By

import settings

class DriverCommandMixin(object):

    def button_by_text(self, text):
        return self.n_by_text(text, n='button')

    def n_by_text(self, text, n=None):
        n = n or '*'
        return self.driver.find_elements_by_xpath(
            "//{n}[contains(text(),'{text}')]".format(n=n, text=text)
        )

    def link_by_text(self, text):
        return self.driver.find_element_by_link_text(text)

    def element_by_name(self, text):
        return self.driver.find_element(by=By.NAME, value=text)

    def get(self, url):
        self.driver.get(url)

    def send_keys(self, element, keys):
        element.click()
        element.send_keys(keys)

class SeleniumRunner(object):
    def __call__(self, f):
        @functools.wraps(f)
        def decorated(_self, *args, **kwargs):
            with self as driver:
                return f(_self, driver, *args, **kwargs)
        return decorated

    def __enter__(self):
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        self.driver = webdriver.Chrome()
        return self.driver

    def __exit__(self, *args, **kwargs):
        try:
            self.driver.quit()
        except (AttributeError,) as e:
            # Someone has messed with our browser
            pass
        try:
            self.display.stop()
        except (AttributeError,) as e:
            # Someone has messed with our display
            pass


class Profiler(DriverCommandMixin, object):

    def login(self):
        self.get('http://localhost:7000')
        login_link = self.link_by_text('Sign in with your Olive account')
        login_link.click()
        username = self.element_by_name('username')
        password = self.element_by_name('password')
        login_button = self.button_by_text('Sign in')[1]
        self.send_keys(username, settings.email)
        self.send_keys(password, settings.password)
        login_button.click()

    @SeleniumRunner()
    def run(self, driver, name='default'):
        self.driver = driver
        self.login()

if __name__ == '__main__':
    Profiler().run()