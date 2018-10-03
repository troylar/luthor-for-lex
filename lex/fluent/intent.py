from lex.fluent.message import WithMessage
from lex.fluent.slot import Slot
from lex import LexIntentManager


class DialogCodeHook:
    def __init__(self, **kwargs):
        self.data = {}
        self.data['uri'] = kwargs.get('Uri')
        self.data['messageVersion'] = kwargs.get('MessageVersion')

    def to_dict(self):
        return self.data


class FulfillmentActivity:
    def __init__(self, **kwargs):
        self.type = kwargs.get('Type')
        self.code_hook = kwargs.get('CodeHook')

    def with_code_hook(self, code_hook):
        self.code_hook = code_hook
        return self

    def with_type(self, type):
        self.type = type
        return self

    def to_dict(self):
        data = {}
        if self.code_hook:
            data['codeHook'] = self.code_hook.to_dict()
        data['type'] = self.type
        return data


class ConclusionStatement(WithMessage):
    def __init__(self, **kwargs):
        super(ConclusionStatement, self).__init__(**kwargs)
        self.key = 'conclusionStatement'


class ConfirmationPrompt(WithMessage):
    def __init__(self, **kwargs):
        super(ConfirmationPrompt, self).__init__(**kwargs)
        self.key = 'confirmationPrompt'


class RejectionStatement(WithMessage):
    def __init__(self, **kwargs):
        super(RejectionStatement, self).__init__(**kwargs)
        self.key = 'rejectionStatement'
        self.max_attempts = None


class Prompt(WithMessage):
    def __init__(self, **kwargs):
        super(Prompt, self).__init__(**kwargs)
        self.key = 'prompt'


class FollowUpPrompt:
    def __init__(self, **kwargs):
        self.prompt = kwargs.get('Prompt')
        self.rejection_statement = kwargs.get('RejectionStatement')

    def with_prompt(self, prompt):
        self.prompt = prompt
        return self

    def with_rejection_statement(self, rejection_statement):
        self.rejection_statement = rejection_statement
        return self

    def to_dict(self):
        data = {}
        if self.prompt:
            data['prompt'] = self.prompt.to_dict()
        if self.rejection_statement:
            data['rejection_statement'] = self.rejection_statement.to_dict()
        return data


