#!/usr/bin/env python2
import unittest
import logging

from MooseDocs.common import load_extensions
from MooseDocs import base
from MooseDocs.tree import tokens, pages
from MooseDocs.extensions import core

logging.basicConfig()



class MooseDocsTestCase(unittest.TestCase):
    EXTENSIONS = []
    READER = base.MarkdownReader()
    RENDERER = base.HTMLRenderer()
    EXECUTIONER = None

    def __init__(self, *args, **kwargs):
        super(MooseDocsTestCase, self).__init__(*args, **kwargs)

        self.__node = None
        self.__meta = None
        self.__translator = None

    @property
    def meta(self):
        return self.__meta

    def setup(self, content=None, reader=None, renderer=None, extensions=None, executioner=None):
        content = content or []
        reader = reader or self.READER
        renderer = renderer or self.RENDERER
        extensions = extensions or self.EXTENSIONS
        executioner = executioner or self.EXECUTIONER

        ext = load_extensions(extensions)
        self.__translator = base.Translator(content, reader, renderer, ext, executioner)
        self.__translator.init()

    def tokenize(self, text, *args, **kwargs):

        if args or kwargs or (self.__translator is None):
            self.setup(*args, **kwargs)

        self.__node = pages.Text(text)
        self.__ast, self.__meta = self.__translator.executioner.tokenize(self.__node)
        return self.__ast

    def render(self, ast, *args, **kwargs):
        if args or kwargs or (self.__translator is None):
            self.setup(*args, **kwargs)

        return self.__translator.executioner.render(self.__node, ast, self.__meta)




class TestCore(MooseDocsTestCase):
    EXTENSIONS = [core]

    def testCodeBlock(self):


        text = u"```\nint x = 0;\n```"
        ast = self.tokenize(text)

        result = self.render(ast)
        print result









if __name__ == '__main__':
    unittest.main(verbosity=2)
