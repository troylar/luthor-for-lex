import json
from lex.fluent.intent import Intent, DialogHookCode
from lex.fluent.slot import Slot, EnumerationValue
from utils import DictUtils
import unittest


class TestCase(unittest.TestCase):
    def test_can_set_name(self):
        i = Intent(Name='test')
        assert i.name == 'test'

    def test_can_set_description(self):
        i = Intent(Name='test', Description='description')
        assert i.description == 'description'

    def test_can_set_dialog_cook_hook(self):
        correct_j = {"name": "test", "description": "description", "dialogCookHook": {"uri":  "urihook", "messageVersion": "2"}}

        i = Intent(Name='test', Description='description')
        i.with_dialog_hook(DialogHookCode(Uri='urihook',
                                          MessageVersion='2'))
        assert DictUtils.are_same(i.to_json(), correct_j)

    def test_can_add_slot(self):
        correct_j = {'name': 'test', 'description': 'description', 'slots': [{'name': 'test', 'createVersion': 'True', 'valueSelectionStrategy': 'ORIGINAL_VALUE', 'description': 'description', 'enumerationValues': [{'value': 'AMAZON.STRING', 'synonyms': ['test', 'mytest']}], 'checksum': 'test_chk'}]}
        s = Slot()
        s.with_name('test') \
         .with_description('description') \
         .with_checksum('test_chk') \
         .with_create_version('True') \
         .with_enumeration_value(EnumerationValue(Value='AMAZON.STRING', Synonyms=['test', 'mytest']))
        i = Intent(Name='test', Description='description')
        i.with_slot(s)
        assert DictUtils.are_same(i.to_json(), correct_j)