class IntentSlot(Slot):
    def __new__(cls, *args, **kwargs):
        if kwargs.get('Slot'):
            s = kwargs.get('Slot')
            s.__class__ = IntentSlot
            return s
        super_new = super(Slot, cls).__new__
        if super_new is object.__new__:
            return super_new(cls)

    def __init__(self, **kwargs):
        if 'name' not in self.__dict__.keys():
            self.name = kwargs.get('Name')
        if 'description' not in self.__dict__.keys():
            self.description = kwargs.get('Description')
        if 'slot_type_version' not in self.__dict__.keys():
            self.slot_type_version = kwargs.get('SlotTypeVersion', '$LATEST')
        if 'slot_constraint' not in self.__dict__.keys():
            self.slot_constraint = kwargs.get('SlotConstraint')
        if 'slot_type' not in self.__dict__.keys():
            self.slot_type = kwargs.get('slot_type', self.name)
        if 'create_version' in self.__dict__:
            del self.__dict__['create_version']
        if 'value_elicitation_prompt' not in self.__dict__.keys():
            self.value_elicitation_prompt = {"messages": []}
        if 'max_attempts' not in self.__dict__.keys():
            self.max_attempts = kwargs.get('PromptMaxAttempts', 3)
        if 'priority' not in self.__dict__.keys():
            self.priority = kwargs.get('Priority')
        if 'sample_utterances' not in self.__dict__.keys():
            self.sample_utterances = kwargs.get('SampleUtterances')
        if 'response_card' not in self.__dict__.keys():
            self.response_card = kwargs.get('ResponseCard')
        if 'enumeration_values' not in self.__dict__.keys():
            self.enumeration_values = kwargs.get('EnumerationValues', [])

    def with_name(self, name):
        self.name = name
        return self

    def with_description(self, description):
        self.description = description
        return self

    def with_slot_constraint(self, slot_constraint):
        self.slot_constraint = slot_constraint
        return self

    def with_slot_type(self, slot_type):
        self.slot_type = slot_type
        return self

    def with_slot_type_version(self, slot_type_version):
        self.slot_type_version = slot_type_version
        return self

    def with_value_elicitation_prompt(self, value_elicitation_prompt):
        self.value_elicitation_prompt = value_elicitation_prompt
        return self

    def with_priority(self, priority):
        self.priority = priority
        return self

    def with_sample_utterances(self, sample_utterances):
        self.sample_utterances = sample_utterances
        return self

    def with_response_card(self, response_card):
        self.response_card = response_card
        return self

    def with_value_elicitation_prompt_message(self, content_type, content, group_number=None):
        data = {'contentType': content_type,
                'content': content}
        if group_number:
            data['groupNumber'] = group_number
        self.value_elicitation_prompt['messages'].append(data)
        return self

    def with_prompt_max_attempts(self, max_attempts):
        self.max_attempts = max_attempts
        return self

    def with_prompt_response_card(self, response_card):
        self.response_card = response_card
        return self

    def to_dict(self):
        data = {}
        data['name'] = self.name
        data['description'] = self.description
        data['slotConstraint'] = self.slot_constraint
        data['slotType'] = self.slot_type
        if not self.slot_type.startswith('AMAZON.'):
            data['slotTypeVersion'] = self.slot_type_version
        if self.priority:
            data['priority'] = self.priority
        if self.response_card:
            data['responseCard'] = self.response_card
        if self.sample_utterances:
            data['sampleUtterances'] = self.sample_utterances
        if self.value_elicitation_prompt:
            data['valueElicitationPrompt'] = {}
            if self.max_attempts:
                data['valueElicitationPrompt']['maxAttempts'] = self.max_attempts
            if self.response_card:
                data['valueElicitationPrompt']['responseCard'] = self.response_card
            if 'messages' in self.value_elicitation_prompt:
                data['valueElicitationPrompt']['messages'] = self.value_elicitation_prompt['messages']
        return data


