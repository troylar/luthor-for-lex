import boto3
from lex.fluent.message import WithMessage
from lex import LexBotManager


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
        self.abort_statement = kwargs.get('AbortStatement')
        self.abort_statement = kwargs.get('AbortStatement',
            AbortStatement(MaxAttempts=3).with_message('PlainText', 'Sorry, I couldn\'t understand.'))
        self.clarification_prompt = kwargs.get('ClarificationPrompt',
            ClarificationPrompt(MaxAttempts=3).with_message('PlainText', 'Sorry, could you please repeat that?'))
        self.locale = kwargs.get('Locale', 'en-US')
        self.child_directed = kwargs.get('ChildDirected', False)
        self.bot_manager = LexBotManager()

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

    def with_abort_statement(self, abort_statement):
        self.abort_statement = abort_statement
        return self

    def with_clarification_prompt(self, clarification_prompt):
        self.clarification_prompt = clarification_prompt
        return self

    def with_intent(self, intent):
        self.intents.append(intent)
        return self

    def apply(self):
        bot_j = {}
        if self.name:
            bot_j['name'] = self.name
        if self.description:
            bot_j['description'] = self.description
        if self.intents:
            bot_j['intents'] = []
            for x in self.intents:
                bot_j['intents'].append({'intentName': x.name, 'intentVersion': x.version})
        if self.clarification_prompt:
            bot_j['clarificationPrompt'] = self.clarification_prompt.to_dict()
        if self.abort_statement:
            bot_j['abortStatement'] = self.abort_statement.to_dict()
        bot_j['locale'] = self.locale
        bot_j['childDirected'] = self.child_directed
        self.bot_manager.upsert(bot_j)
        return self
