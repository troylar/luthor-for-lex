import boto3
from lex.message import WithMessage


class AbortStatement(WithMessage):
    def __init__(self, **kwargs):
        super(AbortStatement, self).__init__(**kwargs)
        self.key = 'abortStatement'
        self.max_attempts = None


class ClarificationPrompt(WithMessage):
    def __init__(self, **kwargs):
        super(ClarificationPrompt, self).__init__(**kwargs)
        self.key = 'clarificationPrompt'


class Bot:
    def __init__(self, **kwargs):
        self.name = kwargs.get('Name')
        self.description = kwargs.get('Description')
        self.intents = kwargs.get('Intents', [])
        self.clarification_prompt = kwargs.get('ClarificationPrompt')
        self.abort_statement = kwargs.get('AbortStatement')
        self.idle_session_ttl_in_seconds = kwargs.get('IdleSessionTtlInSeconds')
        self.voice_id = kwargs.get('VoiceId')
        self.checksum = kwargs.get('Checksum')
        self.processBehavior = kwargs.get('ProcessBehavior', 'SAVE')
        self.locale = kwargs.get('Locale', 'en-US')
        self.childDirected = kwargs.get('ChildDirected', False)
        self.createVersion = kwargs.get('CreateVersion', False)

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

    def with_synonyms(self, synonyms):
        self.synonyms = synonyms
        return self

    def with_create_version(self, create_version):
        self.create_version = create_version
        return self

    def with_value_selection_strategy(self, strategy):
        self.value_selection_strategy = strategy
        return self

    def

    def apply(self):
        client = boto3.client('lex-models')
        slot_j = { "name": self.name,
                   "enumerationValues": [ { "value": self.value } ],
                   "valueSelectionStrategy": self.value_selection_strategy}
        if self.description:
            slot_j['description'] = self.description
        if self.synonyms:
            slot_j['enumerationValues']['synonyms'] = self.synonyms
        if self.checksum:
            slot_j['checksum'] = self.checksum
        client.put_slot_type(**slot_j)
