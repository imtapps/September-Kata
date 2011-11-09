from django.core.urlresolvers import reverse
from lettuce import step
from django.test import Client


@step(u'When I visit the "([^"]*)" page for the "([^"]*)" "([^"]*)"')
def go_to_page(step, page_name, arg_name, arg_val):
    step.scenario.browser = Client()
    step.scenario.response = step.scenario.browser.get(reverse(page_name, kwargs={arg_name:arg_val}))

@step(u'(?:Then|And) I should see "([^"]*)" on the web page')
def assert_webpage_contains(step, stuff):
    assert stuff in step.scenario.response.content, "'{0}' is not on the page".format(stuff)