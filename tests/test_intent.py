import json
from lex.fluent.intent import Intent, DialogHookCode
from lex.fluent.slot import Slot
from utils import DictUtils
import unittest


class TestCase(unittest.TestCase):
    def test_can_set_name(self):
        i = Intent(Name='test')
        assert i.name == 'test'

    def test_can_set_description(self):
        i = Intent(Name='test', Description='description')
        assert i.description == 'description'

    def test_can_set_required_values(self):
        i = Intent(Name='test', Description='description')
        i.with_dialog_hook(DialogHookCode(Uri='urihook',
                                          MessageVersion='2'))
        print(i.to_json())
