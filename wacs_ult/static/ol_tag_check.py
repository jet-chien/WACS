# coding: utf-8
from bs4 import BeautifulSoup
import pathlib
from configparser import ConfigParser
from wacs_ult.error.error_tool import ErrorTool as et


class OlTagCheck:
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
        self.check_ul_tag(self.doc)

    def get_wrong_ol(self, doc: BeautifulSoup, wrong_elements: list):
        ol_list = doc.select('ol')
        for ol in ol_list:
            child_list = ol.findChildren(recursive=False)
            for child in child_list:

                if child.name not in ['ol', 'li', 'br'] and child.parent.name != 'li':
                    wrong_elements.append(child)

                if child.name == 'ol':
                    self.get_wrong_ol(child, wrong_elements)

    def check_ul_tag(self, doc: BeautifulSoup):
        wrong_elements = []
        self.get_wrong_ol(doc, wrong_elements)
        for el in wrong_elements:
            self.result = False

            reduct_point = self.POINT * 1
            self.minus += reduct_point
            msg = 'ol tag 使用錯誤, 錯誤元素: {} , 當前標籤: {} , 父標籤: {}'.format(str(el).replace('\n', ''),
                                                                      el.name, el.parent.name)
            error_data = et.get_error_data(25, msg, 1, reduct_point)

            self.errors.append(error_data)
