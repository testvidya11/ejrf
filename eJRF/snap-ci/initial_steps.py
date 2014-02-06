import glob
import os

from lettuce import *
from splinter import Browser
from django.core.management import call_command

from django.template.defaultfilters import slugify


@before.each_scenario
def flush_database(step):
    call_command('flush', interactive=False)

@before.all
def clear_screen_shots():
    screen_shots = glob.glob('./screenshots/*.png')
    for screen_shot in screen_shots:
        os.remove(screen_shot)
    open_browser()


def open_browser():
    remote_url = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (os.environ['SAUCE_USERNAME'], os.environ['SAUCE_ACCESS_KEY'])
    world.browser = Browser(
            driver_name="remote",
            url=remote_url,
            browser="%s" % os.environ['BROWSER_TYPE'],
            platform="Windows 7",
            version="%s" % os.environ['BROWSER_VERSION'],
            name="eJRF SnapCI test on %s version %s" % (os.environ['BROWSER_TYPE'], os.environ['BROWSER_VERSION'])
        )
    world.browser.driver.set_window_size(1024, 720)

@after.each_scenario
def take_screen_shot(scenario):
    if scenario.failed:
        world.browser.driver.save_screenshot('screenshots/%s.png' % slugify(scenario.name))

@after.each_scenario
def clear_cookies(scenario):
    world.browser.driver.delete_all_cookies()

@after.all
def close_browser(total):
    world.browser.quit()