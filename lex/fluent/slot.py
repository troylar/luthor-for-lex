from lex import LexSlotManager
import json
from collections import namedtuple

import json

class Generic:
    @classmethod
    def from_dict(cls, dict):
        obj = cls()
        obj.__dict__.update(dict)
        return obj

class EnumerationValue:
    def __init__(self, **kwargs):
        self.value = kwargs.get('Value')
        self.synonyms = kwargs.get('Synonyms')


class Slot:
    def __init__(self, **kwargs):
        self.name = kwargs.get('Name')
        self.description = kwargs.get('Description')
        self.checksum = kwargs.get('Checksum')
        self.value = kwargs.get('Value')
        self.version = kwargs.get('Version', '$LATEST')
        self.create_version = kwargs.get('CreateVersion', False)
        self.value_selection_strategy = kwargs.get('ValueSelectionStrategy', 'ORIGINAL_VALUE')
        self.enumeration_values = kwargs.get('EnumerationValues', [])
        self.slot_manager = LexSlotManager()

    def with_name(self, name):
        self.name = name
        return self

    def with_description(self, description):
        self.description = description
        return self

    def with_checksum(self, checksum):
        self.checksum = checksum
        return self

    def with_version(self, version):
        self.version = version
        return self

    def with_value(self, value):
        self.value = value
        return self

    def with_create_version(self, create_version):
        self.create_version = create_version
        return self

    def with_value_selection_strategy(self, strategy):
        self.value_selection_strategy = strategy
        return self

    def with_enumeration_value(self, enumeration_value):
        self.enumeration_values.append({'value': enumeration_value.value,
                                        'synonyms': enumeration_value.synonyms})
        return self

    def to_json(self):
        slot_j = {"name": self.name}
        if self.create_version:
            slot_j['createVersion'] = self.create_version
        if self.value_selection_strategy:
            slot_j['valueSelectionStrategy'] = self.value_selection_strategy
        if self.description:
            slot_j['description'] = self.description
        if self.enumeration_values:
            slot_j['enumerationValues'] = self.enumeration_values
        if self.checksum:
            slot_j['checksum'] = self.checksum
        if slot_j['slotType'].startswith('AMAZON.') and 'version' in slot_j.keys():
            del slot_j['version']
        return slot_j

    @staticmethod
    def from_json(slot_j):
        s = Slot()
        if 'name' in slot_j.keys():
            s.with_name(slot_j['name'])
        if 'description' in slot_j.keys():
            s.with_description(slot_j['description'])
        if 'checksum' in slot_j.keys():
            s.with_checksum(slot_j['checksum'])
        if 'version' in slot_j.keys():
            s.with_checksum(slot_j['version'])
        if 'createVersion' in slot_j.keys():
            s.with_create_version(slot_j['createVersion'])
        if 'valueSelectionStrategy' in slot_j.keys():
            s.with_value_selection_strategy(slot_j['valueSelectionStrategy'])
        if 'enumerationValues' in slot_j.keys():
            for v in slot_j['enumerationValues']:
                s.enumeration_values.append(EnumerationValue(Value=v['value'],
                                                             Synonyms=v['synonyms']))
        return s

    def apply(self):
        self.slot_manager.upsert(self.to_json())
        return self

    def get(self):
        slot_j = self.slot_manager.get_slot_type(Name=self.name, Version=self.version)
        return Slot.from_json(slot_j)
