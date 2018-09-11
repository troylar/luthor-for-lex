import json
from lex.fluent.slot import Slot, EnumerationValue
from utils import DictUtils
import unittest


class TestCase(unittest.TestCase):
    def test_can_set_name(self):
        s = Slot(Name='test')
        assert s.name == 'test'

    def test_can_set_description(self):
        s = Slot(Name='test', Description='description')
        assert s.description == 'description'

    def test_can_set_checksum(self):
        s = Slot(Checksum='checksum')
        assert s.checksum == 'checksum'

    def test_can_set_strategy(self):
        s = Slot(ValueSelectionStrategy='TOP_RESOLUTION')
        assert s.value_selection_strategy == 'TOP_RESOLUTION'

    def test_strategy_defaults_to_original_value(self):
        s = Slot()
        assert s.value_selection_strategy == 'ORIGINAL_VALUE'

    def test_create_version_defaults_to_false(self):
        s = Slot()
        assert not s.create_version

    def test_can_initialize_create_version(self):
        s = Slot(CreateVersion=True)
        assert s.create_version

    def test_minimal_json_is_correct(self):
        correct_j = """
{
   "name":"test",
   "valueSelectionStrategy":"ORIGINAL_VALUE",
   "description": "description",
   "createVersion": "True",
   "checksum": "test_chk",
   "enumerationValues":[
      {
         "value":"AMAZON.STRING",
         "synonyms":[
            "test",
            "mytest"
         ]
      }
   ]
}
"""
        s = Slot()
        s.with_name('test') \
         .with_description('description') \
         .with_checksum('test_chk') \
         .with_create_version('True') \
         .with_enumeration_value(EnumerationValue(Value='AMAZON.STRING', Synonyms=['test', 'mytest']))

        assert DictUtils.are_same(json.loads(correct_j), s.to_json())
