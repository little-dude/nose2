"""Test doctests plugin."""
import doctest

from nose2.plugins import doctests
from nose2.tests._common import TestCase, FakeHandleFileEvent


class UnitTestDocTestLoader(TestCase):
    """Test class DocTestLoader."""
    tags = ['unit']

    _RUN_IN_TEMP = True

    def test___init__(self):
        """Test the __init__ method."""
        plug = self._create()

        self.assertEqual(plug.extensions, ['.txt', '.rst'])

    def test_handle_file(self):
        """Test method handleFile."""
        # Create doctest files of supported types
        doc_test = """\
>>> 2 == 2
True
"""
        txt_event = self._handle_file('docs.txt', doc_test)
        rst_event = self._handle_file('docs.rst', doc_test)
        # Excercise loading of doctests from Python code
        py_event = self._handle_file('docs.py', """\
\"\"\"
>>> 2 == 2
True
\"\"\"
""")
        for event, ext in [(txt_event, 'txt'), (rst_event, 'rst')]:
            test, = event.extraTests
            self.assertTrue(isinstance(test, doctest.DocFileCase))
            self.assertEqual(repr(test), "docs.%s" % ext)

        testsuite, = py_event.extraTests
        test, = list(testsuite)
        self.assertEqual(repr(test), 'docs ()')

    def test_handle_file_python_without_doctests(self):
        """Test calling handleFile for a Python module without doctests."""
        event = self._handle_file("mod.py", """\
def func():
    pass
""")
        self.assertEqual(event.extraTests, [])

    def _handle_file(self, fpath, content):
        """Have plugin handle a file with certain content.

        The file is created, then a plugin is instantiated and its handleFile
        method is called for the file.
        """
        plug = self._create()
        fh = open(fpath, "wb")
        try:
            fh.write(content)
        finally:
            fh.close()

        event = FakeHandleFileEvent(fh.name)
        plug.handleFile(event)
        return event

    def _create(self):
        """Create a DocTestLoader instance."""
        plug = doctests.DocTestLoader()
        return plug
