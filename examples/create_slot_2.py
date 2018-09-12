from lex.fluent.slot import Slot
from lex.fluent.intent import Intent, IntentSlot
from lex import LexBotManager, LexIntentManager, LexSlotManager, LexPlayer


s = Slot(Name='testslot').with_value('AMAZON.NUMBER').apply()
sm = LexSlotManager()
slot_j = sm.get_slot_type(Name='testslot')
slot = Slot.from_json(slot_j)
slot.with_description('test description').apply()
slot_j = sm.get_slot_type(Name='testslot')
slot = Slot.from_json(slot_j)
print(slot.to_json())
# s = Slot(Name='test_timeslot').with_description('test_descript').apply()
