from collections import defaultdict

from lxml import html
import requests

class Group(object):
    def get(self):
        """
            This class should be subclassed with each subclass implementing
            this method. This method returns a dictionary where keys
            are group names and the values are lists of people
        """
        raise NotImplementedError

class GCGroup(Group):
    BLACK_LIST = ['Patricia Wintermuth', 'Sean Wheeler']
    GC_URL = 'https://gc.com/team'

    def get(self):
        """
            This method does a simply web scrape of GC_URL with an attempt to grab each employee at
            GameChanger's name.
        """
        return_dict = defaultdict(list)
        page = requests.get(self.GC_URL)
        html_element = html.fromstring(page.content)

        # Executives
        execs = html_element.find_class('execs')[0]
        for name_span in execs.find_class('name'):
            name = name_span.text.strip()
            if name not in self.BLACK_LIST:
                return_dict['Executives'].append(name)

        # Non-executives
        for container in html_element.find_class('teamNameContainer'):
            name = container.find_class('name')[0].text.strip()
            group = container.find_class('position')[0].text.strip()
            if name not in self.BLACK_LIST:
                return_dict[group].append(name)

        return return_dict
