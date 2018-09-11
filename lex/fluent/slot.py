from lex import LexSlotManager

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
        return slot_j

    def apply(self):
        self.slot_manager.upsert(self.to_json())
        return self