class Intent:
    def __init__(self, **kwargs):
        self.name = kwargs.get('Name')
        self.description = kwargs.get('Description')
        self.checksum = kwargs.get('Checksum')
        self.value = kwargs.get('Value')
        self.create_version = kwargs.get('CreateVersion', False)
        self.value_selection_strategy = kwargs.get('ValueSelectionStrategy', 'ORIGINAL_VALUE')
        self.synonyms = kwargs.get('Synonyms')
        self.confirmation_prompt = kwargs.get('ConfirmationPrompt', {})
        self.rejection_statement = kwargs.get('RejectionStatement', {})
        self.conclusion_statement = kwargs.get('ConclusionStatement', {})
        self.follow_up_prompt = kwargs.get('FollowUpPrompt', {})
        self.parentIntentSignature = kwargs.get('ParentIntentSignature')
        self.checksum = kwargs.get('Checksum')
        self.slots = kwargs.get('Slots', [])
        self.dialog_hook = kwargs.get('DialogHook')
        self.fulfillment_activity = kwargs.get('FulfillmentActivity', {})
        self.sample_utterances = kwargs.get('SampleUtterances', [])
        self.version = kwargs.get('Version', '$LATEST')
        self.intent_manager = LexIntentManager()

    def with_name(self, name):
        self.name = name
        return self

    def with_description(self, description):
        self.description = description
        return self

    def with_checksum(self, checksum):
        self.checksum = checksum
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

    def with_confirmation_prompt(self, confirmation_prompt):
        self.confirmation_prompt = confirmation_prompt
        return self

    def with_rejection_statement(self, rejection_statement):
        self.rejection_statement = rejection_statement
        return self

    def with_follow_up_prompt(self, follow_up_prompt):
        self.follow_up_prompt = follow_up_prompt
        return self

    def with_conclusion_statement(self, conclusion_statement):
        self.conclusion_statement = conclusion_statement
        return self

    def with_version(self, version):
        self.version = version
        return self

    def with_dialog_hook(self, dialog_hook):
        self.dialog_hook = dialog_hook
        return self

    def with_intent_slot(self, slot):
        self.slots.append(slot)
        return self

    def with_slot(self, slot):
        self.slots.append(IntentSlot(Slot=slot).to_dict())
        return self

    def with_sample_utterances(self, sample_utterance):
        self.sample_utterances.append(sample_utterance)
        return self

    def with_fulfillment_activity(self, fulfillment_activity):
        self.fulfillment_activity = fulfillment_activity
        return self

    def to_json(self):
        intent_j = {"name": self.name}
        if self.description:
            intent_j['description'] = self.description
        if self.sample_utterances:
            intent_j['sampleUtterances'] = self.sample_utterances
        if self.slots:
            intent_j['slots'] = self.slots
        if self.rejection_statement:
            intent_j['rejectionStatement'] = self.rejection_statement.to_dict()
        if self.confirmation_prompt:
            intent_j['confirmationPrompt'] = self.confirmation_prompt.to_dict()
        if self.conclusion_statement:
            intent_j['conclusionStatement'] = self.conclusion_statement.to_dict()
        if self.fulfillment_activity:
            intent_j['fulfillmentActivity'] = self.fulfillment_activity.to_dict()
        if self.follow_up_prompt:
            intent_j['followUpPrompt'] = self.follow_up_prompt.to_dict()
        if self.dialog_hook:
            intent_j['dialogCodeHook'] = self.dialog_hook.to_dict()
        return intent_j

    def from_json(intent_j):
        intent = Intent()
        if 'name' in intent_j.keys():
            intent.with_name(intent_j['name'])
        if 'checksum' in intent_j.keys():
            intent.with_checksum(intent_j['checksum'])
        if 'description' in intent_j.keys():
            intent.with_description(intent_j['description'])
        if 'sampleUtterances' in intent_j.keys():
            for u in intent_j['sampleUtterances']:
                intent.with_sample_utterances(u)
        if 'slots' in intent_j.keys():
            for s in intent_j['slots']:
                intent.with_intent_slot(s)
        if 'dialogCodeHook' in intent_j.keys():
            d = intent_j['dialogCodeHook']
            intent.with_dialog_hook(DialogCodeHook(Uri=d['uri'],
                                    MessageVersion=d['messageVersion']))
        if 'rejectionStatement' in intent_j.keys():
            r = WithMessage.from_json(intent_j['rejectionStatment'])
            intent.with_rejection_statement(r)

        if 'conclusionStatement' in intent_j.keys():
            c = WithMessage.from_json(intent_j['conclusionStatement'])
            intent.with_confirmation_prompt(c)

        if 'confirmationPrompt' in intent_j.keys():
            c = WithMessage.from_json(intent_j['confirmationPrompt'])
            intent.with_confirmation_prompt(c)

        if 'followUpPrompt' in intent_j.keys():
            f = FollowUpPrompt()
            if 'rejectionStatement' in intent_j['followUpPrompt']:
                r = WithMessage.from_json(intent_j['followUpPrompt']['rejectionStatment'])
                f.with_rejection_statment(r)
            if 'prompt' in intent_j['followUpPrompt']:
                p = WithMessage.from_json(intent_j['followUpPrompt']['prompt'])
                f.with_prompt(p)
            intent.with_follow_up_prompt(f)

        if 'fulfillmentActivity' in intent_j.keys():
            f = FulfillmentActivity()
            f.with_type(intent_j['fulfillmentActivity']['type'])
            if 'codeHook' in intent_j['fulfillmentActivity']:
                d = intent_j['fulfillmentActivity']['codeHook']
                f.with_code_hook(DialogCodeHook(Uri=d['uri'],
                                 MessageVersion=d['messageVersion']))
            intent.with_fulfillment_activity(f)

        if 'version' in intent_j.keys():
            intent.with_version(intent_j['version'])
        return intent

    def apply(self):
        print(self.to_json())
        self.intent_manager.upsert(self.to_json())
        return self.get()

    def get(self):
        intent_j = self.intent_manager.get_intent(Name=self.name, Version=self.version)
        return Intent.from_json(intent_j)
