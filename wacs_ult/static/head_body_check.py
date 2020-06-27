# coding: utf-8
import bs4
from bs4 import BeautifulSoup
import pathlib
from configparser import ConfigParser
from wacs_ult.error.error_tool import ErrorTool as et


class HeadBodyCheck:
    def __init__(self, doc: BeautifulSoup):
        self.doc = doc

        self.config_path = None
        self.config = None
        self.POINT = None
        self.load_point()

        self.result = True
        self.minus = 0
        self.errors = list()

    def load_point(self):
        self.config_path = '{}/reduct.ini'.format(pathlib.Path(__file__).parent.parent.absolute())
        self.config = ConfigParser()
        self.config.read(self.config_path)
        self.POINT = int(self.config[self.__class__.__name__]['POINT'])

    def check(self):
        self.check_head_body(self.doc)

    def check_head_body(self, doc: BeautifulSoup):
        tag_list = doc.select('head')[0].children

        for tag in tag_list:
            if type(tag) is not bs4.element.Tag:
                continue

            if tag.name not in ['base', 'link', 'meta', 'script', 'style', 'title']:
                self.result = False

                reduct_point = self.POINT * 1
                self.minus += reduct_point
                msg = '網頁內容不在 <body></body> 區間內'
                error_data = et.get_error_data(7, msg, 1, reduct_point)

                self.errors.append(error_data)
