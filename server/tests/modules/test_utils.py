import io
import unittest
import pandas
from server.modules.types import ProcessResult
from server.modules.utils import build_globals_for_eval, parse_bytesio


class SafeExecTest(unittest.TestCase):
    def exec_code(self, code):
        built_globals = build_globals_for_eval()
        inner_locals = {}
        exec(code, built_globals, inner_locals)
        return inner_locals

    def test_builtin_functions(self):
        env = self.exec_code("""
ret = sorted(list([1, 2, sum([3, 4])]))
""")
        self.assertEqual(env['ret'], [1, 2, 7])


class ParseBytesIoTest(unittest.TestCase):
    def test_parse_utf8_csv(self):
        result = parse_bytesio(io.BytesIO(b'A\ncaf\xc3\xa9'),
                               'text/csv', 'utf-8')
        expected = ProcessResult(pandas.DataFrame({'A': ['café']}))
        self.assertEqual(result, expected)

    def test_replace_invalid_utf8(self):
        # \xe9 is ISO-8859-1 and we select 'utf-8' to test Workbench's recovery
        result = parse_bytesio(io.BytesIO(b'A\ncaf\xe9'),
                               'text/csv', 'utf-8')
        expected = ProcessResult(pandas.DataFrame({'A': ['caf�']}))
        self.assertEqual(result, expected)

    def test_autodetect_charset(self):
        # \xe9 is ISO-8859-1 so Workbench should auto-detect it
        result = parse_bytesio(io.BytesIO(b'A\ncaf\xe9'),
                               'text/csv', None)
        expected = ProcessResult(pandas.DataFrame({'A': ['café']}))
        self.assertEqual(result, expected)

        # \x96 is - in windows-1252, does not exist in UTF-8
        result = parse_bytesio(io.BytesIO(b'A\n2000\x962018'),
                               'text/csv', None)
        expected = ProcessResult(pandas.DataFrame({'A': ['2000–2018']}))
        self.assertEqual(result, expected)

        # 'Thank you' in Mandarin should resolve to UTF-8
        result = parse_bytesio(io.BytesIO(b'A\n\xE8\xB0\xA2\xE8\xB0\xA2\xE4\xBD\xA0'),
                               'text/csv', None)
        expected = ProcessResult(pandas.DataFrame({'A': ['谢谢你']}))
        self.assertEqual(result, expected)

