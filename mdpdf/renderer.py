# https://github.com/readthedocs/commonmark.py/blob/master/commonmark/render/renderer.py
from __future__ import unicode_literals


class Renderer(object):
    def render(self, ast):
        """Walks the AST and calls member methods for each Node type.

        @param ast {Node} The root of the abstract syntax tree.
        """

        self.buf = ""
        self.last_out = "\n"

        for node, entering in ast.walker():
            getattr(self, node.t)(node, entering)

        return self.buf

    def document(self, node, entering):
        pass

    def lit(self, s):
        """Concatenate a literal string to the buffer.

        @param str {String} The string to concatenate.
        """
        self.buf += s
        self.last_out = s

    def cr(self):
        if self.last_out != "\n":
            self.lit("\n")

    def out(self, s):
        """Concatenate a string to the buffer possibly escaping the content.

        Concrete renderer implementations should override this method.

        @param str {String} The string to concatenate.
        """
        self.lit(s)
