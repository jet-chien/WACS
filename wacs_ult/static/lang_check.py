# coding: utf-8
from bs4 import BeautifulSoup
import pathlib
from configparser import ConfigParser
from wacs_ult.error.error_tool import ErrorTool as et


class LangCheck:
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
        self.check_lang(self.doc)

    def check_lang(self, doc: BeautifulSoup):
        tag = doc.select('html[lang]')
        if len(tag) == 0:
            self.result = False

            reduct_point = self.POINT * 1
            self.minus += reduct_point
            msg = 'lang 屬性未建立'
            error_data = et.get_error_data(4, msg, 1, reduct_point)

            self.errors.append(error_data)

            return

        lang = tag[0].get('lang')
        if lang not in ['zh-TW', 'zh-tw', 'ZH-TW']:
            self.result = False

            reduct_point = self.POINT * 1
            self.minus += reduct_point
            msg = 'lang 屬性錯誤。 tag: {}'.format(lang)
            error_data = et.get_error_data(4, msg, 1, reduct_point)

            self.errors.append(error_data)
