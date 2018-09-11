import json
from lex.fluent.intent import Intent, DialogHookCode, ConfirmationPrompt, \
                              RejectionStatement, Prompt, FollowUpPrompt, \
                              ConclusionStatement, FulfillmentActivity, \
                              IntentSlot
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

    def test_can_add_sample_utterances(self):
        correct_j = {'name': 'test', 'description': 'description', 'sampleUtterances': [['what time', 'which time']]}
        i = Intent(Name='test', Description='description')
        i.with_sample_utterances(['what time', 'which time'])

        assert DictUtils.are_same(i.to_json(), correct_j)

    def test_can_add_confirmation_prompt(self):
        correct_j = {'name': 'test', 'description': 'description', 'confirmationPrompt': {'messages': [{'contentType': 'PlainText', 'content': 'content'}, {'contentType': 'SSML', 'content': 'ssml_content', 'groupNumber': 123}], 'maxAttempts': 3, 'responseCard': 'test_card'}}
        i = Intent(Name='test', Description='description')
        c = ConfirmationPrompt()
        c.with_message('PlainText', 'content') \
         .with_message('SSML', 'ssml_content', 123) \
         .with_max_attempts(3) \
         .with_response_card('test_card')
        i.with_confirmation_prompt(c)
        assert DictUtils.are_same(i.to_json(), correct_j)

    def test_can_add_rejection_statement(self):
        correct_j = {'name': 'test', 'description': 'description', 'rejectionStatement': {'messages': [{'contentType': 'PlainText', 'content': 'content'}, {'contentType': 'SSML', 'content': 'ssml_content', 'groupNumber': 123}], 'responseCard': 'test_card'}}
        i = Intent(Name='test', Description='description')
        r = RejectionStatement()
        r.with_message('PlainText', 'content') \
         .with_message('SSML', 'ssml_content', 123) \
         .with_response_card('test_card')
        i.with_rejection_statement(r)
        print(i.to_json())
        assert DictUtils.are_same(i.to_json(), correct_j)

    def test_can_add_follow_up_prompt(self):
        correct_j = {'name': 'test', 'description': 'description', 'followUpPrompt': {'prompt': {'messages': [{'contentType': 'PlainText', 'content': 'content'}, {'contentType': 'SSML', 'content': 'ssml_content', 'groupNumber': 123}], 'maxAttempts': 3, 'responseCard': 'test_card'}, 'rejection_statement': {'messages': [{'contentType': 'PlainText', 'content': 'content'}, {'contentType': 'SSML', 'content': 'ssml_content', 'groupNumber': 123}], 'responseCard': 'test_card'}}}
        i = Intent(Name='test', Description='description')

        p = Prompt()
        p.with_message('PlainText', 'content') \
         .with_message('SSML', 'ssml_content', 123) \
         .with_max_attempts(3) \
         .with_response_card('test_card')

        r = RejectionStatement()
        r.with_message('PlainText', 'content') \
         .with_message('SSML', 'ssml_content', 123) \
         .with_response_card('test_card')
        f = FollowUpPrompt()
        f.with_rejection_statement(r) \
         .with_prompt(p)
        i.with_follow_up_prompt(f)
        print(i.to_json())
        assert DictUtils.are_same(i.to_json(), correct_j)

    def test_can_add_conclusion_statement(self):
        correct_j = {'name': 'test', 'description': 'description', 'conclusionStatement': {'messages': [{'contentType': 'PlainText', 'content': 'content'}, {'contentType': 'SSML', 'content': 'ssml_content', 'groupNumber': 123}], 'responseCard': 'test_card'}}
        i = Intent(Name='test', Description='description')
        c = ConclusionStatement()
        c.with_message('PlainText', 'content') \
         .with_message('SSML', 'ssml_content', 123) \
         .with_response_card('test_card')
        i.with_conclusion_statement(c)
        print(i.to_json())
        assert DictUtils.are_same(i.to_json(), correct_j)

    def test_can_set_fulfillment_activity(self):
        correct_j = {'name': 'test', 'description': 'description', 'fulfillmentActivity': {'codeHook': {'uri': 'urihook', 'messageVersion': '2'}, 'type': 'ReturnIntent'}}

        i = Intent(Name='test', Description='description')
        f = FulfillmentActivity()
        f.with_code_hook(DialogHookCode(Uri='urihook',
                                          MessageVersion='2'))
        f.with_type('ReturnIntent')
        i.with_fulfillment_activity(f)
        assert DictUtils.are_same(i.to_json(), correct_j)

    def test_can_pass_slot_to_intent_slot(self):
        s = Slot(Name='testslot', Description='testdescript')
        intent_slot = IntentSlot(Slot=s).with_slot_constraint('Required')
        assert intent_slot.description == 'testdescript'
        assert intent_slot.name == 'testslot'
        assert intent_slot.slot_constraint == 'Required'
